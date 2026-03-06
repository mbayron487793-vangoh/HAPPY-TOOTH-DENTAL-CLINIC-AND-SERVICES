# =============================================================================
# Happy Tooth Dental Clinic and Services
# Dentist Model — Blueprint for dentist data structure
# =============================================================================


class DentistModel:
    """
    Blueprint for dentist data.
    Defines the structure and fields of a dentist record.
    All database transactions are handled by the controller.
    """

    TABLE = "dentists"

    FIELDS = [
        "id",
        "first_name",
        "last_name",
        "specialization",
        "contact_number",
        "email",
        "user_id",
        "is_active",
        "date_created",
    ]

    # Queries used by the controller
    Q_SELECT_ALL = (
        "SELECT d.id, d.first_name, d.last_name, d.specialization, "
        "d.contact_number, d.email, d.is_active, d.date_created, "
        "u.username AS user_account "
        "FROM dentists d "
        "LEFT JOIN users u ON d.user_id = u.id "
        "ORDER BY d.last_name, d.first_name"
    )
    Q_SELECT_ACTIVE = (
        "SELECT id, first_name, last_name, specialization "
        "FROM dentists WHERE is_active = 1 "
        "ORDER BY last_name, first_name"
    )
    Q_SELECT_BY_ID = (
        "SELECT d.*, u.username AS user_account "
        "FROM dentists d "
        "LEFT JOIN users u ON d.user_id = u.id "
        "WHERE d.id = %s"
    )
    Q_SELECT_BY_USER_ID = "SELECT id FROM dentists WHERE user_id = %s"
    Q_SEARCH = (
        "SELECT d.id, d.first_name, d.last_name, d.specialization, "
        "d.contact_number, d.email, d.is_active, d.date_created "
        "FROM dentists d "
        "WHERE d.first_name LIKE %s OR d.last_name LIKE %s "
        "OR d.specialization LIKE %s "
        "ORDER BY d.last_name, d.first_name"
    )
    Q_INSERT = (
        "INSERT INTO dentists (first_name, last_name, specialization, "
        "contact_number, email, user_id) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    Q_UPDATE = (
        "UPDATE dentists SET first_name = %s, last_name = %s, "
        "specialization = %s, contact_number = %s, email = %s, user_id = %s "
        "WHERE id = %s"
    )
    Q_TOGGLE_STATUS = "UPDATE dentists SET is_active = NOT is_active WHERE id = %s"
    Q_DELETE = "DELETE FROM dentists WHERE id = %s"

    def __init__(self, data=None):
        """Initialize a dentist blueprint with optional data dict."""
        data = data or {}
        self.id = data.get("id")
        self.first_name = data.get("first_name", "")
        self.last_name = data.get("last_name", "")
        self.specialization = data.get("specialization", "")
        self.contact_number = data.get("contact_number", "")
        self.email = data.get("email", "")
        self.user_id = data.get("user_id")
        self.is_active = data.get("is_active", 1)
        self.date_created = data.get("date_created")
