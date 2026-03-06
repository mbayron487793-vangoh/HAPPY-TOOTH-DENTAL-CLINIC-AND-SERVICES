# =============================================================================
# Happy Tooth Dental Clinic and Services
# Patient Controller — Handles patient CRUD logic
# =============================================================================

from database import Database
from models.patient_model import PatientModel
from models.dentist_model import DentistModel
from models.appointment_model import AppointmentModel
from models.treatment_model import TreatmentModel
from views.patient_view import PatientDialog
from views.patient_history_dialog import PatientHistoryDialog


class PatientController:
    """Controller for Patient management."""
    
    def __init__(self, view, user_data=None):
        self.view = view
        self.db = Database()
        self.user_data = user_data or {}
        self._connect_signals()
    
    def _connect_signals(self):
        """Connect view signals to controller methods."""
        self.view.add_btn.clicked.connect(self.add_patient)
        self.view.search_input.textChanged.connect(self.search_patients)
        self.view._edit_callback = self.edit_patient
        self.view._history_callback = self.view_history
        self.view._delete_callback = self.delete_patient
    
    def load_patients(self):
        """Load patients into the table. Dentist sees only their own patients."""
        role = self.user_data.get('role', 'Admin')
        if role == 'Dentist':
            # Get dentist_id
            user_id = self.user_data.get('id')
            dentist = self.db.fetch_one(DentistModel.Q_SELECT_BY_USER_ID, (user_id,))
            if dentist:
                patients = self.db.fetch_all(PatientModel.Q_SELECT_BY_DENTIST, (dentist['id'],))
            else:
                patients = []
        else:
            patients = self.db.fetch_all(PatientModel.Q_SELECT_ALL)
        self.view.load_table(patients)
    
    def search_patients(self, keyword):
        """Search patients and update table."""
        if keyword.strip():
            search = f"%{keyword}%"
            patients = self.db.fetch_all(PatientModel.Q_SEARCH, (search, search, search, search))
        else:
            patients = self.db.fetch_all(PatientModel.Q_SELECT_ALL)
        self.view.load_table(patients)
    
    def add_patient(self):
        """Open dialog to add a new patient."""
        dialog = PatientDialog(self.view)
        if dialog.exec():
            data = dialog.get_data()
            result = self.db.execute_query(
                PatientModel.Q_INSERT,
                (data['first_name'], data['last_name'], data['gender'],
                 data['birthdate'], data['contact_number'], data['email'],
                 data['address'], data['medical_history'])
            )
            if result:
                self.view.show_info("Success", "Patient registered successfully!")
                self.load_patients()
            else:
                self.view.show_warning("Error", "Failed to register patient.")
    
    def edit_patient(self, patient_id):
        """Open dialog to edit an existing patient."""
        patient = self.db.fetch_one(PatientModel.Q_SELECT_BY_ID, (patient_id,))
        if not patient:
            self.view.show_warning("Error", "Patient not found.")
            return
        
        dialog = PatientDialog(self.view, patient)
        if dialog.exec():
            data = dialog.get_data()
            result = self.db.execute_query(
                PatientModel.Q_UPDATE,
                (data['first_name'], data['last_name'], data['gender'],
                 data['birthdate'], data['contact_number'], data['email'],
                 data['address'], data['medical_history'], patient_id)
            )
            if result:
                self.view.show_info("Success", "Patient updated successfully!")
                self.load_patients()
            else:
                self.view.show_warning("Error", "Failed to update patient.")
    
    def view_history(self, patient_id):
        """Open medical history dialog for a patient."""
        patient = self.db.fetch_one(PatientModel.Q_SELECT_BY_ID, (patient_id,))
        if not patient:
            self.view.show_warning("Error", "Patient not found.")
            return
        # Fetch all history data for the dialog
        appointments = self.db.fetch_all(AppointmentModel.Q_SELECT_BY_PATIENT, (patient_id,))
        treatments = self.db.fetch_all(TreatmentModel.Q_SELECT_BY_PATIENT, (patient_id,))
        billings = self.db.fetch_all(
            "SELECT b.*, a.appointment_date "
            "FROM billings b "
            "JOIN appointments a ON b.appointment_id = a.id "
            "WHERE a.patient_id = %s "
            "ORDER BY b.date_created DESC",
            (patient_id,)
        )
        bill_stats = self.db.fetch_one(
            "SELECT COALESCE(SUM(b.total_amount), 0) AS total_billed "
            "FROM billings b "
            "JOIN appointments a ON b.appointment_id = a.id "
            "WHERE a.patient_id = %s",
            (patient_id,)
        )
        total_billed = float(bill_stats['total_billed']) if bill_stats else 0.0
        history_data = {
            'appointments': appointments,
            'treatments': treatments,
            'billings': billings,
            'total_billed': total_billed
        }
        dialog = PatientHistoryDialog(self.view, patient, history_data)
        dialog.exec()
    
    def delete_patient(self, patient_id):
        """Delete a patient after confirmation."""
        if self.view.show_confirm(
            "Confirm Delete",
            "Are you sure you want to delete this patient?\nThis will also delete all related appointments, treatments, and billings."
        ):
            result = self.db.execute_query(PatientModel.Q_DELETE, (patient_id,))
            if result:
                self.view.show_info("Deleted", "Patient deleted successfully.")
                self.load_patients()
            else:
                self.view.show_warning("Error", "Failed to delete patient.")
