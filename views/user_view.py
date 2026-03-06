# =============================================================================
# Happy Tooth Dental Clinic and Services
# User View — User/Staff/Account management for Admin
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QComboBox, QMessageBox, QCheckBox, QMenu
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
import qtawesome as qta


class UserView(QWidget):
    """User management page — Admin can manage all accounts."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Build the user management layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        # ---- Header Row: Title + Add Button ----
        header_layout = QHBoxLayout()
        
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.user-cog', color='#1A6E7A').pixmap(24, 24))
        title_icon.setStyleSheet("background: transparent;")
        header_layout.addWidget(title_icon)
        
        title = QLabel("User & Staff Management")
        title.setObjectName("section_title")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Search users...")
        self.search_input.setMaximumWidth(320)
        self.search_input.setMinimumHeight(44)
        header_layout.addWidget(self.search_input)
        
        # Add User Button
        self.add_btn = QPushButton("  Add User")
        self.add_btn.setObjectName("success_btn")
        self.add_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        # ---- User Table ----
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Username", "First Name", "Last Name",
            "Role", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 80)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
    
    def load_table(self, users):
        """Populate the table with user data."""
        self.table.setRowCount(0)
        for row_num, user in enumerate(users):
            self.table.insertRow(row_num)
            
            uname_item = QTableWidgetItem(user['username'])
            uname_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 0, uname_item)
            
            fname_item = QTableWidgetItem(user['first_name'])
            fname_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 1, fname_item)
            
            lname_item = QTableWidgetItem(user['last_name'])
            lname_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 2, lname_item)
            
            # Role with color
            role_item = QTableWidgetItem(user['role'])
            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if user['role'] == 'Admin':
                role_item.setForeground(Qt.GlobalColor.darkRed)
            elif user['role'] == 'Dentist':
                role_item.setForeground(Qt.GlobalColor.darkBlue)
            else:
                role_item.setForeground(Qt.GlobalColor.darkGreen)
            self.table.setItem(row_num, 3, role_item)
            
            # Status
            is_active = user.get('is_active', 1)
            status_text = "Active" if is_active else "Inactive"
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(Qt.GlobalColor.darkGreen if is_active else Qt.GlobalColor.red)
            self.table.setItem(row_num, 4, status_item)
            
            # Action dropdown button
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            action_btn = QPushButton()
            action_btn.setIcon(qta.icon('fa5s.ellipsis-h', color='#1A6E7A'))
            action_btn.setIconSize(QSize(16, 16))
            action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            action_btn.setFixedSize(36, 32)
            action_btn.setStyleSheet("""
                QPushButton { background: #FFFFFF; border: 1px solid #D4E6E9; border-radius: 6px; padding: 0px; text-align: center; }
                QPushButton:hover { background: #E8F4F5; border-color: #1A6E7A; }
                QPushButton::menu-indicator { image: none; width: 0px; }
            """)
            
            menu = QMenu(action_btn)
            menu.setStyleSheet("""
                QMenu { background: white; border: 1px solid #D4E6E9; border-radius: 8px; padding: 4px; }
                QMenu::item { padding: 8px 20px; border-radius: 4px; }
                QMenu::item:selected { background: #E8F4F5; color: #1A6E7A; }
            """)
            
            edit_action = QAction("Edit", menu)
            edit_action.triggered.connect(lambda _, uid=user['id']: self._edit_clicked(uid))
            menu.addAction(edit_action)
            
            toggle_text = "Deactivate" if is_active else "Activate"
            toggle_action = QAction(toggle_text, menu)
            toggle_action.triggered.connect(lambda _, uid=user['id']: self._toggle_clicked(uid))
            menu.addAction(toggle_action)
            
            reset_action = QAction("Reset Password", menu)
            reset_action.triggered.connect(lambda _, uid=user['id']: self._reset_clicked(uid))
            menu.addAction(reset_action)
            
            delete_action = QAction("Delete", menu)
            delete_action.triggered.connect(lambda _, uid=user['id']: self._delete_clicked(uid))
            menu.addAction(delete_action)
            
            action_btn.setMenu(menu)
            action_layout.addWidget(action_btn)
            
            self.table.setCellWidget(row_num, 5, action_widget)
            self.table.setRowHeight(row_num, 60)
    
    def _edit_clicked(self, user_id):
        if hasattr(self, '_edit_callback'):
            self._edit_callback(user_id)
    
    def _toggle_clicked(self, user_id):
        if hasattr(self, '_toggle_callback'):
            self._toggle_callback(user_id)
    
    def _reset_clicked(self, user_id):
        if hasattr(self, '_reset_callback'):
            self._reset_callback(user_id)
    
    def _delete_clicked(self, user_id):
        if hasattr(self, '_delete_callback'):
            self._delete_callback(user_id)

    # ---- Message helpers (keep PyQt6 UI logic in the view) ----
    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_confirm(self, title, message):
        reply = QMessageBox.question(
            self, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class UserDialog(QDialog):
    """Dialog for adding or editing a user account."""
    
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        if user_data:
            self.setWindowTitle("Edit User")
        else:
            self.setWindowTitle("Add New User")
        self.setMinimumWidth(480)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        self.init_ui()
    
    def init_ui(self):
        """Build the dialog form."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Title
        if self.user_data:
            title_text = "Edit User"
        else:
            title_text = "Add New User"
        title = QLabel(title_text)
        title.setObjectName("section_title")
        layout.addWidget(title)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")
        self.first_name_input.setMinimumHeight(38)
        form.addRow(self._label("First Name *"), self.first_name_input)
        
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")
        self.last_name_input.setMinimumHeight(38)
        form.addRow(self._label("Last Name *"), self.last_name_input)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMinimumHeight(38)
        form.addRow(self._label("Username *"), self.username_input)
        
        # Password (required for new, optional for edit)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(38)
        if self.user_data:
            self.password_input.setPlaceholderText("Leave blank to keep current password")
            form.addRow(self._label("New Password"), self.password_input)
        else:
            self.password_input.setPlaceholderText("Enter password")
            form.addRow(self._label("Password *"), self.password_input)
        
        # Role dropdown
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Staff", "Admin", "Dentist"])
        self.role_combo.setMinimumHeight(38)
        form.addRow(self._label("Role *"), self.role_combo)
        
        layout.addLayout(form)
        
        # Pre-fill if editing
        if self.user_data:
            self.first_name_input.setText(self.user_data.get('first_name', ''))
            self.last_name_input.setText(self.user_data.get('last_name', ''))
            self.username_input.setText(self.user_data.get('username', ''))
            role = self.user_data.get('role', 'Staff')
            idx = self.role_combo.findText(role)
            if idx >= 0:
                self.role_combo.setCurrentIndex(idx)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("  Cancel")
        cancel_btn.setObjectName("outline_btn")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("  Save User")
        save_btn.setObjectName("success_btn")
        save_btn.setIcon(qta.icon('fa5s.check', color='white'))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.validate_and_accept)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def _label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("form_label")
        return lbl
    
    def validate_and_accept(self):
        """Validate inputs before accepting."""
        if not self.first_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "First name is required.")
            return
        if not self.last_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Last name is required.")
            return
        if not self.username_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Username is required.")
            return
        # Password required for new users only
        if not self.user_data and not self.password_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Password is required for new users.")
            return
        if self.password_input.text().strip() and len(self.password_input.text().strip()) < 6:
            QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters.")
            return
        self.accept()
    
    def get_data(self):
        """Return all form data as a dict."""
        data = {
            'first_name': self.first_name_input.text().strip(),
            'last_name': self.last_name_input.text().strip(),
            'username': self.username_input.text().strip(),
            'role': self.role_combo.currentText()
        }
        pwd = self.password_input.text().strip()
        if pwd:
            data['password'] = pwd
        return data


class ResetPasswordDialog(QDialog):
    """Simple dialog for resetting a user's password."""
    
    def __init__(self, parent=None, username=""):
        super().__init__(parent)
        self.setWindowTitle(f"Reset Password — {username}")
        self.setMinimumWidth(400)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)
        
        title = QLabel("Reset Password")
        title.setObjectName("section_title")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(10)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setPlaceholderText("Enter new password")
        self.new_password.setMinimumHeight(38)
        form.addRow(self._label("New Password *"), self.new_password)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setPlaceholderText("Confirm new password")
        self.confirm_password.setMinimumHeight(38)
        form.addRow(self._label("Confirm Password *"), self.confirm_password)
        
        layout.addLayout(form)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("  Cancel")
        cancel_btn.setObjectName("outline_btn")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("  Reset Password")
        save_btn.setObjectName("success_btn")
        save_btn.setIcon(qta.icon('fa5s.key', color='white'))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.validate_and_accept)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def _label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("form_label")
        return lbl
    
    def validate_and_accept(self):
        pwd = self.new_password.text().strip()
        confirm = self.confirm_password.text().strip()
        if not pwd:
            QMessageBox.warning(self, "Error", "Password is required.")
            return
        if len(pwd) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters.")
            return
        if pwd != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        self.accept()
    
    def get_password(self):
        return self.new_password.text().strip()
