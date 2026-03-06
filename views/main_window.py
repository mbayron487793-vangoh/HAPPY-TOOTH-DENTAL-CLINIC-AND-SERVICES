# =============================================================================
# Happy Tooth Dental Clinic and Services
# Main Window — Sidebar navigation + content area
# =============================================================================

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QSpacerItem, QSizePolicy, QMessageBox, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QCloseEvent
import qtawesome as qta

from views.dashboard_view import DashboardView
from views.patient_view import PatientView
from views.dentist_view import DentistView
from views.appointment_view import AppointmentView
from views.service_view import ServiceView
from views.treatment_view import TreatmentView
from views.billing_view import BillingView
from views.user_view import UserView

from controllers.dashboard_controller import DashboardController
from controllers.patient_controller import PatientController
from controllers.dentist_controller import DentistController
from controllers.appointment_controller import AppointmentController
from controllers.service_controller import ServiceController
from controllers.treatment_controller import TreatmentController
from controllers.billing_controller import BillingController
from controllers.user_controller import UserController


class MainWindow(QMainWindow):
    """Main application window with sidebar and content area."""
    
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Happy Tooth Dental Clinic and Services")
        self.setMinimumSize(1200, 700)
        self.sidebar_buttons = []
        self.init_ui()
        self.show_page(0)  # Show dashboard by default
    
    def init_ui(self):
        """Build the main window layout."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ---- SIDEBAR ----
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo in sidebar
        logo_container = QWidget()
        logo_container.setStyleSheet("background-color: transparent;")
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 24, 20, 8)
        logo_layout.setSpacing(8)
        
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled = pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled)
        logo_label.setStyleSheet("background-color: transparent;")
        logo_layout.addWidget(logo_label)
        
        clinic_name = QLabel("Happy Tooth")
        clinic_name.setObjectName("sidebar_title")
        clinic_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clinic_name.setStyleSheet("""
            color: #1A6E7A;
            font-family: 'Poppins', 'Segoe UI', sans-serif;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 0.3px;
            padding: 4px 0px;
            background-color: transparent;
        """)
        logo_layout.addWidget(clinic_name)
        
        sidebar_layout.addWidget(logo_container)
        
        # Separator line
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #E8F0F2; margin: 8px 20px;")
        sidebar_layout.addWidget(separator)
        
        # Navigation buttons — role-based filtering
        # Define all nav items: (icon, text, allowed_roles)
        all_nav_items = [
            ('fa5s.th-large',           'Dashboard',     ['Admin', 'Dentist', 'Staff']),
            ('fa5s.users',              'Patients',      ['Admin', 'Staff', 'Dentist']),
            ('fa5s.user-md',            'Dentists',      ['Admin']),
            ('fa5s.calendar-check',     'Appointments',  ['Admin', 'Dentist', 'Staff']),
            ('fa5s.tools',              'Services',      ['Admin', 'Staff']),
            ('fa5s.notes-medical',      'Treatments',    ['Admin', 'Dentist']),
            ('fa5s.file-invoice-dollar', 'Billing',      ['Admin', 'Staff']),
            ('fa5s.user-cog',           'Users',         ['Admin']),
        ]
        
        user_role = self.user_data.get('role', 'Staff')
        self.page_map = []  # Maps sidebar button index → stacked widget index
        self.button_icons = []  # Store icon names for dynamic color updates
        
        # All page indices (always created):
        # 0=Dashboard, 1=Patients, 2=Dentists, 3=Appointments,
        # 4=Services, 5=Treatments, 6=Billing, 7=Users
        page_index_map = {
            'Dashboard': 0, 'Patients': 1, 'Dentists': 2,
            'Appointments': 3, 'Services': 4, 'Treatments': 5,
            'Billing': 6, 'Users': 7
        }
        
        for icon_name, text, roles in all_nav_items:
            # Enforce role-based access control
            if user_role not in roles:
                continue  # Skip items not allowed for this role
            # Dentist cannot access Billing
            if user_role == 'Dentist' and text == 'Billing':
                continue
            # Dentist cannot access Users
            if user_role == 'Dentist' and text == 'Users':
                continue
            # Staff cannot access Treatments
            if user_role == 'Staff' and text == 'Treatments':
                continue
            btn = QPushButton(f"   {text}")
            btn.setObjectName("sidebar_btn")
            btn.setIcon(qta.icon(icon_name, color='#6B8A8F'))
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(48)
            sidebar_btn_idx = len(self.sidebar_buttons)
            btn.clicked.connect(lambda checked, i=sidebar_btn_idx: self.show_page(i))
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons.append(btn)
            self.button_icons.append(icon_name)
            self.page_map.append(page_index_map[text])
        
        # Spacer to push logout to bottom
        sidebar_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
        
        # User info bar at bottom of sidebar — avatar, name, role, three-dots menu
        user_bar = QWidget()
        user_bar.setObjectName("user_bar")
        user_bar.setStyleSheet("""
            QWidget#user_bar {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F0F8F9, stop:1 #E4F1F3);
                border-radius: 14px;
                border: 1px solid #D4E6E9;
                margin: 10px 14px;
            }
        """)
        user_bar_layout = QHBoxLayout(user_bar)
        user_bar_layout.setContentsMargins(12, 12, 12, 12)
        user_bar_layout.setSpacing(10)

        # User avatar circle
        avatar_label = QLabel()
        initials = f"{self.user_data.get('first_name', 'U')[0]}{self.user_data.get('last_name', '')[0] if self.user_data.get('last_name') else ''}"
        avatar_label.setText(initials.upper())
        avatar_label.setFixedSize(38, 38)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setStyleSheet("""
            QLabel {
                background-color: #1A6E7A;
                color: #FFFFFF;
                border-radius: 19px;
                font-family: 'Poppins', 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 700;
            }
        """)
        user_bar_layout.addWidget(avatar_label)

        # Name and Role stacked
        info_layout = QVBoxLayout()
        info_layout.setSpacing(1)
        user_name_label = QLabel(f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}")
        user_name_label.setStyleSheet("color: #1A6E7A; font-family: 'Poppins', 'Segoe UI', sans-serif; font-size: 12px; font-weight: 600; background-color: transparent;")
        info_layout.addWidget(user_name_label)

        role_text = self.user_data.get('role', 'N/A')
        if role_text == 'Admin':
            role_text = 'User'
        role_label = QLabel(role_text)
        role_label.setStyleSheet("color: #7FA8AE; font-family: 'Poppins', 'Segoe UI', sans-serif; font-size: 12px; font-weight: 600; background-color: transparent;")
        info_layout.addWidget(role_label)
        user_bar_layout.addLayout(info_layout)

        user_bar_layout.addStretch()

        # Three-dots menu button
        menu_btn = QPushButton()
        menu_btn.setIcon(qta.icon('fa5s.ellipsis-v', color='#1A6E7A'))
        menu_btn.setIconSize(QSize(14, 14))
        menu_btn.setFixedSize(30, 30)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.setToolTip("Options")
        menu_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.7);
                border: 1px solid #D4E6E9;
                border-radius: 8px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #FFFFFF;
                border-color: #1A6E7A;
            }
            QPushButton::menu-indicator { width: 0px; }
        """)

        # Popup menu with Change Password and Logout
        user_menu = QMenu(menu_btn)
        user_menu.setStyleSheet("""
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #D4E6E9;
                border-radius: 10px;
                padding: 8px 0px;
                font-family: 'Poppins', 'Segoe UI', sans-serif;
                font-size: 12px;
            }
            QMenu::item {
                padding: 10px 24px 10px 16px;
                color: #2C3E50;
                border-radius: 6px;
                margin: 2px 8px;
            }
            QMenu::item:hover {
                background-color: #E8F4F5;
                color: #1A6E7A;
            }
            QMenu::separator {
                height: 1px;
                background-color: #E8EDEF;
                margin: 4px 12px;
            }
        """)

        change_pwd_action = user_menu.addAction(qta.icon('fa5s.key', color='#1A6E7A'), "  Change Password")
        change_pwd_action.triggered.connect(self.open_change_password)
        user_menu.addSeparator()
        logout_action = user_menu.addAction(qta.icon('fa5s.sign-out-alt', color='#D32F2F'), "  Logout")
        logout_action.triggered.connect(self.handle_logout)

        menu_btn.setMenu(user_menu)
        user_bar_layout.addWidget(menu_btn)

        sidebar_layout.addWidget(user_bar)
        
        # Add spacing at bottom
        bottom_spacer = QWidget()
        bottom_spacer.setFixedHeight(16)
        bottom_spacer.setStyleSheet("background-color: transparent;")
        sidebar_layout.addWidget(bottom_spacer)
        
        main_layout.addWidget(sidebar)
        
        # ---- RIGHT SIDE (Top Bar + Content) ----
        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # ---- TOP BAR ----
        topbar = QWidget()
        topbar.setObjectName("topbar")
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(20, 0, 20, 0)
        
        self.topbar_title = QLabel("Dashboard")
        self.topbar_title.setObjectName("topbar_title")
        topbar_layout.addWidget(self.topbar_title)
        
        topbar_layout.addStretch()
        
        # Current user display
        user_display = QLabel(f"{self.user_data.get('first_name', '')}  |  {self.user_data.get('role', '')}")
        user_display.setObjectName("topbar_user")
        topbar_layout.addWidget(user_display)
        
        right_layout.addWidget(topbar)
        
        # ---- CONTENT AREA (Stacked Widget) ----
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")
        
        # Create all page views
        self.dashboard_view = DashboardView()
        self.patient_view = PatientView()
        self.dentist_view = DentistView()
        self.appointment_view = AppointmentView()
        self.service_view = ServiceView()
        self.treatment_view = TreatmentView()
        self.billing_view = BillingView()
        self.user_view = UserView()
        
        # Add views to stacked widget
        self.content_stack.addWidget(self.dashboard_view)     # Index 0
        self.content_stack.addWidget(self.patient_view)       # Index 1
        self.content_stack.addWidget(self.dentist_view)       # Index 2
        self.content_stack.addWidget(self.appointment_view)   # Index 3
        self.content_stack.addWidget(self.service_view)       # Index 4
        self.content_stack.addWidget(self.treatment_view)     # Index 5
        self.content_stack.addWidget(self.billing_view)       # Index 6
        self.content_stack.addWidget(self.user_view)          # Index 7
        
        right_layout.addWidget(self.content_stack)
        main_layout.addWidget(right_side)
        
        # ---- Create Controllers ----
        self.dashboard_controller = DashboardController(self.dashboard_view, self.user_data)
        self.patient_controller = PatientController(self.patient_view)
        self.dentist_controller = DentistController(self.dentist_view)
        self.appointment_controller = AppointmentController(self.appointment_view, self.user_data)
        self.service_controller = ServiceController(self.service_view)
        self.treatment_controller = TreatmentController(self.treatment_view, self.user_data)
        self.billing_controller = BillingController(self.billing_view, self.user_data)
        self.user_controller = UserController(self.user_view)
    
    def show_page(self, sidebar_index):
        """Switch to a specific page and update sidebar/topbar."""
        page_titles = [
            'Dashboard', 'Patients', 'Dentists', 'Appointments',
            'Services', 'Treatments', 'Billing', 'Users'
        ]
        
        # Map sidebar button index to actual stacked widget index
        stack_index = self.page_map[sidebar_index]
        
        self.content_stack.setCurrentIndex(stack_index)
        self.topbar_title.setText(page_titles[stack_index])
        
        # Update sidebar button states and icon colors
        for i, btn in enumerate(self.sidebar_buttons):
            if i == sidebar_index:
                btn.setChecked(True)
                # Active icon color - teal
                btn.setIcon(qta.icon(self.button_icons[i], color='#1A6E7A'))
            else:
                btn.setChecked(False)
                # Inactive icon color - gray
                btn.setIcon(qta.icon(self.button_icons[i], color='#6B8A8F'))
        
        # Refresh data when switching pages
        self._refresh_page(stack_index)
    
    def _refresh_page(self, index):
        """Refresh data on the current page."""
        try:
            if index == 0:
                self.dashboard_controller.load_dashboard()
            elif index == 1:
                self.patient_controller.load_patients()
            elif index == 2:
                self.dentist_controller.load_dentists()
            elif index == 3:
                self.appointment_controller.load_appointments()
            elif index == 4:
                self.service_controller.load_services()
            elif index == 5:
                self.treatment_controller.load_treatments()
            elif index == 6:
                self.billing_controller.load_billings()
            elif index == 7:
                self.user_controller.load_users()
        except Exception as e:
            print(f"[Error] Failed to refresh page {index}: {e}")
    
    def open_change_password(self):
        """Open the Change Password dialog via the user controller."""
        self.user_controller.change_password(self, self.user_data)
    
    def handle_logout(self):
        """Show logout confirmation and log out if confirmed. Do not trigger app close logic."""
        reply = QMessageBox.question(
            self, "Confirm Logout",
            "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit()

    def closeEvent(self, event: QCloseEvent):
        """Confirm before closing the application. Only triggers on window close, not logout."""
        reply = QMessageBox.question(
            self, "Confirm Exit",
            "Are you sure you want to close the application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
