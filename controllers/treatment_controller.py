# =============================================================================
# Happy Tooth Dental Clinic and Services
# Treatment Controller
# =============================================================================

from database import Database
from models.treatment_model import TreatmentModel
from models.dentist_model import DentistModel
from models.billing_model import BillingModel
from models.appointment_model import AppointmentModel
from models.service_model import ServiceModel
from views.treatment_view import TreatmentDialog


class TreatmentController:
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
        self.view.add_btn.clicked.connect(self.add_treatment)
        self.view.search_input.textChanged.connect(self.search_treatments)
        self.view._edit_callback = self.edit_treatment
        self.view._delete_callback = self.delete_treatment
    
    def load_treatments(self):
        if self._is_dentist_role():
            dentist_id = self._get_dentist_id()
            if dentist_id:
                treatments = self.db.fetch_all(
                    TreatmentModel.Q_SELECT_BY_DENTIST, (dentist_id,)
                )
            else:
                treatments = []
        else:
            treatments = self.db.fetch_all(TreatmentModel.Q_SELECT_ALL)
        self.view.load_table(treatments)
    
    def search_treatments(self, keyword):
        if self._is_dentist_role():
            dentist_id = self._get_dentist_id()
            if keyword.strip() and dentist_id:
                search = f"%{keyword}%"
                treatments = self.db.fetch_all(
                    TreatmentModel.Q_SEARCH_BY_DENTIST,
                    (dentist_id, search, search, search, search)
                )
            else:
                self.load_treatments()
                return
        else:
            if keyword.strip():
                search = f"%{keyword}%"
                treatments = self.db.fetch_all(
                    TreatmentModel.Q_SEARCH, (search, search, search, search)
                )
            else:
                treatments = self.db.fetch_all(TreatmentModel.Q_SELECT_ALL)
        self.view.load_table(treatments)
    
    def add_treatment(self):
        # Only allow dentist to record treatment for their own appointments
        if self.user_data.get('role') != 'Dentist':
            self.view.show_warning("Access Denied", "Only dentists can record treatments.")
            return
        appointments = self.db.fetch_all(AppointmentModel.Q_SELECT_ALL)
        services = self.db.fetch_all(ServiceModel.Q_SELECT_ACTIVE)
        dialog = TreatmentDialog(self.view, appointments=appointments, services=services)
        if dialog.exec():
            data = dialog.get_data()
            # Check if appointment belongs to this dentist
            dentist_id = self._get_dentist_id()
            appt = self.db.fetch_one(
                TreatmentModel.Q_SELECT_DENTIST_OF_APPOINTMENT, (data['appointment_id'],)
            )
            if not appt or appt['dentist_id'] != dentist_id:
                self.view.show_warning("Access Denied", "You can only record treatments for your own appointments.")
                return
            result = self.db.execute_query(
                TreatmentModel.Q_INSERT,
                (data['appointment_id'], data['service_id'],
                 data['tooth_number'], data['notes'])
            )
            if result:
                # Auto-create billing record with status 'Unpaid'
                try:
                    price = self.db.fetch_one(
                        TreatmentModel.Q_SELECT_PRICE_BY_SERVICE, (data['service_id'],)
                    )
                    total_amount = price['price'] if price else 0
                    self.db.execute_query(
                        BillingModel.Q_INSERT_FULL,
                        (data['appointment_id'], total_amount, 0, total_amount, 'Unpaid')
                    )
                except Exception as e:
                    print(f"[Billing] Could not create billing record: {e}")
                msg = "Treatment recorded successfully!\nBilling record created with status 'Unpaid'."
                self.view.show_info("Success", msg)
                self.load_treatments()
            else:
                self.view.show_warning("Error", "Failed to record treatment.")
    
    def edit_treatment(self, treatment_id):
        # Get treatment data by ID (efficient single-row fetch)
        treatment = self.db.fetch_one(TreatmentModel.Q_SELECT_BY_ID, (treatment_id,))
        
        if not treatment:
            self.view.show_warning("Error", "Treatment not found.")
            return
        
        appointments = self.db.fetch_all(AppointmentModel.Q_SELECT_ALL)
        services = self.db.fetch_all(ServiceModel.Q_SELECT_ACTIVE)
        dialog = TreatmentDialog(self.view, treatment, appointments, services)
        if dialog.exec():
            data = dialog.get_data()
            result = self.db.execute_query(
                TreatmentModel.Q_UPDATE,
                (data['service_id'], data['tooth_number'], data['notes'], treatment_id)
            )
            if result:
                self.view.show_info("Success", "Treatment updated successfully!")
                self.load_treatments()
            else:
                self.view.show_warning("Error", "Failed to update treatment.")
    
    def delete_treatment(self, treatment_id):
        if self.view.show_confirm("Confirm Delete", "Are you sure you want to delete this treatment record?"):
            result = self.db.execute_query(TreatmentModel.Q_DELETE, (treatment_id,))
            if result:
                self.view.show_info("Deleted", "Treatment deleted successfully.")
                self.load_treatments()
            else:
                self.view.show_warning("Error", "Failed to delete treatment.")
