# =============================================================================
# Happy Tooth Dental Clinic and Services
# Patient View — Patient management CRUD interface
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QComboBox, QDateEdit, QTextEdit,
    QMessageBox, QFrame, QSpacerItem, QSizePolicy, QScrollArea, QMenu
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QSize
from PyQt6.QtGui import QAction
import qtawesome as qta


class PatientView(QWidget):
    """Patient management page with table and CRUD operations."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Build the patient management layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        # ---- Header Row: Title + Add Button ----
        header_layout = QHBoxLayout()
        
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.users', color='#1A6E7A').pixmap(24, 24))
        title_icon.setStyleSheet("background: transparent;")
        header_layout.addWidget(title_icon)
        
        title = QLabel("Patient Management")
        title.setObjectName("section_title")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Search patients...")
        self.search_input.setMaximumWidth(320)
        self.search_input.setMinimumHeight(44)
        header_layout.addWidget(self.search_input)
        
        # Add Patient Button
        self.add_btn = QPushButton("  Add Patient")
        self.add_btn.setObjectName("primary_btn")
        self.add_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        # ---- Patient Table ----
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "First Name", "Last Name", "Sex",
            "Birthdate", "Age", "Contact", "Email", "Address", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(8, 80)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
    
    def load_table(self, patients):
        """Populate the table with patient data."""
        from datetime import date
        self.table.setRowCount(0)
        for row_num, patient in enumerate(patients):
            self.table.insertRow(row_num)
            
            fname_item = QTableWidgetItem(patient['first_name'])
            fname_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 0, fname_item)
            
            lname_item = QTableWidgetItem(patient['last_name'])
            lname_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 1, lname_item)
            
            gender_item = QTableWidgetItem(patient.get('gender', ''))
            gender_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 2, gender_item)
            
            bdate_item = QTableWidgetItem(str(patient.get('birthdate', '')))
            bdate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 3, bdate_item)
            
            # Calculate age from birthdate
            age_str = ''
            bd = patient.get('birthdate')
            if bd:
                try:
                    from datetime import datetime
                    if isinstance(bd, str):
                        bd = datetime.strptime(bd, "%Y-%m-%d").date()
                    today = date.today()
                    age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
                    age_str = str(age)
                except Exception:
                    age_str = ''
            age_item = QTableWidgetItem(age_str)
            age_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 4, age_item)
            
            contact_item = QTableWidgetItem(patient.get('contact_number', '') or '')
            contact_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 5, contact_item)
            
            email_item = QTableWidgetItem(patient.get('email', '') or '')
            email_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 6, email_item)
            
            addr_item = QTableWidgetItem(patient.get('address', '') or '')
            addr_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 7, addr_item)
            
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
            edit_action.triggered.connect(lambda _, pid=patient['id']: self._edit_clicked(pid))
            menu.addAction(edit_action)
            
            history_action = QAction("View History", menu)
            history_action.triggered.connect(lambda _, pid=patient['id']: self._history_clicked(pid))
            menu.addAction(history_action)
            
            delete_action = QAction("Delete", menu)
            delete_action.triggered.connect(lambda _, pid=patient['id']: self._delete_clicked(pid))
            menu.addAction(delete_action)
            
            action_btn.setMenu(menu)
            action_layout.addWidget(action_btn)
            
            self.table.setCellWidget(row_num, 8, action_widget)
            self.table.setRowHeight(row_num, 60)
    
    def _edit_clicked(self, patient_id):
        """Store patient_id and trigger edit signal (handled by controller)."""
        self._current_edit_id = patient_id
        if hasattr(self, '_edit_callback'):
            self._edit_callback(patient_id)
    
    def _history_clicked(self, patient_id):
        """Trigger history view (handled by controller)."""
        if hasattr(self, '_history_callback'):
            self._history_callback(patient_id)
    
    def _delete_clicked(self, patient_id):
        """Trigger delete signal (handled by controller)."""
        if hasattr(self, '_delete_callback'):
            self._delete_callback(patient_id)

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


class PatientDialog(QDialog):
    """Dialog for adding or editing a patient."""
    
    def __init__(self, parent=None, patient_data=None):
        super().__init__(parent)
        self.patient_data = patient_data
        self.setWindowTitle("Edit Patient" if patient_data else "Add New Patient")
        self.setMinimumWidth(550)
        self.setMinimumHeight(620)
        self.setStyleSheet("""
            QDialog { background-color: #FFFFFF; }
            QDialog QLineEdit {
                border: 2px solid #E0EDF0;
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 14px;
                background-color: #FFFFFF;
                color: #1E3A3D;
            }
            QDialog QLineEdit:focus {
                border: 2px solid #1A6E7A;
            }
            QDialog QLineEdit:hover {
                border: 2px solid #A8CDD2;
            }
            QDialog QComboBox {
                border: 2px solid #E0EDF0;
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 14px;
                background-color: #FFFFFF;
                color: #1E3A3D;
            }
            QDialog QComboBox:focus {
                border: 2px solid #1A6E7A;
            }
            QDialog QComboBox:hover {
                border: 2px solid #A8CDD2;
            }
            QDialog QDateEdit {
                border: 2px solid #E0EDF0;
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 14px;
                background-color: #FFFFFF;
                color: #1E3A3D;
            }
            QDialog QDateEdit:focus {
                border: 2px solid #1A6E7A;
            }
            QDialog QDateEdit:hover {
                border: 2px solid #A8CDD2;
            }
            QDialog QTextEdit {
                border: 2px solid #E0EDF0;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                background-color: #FFFFFF;
                color: #1E3A3D;
            }
            QDialog QTextEdit:focus {
                border: 2px solid #1A6E7A;
            }
            QDialog QTextEdit:hover {
                border: 2px solid #A8CDD2;
            }
        """)
        self.init_ui()
    
    def init_ui(self):
        """Build the dialog form."""
        from PyQt6.QtWidgets import QGridLayout
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Title
        title = QLabel("Edit Patient" if self.patient_data else "Add New Patient")
        title.setObjectName("section_title")
        layout.addWidget(title)
        
        # Form using QGridLayout for uniform field widths
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnMinimumWidth(0, 120)
        grid.setColumnStretch(1, 1)
        
        row = 0
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")
        self.first_name_input.setMinimumHeight(40)
        grid.addWidget(self._label("First Name *"), row, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(self.first_name_input, row, 1)
        
        row += 1
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")
        self.last_name_input.setMinimumHeight(40)
        grid.addWidget(self._label("Last Name *"), row, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(self.last_name_input, row, 1)
        
        row += 1
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.gender_combo.setMinimumHeight(40)
        self.gender_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        grid.addWidget(self._label("Sex *"), row, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(self.gender_combo, row, 1)
        
        row += 1
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setDate(QDate.currentDate().addYears(-25))
        self.birthdate_input.setMaximumDate(QDate.currentDate())
        self.birthdate_input.setDisplayFormat("yyyy-MM-dd")
        self.birthdate_input.setMinimumHeight(40)
        self.birthdate_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        grid.addWidget(self._label("Birthdate *"), row, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(self.birthdate_input, row, 1)
        
        row += 1
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("e.g. 09123456789")
        self.contact_input.setMinimumHeight(40)
        grid.addWidget(self._label("Contact Number"), row, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(self.contact_input, row, 1)
        
        row += 1
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g. patient@email.com")
        self.email_input.setMinimumHeight(40)
        grid.addWidget(self._label("Email"), row, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(self.email_input, row, 1)
        
        row += 1
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Enter address")
        self.address_input.setMinimumHeight(70)
        self.address_input.setMaximumHeight(80)
        grid.addWidget(self._label("Address"), row, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.address_input, row, 1)
        
        row += 1
        self.medical_input = QTextEdit()
        self.medical_input.setPlaceholderText("Any allergies, medical conditions, etc.")
        self.medical_input.setMinimumHeight(70)
        self.medical_input.setMaximumHeight(80)
        grid.addWidget(self._label("Medical History"), row, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.medical_input, row, 1)
        
        layout.addLayout(grid)
        
        # Pre-fill if editing
        if self.patient_data:
            self.first_name_input.setText(self.patient_data.get('first_name', ''))
            self.last_name_input.setText(self.patient_data.get('last_name', ''))
            gender = self.patient_data.get('gender', 'Male')
            idx = self.gender_combo.findText(gender)
            if idx >= 0:
                self.gender_combo.setCurrentIndex(idx)
            bd = self.patient_data.get('birthdate')
            if bd:
                self.birthdate_input.setDate(QDate.fromString(str(bd), "yyyy-MM-dd"))
            self.contact_input.setText(self.patient_data.get('contact_number', '') or '')
            self.email_input.setText(self.patient_data.get('email', '') or '')
            self.address_input.setPlainText(self.patient_data.get('address', '') or '')
            self.medical_input.setPlainText(self.patient_data.get('medical_history', '') or '')
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("  Cancel")
        cancel_btn.setObjectName("outline_btn")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("  Save Patient")
        save_btn.setObjectName("success_btn")
        save_btn.setIcon(qta.icon('fa5s.check', color='white'))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.validate_and_accept)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def _label(self, text):
        """Create a styled form label."""
        lbl = QLabel(text)
        lbl.setObjectName("form_label")
        lbl.setFixedWidth(120)
        return lbl
    
    def validate_and_accept(self):
        """Validate inputs before accepting."""
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
                QMessageBox.warning(self, "Validation Error", "Please enter a valid email address (e.g. patient@email.com).")
                return
        
        self.accept()
    
    def get_data(self):
        """Return all form data as a dict."""
        return {
            'first_name': self.first_name_input.text().strip(),
            'last_name': self.last_name_input.text().strip(),
            'gender': self.gender_combo.currentText(),
            'birthdate': self.birthdate_input.date().toString("yyyy-MM-dd"),
            'contact_number': self.contact_input.text().strip(),
            'email': self.email_input.text().strip(),
            'address': self.address_input.toPlainText().strip(),
            'medical_history': self.medical_input.toPlainText().strip()
        }
