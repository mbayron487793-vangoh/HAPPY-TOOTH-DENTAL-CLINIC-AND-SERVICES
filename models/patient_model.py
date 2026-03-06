# =============================================================================
# Happy Tooth Dental Clinic and Services
# Patient Model — Blueprint for patient data structure
# =============================================================================


class PatientModel:
    """
    Blueprint for patient data.
    Defines the structure and fields of a patient record.
    All database transactions are handled by the controller.
    """

    TABLE = "patients"

    FIELDS = [
        "id",
        "first_name",
        "last_name",
        "gender",
        "birthdate",
        "contact_number",
        "email",
        "address",
        "medical_history",
        "date_registered",
    ]

    # Queries used by the controller
    Q_SELECT_ALL = (
        "SELECT id, first_name, last_name, gender, birthdate, "
        "contact_number, email, address, date_registered "
        "FROM patients ORDER BY last_name, first_name"
    )
    Q_SELECT_BY_ID = "SELECT * FROM patients WHERE id = %s"
    Q_SELECT_BY_DENTIST = (
        "SELECT DISTINCT p.id, p.first_name, p.last_name, p.gender, p.birthdate, "
        "p.contact_number, p.email, p.address, p.date_registered "
        "FROM patients p "
        "JOIN appointments a ON p.id = a.patient_id "
        "WHERE a.dentist_id = %s "
        "ORDER BY p.last_name, p.first_name"
    )
    Q_SEARCH = (
        "SELECT id, first_name, last_name, gender, birthdate, "
        "contact_number, email, address, date_registered "
        "FROM patients "
        "WHERE first_name LIKE %s OR last_name LIKE %s "
        "OR contact_number LIKE %s OR email LIKE %s "
        "ORDER BY last_name, first_name"
    )
    Q_INSERT = (
        "INSERT INTO patients (first_name, last_name, gender, birthdate, "
        "contact_number, email, address, medical_history) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )
    Q_UPDATE = (
        "UPDATE patients SET first_name = %s, last_name = %s, gender = %s, "
        "birthdate = %s, contact_number = %s, email = %s, "
        "address = %s, medical_history = %s "
        "WHERE id = %s"
    )
    Q_DELETE = "DELETE FROM patients WHERE id = %s"
    Q_COUNT = "SELECT COUNT(*) AS total FROM patients"
    Q_RECENT = (
        "SELECT id, first_name, last_name, contact_number, date_registered "
        "FROM patients ORDER BY date_registered DESC LIMIT %s"
    )

    def __init__(self, data=None):
        """Initialize a patient blueprint with optional data dict."""
        data = data or {}
        self.id = data.get("id")
        self.first_name = data.get("first_name", "")
        self.last_name = data.get("last_name", "")
        self.gender = data.get("gender", "")
        self.birthdate = data.get("birthdate")
        self.contact_number = data.get("contact_number", "")
        self.email = data.get("email", "")
        self.address = data.get("address", "")
        self.medical_history = data.get("medical_history", "")
        self.date_registered = data.get("date_registered")
