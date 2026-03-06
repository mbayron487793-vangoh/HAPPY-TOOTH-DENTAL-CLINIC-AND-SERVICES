# =============================================================================
# Happy Tooth Dental Clinic and Services
# Appointment Model — Blueprint for appointment data structure
# =============================================================================


class AppointmentModel:
    """
    Blueprint for appointment data.
    Defines the structure and fields of an appointment record.
    All database transactions are handled by the controller.
    """

    TABLE = "appointments"

    FIELDS = [
        "id",
        "patient_id",
        "dentist_id",
        "appointment_date",
        "appointment_time",
        "status",
        "notes",
        "created_by",
        "date_created",
    ]

    # Queries used by the controller
    Q_SELECT_ALL = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, a.notes, "
        "a.patient_id, a.dentist_id, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name, "
        "d.specialization "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.is_archived = 0 "
        "ORDER BY a.appointment_date DESC, a.appointment_time DESC"
    )
    Q_SELECT_TODAY = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, a.notes, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.appointment_date = CURDATE() AND a.is_archived = 0 "
        "ORDER BY a.appointment_time"
    )
    Q_SELECT_BY_DATE = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, a.notes, "
        "a.patient_id, a.dentist_id, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.appointment_date = %s AND a.is_archived = 0 "
        "ORDER BY a.appointment_time"
    )
    Q_SELECT_BY_ID = (
        "SELECT a.*, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "p.contact_number AS patient_contact, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name, "
        "d.specialization "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.id = %s"
    )
    Q_SELECT_BY_PATIENT = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, a.notes, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM appointments a "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.patient_id = %s AND a.is_archived = 0 "
        "ORDER BY a.appointment_date DESC, a.appointment_time DESC"
    )
    Q_SEARCH = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, a.notes, "
        "a.patient_id, a.dentist_id, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.is_archived = 0 AND ("
        "p.first_name LIKE %s OR p.last_name LIKE %s "
        "OR d.first_name LIKE %s OR d.last_name LIKE %s "
        "OR a.status LIKE %s) "
        "ORDER BY a.appointment_date DESC, a.appointment_time DESC"
    )
    Q_INSERT = (
        "INSERT INTO appointments (patient_id, dentist_id, appointment_date, "
        "appointment_time, notes, created_by) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    Q_UPDATE = (
        "UPDATE appointments SET patient_id = %s, dentist_id = %s, "
        "appointment_date = %s, appointment_time = %s, "
        "status = %s, notes = %s "
        "WHERE id = %s"
    )
    Q_UPDATE_STATUS = "UPDATE appointments SET status = %s WHERE id = %s"
    Q_ARCHIVE = "UPDATE appointments SET is_archived = 1 WHERE id = %s"
    Q_DELETE = "DELETE FROM appointments WHERE id = %s"
    Q_COUNT_TODAY = (
        "SELECT COUNT(*) AS total FROM appointments WHERE appointment_date = CURDATE() AND is_archived = 0"
    )
    Q_UPCOMING = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.appointment_date >= CURDATE() AND a.status = 'Scheduled' "
        "AND a.is_archived = 0 "
        "ORDER BY a.appointment_date, a.appointment_time "
        "LIMIT %s"
    )
    Q_CHECK_CONFLICT = (
        "SELECT a.id, CONCAT(p.first_name, ' ', p.last_name) AS patient_name "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "WHERE a.dentist_id = %s AND a.appointment_date = %s "
        "AND a.appointment_time = %s AND a.status != 'Cancelled'"
    )
    Q_CHECK_CONFLICT_EXCLUDE = (
        "SELECT a.id, CONCAT(p.first_name, ' ', p.last_name) AS patient_name "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "WHERE a.dentist_id = %s AND a.appointment_date = %s "
        "AND a.appointment_time = %s AND a.status != 'Cancelled' "
        "AND a.id != %s"
    )
    Q_SELECT_BY_DENTIST = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, a.notes, "
        "a.patient_id, a.dentist_id, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name, "
        "d.specialization "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.dentist_id = %s AND a.is_archived = 0 "
        "ORDER BY a.appointment_date DESC, a.appointment_time DESC"
    )
    Q_SEARCH_BY_DENTIST = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, a.notes, "
        "a.patient_id, a.dentist_id, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.dentist_id = %s AND a.is_archived = 0 "
        "AND (p.first_name LIKE %s OR p.last_name LIKE %s "
        "OR a.status LIKE %s) "
        "ORDER BY a.appointment_date DESC, a.appointment_time DESC"
    )
    Q_SELECT_TODAY_BY_DENTIST = (
        "SELECT a.id, a.appointment_date, a.appointment_time, a.status, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name "
        "FROM appointments a "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "WHERE a.appointment_date = CURDATE() AND a.dentist_id = %s "
        "AND a.is_archived = 0 "
        "ORDER BY a.appointment_time"
    )

    def __init__(self, data=None):
        """Initialize an appointment blueprint with optional data dict."""
        data = data or {}
        self.id = data.get("id")
        self.patient_id = data.get("patient_id")
        self.dentist_id = data.get("dentist_id")
        self.appointment_date = data.get("appointment_date")
        self.appointment_time = data.get("appointment_time")
        self.status = data.get("status", "Scheduled")
        self.notes = data.get("notes", "")
        self.created_by = data.get("created_by")
        self.date_created = data.get("date_created")
