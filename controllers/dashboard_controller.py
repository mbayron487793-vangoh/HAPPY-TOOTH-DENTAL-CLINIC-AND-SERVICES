# =============================================================================
# Happy Tooth Dental Clinic and Services
# Dashboard Controller
# =============================================================================

from database import Database
from models.patient_model import PatientModel
from models.appointment_model import AppointmentModel
from models.billing_model import BillingModel
from models.dentist_model import DentistModel


class DashboardController:
    """Controller for the Dashboard page."""
    
    def __init__(self, view, user_data=None):
        self.view = view
        self.user_data = user_data or {}
        self.db = Database()
        
        # Set role on the view to show/hide sections
        role = self.user_data.get('role', 'Admin')
        self.view.set_user_role(role)
    
    def _is_dentist_role(self):
        return self.user_data.get('role') == 'Dentist'
    
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
    
    def load_dashboard(self):
        """Load all dashboard data based on user role."""
        role = self.user_data.get('role', 'Admin')
        try:
            if role == 'Admin':
                self._load_admin_dashboard()
            elif role == 'Dentist':
                self._load_dentist_dashboard()
            elif role == 'Staff':
                self._load_staff_dashboard()
        except Exception as e:
            print(f"[Dashboard Error] {e}")
    
    def _load_admin_dashboard(self):
        """Admin sees everything."""
        patient_count_row = self.db.fetch_one(PatientModel.Q_COUNT)
        patient_count = patient_count_row['total'] if patient_count_row else 0
        
        today_count_row = self.db.fetch_one(AppointmentModel.Q_COUNT_TODAY)
        today_count = today_count_row['total'] if today_count_row else 0
        
        # Monthly revenue: sum only paid bills
        paid_bills = self.db.fetch_all(BillingModel.Q_MONTHLY_PAID)
        monthly_revenue = sum(b['total_amount'] for b in paid_bills) if paid_bills else 0
        
        # Unpaid bills summary
        unpaid_row = self.db.fetch_one(BillingModel.Q_UNPAID_COUNT_ONLY)
        unpaid_count = unpaid_row['total'] if unpaid_row else 0
        
        self.view.update_stats(patient_count, today_count, monthly_revenue, unpaid_count)
        
        today_appts = self.db.fetch_all(AppointmentModel.Q_SELECT_TODAY)
        self.view.load_today_appointments(today_appts)
        
        recent_patients = self.db.fetch_all(PatientModel.Q_RECENT, (5,))
        self.view.load_recent_patients(recent_patients)
        
        # --- Load charts ---
        self._load_charts()
    
    def _load_dentist_dashboard(self):
        """Dentist sees only their own appointments and patient count."""
        dentist_id = self._get_dentist_id()
        
        patient_count_row = self.db.fetch_one(PatientModel.Q_COUNT)
        patient_count = patient_count_row['total'] if patient_count_row else 0
        
        # Only this dentist's today appointments
        if dentist_id:
            today_appts = self.db.fetch_all(
                AppointmentModel.Q_SELECT_TODAY_BY_DENTIST, (dentist_id,)
            )
            today_count = len(today_appts)
        else:
            today_appts = []
            today_count = 0
        
        self.view.update_stats(patient_count, today_count, 0, 0)
        self.view.load_today_appointments(today_appts)
    
    def _load_staff_dashboard(self):
        """Staff sees patients, all appointments, billing stats."""
        patient_count_row = self.db.fetch_one(PatientModel.Q_COUNT)
        patient_count = patient_count_row['total'] if patient_count_row else 0
        
        today_count_row = self.db.fetch_one(AppointmentModel.Q_COUNT_TODAY)
        today_count = today_count_row['total'] if today_count_row else 0
        
        monthly_revenue_row = self.db.fetch_one(BillingModel.Q_MONTHLY_REVENUE)
        monthly_revenue = float(monthly_revenue_row['revenue']) if monthly_revenue_row else 0.0
        
        unpaid_row = self.db.fetch_one(BillingModel.Q_UNPAID_COUNT)
        unpaid_count = unpaid_row['total'] if unpaid_row else 0
        
        self.view.update_stats(patient_count, today_count, monthly_revenue, unpaid_count)
        
        today_appts = self.db.fetch_all(AppointmentModel.Q_SELECT_TODAY)
        self.view.load_today_appointments(today_appts)
        
        recent_patients = self.db.fetch_all(PatientModel.Q_RECENT, (5,))
        self.view.load_recent_patients(recent_patients)
        
        # --- Load charts ---
        self._load_charts()
    
    # -------------------------------------------------------------------------
    # Chart Data Methods
    # -------------------------------------------------------------------------
    
    def _load_charts(self):
        """Fetch data for all 3 dashboard charts and render them."""
        try:
            self._load_weekly_chart()
        except Exception as e:
            print(f"[Chart Error - Weekly] {e}")
        try:
            self._load_services_chart()
        except Exception as e:
            print(f"[Chart Error - Services] {e}")
        try:
            self._load_revenue_chart()
        except Exception as e:
            print(f"[Chart Error - Revenue] {e}")
    
    def _load_weekly_chart(self):
        """Fetch appointment counts for each day of the current week."""
        rows = self.db.fetch_all(
            """SELECT DAYNAME(appointment_date) AS day_name,
                      COUNT(*) AS count
               FROM appointments
               WHERE YEARWEEK(appointment_date, 1) = YEARWEEK(CURDATE(), 1)
               GROUP BY DAYOFWEEK(appointment_date), DAYNAME(appointment_date)
               ORDER BY DAYOFWEEK(appointment_date)"""
        )
        
        # Build full week data (Mon-Sun) with 0-fill
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        short_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        day_map = {}
        if rows:
            for r in rows:
                day_map[r['day_name']] = r['count']
        
        data = []
        for full, short in zip(day_order, short_names):
            data.append({'day_name': short, 'count': day_map.get(full, 0)})
        
        self.view.load_weekly_chart(data)
    
    def _load_services_chart(self):
        """Fetch top services by treatment count."""
        rows = self.db.fetch_all(
            """SELECT s.service_name, COUNT(*) AS count
               FROM treatments t
               JOIN services s ON t.service_id = s.id
               GROUP BY s.id, s.service_name
               ORDER BY count DESC
               LIMIT 6"""
        )
        
        data = []
        if rows:
            for r in rows:
                data.append({'service_name': r['service_name'], 'count': r['count']})
        
        self.view.load_services_chart(data)
    
    def _load_revenue_chart(self):
        """Fetch monthly revenue for the last 6 months."""
        rows = self.db.fetch_all(
            """SELECT DATE_FORMAT(date_created, '%%b') AS month_name,
                      SUM(total_amount) AS revenue
               FROM billings
               WHERE date_created >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
               GROUP BY YEAR(date_created), MONTH(date_created),
                        DATE_FORMAT(date_created, '%%b')
               ORDER BY YEAR(date_created), MONTH(date_created)"""
        )
        
        data = []
        if rows:
            for r in rows:
                data.append({'month_name': r['month_name'], 'revenue': r['revenue'] or 0})
        
        self.view.load_revenue_chart(data)
