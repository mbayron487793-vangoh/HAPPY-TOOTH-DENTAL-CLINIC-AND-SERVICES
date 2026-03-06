# =============================================================================
# Happy Tooth Dental Clinic and Services
# Appointment Controller
# =============================================================================

from datetime import datetime, date, time
from database import Database
from models.appointment_model import AppointmentModel
from models.dentist_model import DentistModel
from models.patient_model import PatientModel
from models.billing_model import BillingModel
from models.treatment_model import TreatmentModel
from views.appointment_view import AppointmentDialog


class AppointmentController:
    def __init__(self, view, user_data=None):
        self.view = view
        self.db = Database()
        self.user_data = user_data or {}
        self._connect_signals()
    
    def _get_dentist_id(self):
        """Get the dentist ID linked to the current user. Auto-creates if missing."""
        user_id = self.user_data.get('id')
        if user_id:
            result = self.db.fetch_one(DentistModel.Q_SELECT_BY_USER_ID, (user_id,))
            if result:
                return result['id']
            
            # Auto-create dentist record for dentist user without a linked record
            if self._is_dentist_role():
                first_name = self.user_data.get('first_name', 'Unknown')
                last_name = self.user_data.get('last_name', 'Dentist')
                self.db.execute_query(
                    DentistModel.Q_INSERT,
                    (first_name, last_name, 'General Dentist', '', '', user_id)
                )
                # Fetch the newly created dentist ID
                result = self.db.fetch_one(DentistModel.Q_SELECT_BY_USER_ID, (user_id,))
                return result['id'] if result else None
        return None
    
    def _is_dentist_role(self):
        return self.user_data.get('role') == 'Dentist'
    
    def _connect_signals(self):
        self.view.add_btn.clicked.connect(self.add_appointment)
        self.view.search_input.textChanged.connect(self.search_appointments)
        self.view._archive_callback = self.archive_appointment
        self.view._mark_complete_callback = self.mark_complete
    
    def load_appointments(self):
        if self._is_dentist_role():
            dentist_id = self._get_dentist_id()
            if dentist_id:
                appointments = self.db.fetch_all(
                    AppointmentModel.Q_SELECT_BY_DENTIST, (dentist_id,)
                )
            else:
                appointments = []
        else:
            appointments = self.db.fetch_all(AppointmentModel.Q_SELECT_ALL)
        self.view.load_table(appointments)
    
    def search_appointments(self, keyword):
        if self._is_dentist_role():
            dentist_id = self._get_dentist_id()
            if keyword.strip() and dentist_id:
                search = f"%{keyword}%"
                appointments = self.db.fetch_all(
                    AppointmentModel.Q_SEARCH_BY_DENTIST,
                    (dentist_id, search, search, search)
                )
            else:
                self.load_appointments()
                return
        else:
            if keyword.strip():
                search = f"%{keyword}%"
                appointments = self.db.fetch_all(
                    AppointmentModel.Q_SEARCH,
                    (search, search, search, search, search)
                )
            else:
                appointments = self.db.fetch_all(AppointmentModel.Q_SELECT_ALL)
        self.view.load_table(self._enrich_appointments(appointments))
    
    def add_appointment(self):
        # Only staff/admin can create appointments
        if self.user_data.get('role') not in ['Staff', 'Admin']:
            self.view.show_warning("Access Denied", "Only staff can create appointments.")
            return
        patients = self.db.fetch_all(PatientModel.Q_SELECT_ALL)
        dentists = self.db.fetch_all(DentistModel.Q_SELECT_ACTIVE)
        dialog = AppointmentDialog(self.view, patients=patients, dentists=dentists)
        if dialog.exec():
            data = dialog.get_data()
            # Prevent booking in the past
            appt_date = data['appointment_date']  # could be str or date
            appt_time = data['appointment_time']  # could be str or time/timedelta
            try:
                if isinstance(appt_date, str):
                    appt_date_obj = datetime.strptime(appt_date, "%Y-%m-%d").date()
                else:
                    appt_date_obj = appt_date

                if isinstance(appt_time, str):
                    # Handle both HH:MM and HH:MM:SS formats
                    fmt = "%H:%M:%S" if appt_time.count(':') == 2 else "%H:%M"
                    appt_time_obj = datetime.strptime(appt_time, fmt).time()
                elif hasattr(appt_time, 'total_seconds'):
                    # Handle timedelta from DB/widget
                    total_secs = int(appt_time.total_seconds())
                    hours, remainder = divmod(total_secs, 3600)
                    minutes, _ = divmod(remainder, 60)
                    appt_time_obj = time(hours, minutes)
                else:
                    appt_time_obj = appt_time

                appt_datetime = datetime.combine(appt_date_obj, appt_time_obj)
                if appt_datetime < datetime.now():
                    self.view.show_warning(
                        "Invalid Schedule",
                        "Cannot book an appointment in the past.\n"
                        "Please select a future date and time."
                    )
                    return
            except Exception as e:
                print(f"[Validation] Date/time check error: {e}")

            # Check for double-booking (same dentist, same date, same time)
            conflict = self.db.fetch_one(
                AppointmentModel.Q_CHECK_CONFLICT,
                (data['dentist_id'], data['appointment_date'], data['appointment_time'])
            )
            if conflict:
                self.view.show_warning(
                    "Scheduling Conflict",
                    f"This dentist already has an appointment at this date and time.\n\n"
                    f"Existing patient: {conflict['patient_name']}\n"
                    f"Please choose a different time slot."
                )
                return
            # Appointment is assigned to dentist and will appear in their list
            result = self.db.execute_query(
                AppointmentModel.Q_INSERT,
                (data['patient_id'], data['dentist_id'],
                 data['appointment_date'], data['appointment_time'],
                 data['notes'], self.user_data.get('id'))
            )
            if result:
                self.view.show_info("Success", "Appointment booked successfully!")
                self.load_appointments()
            else:
                self.view.show_warning("Error", "Failed to book appointment.")
    
    def mark_complete(self, appointment_id):
        """Mark an appointment as Completed. Dentists can only complete their own."""
        appointment = self.db.fetch_one(AppointmentModel.Q_SELECT_BY_ID, (appointment_id,))
        if not appointment:
            self.view.show_warning("Error", "Appointment not found.")
            return
        
        if appointment['status'] == 'Completed':
            self.view.show_info("Info", "This appointment is already marked as completed.")
            return
        
        if appointment['status'] == 'Cancelled':
            self.view.show_warning("Error", "Cannot complete a cancelled appointment.")
            return
        
        # Confirm before marking complete
        if self.view.show_confirm(
            "Confirm Completion",
            f"Mark this appointment as completed?\n\n"
            f"Patient: {appointment['patient_name']}\n"
            f"Date: {appointment['appointment_date']}\n"
            f"Time: {appointment['appointment_time']}"
        ):
            result = self.db.execute_query(
                AppointmentModel.Q_UPDATE_STATUS, ('Completed', appointment_id)
            )
            if result:
                self.view.show_info("Success", "Appointment marked as completed!")
                self.load_appointments()
            else:
                self.view.show_warning("Error", "Failed to update appointment status.")
    
    def archive_appointment(self, appointment_id):
        appointment = self.db.fetch_one(AppointmentModel.Q_SELECT_BY_ID, (appointment_id,))
        if not appointment:
            self.view.show_warning("Error", "Appointment not found.")
            return
        if self.view.show_confirm(
            "Confirm Archive",
            f"Are you sure you want to archive this appointment?\n\n"
            f"Patient: {appointment['patient_name']}\n"
            f"Date: {appointment['appointment_date']}\n"
            f"This appointment will be hidden from the list."
        ):
            result = self.db.execute_query(AppointmentModel.Q_ARCHIVE, (appointment_id,))
            if result:
                self.view.show_info("Archived", "Appointment archived successfully.")
                self.load_appointments()
            else:
                self.view.show_warning("Error", "Failed to archive appointment.")
