# =============================================================================
# Happy Tooth Dental Clinic and Services
# Treatment Model — Blueprint for treatment data structure
# =============================================================================


class TreatmentModel:
    """
    Blueprint for treatment data.
    Defines the structure and fields of a treatment record.
    All database transactions are handled by the controller.
    """

    TABLE = "treatments"

    FIELDS = [
        "id",
        "appointment_id",
        "service_id",
        "tooth_number",
        "notes",
        "date_created",
    ]

    # Queries used by the controller
    Q_SELECT_BY_APPOINTMENT = (
        "SELECT t.id, t.tooth_number, t.notes, t.date_created, "
        "s.service_name, s.price, t.service_id "
        "FROM treatments t "
        "JOIN services s ON t.service_id = s.id "
        "WHERE t.appointment_id = %s "
        "ORDER BY t.id"
    )
    Q_SELECT_BY_PATIENT = (
        "SELECT t.id, t.tooth_number, t.notes, t.date_created, "
        "s.service_name, s.price, "
        "a.appointment_date, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM treatments t "
        "JOIN services s ON t.service_id = s.id "
        "JOIN appointments a ON t.appointment_id = a.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.patient_id = %s "
        "ORDER BY a.appointment_date DESC, t.id"
    )
    Q_SELECT_ALL = (
        "SELECT t.id, t.tooth_number, t.notes, t.date_created, "
        "t.appointment_id, t.service_id, "
        "s.service_name, s.price, "
        "a.appointment_date, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM treatments t "
        "JOIN services s ON t.service_id = s.id "
        "JOIN appointments a ON t.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "ORDER BY a.appointment_date DESC, t.id"
    )
    Q_SELECT_BY_ID = (
        "SELECT t.id, t.tooth_number, t.notes, t.date_created, "
        "t.appointment_id, t.service_id, "
        "s.service_name, s.price, "
        "a.appointment_date, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM treatments t "
        "JOIN services s ON t.service_id = s.id "
        "JOIN appointments a ON t.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE t.id = %s"
    )
    Q_SEARCH = (
        "SELECT t.id, t.tooth_number, t.notes, t.date_created, "
        "t.appointment_id, t.service_id, "
        "s.service_name, s.price, "
        "a.appointment_date, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM treatments t "
        "JOIN services s ON t.service_id = s.id "
        "JOIN appointments a ON t.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE p.first_name LIKE %s OR p.last_name LIKE %s "
        "OR s.service_name LIKE %s OR t.tooth_number LIKE %s "
        "ORDER BY a.appointment_date DESC, t.id"
    )
    Q_INSERT = (
        "INSERT INTO treatments (appointment_id, service_id, tooth_number, notes) "
        "VALUES (%s, %s, %s, %s)"
    )
    Q_UPDATE = (
        "UPDATE treatments SET service_id = %s, tooth_number = %s, notes = %s "
        "WHERE id = %s"
    )
    Q_DELETE = "DELETE FROM treatments WHERE id = %s"
    Q_TOTAL_BY_APPOINTMENT = (
        "SELECT COALESCE(SUM(s.price), 0) AS total "
        "FROM treatments t "
        "JOIN services s ON t.service_id = s.id "
        "WHERE t.appointment_id = %s"
    )
    Q_SELECT_BY_DENTIST = (
        "SELECT t.id, t.tooth_number, t.notes, t.date_created, "
        "t.appointment_id, t.service_id, "
        "s.service_name, s.price, "
        "a.appointment_date, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM treatments t "
        "JOIN services s ON t.service_id = s.id "
        "JOIN appointments a ON t.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.dentist_id = %s "
        "ORDER BY a.appointment_date DESC, t.id"
    )
    Q_SEARCH_BY_DENTIST = (
        "SELECT t.id, t.tooth_number, t.notes, t.date_created, "
        "t.appointment_id, t.service_id, "
        "s.service_name, s.price, "
        "a.appointment_date, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM treatments t "
        "JOIN services s ON t.service_id = s.id "
        "JOIN appointments a ON t.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.dentist_id = %s "
        "AND (p.first_name LIKE %s OR p.last_name LIKE %s "
        "OR s.service_name LIKE %s OR t.tooth_number LIKE %s) "
        "ORDER BY a.appointment_date DESC, t.id"
    )
    Q_SELECT_PRICE_BY_SERVICE = "SELECT s.price FROM services s WHERE s.id = %s"
    Q_SELECT_DENTIST_OF_APPOINTMENT = (
        "SELECT dentist_id FROM appointments WHERE id = %s"
    )

    def __init__(self, data=None):
        """Initialize a treatment blueprint with optional data dict."""
        data = data or {}
        self.id = data.get("id")
        self.appointment_id = data.get("appointment_id")
        self.service_id = data.get("service_id")
        self.tooth_number = data.get("tooth_number", "")
        self.notes = data.get("notes", "")
        self.date_created = data.get("date_created")
