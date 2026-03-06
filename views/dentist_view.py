# =============================================================================
# Happy Tooth Dental Clinic and Services
# Dentist View — Dentist management CRUD interface
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QComboBox, QTextEdit, QMessageBox,
    QCheckBox, QGroupBox, QMenu
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
import qtawesome as qta


class DentistView(QWidget):
    """Dentist management page."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.user-md', color='#1A6E7A').pixmap(24, 24))
        title_icon.setStyleSheet("background: transparent;")
        header_layout.addWidget(title_icon)
        
        title = QLabel("Dentist Management")
        title.setObjectName("section_title")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Search dentists...")
        self.search_input.setMaximumWidth(320)
        self.search_input.setMinimumHeight(44)
        header_layout.addWidget(self.search_input)
        
        self.add_btn = QPushButton("  Add Dentist")
        self.add_btn.setObjectName("primary_btn")
        self.add_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "First Name", "Last Name", "Specialization",
            "Contact", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 80)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
    
    def load_table(self, dentists):
        self.table.setRowCount(0)
        for row_num, dentist in enumerate(dentists):
            self.table.insertRow(row_num)
            
            fname_item = QTableWidgetItem(dentist['first_name'])
            fname_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 0, fname_item)
            
            lname_item = QTableWidgetItem(dentist['last_name'])
            lname_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 1, lname_item)
            
            spec_item = QTableWidgetItem(dentist.get('specialization', ''))
            spec_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 2, spec_item)
            
            contact_item = QTableWidgetItem(dentist.get('contact_number', '') or '')
            contact_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 3, contact_item)
            
            status = "Active" if dentist.get('is_active', 1) else "Inactive"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(Qt.GlobalColor.darkGreen if status == "Active" else Qt.GlobalColor.red)
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
            edit_action.triggered.connect(lambda _, did=dentist['id']: self._edit_callback(did) if hasattr(self, '_edit_callback') else None)
            menu.addAction(edit_action)
            
            delete_action = QAction("Delete", menu)
            delete_action.triggered.connect(lambda _, did=dentist['id']: self._delete_callback(did) if hasattr(self, '_delete_callback') else None)
            menu.addAction(delete_action)
            
            action_btn.setMenu(menu)
            action_layout.addWidget(action_btn)
            
            self.table.setCellWidget(row_num, 5, action_widget)
            self.table.setRowHeight(row_num, 60)

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


class DentistDialog(QDialog):
    """Dialog for adding/editing a dentist."""
    
    def __init__(self, parent=None, dentist_data=None):
        super().__init__(parent)
        self.dentist_data = dentist_data
        self.setWindowTitle("Edit Dentist" if dentist_data else "Add New Dentist")
        self.setMinimumWidth(480)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)
        
        title = QLabel("Edit Dentist" if self.dentist_data else "Add New Dentist")
        title.setObjectName("section_title")
        layout.addWidget(title)
        
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
        
        self.specialization_combo = QComboBox()
        self.specialization_combo.setEditable(True)
        self.specialization_combo.addItems([
            "General Dentistry", "Orthodontics", "Pediatric Dentistry",
            "Oral Surgery", "Endodontics", "Periodontics",
            "Prosthodontics", "Cosmetic Dentistry"
        ])
        self.specialization_combo.setMinimumHeight(38)
        form.addRow(self._label("Specialization"), self.specialization_combo)
        
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("e.g. 09123456789")
        self.contact_input.setMinimumHeight(38)
        form.addRow(self._label("Contact Number"), self.contact_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g. doctor@email.com")
        self.email_input.setMinimumHeight(38)
        form.addRow(self._label("Email"), self.email_input)
        
        layout.addLayout(form)
        
        # ── Login Account Section ────────────────────────────────
        self.account_group = QGroupBox()
        self.account_group.setStyleSheet(
            "QGroupBox { border: 1px solid #D4E6E9; border-radius: 8px; "
            "padding: 15px; margin-top: 8px; background: #F8FDFD; }"
        )
        account_layout = QVBoxLayout(self.account_group)
        account_layout.setSpacing(10)
        
        self.create_account_check = QCheckBox("  Create a login account for this dentist")
        self.create_account_check.setStyleSheet(
            "QCheckBox { font-size: 13px; font-weight: 600; color: #2AACB8; }"
        )
        self.create_account_check.toggled.connect(self._toggle_account_fields)
        account_layout.addWidget(self.create_account_check)
        
        self.account_fields_widget = QWidget()
        acc_form = QFormLayout(self.account_fields_widget)
        acc_form.setSpacing(8)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Login username (e.g. dr.santos)")
        self.username_input.setMinimumHeight(38)
        acc_form.addRow(self._label("Username *"), self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Login password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(38)
        acc_form.addRow(self._label("Password *"), self.password_input)
        
        account_layout.addWidget(self.account_fields_widget)
        self.account_fields_widget.setVisible(False)
        
        layout.addWidget(self.account_group)
        
        # Pre-fill for edit mode
        if self.dentist_data:
            self.first_name_input.setText(self.dentist_data.get('first_name', ''))
            self.last_name_input.setText(self.dentist_data.get('last_name', ''))
            spec = self.dentist_data.get('specialization', '')
            idx = self.specialization_combo.findText(spec)
            if idx >= 0:
                self.specialization_combo.setCurrentIndex(idx)
            else:
                self.specialization_combo.setEditText(spec)
            self.contact_input.setText(self.dentist_data.get('contact_number', '') or '')
            self.email_input.setText(self.dentist_data.get('email', '') or '')
            # If dentist already has a linked user account, show it
            if self.dentist_data.get('user_id'):
                self.create_account_check.setText("  ✅ Has linked login account")
                self.create_account_check.setEnabled(False)
                self.account_group.setStyleSheet(
                    "QGroupBox { border: 1px solid #C8E6C9; border-radius: 8px; "
                    "padding: 15px; margin-top: 8px; background: #F1F8E9; }"
                )
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("  Cancel")
        cancel_btn.setObjectName("outline_btn")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("  Save Dentist")
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
    
    def _toggle_account_fields(self, checked):
        """Show/hide the username + password fields."""
        self.account_fields_widget.setVisible(checked)
        # Auto-generate username suggestion from name
        if checked and not self.username_input.text().strip():
            fn = self.first_name_input.text().strip().lower()
            ln = self.last_name_input.text().strip().lower()
            if fn and ln:
                self.username_input.setText(f"{fn}.{ln}")
    
    def validate_and_accept(self):
        if not self.first_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "First name is required.")
            return
        if not self.last_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Last name is required.")
            return
        
        # Validate contact number (Philippine format)
        contact = self.contact_input.text().strip()
        if contact:
            if not contact.isdigit():
                QMessageBox.warning(self, "Validation Error", "Contact number must contain only digits.")
                return
            if not contact.startswith('09'):
                QMessageBox.warning(self, "Validation Error", "Contact number must start with 09 (e.g. 09123456789).")
                return
            if len(contact) != 11:
                QMessageBox.warning(self, "Validation Error", "Contact number must be exactly 11 digits (e.g. 09123456789).")
                return
        
        # Validate email format
        email = self.email_input.text().strip()
        if email:
            import re
            pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                QMessageBox.warning(self, "Validation Error", "Please enter a valid email address (e.g. doctor@email.com).")
                return
        
        # Validate account fields if checkbox is checked
        if self.create_account_check.isChecked() and self.create_account_check.isEnabled():
            if not self.username_input.text().strip():
                QMessageBox.warning(self, "Validation Error", "Username is required for login account.")
                return
            if not self.password_input.text().strip():
                QMessageBox.warning(self, "Validation Error", "Password is required for login account.")
                return
            if len(self.password_input.text().strip()) < 6:
                QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters.")
                return
        self.accept()
    
    def get_data(self):
        data = {
            'first_name': self.first_name_input.text().strip(),
            'last_name': self.last_name_input.text().strip(),
            'specialization': self.specialization_combo.currentText().strip(),
            'contact_number': self.contact_input.text().strip(),
            'email': self.email_input.text().strip(),
            'create_account': self.create_account_check.isChecked() and self.create_account_check.isEnabled(),
            'username': self.username_input.text().strip(),
            'password': self.password_input.text().strip()
        }
        return data
