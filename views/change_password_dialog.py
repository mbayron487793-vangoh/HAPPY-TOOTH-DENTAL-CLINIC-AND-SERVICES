# =============================================================================
# Happy Tooth Dental Clinic and Services
# Change Password Dialog — Allows any user to change their own password
# =============================================================================

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
import qtawesome as qta


class ChangePasswordDialog(QDialog):
    """Dialog for changing the logged-in user's password."""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data or {}
        self.setWindowTitle("Change Password")
        self.setMinimumWidth(440)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; border-radius: 16px; }")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(36, 32, 36, 32)
        
        title = QLabel("Change Password")
        title.setObjectName("section_title")
        layout.addWidget(title)
        
        # Info label
        info = QLabel(f"Changing password for: {self.user_data.get('username', 'N/A')}")
        info.setStyleSheet("color: #6B8A8F; font-size: 13px; font-weight: 500; padding: 6px 0;")
        layout.addWidget(info)
        
        form = QFormLayout()
        form.setSpacing(14)
        
        self.current_password = QLineEdit()
        self.current_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password.setPlaceholderText("Enter current password")
        self.current_password.setMinimumHeight(44)
        form.addRow(self._label("Current Password *"), self.current_password)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setPlaceholderText("Enter new password (min 6 chars)")
        self.new_password.setMinimumHeight(44)
        form.addRow(self._label("New Password *"), self.new_password)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setPlaceholderText("Re-enter new password")
        self.confirm_password.setMinimumHeight(44)
        form.addRow(self._label("Confirm Password *"), self.confirm_password)
        
        layout.addLayout(form)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("  Cancel")
        cancel_btn.setObjectName("outline_btn")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#1A6E7A'))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("  Change Password")
        save_btn.setObjectName("success_btn")
        save_btn.setIcon(qta.icon('fa5s.key', color='white'))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.validate_and_save)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def _label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("form_label")
        return lbl
    
    def validate_and_save(self):
        """Validate password fields and accept dialog if valid."""
        current = self.current_password.text().strip()
        new_pwd = self.new_password.text().strip()
        confirm = self.confirm_password.text().strip()
        
        if not current:
            QMessageBox.warning(self, "Error", "Current password is required.")
            return
        if not new_pwd:
            QMessageBox.warning(self, "Error", "New password is required.")
            return
        if len(new_pwd) < 6:
            QMessageBox.warning(self, "Error", "New password must be at least 6 characters.")
            return
        if new_pwd != confirm:
            QMessageBox.warning(self, "Error", "New passwords do not match.")
            return
        if current == new_pwd:
            QMessageBox.warning(self, "Error", "New password must be different from current password.")
            return
        
        self.accept()
    
    def get_data(self):
        """Return the password data entered by the user."""
        return {
            'current_password': self.current_password.text().strip(),
            'new_password': self.new_password.text().strip()
        }
