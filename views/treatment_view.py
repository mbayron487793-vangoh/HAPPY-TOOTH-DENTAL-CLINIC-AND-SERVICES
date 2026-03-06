# =============================================================================
# Happy Tooth Dental Clinic and Services
# Treatment View — Treatment records interface
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QComboBox, QTextEdit, QMessageBox, QMenu, QTextBrowser
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
import qtawesome as qta


class TreatmentView(QWidget):
    """Treatment records page."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.notes-medical', color='#1A6E7A').pixmap(24, 24))
        title_icon.setStyleSheet("background: transparent;")
        header_layout.addWidget(title_icon)
        
        title = QLabel("Treatment Records")
        title.setObjectName("section_title")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Search treatments...")
        self.search_input.setMaximumWidth(320)
        self.search_input.setMinimumHeight(44)
        header_layout.addWidget(self.search_input)
        
        self.add_btn = QPushButton("  Add Treatment")
        self.add_btn.setObjectName("primary_btn")
        self.add_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Date", "Patient", "Dentist",
            "Service", "Tooth #", "Price (₱)", "Notes", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(7, 80)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self._on_cell_clicked)
        layout.addWidget(self.table)
    
    def load_table(self, treatments):
        self.table.setRowCount(0)
        for row_num, treat in enumerate(treatments):
            self.table.insertRow(row_num)
            
            date_item = QTableWidgetItem(str(treat.get('appointment_date', '')))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 0, date_item)
            
            patient_item = QTableWidgetItem(treat.get('patient_name', ''))
            patient_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 1, patient_item)
            
            dentist_item = QTableWidgetItem(treat.get('dentist_name', ''))
            dentist_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 2, dentist_item)
            
            service_item = QTableWidgetItem(treat.get('service_name', ''))
            service_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 3, service_item)
            
            tooth_item = QTableWidgetItem(treat.get('tooth_number', '') or '')
            tooth_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 4, tooth_item)
            
            price_item = QTableWidgetItem(f"₱{float(treat.get('price', 0)):,.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_num, 5, price_item)
            
            notes_item = QTableWidgetItem(treat.get('notes', '') or '')
            notes_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 6, notes_item)
            
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
            edit_action.triggered.connect(lambda _, tid=treat['id']: self._edit_callback(tid) if hasattr(self, '_edit_callback') else None)
            menu.addAction(edit_action)
            
            delete_action = QAction("Delete", menu)
            delete_action.triggered.connect(lambda _, tid=treat['id']: self._delete_callback(tid) if hasattr(self, '_delete_callback') else None)
            menu.addAction(delete_action)
            
            action_btn.setMenu(menu)
            action_layout.addWidget(action_btn)
            
            self.table.setCellWidget(row_num, 7, action_widget)
            self.table.setRowHeight(row_num, 60)
    
    def _on_cell_clicked(self, row, column):
        """Show full notes in a popup when clicking the Notes column."""
        if column == 6:  # Notes column
            item = self.table.item(row, column)
            notes_text = item.text() if item else ''
            if not notes_text:
                return
            patient_item = self.table.item(row, 1)
            service_item = self.table.item(row, 3)
            patient_name = patient_item.text() if patient_item else 'Unknown'
            service_name = service_item.text() if service_item else ''
            
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Treatment Notes — {patient_name}")
            dialog.setMinimumSize(400, 250)
            dialog.setStyleSheet("QDialog { background-color: #FFFFFF; }")
            layout = QVBoxLayout(dialog)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(12)
            
            title = QLabel(f"Notes for {patient_name}")
            title.setObjectName("section_title")
            layout.addWidget(title)
            
            if service_name:
                service_label = QLabel(f"Service: {service_name}")
                service_label.setStyleSheet("color: #1A6E7A; font-size: 13px; font-weight: 600;")
                layout.addWidget(service_label)
            
            notes_display = QTextBrowser()
            notes_display.setStyleSheet(
                "QTextBrowser { background: #F8FBFC; border: 1px solid #D4E6E9; "
                "border-radius: 8px; padding: 12px; font-size: 14px; color: #263238; }"
            )
            notes_display.setPlainText(notes_text)
            layout.addWidget(notes_display)
            
            close_btn = QPushButton("  Close")
            close_btn.setObjectName("outline_btn")
            close_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
            close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            close_btn.clicked.connect(dialog.close)
            btn_layout = QHBoxLayout()
            btn_layout.addStretch()
            btn_layout.addWidget(close_btn)
            layout.addLayout(btn_layout)
            
            dialog.exec()

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


class TreatmentDialog(QDialog):
    """Dialog for adding/editing treatments."""
    
    def __init__(self, parent=None, treatment_data=None, appointments=None, services=None):
        super().__init__(parent)
        self.treatment_data = treatment_data
        self._appointments = appointments or []
        self._services = services or []
        self.setWindowTitle("Edit Treatment" if treatment_data else "Add New Treatment")
        self.setMinimumWidth(500)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)
        
        title = QLabel("Edit Treatment" if self.treatment_data else "Add New Treatment")
        title.setObjectName("section_title")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(10)
        
        # Appointment dropdown (shows patient + date)
        self.appointment_combo = QComboBox()
        self.appointment_combo.setMinimumHeight(38)
        for a in self._appointments:
            label = f"{a['patient_name']} — {a['appointment_date']} ({a['status']})"
            self.appointment_combo.addItem(label, a['id'])
        form.addRow(self._label("Appointment *"), self.appointment_combo)
        
        # Service dropdown
        self.service_combo = QComboBox()
        self.service_combo.setMinimumHeight(38)
        for s in self._services:
            self.service_combo.addItem(f"{s['service_name']} (₱{float(s['price']):,.2f})", s['id'])
        form.addRow(self._label("Service *"), self.service_combo)
        
        # Tooth number
        self.tooth_input = QLineEdit()
        self.tooth_input.setPlaceholderText("e.g. 14, 16, Upper Left")
        self.tooth_input.setMinimumHeight(38)
        form.addRow(self._label("Tooth Number"), self.tooth_input)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Treatment notes...")
        self.notes_input.setMaximumHeight(80)
        form.addRow(self._label("Notes"), self.notes_input)
        
        layout.addLayout(form)
        
        # Pre-fill
        if self.treatment_data:
            aid = self.treatment_data.get('appointment_id')
            for i in range(self.appointment_combo.count()):
                if self.appointment_combo.itemData(i) == aid:
                    self.appointment_combo.setCurrentIndex(i)
                    break
            sid = self.treatment_data.get('service_id')
            for i in range(self.service_combo.count()):
                if self.service_combo.itemData(i) == sid:
                    self.service_combo.setCurrentIndex(i)
                    break
            self.tooth_input.setText(self.treatment_data.get('tooth_number', '') or '')
            self.notes_input.setPlainText(self.treatment_data.get('notes', '') or '')
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("  Cancel")
        cancel_btn.setObjectName("outline_btn")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("  Save Treatment")
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
        if self.appointment_combo.count() == 0:
            QMessageBox.warning(self, "Error", "No appointments found. Please create an appointment first.")
            return
        if self.service_combo.count() == 0:
            QMessageBox.warning(self, "Error", "No services found. Please add services first.")
            return
        self.accept()
    
    def get_data(self):
        return {
            'appointment_id': self.appointment_combo.currentData(),
            'service_id': self.service_combo.currentData(),
            'tooth_number': self.tooth_input.text().strip(),
            'notes': self.notes_input.toPlainText().strip()
        }
