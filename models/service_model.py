# =============================================================================
# Happy Tooth Dental Clinic and Services
# Service Model — Blueprint for dental service data structure
# =============================================================================


class ServiceModel:
    """
    Blueprint for dental service data.
    Defines the structure and fields of a service record.
    All database transactions are handled by the controller.
    """

    TABLE = "services"

    FIELDS = [
        "id",
        "service_name",
        "description",
        "price",
        "is_active",
        "date_created",
    ]

    # Queries used by the controller
    Q_SELECT_ALL = (
        "SELECT id, service_name, description, price, is_active, date_created "
        "FROM services ORDER BY service_name"
    )
    Q_SELECT_ACTIVE = (
        "SELECT id, service_name, description, price "
        "FROM services WHERE is_active = 1 "
        "ORDER BY service_name"
    )
    Q_SELECT_BY_ID = "SELECT * FROM services WHERE id = %s"
    Q_SEARCH = (
        "SELECT id, service_name, description, price, is_active, date_created "
        "FROM services "
        "WHERE service_name LIKE %s OR description LIKE %s "
        "ORDER BY service_name"
    )
    Q_INSERT = (
        "INSERT INTO services (service_name, description, price) "
        "VALUES (%s, %s, %s)"
    )
    Q_UPDATE = (
        "UPDATE services SET service_name = %s, description = %s, price = %s "
        "WHERE id = %s"
    )
    Q_TOGGLE_STATUS = "UPDATE services SET is_active = NOT is_active WHERE id = %s"
    Q_DELETE = "DELETE FROM services WHERE id = %s"

    def __init__(self, data=None):
        """Initialize a service blueprint with optional data dict."""
        data = data or {}
        self.id = data.get("id")
        self.service_name = data.get("service_name", "")
        self.description = data.get("description", "")
        self.price = data.get("price", 0.0)
        self.is_active = data.get("is_active", 1)
        self.date_created = data.get("date_created")
