# =============================================================================
# Happy Tooth Dental Clinic and Services
# Login View — Login screen with logo and authentication form
# =============================================================================

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QIcon, QAction
import qtawesome as qta


class LoginView(QWidget):
    """Login screen for the application."""
    
    # Signal emitted when login is successful — sends user dict
    login_success = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("login_bg")
        self.init_ui()
    
    def init_ui(self):
        """Build the login screen layout."""
        # Main layout — centers the login card
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Center container
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # ---- Login Card ----
        self.login_card = QFrame()
        self.login_card.setObjectName("login_card")
        self.login_card.setFixedWidth(440)
        card_layout = QVBoxLayout(self.login_card)
        card_layout.setSpacing(18)
        card_layout.setContentsMargins(48, 40, 48, 40)
        
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled)
        else:
            # Fallback — show icon if logo not found
            logo_label.setPixmap(qta.icon('fa5s.tooth', color='#1A6E7A').pixmap(80, 80))
        logo_label.setStyleSheet("background-color: transparent;")
        card_layout.addWidget(logo_label)
        
        # Title
        title = QLabel("Happy Tooth")
        title.setObjectName("login_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Dental Clinic and Services")
        subtitle.setObjectName("login_subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)
        
        # Spacer
        card_layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Username field
        username_label = QLabel("Username")
        username_label.setObjectName("form_label")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g. Admin123")
        self.username_input.setMinimumHeight(48)
        card_layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setObjectName("form_label")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("e.g. admin123")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(48)
        
        # Toggle password visibility (eye icon)
        self._password_visible = False
        self._eye_action = QAction(self.password_input)
        self._eye_action.setIcon(qta.icon('fa5s.eye-slash', color='#999999'))
        self._eye_action.triggered.connect(self._toggle_password_visibility)
        self.password_input.addAction(self._eye_action, QLineEdit.ActionPosition.TrailingPosition)
        
        card_layout.addWidget(self.password_input)
        
        # Spacer
        card_layout.addSpacerItem(QSpacerItem(20, 16, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Login Button
        self.login_btn = QPushButton("  Sign In")
        self.login_btn.setObjectName("login_btn")
        self.login_btn.setIcon(qta.icon('fa5s.sign-in-alt', color='white'))
        self.login_btn.setMinimumHeight(52)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        card_layout.addWidget(self.login_btn)
        
        # Error label (hidden by default)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("""
            color: #C62828; 
            font-size: 13px; 
            font-weight: 500;
            padding: 12px 16px;
            background-color: #FFEBEE;
            border-radius: 10px;
            border: 1px solid #FFCDD2;
        """)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)
        
        center_layout.addWidget(self.login_card)
        main_layout.addWidget(center_widget)
        
        # ---- Connect Enter key ----
        self.password_input.returnPressed.connect(self.login_btn.click)
        self.username_input.returnPressed.connect(self.password_input.setFocus)
    
    def get_credentials(self):
        """Return entered username and password."""
        return self.username_input.text().strip(), self.password_input.text().strip()
    
    def show_error(self, message):
        """Display error message on the login card."""
        self.error_label.setText(message)
        self.error_label.show()
    
    def _toggle_password_visibility(self):
        """Toggle password field between visible and hidden."""
        self._password_visible = not self._password_visible
        if self._password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self._eye_action.setIcon(qta.icon('fa5s.eye', color='#1A6E7A'))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self._eye_action.setIcon(qta.icon('fa5s.eye-slash', color='#999999'))
    
    def clear_fields(self):
        """Clear all input fields and error message."""
        self.username_input.clear()
        self.password_input.clear()
        self.error_label.hide()
        self._password_visible = False
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._eye_action.setIcon(qta.icon('fa5s.eye-slash', color='#999999'))
        self.username_input.setFocus()
