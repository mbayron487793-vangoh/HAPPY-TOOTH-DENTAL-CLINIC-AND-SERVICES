# =============================================================================
# Happy Tooth Dental Clinic and Services
# Dashboard View — Overview stats and today's appointments + Charts
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import qtawesome as qta

# Matplotlib imports for embedded charts
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DashboardView(QWidget):
    """Dashboard page showing clinic overview."""
    
    def __init__(self):
        super().__init__()
        self.user_role = 'Admin'  # default, overridden by controller
        self.init_ui()
    
    def set_user_role(self, role):
        """Set the role and show/hide sections accordingly."""
        self.user_role = role
        # Revenue & Unpaid cards — Admin/Staff only
        is_admin_staff = role in ('Admin', 'Staff')
        self.revenue_card.setVisible(is_admin_staff)
        self.unpaid_card.setVisible(is_admin_staff)
        # Recent patients — Admin/Staff only
        self.recent_header.setVisible(is_admin_staff)
        self.recent_table.setVisible(is_admin_staff)
        # Charts — Admin/Staff only
        self.charts_header.setVisible(is_admin_staff)
        self.weekly_card.setVisible(is_admin_staff)
        self.services_card.setVisible(is_admin_staff)
        self.revenue_chart_card.setVisible(is_admin_staff)
        # Update welcome label
        if role == 'Dentist':
            self.welcome_label.setText("Welcome, Doctor!")
            self.appt_header.setText("Your Appointments Today")
        elif role == 'Staff':
            self.welcome_label.setText("Welcome, Staff!")
        else:
            self.welcome_label.setText("Welcome to Happy Tooth Dental Clinic!")
    
    def init_ui(self):
        """Build dashboard layout."""
        # Scroll area for the content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: #F8FBFC; border: none;")
        
        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(32, 24, 32, 32)
        self.main_layout.setSpacing(24)
        
        # ---- Welcome Section ----
        self.welcome_label = QLabel("Welcome to Happy Tooth Dental Clinic!")
        self.welcome_label.setStyleSheet("""
            font-family: 'Poppins', 'Segoe UI', sans-serif;
            font-size: 22px;
            font-weight: 600;
            color: #1A6E7A;
            background-color: transparent;
            padding: 8px 0px;
            letter-spacing: 0.3px;
        """)
        self.main_layout.addWidget(self.welcome_label)
        
        # ---- Stat Cards Row ----
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        stats_layout.setContentsMargins(0, 8, 0, 8)
        
        # Patient Count Card
        self.patient_card, self.patient_count_label = self._create_stat_card(
            "Total Patients", "0", 'fa5s.users', '#1A6E7A', 'stat_card'
        )
        stats_layout.addWidget(self.patient_card, 1)  # stretch factor 1
        
        # Today's Appointments Card
        self.appt_card, self.appt_count_label = self._create_stat_card(
            "Today's Appointments", "0", 'fa5s.calendar-check', '#2AACB8', 'stat_card'
        )
        stats_layout.addWidget(self.appt_card, 1)
        
        # Monthly Revenue Card
        self.revenue_card, self.revenue_label = self._create_stat_card(
            "Monthly Revenue", "₱0.00", 'fa5s.money-bill-wave', '#2E7D32', 'stat_card_green'
        )
        stats_layout.addWidget(self.revenue_card, 1)
        
        # Unpaid Billings Card
        self.unpaid_card, self.unpaid_label = self._create_stat_card(
            "Unpaid Bills", "0", 'fa5s.exclamation-triangle', '#FB8C00', 'stat_card'
        )
        stats_layout.addWidget(self.unpaid_card, 1)
        
        self.main_layout.addLayout(stats_layout)
        
        # ---- Today's Appointments Table ----
        self.appt_header = QLabel("Today's Appointments")
        self.appt_header.setObjectName("section_title")
        self.main_layout.addWidget(self.appt_header)
        
        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(4)
        self.appointments_table.setHorizontalHeaderLabels([
            "Patient", "Dentist", "Time", "Status"
        ])
        self.appointments_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.appointments_table.setAlternatingRowColors(True)
        self.appointments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.appointments_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.appointments_table.verticalHeader().setVisible(False)
        self.appointments_table.setMinimumHeight(250)
        self.main_layout.addWidget(self.appointments_table)
        
        # ---- Recently Registered Patients ----
        self.recent_header = QLabel("Recently Registered Patients")
        self.recent_header.setObjectName("section_title")
        self.main_layout.addWidget(self.recent_header)
        
        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(3)
        self.recent_table.setHorizontalHeaderLabels([
            "Patient Name", "Contact", "Date Registered"
        ])
        self.recent_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recent_table.setAlternatingRowColors(True)
        self.recent_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.recent_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.recent_table.verticalHeader().setVisible(False)
        self.recent_table.setMinimumHeight(200)
        self.main_layout.addWidget(self.recent_table)
        
        # ---- Charts Section (Admin / Staff only) ----
        self.charts_header = QLabel("Analytics & Reports")
        self.charts_header.setObjectName("section_title")
        self.main_layout.addWidget(self.charts_header)
        
        # Charts row — two charts side by side
        charts_row = QHBoxLayout()
        charts_row.setSpacing(24)
        
        # Left chart: Weekly Appointments Bar Chart
        self.weekly_card = QFrame()
        self.weekly_card.setObjectName("stat_card")
        self.weekly_card.setMinimumHeight(320)
        # Add shadow to chart card
        weekly_shadow = QGraphicsDropShadowEffect()
        weekly_shadow.setBlurRadius(24)
        weekly_shadow.setXOffset(0)
        weekly_shadow.setYOffset(4)
        weekly_shadow.setColor(QColor(26, 110, 122, 30))
        self.weekly_card.setGraphicsEffect(weekly_shadow)
        
        weekly_layout = QVBoxLayout(self.weekly_card)
        weekly_layout.setContentsMargins(20, 20, 20, 20)
        weekly_title = QLabel("Appointments This Week")
        weekly_title.setStyleSheet("font-family: 'Poppins', 'Segoe UI', sans-serif; font-size: 14px; font-weight: 600; color: #1A6E7A; background: transparent; letter-spacing: 0.2px; padding-bottom: 8px;")
        weekly_layout.addWidget(weekly_title)
        
        self.weekly_figure = Figure(figsize=(5, 3), dpi=100)
        self.weekly_figure.patch.set_facecolor('#FFFFFF')
        self.weekly_canvas = FigureCanvas(self.weekly_figure)
        self.weekly_canvas.setStyleSheet("background-color: #FFFFFF; border-radius: 8px;")
        weekly_layout.addWidget(self.weekly_canvas)
        charts_row.addWidget(self.weekly_card)
        
        # Right chart: Services Pie Chart
        self.services_card = QFrame()
        self.services_card.setObjectName("stat_card")
        self.services_card.setMinimumHeight(320)
        # Add shadow to services chart card
        services_shadow = QGraphicsDropShadowEffect()
        services_shadow.setBlurRadius(24)
        services_shadow.setXOffset(0)
        services_shadow.setYOffset(4)
        services_shadow.setColor(QColor(26, 110, 122, 30))
        self.services_card.setGraphicsEffect(services_shadow)
        
        services_layout = QVBoxLayout(self.services_card)
        services_layout.setContentsMargins(20, 20, 20, 20)
        services_title = QLabel("Top Services Breakdown")
        services_title.setStyleSheet("font-family: 'Poppins', 'Segoe UI', sans-serif; font-size: 14px; font-weight: 600; color: #1A6E7A; background: transparent; letter-spacing: 0.2px; padding-bottom: 8px;")
        services_layout.addWidget(services_title)
        
        self.services_figure = Figure(figsize=(5, 3), dpi=100)
        self.services_figure.patch.set_facecolor('#FFFFFF')
        self.services_canvas = FigureCanvas(self.services_figure)
        self.services_canvas.setStyleSheet("background-color: #FFFFFF; border-radius: 8px;")
        services_layout.addWidget(self.services_canvas)
        charts_row.addWidget(self.services_card)
        
        self.main_layout.addLayout(charts_row)
        
        # Second charts row — Revenue Trend
        self.revenue_chart_card = QFrame()
        self.revenue_chart_card.setObjectName("stat_card")
        self.revenue_chart_card.setMinimumHeight(320)
        # Add shadow to revenue chart card
        revenue_shadow = QGraphicsDropShadowEffect()
        revenue_shadow.setBlurRadius(24)
        revenue_shadow.setXOffset(0)
        revenue_shadow.setYOffset(4)
        revenue_shadow.setColor(QColor(26, 110, 122, 30))
        self.revenue_chart_card.setGraphicsEffect(revenue_shadow)
        
        revenue_chart_layout = QVBoxLayout(self.revenue_chart_card)
        revenue_chart_layout.setContentsMargins(20, 20, 20, 20)
        revenue_chart_title = QLabel("Monthly Revenue Trend")
        revenue_chart_title.setStyleSheet("font-family: 'Poppins', 'Segoe UI', sans-serif; font-size: 14px; font-weight: 600; color: #2E7D32; background: transparent; letter-spacing: 0.2px; padding-bottom: 8px;")
        revenue_chart_layout.addWidget(revenue_chart_title)
        
        self.revenue_figure = Figure(figsize=(10, 3), dpi=100)
        self.revenue_figure.patch.set_facecolor('#FFFFFF')
        self.revenue_canvas = FigureCanvas(self.revenue_figure)
        self.revenue_canvas.setStyleSheet("background-color: #FFFFFF; border-radius: 8px;")
        revenue_chart_layout.addWidget(self.revenue_canvas)
        self.main_layout.addWidget(self.revenue_chart_card)
        
        # Spacer at bottom
        self.main_layout.addSpacerItem(
            QSpacerItem(20, 32, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
        
        scroll.setWidget(scroll_content)
        
        # Set scroll as the main layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)
    
    def _create_stat_card(self, title, value, icon_name, icon_color, card_style):
        """Create a modern stat card widget. Returns (card_frame, value_label)."""
        card = QFrame()
        card.setObjectName(card_style)
        card.setFixedHeight(180)
        card.setMinimumWidth(220)
        
        # Add colored left border line instead of shadow
        card.setStyleSheet(f"""
            QFrame#{card_style} {{
                background-color: #FFFFFF;
                border: none;
                border-left: 4px solid {icon_color};
                border-radius: 16px;
                padding: 0px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon with circular background - larger container with proper padding
        icon_container = QFrame()
        icon_container.setFixedSize(56, 56)
        # Create a light tint of the icon color for background
        bg_color = self._get_icon_bg_color(icon_color)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 28px;
                padding: 0px;
                margin: 0px;
            }}
        """)
        
        # Use a widget-based centering approach instead of layout
        icon_label = QLabel(icon_container)
        icon_label.setFixedSize(56, 56)
        icon_label.setPixmap(qta.icon(icon_name, color=icon_color).pixmap(28, 28))
        icon_label.setStyleSheet("background-color: transparent; padding: 0px; margin: 0px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Center the icon container horizontally
        icon_wrapper = QHBoxLayout()
        icon_wrapper.setContentsMargins(0, 0, 0, 4)
        icon_wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_wrapper.addWidget(icon_container)
        layout.addLayout(icon_wrapper)
        
        # Value - large bold number
        value_label = QLabel(value)
        value_label.setObjectName("stat_number" if 'green' not in card_style else "stat_number_green")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        # Title - subtle label
        title_label = QLabel(title)
        title_label.setObjectName("stat_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        return card, value_label
    
    def _get_icon_bg_color(self, icon_color):
        """Get a light background tint for the icon circle."""
        color_map = {
            '#1A6E7A': 'rgba(26, 110, 122, 0.12)',   # Teal
            '#2AACB8': 'rgba(42, 172, 184, 0.12)',   # Light teal
            '#2E7D32': 'rgba(46, 125, 50, 0.12)',    # Green
            '#FB8C00': 'rgba(251, 140, 0, 0.12)',    # Orange/Warning
        }
        return color_map.get(icon_color, 'rgba(26, 110, 122, 0.1)')
    
    def update_stats(self, patient_count, today_appt, monthly_revenue, unpaid_count):
        """Update all stat card values."""
        self.patient_count_label.setText(str(patient_count))
        self.appt_count_label.setText(str(today_appt))
        self.revenue_label.setText(f"₱{monthly_revenue:,.2f}")
        self.unpaid_label.setText(str(unpaid_count))
    
    def load_today_appointments(self, appointments):
        """Populate today's appointments table."""
        self.appointments_table.setRowCount(0)
        for row_num, appt in enumerate(appointments):
            self.appointments_table.insertRow(row_num)
            
            patient_item = QTableWidgetItem(appt['patient_name'])
            patient_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointments_table.setItem(row_num, 0, patient_item)
            
            dentist_item = QTableWidgetItem(appt['dentist_name'])
            dentist_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointments_table.setItem(row_num, 1, dentist_item)
            
            # Format time as AM/PM
            raw_time = appt.get('appointment_time', '')
            time_display = self._format_time_ampm(raw_time)
            time_item = QTableWidgetItem(time_display)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.appointments_table.setItem(row_num, 2, time_item)
            
            # Status with color
            status_item = QTableWidgetItem(appt['status'])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if appt['status'] == 'Completed':
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif appt['status'] == 'Cancelled':
                status_item.setForeground(Qt.GlobalColor.red)
            elif appt['status'] == 'Scheduled':
                status_item.setForeground(Qt.GlobalColor.blue)
            self.appointments_table.setItem(row_num, 3, status_item)
    
    def load_recent_patients(self, patients):
        """Populate recent patients table."""
        self.recent_table.setRowCount(0)
        for row_num, patient in enumerate(patients):
            self.recent_table.insertRow(row_num)
            
            name = f"{patient['first_name']} {patient['last_name']}"
            name_item = QTableWidgetItem(name)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.recent_table.setItem(row_num, 0, name_item)
            
            contact_item = QTableWidgetItem(patient.get('contact_number', ''))
            contact_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.recent_table.setItem(row_num, 1, contact_item)
            
            date_item = QTableWidgetItem(str(patient.get('date_registered', '')))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.recent_table.setItem(row_num, 2, date_item)
    
    @staticmethod
    def _format_time_ampm(raw_time):
        """Convert timedelta or HH:MM:SS string to 12-hour AM/PM format."""
        try:
            time_str = str(raw_time)
            parts = time_str.split(':')
            if len(parts) >= 2:
                hour = int(parts[0])
                minute = int(parts[1])
                period = "AM" if hour < 12 else "PM"
                display_hour = hour % 12
                if display_hour == 0:
                    display_hour = 12
                return f"{display_hour}:{minute:02d} {period}"
        except Exception:
            pass
        return str(raw_time)
    
    def load_weekly_chart(self, data):
        """
        Draw weekly appointments bar chart.
        data: list of dicts with 'day_name' and 'count'
        """
        self.weekly_figure.clear()
        ax = self.weekly_figure.add_subplot(111)
        
        if data:
            days = [d['day_name'] for d in data]
            counts = [d['count'] for d in data]
        else:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            counts = [0] * 7
        
        colors = ['#2AACB8', '#35C4D0', '#1B8FA0', '#157080', '#2AACB8', '#35C4D0', '#1B8FA0']
        bars = ax.bar(days, counts, color=colors[:len(days)], edgecolor='white', linewidth=0.5, width=0.6)
        
        # Add count labels on bars
        for bar, count in zip(bars, counts):
            if count > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                        str(count), ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1A6E7A')
        
        ax.set_ylabel('Appointments', fontsize=10, color='#78909C')
        ax.set_ylim(bottom=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#D4E6E9')
        ax.spines['bottom'].set_color('#D4E6E9')
        ax.tick_params(colors='#78909C', labelsize=9)
        ax.set_facecolor('#FAFFFE')
        self.weekly_figure.tight_layout(pad=1.5)
        self.weekly_canvas.draw()
    
    def load_services_chart(self, data):
        """
        Draw services pie chart.
        data: list of dicts with 'service_name' and 'count'
        """
        self.services_figure.clear()
        ax = self.services_figure.add_subplot(111)
        
        if data:
            labels = [d['service_name'][:20] for d in data]
            sizes = [d['count'] for d in data]
        else:
            labels = ['No data']
            sizes = [1]
        
        colors_list = ['#2AACB8', '#1A6E7A', '#35C4D0', '#66BB6A', '#FB8C00',
                        '#7B1FA2', '#E53935', '#1565C0', '#FFD54F', '#78909C']
        
        wedges, texts, autotexts = ax.pie(
            sizes, labels=None, autopct='%1.0f%%',
            colors=colors_list[:len(sizes)],
            startangle=90, pctdistance=0.75,
            textprops={'fontsize': 9, 'color': 'white', 'fontweight': 'bold'}
        )
        
        # Add a legend on the side
        ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0.5),
                  fontsize=8, frameon=False)
        
        ax.set_facecolor('#FFFFFF')
        self.services_figure.tight_layout(pad=1.0)
        self.services_canvas.draw()
    
    def load_revenue_chart(self, data):
        """
        Draw monthly revenue line/bar chart.
        data: list of dicts with 'month_name' and 'revenue'
        """
        self.revenue_figure.clear()
        ax = self.revenue_figure.add_subplot(111)
        
        if data:
            months = [d['month_name'] for d in data]
            revenues = [float(d['revenue']) for d in data]
        else:
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            revenues = [0] * 6
        
        # Bar chart with gradient-like colors
        bar_colors = ['#2E7D32' if r > 0 else '#E0E0E0' for r in revenues]
        bars = ax.bar(months, revenues, color=bar_colors, edgecolor='white', linewidth=0.5, width=0.5)
        
        # Line overlay
        if any(r > 0 for r in revenues):
            ax.plot(months, revenues, color='#1A6E7A', marker='o', markersize=6,
                    linewidth=2, markerfacecolor='#2AACB8', markeredgecolor='white', markeredgewidth=1.5)
        
        # Value labels
        for bar, rev in zip(bars, revenues):
            if rev > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(revenues) * 0.03,
                        f'₱{rev:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color='#2E7D32')
        
        ax.set_ylabel('Revenue (₱)', fontsize=10, color='#78909C')
        ax.set_ylim(bottom=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#D4E6E9')
        ax.spines['bottom'].set_color('#D4E6E9')
        ax.tick_params(colors='#78909C', labelsize=9)
        ax.set_facecolor('#FAFFFE')
        
        # Format y-axis with peso
        from matplotlib.ticker import FuncFormatter
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'₱{x:,.0f}'))
        
        self.revenue_figure.tight_layout(pad=1.5)
        self.revenue_canvas.draw()
