# =============================================================================
# Happy Tooth Dental Clinic and Services
# Billing Controller
# =============================================================================

from database import Database
from models.billing_model import BillingModel
from models.appointment_model import AppointmentModel
from models.treatment_model import TreatmentModel
from views.billing_view import BillingDialog, ReceiptDialog


class BillingController:
    def __init__(self, view, user_data=None):
        self.view = view
        self.user_data = user_data or {}
        self.db = Database()
        self._connect_signals()
    
    def _connect_signals(self):
        self.view.add_btn.clicked.connect(self.generate_bill)
        self.view.search_input.textChanged.connect(self.search_billings)
        self.view._edit_callback = self.process_payment
        self.view._receipt_callback = self.view_receipt
        self.view._delete_callback = self.delete_billing
    
    def load_billings(self):
        billings = self.db.fetch_all(BillingModel.Q_SELECT_ALL)
        self.view.load_table(billings)
    
    def search_billings(self, keyword):
        if keyword.strip():
            search = f"%{keyword}%"
            billings = self.db.fetch_all(BillingModel.Q_SEARCH, (search, search, search))
        else:
            billings = self.db.fetch_all(BillingModel.Q_SELECT_ALL)
        self.view.load_table(billings)
    
    def _calculate_payment_status(self, total_amount, amount_paid):
        """Calculate balance and payment status from amounts."""
        balance = float(total_amount) - float(amount_paid)
        if balance <= 0:
            status = 'Paid'
        elif float(amount_paid) > 0:
            status = 'Partial'
        else:
            status = 'Unpaid'
        return balance, status
    
    def generate_bill(self):
        """Generate a new bill from an appointment's treatments."""
        appointments = self.db.fetch_all(AppointmentModel.Q_SELECT_ALL)
        # Pre-fetch treatment totals for all appointments
        treatment_totals = {}
        for a in appointments:
            result = self.db.fetch_one(TreatmentModel.Q_TOTAL_BY_APPOINTMENT, (a['id'],))
            treatment_totals[a['id']] = float(result['total']) if result and result['total'] else 0
        dialog = BillingDialog(self.view, appointments=appointments, treatment_totals=treatment_totals)
        if dialog.exec():
            data = dialog.get_data()
            appointment_id = data.get('appointment_id')
            
            if not appointment_id:
                self.view.show_warning("Error", "Please select an appointment.")
                return
            
            # Check if bill already exists for this appointment
            existing = self.db.fetch_one(BillingModel.Q_SELECT_BY_APPOINTMENT, (appointment_id,))
            if existing:
                self.view.show_warning("Exists",
                    "A bill already exists for this appointment. Use the payment button to update it.")
                return
            
            # Create billing — user_id passed from constructor + MySQL trigger as backup
            user_id = self.user_data.get('id') if self.user_data else None
            result = self.db.execute_query(
                BillingModel.Q_INSERT,
                (appointment_id, data['total_amount'], data['total_amount'], user_id)
            )
            if result:
                billing_id = result
                # If amount paid, process it
                if data['amount_paid'] > 0:
                    balance, status = self._calculate_payment_status(
                        data['total_amount'], data['amount_paid']
                    )
                    if status == 'Paid':
                        self.db.execute_query(
                            BillingModel.Q_UPDATE_WITH_DATE,
                            (data['total_amount'], data['amount_paid'], balance,
                             data['payment_method'], status, user_id, billing_id)
                        )
                    else:
                        self.db.execute_query(
                            BillingModel.Q_UPDATE,
                            (data['total_amount'], data['amount_paid'], balance,
                             data['payment_method'], status, user_id, billing_id)
                        )
                
                # Auto-update appointment status to "Completed"
                try:
                    self.db.execute_query(
                        AppointmentModel.Q_UPDATE_STATUS,
                        ('Completed', appointment_id)
                    )
                except Exception as e:
                    print(f"[Auto-Status] Could not update appointment status: {e}")
                
                self.view.show_info("Success", "Bill generated successfully!")
                self.load_billings()
            else:
                self.view.show_warning("Error", "Failed to generate bill.")
    
    def process_payment(self, billing_id):
        """Process payment on existing bill. Only staff/admin allowed."""
        if not self.user_data or self.user_data.get('role') not in ['Staff', 'Admin']:
            self.view.show_warning("Access Denied", "Only staff can process payments.")
            return
        billing = self.db.fetch_one(BillingModel.Q_SELECT_BY_ID, (billing_id,))
        if not billing:
            self.view.show_warning("Error", "Billing record not found.")
            return
        dialog = BillingDialog(self.view, billing)
        if dialog.exec():
            data = dialog.get_data()
            balance, status = self._calculate_payment_status(
                data['total_amount'], data['amount_paid']
            )
            # Get current user ID
            current_user_id = self.user_data.get('id') if self.user_data else None
            if status == 'Paid':
                result = self.db.execute_query(
                    BillingModel.Q_UPDATE_WITH_DATE,
                    (data['total_amount'], data['amount_paid'], balance,
                     data['payment_method'], status, current_user_id, billing_id)
                )
            else:
                result = self.db.execute_query(
                    BillingModel.Q_UPDATE,
                    (data['total_amount'], data['amount_paid'], balance,
                     data['payment_method'], status, current_user_id, billing_id)
                )
            if result:
                # If bill is fully paid, mark appointment as Completed
                updated_billing = self.db.fetch_one(BillingModel.Q_SELECT_BY_ID, (billing_id,))
                if updated_billing and updated_billing.get('payment_status') == 'Paid':
                    self.db.execute_query(
                        AppointmentModel.Q_UPDATE_STATUS,
                        ('Completed', updated_billing['appointment_id'])
                    )
                self.view.show_info("Success", "Payment processed successfully!")
                self.load_billings()
            else:
                self.view.show_warning("Error", "Failed to process payment.")
    
    def view_receipt(self, billing_id):
        """Open receipt preview for a billing record."""
        billing = self.db.fetch_one(BillingModel.Q_SELECT_BY_ID, (billing_id,))
        if not billing:
            self.view.show_warning("Error", "Billing record not found.")
            return
        treatments = self.db.fetch_all(
            TreatmentModel.Q_SELECT_BY_APPOINTMENT, (billing['appointment_id'],)
        )
        dialog = ReceiptDialog(self.view, billing_data=billing, treatments=treatments)
        dialog.exec()
    
    def delete_billing(self, billing_id):
        if self.view.show_confirm("Confirm Delete", "Are you sure you want to delete this billing record?"):
            result = self.db.execute_query(BillingModel.Q_DELETE, (billing_id,))
            if result:
                self.view.show_info("Deleted", "Billing record deleted successfully.")
                self.load_billings()
            else:
                self.view.show_warning("Error", "Failed to delete billing record.")
