# =============================================================================
# Happy Tooth Dental Clinic and Services
# Billing Model — Blueprint for billing data structure
# =============================================================================


class BillingModel:
    """
    Blueprint for billing data.
    Defines the structure and fields of a billing record.
    All database transactions are handled by the controller.
    """

    TABLE = "billings"

    FIELDS = [
        "id",
        "appointment_id",
        "total_amount",
        "amount_paid",
        "balance",
        "payment_method",
        "payment_status",
        "date_paid",
        "generated_by",
        "processed_by",
        "date_created",
    ]

    # Queries used by the controller
    Q_SELECT_ALL = (
        "SELECT b.id, b.total_amount, b.amount_paid, b.balance, "
        "b.payment_method, b.payment_status, b.date_paid, "
        "b.date_created, b.appointment_id, "
        "a.appointment_date, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name, "
        "CONCAT(u.first_name, ' ', u.last_name) AS generated_by_name "
        "FROM billings b "
        "JOIN appointments a ON b.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "LEFT JOIN users u ON b.generated_by = u.id "
        "ORDER BY b.date_created DESC"
    )
    Q_SELECT_BY_ID = (
        "SELECT b.*, "
        "a.appointment_date, a.appointment_time, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "p.contact_number AS patient_contact, "
        "p.address AS patient_address, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name, "
        "d.specialization, "
        "CONCAT(u.first_name, ' ', u.last_name) AS generated_by_name, "
        "CONCAT(u2.first_name, ' ', u2.last_name) AS processed_by_name "
        "FROM billings b "
        "JOIN appointments a ON b.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "LEFT JOIN users u ON b.generated_by = u.id "
        "LEFT JOIN users u2 ON b.processed_by = u2.id "
        "WHERE b.id = %s"
    )
    Q_SELECT_BY_APPOINTMENT = (
        "SELECT b.*, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name "
        "FROM billings b "
        "JOIN appointments a ON b.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "WHERE b.appointment_id = %s"
    )
    Q_SELECT_RAW_BY_ID = "SELECT * FROM billings WHERE id = %s"
    Q_SEARCH = (
        "SELECT b.id, b.total_amount, b.amount_paid, b.balance, "
        "b.payment_method, b.payment_status, b.date_paid, "
        "b.date_created, b.appointment_id, "
        "a.appointment_date, "
        "CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "CONCAT(d.first_name, ' ', d.last_name) AS dentist_name, "
        "CONCAT(u.first_name, ' ', u.last_name) AS generated_by_name "
        "FROM billings b "
        "JOIN appointments a ON b.appointment_id = a.id "
        "JOIN patients p ON a.patient_id = p.id "
        "JOIN dentists d ON a.dentist_id = d.id "
        "LEFT JOIN users u ON b.generated_by = u.id "
        "WHERE p.first_name LIKE %s OR p.last_name LIKE %s "
        "OR b.payment_status LIKE %s "
        "ORDER BY b.date_created DESC"
    )
    Q_INSERT = (
        "INSERT INTO billings (appointment_id, total_amount, balance, payment_status, generated_by) "
        "VALUES (%s, %s, %s, 'Unpaid', %s)"
    )
    Q_INSERT_FULL = (
        "INSERT INTO billings (appointment_id, total_amount, amount_paid, balance, "
        "payment_status, date_created) VALUES (%s, %s, %s, %s, %s, NOW())"
    )
    Q_UPDATE = (
        "UPDATE billings SET total_amount = %s, amount_paid = %s, balance = %s, "
        "payment_method = %s, payment_status = %s, processed_by = %s "
        "WHERE id = %s"
    )
    Q_UPDATE_WITH_DATE = (
        "UPDATE billings SET total_amount = %s, amount_paid = %s, balance = %s, "
        "payment_method = %s, payment_status = %s, processed_by = %s, date_paid = CURRENT_TIMESTAMP "
        "WHERE id = %s"
    )
    Q_UPDATE_PAYMENT = (
        "UPDATE billings SET amount_paid = %s, balance = %s, "
        "payment_method = %s, payment_status = %s "
        "WHERE id = %s"
    )
    Q_UPDATE_PAYMENT_WITH_DATE = (
        "UPDATE billings SET amount_paid = %s, balance = %s, "
        "payment_method = %s, payment_status = %s, date_paid = CURRENT_TIMESTAMP "
        "WHERE id = %s"
    )
    Q_DELETE = "DELETE FROM billings WHERE id = %s"
    Q_TODAY_REVENUE = (
        "SELECT COALESCE(SUM(amount_paid), 0) AS revenue "
        "FROM billings "
        "WHERE DATE(date_paid) = CURDATE() AND payment_status IN ('Paid', 'Partial')"
    )
    Q_MONTHLY_REVENUE = (
        "SELECT COALESCE(SUM(amount_paid), 0) AS revenue "
        "FROM billings "
        "WHERE MONTH(date_paid) = MONTH(CURDATE()) "
        "AND YEAR(date_paid) = YEAR(CURDATE()) "
        "AND payment_status IN ('Paid', 'Partial')"
    )
    Q_UNPAID_COUNT = (
        "SELECT COUNT(*) AS total FROM billings "
        "WHERE payment_status IN ('Unpaid', 'Partial')"
    )
    Q_MONTHLY_PAID = (
        "SELECT total_amount FROM billings "
        "WHERE payment_status = 'Paid' "
        "AND MONTH(date_paid) = MONTH(CURDATE()) "
        "AND YEAR(date_paid) = YEAR(CURDATE())"
    )
    Q_UNPAID_COUNT_ONLY = (
        "SELECT COUNT(*) AS total FROM billings WHERE payment_status = 'Unpaid'"
    )

    def __init__(self, data=None):
        """Initialize a billing blueprint with optional data dict."""
        data = data or {}
        self.id = data.get("id")
        self.appointment_id = data.get("appointment_id")
        self.total_amount = data.get("total_amount", 0.0)
        self.amount_paid = data.get("amount_paid", 0.0)
        self.balance = data.get("balance", 0.0)
        self.payment_method = data.get("payment_method", "")
        self.payment_status = data.get("payment_status", "Unpaid")
        self.date_paid = data.get("date_paid")
        self.generated_by = data.get("generated_by")
        self.processed_by = data.get("processed_by")
        self.date_created = data.get("date_created")
