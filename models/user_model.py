# =============================================================================
# Happy Tooth Dental Clinic and Services
# User Model — Blueprint for user data structure
# =============================================================================


class UserModel:
    """
    Blueprint for user data.
    Defines the structure and fields of a user record.
    All database transactions are handled by the controller.
    """

    TABLE = "users"

    FIELDS = [
        "id",
        "username",
        "password_hash",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "date_created",
    ]

    # Queries used by the controller
    Q_SELECT_ALL = (
        "SELECT id, username, first_name, last_name, role, is_active, date_created "
        "FROM users ORDER BY id"
    )
    Q_SELECT_BY_ID = "SELECT * FROM users WHERE id = %s"
    Q_SELECT_BY_USERNAME = "SELECT * FROM users WHERE username = %s AND is_active = 1"
    Q_CHECK_USERNAME = "SELECT id FROM users WHERE username = %s"
    Q_CHECK_USERNAME_EXCLUDE = "SELECT id FROM users WHERE username = %s AND id != %s"
    Q_GET_ID_BY_USERNAME = "SELECT id FROM users WHERE username = %s"
    Q_INSERT = (
        "INSERT INTO users (username, password_hash, first_name, last_name, role) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    Q_UPDATE = (
        "UPDATE users SET username = %s, first_name = %s, last_name = %s, role = %s "
        "WHERE id = %s"
    )
    Q_UPDATE_PASSWORD = "UPDATE users SET password_hash = %s WHERE id = %s"
    Q_TOGGLE_STATUS = "UPDATE users SET is_active = NOT is_active WHERE id = %s"
    Q_DELETE = "DELETE FROM users WHERE id = %s"

    def __init__(self, data=None):
        """Initialize a user blueprint with optional data dict."""
        data = data or {}
        self.id = data.get("id")
        self.username = data.get("username", "")
        self.password_hash = data.get("password_hash", "")
        self.first_name = data.get("first_name", "")
        self.last_name = data.get("last_name", "")
        self.role = data.get("role", "Staff")
        self.is_active = data.get("is_active", 1)
        self.date_created = data.get("date_created")
