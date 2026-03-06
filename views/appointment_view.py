# =============================================================================
# Happy Tooth Dental Clinic and Services
# Appointment View — Appointment scheduling interface
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QComboBox, QDateEdit, QTimeEdit,
    QTextEdit, QMessageBox, QMenu, QTextBrowser
)
from PyQt6.QtCore import Qt, QDate, QTime, QSize
from PyQt6.QtGui import QAction
import qtawesome as qta


class AppointmentView(QWidget):
    """Appointment management page."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.calendar-check', color='#1A6E7A').pixmap(24, 24))
        title_icon.setStyleSheet("background: transparent;")
        header_layout.addWidget(title_icon)
        
        title = QLabel("Appointment Scheduling")
        title.setObjectName("section_title")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Search appointments...")
        self.search_input.setMaximumWidth(320)
        self.search_input.setMinimumHeight(44)
        header_layout.addWidget(self.search_input)
        
        self.add_btn = QPushButton("  Book Appointment")
        self.add_btn.setObjectName("primary_btn")
        self.add_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Patient", "Dentist", "Date", "Time",
            "Status", "Notes", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 80)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self._on_cell_clicked)
        layout.addWidget(self.table)
    
    def load_table(self, appointments):
        self.table.setRowCount(0)
        for row_num, appt in enumerate(appointments):
            self.table.insertRow(row_num)
            patient_item = QTableWidgetItem(appt['patient_name'])
            patient_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 0, patient_item)
            dentist_item = QTableWidgetItem(appt['dentist_name'])
            dentist_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 1, dentist_item)
            date_item = QTableWidgetItem(str(appt['appointment_date']))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 2, date_item)
            # Format time as AM/PM
            raw_time = appt.get('appointment_time', '')
            time_display = self._format_time_ampm(raw_time)
            time_item = QTableWidgetItem(time_display)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 3, time_item)
            # Status indicator — uses pre-enriched display_status from controller
            display_status = appt.get('display_status', appt['status'])
            status_item = QTableWidgetItem(display_status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if 'Paid' in display_status and '✓' in display_status:
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif 'Partial' in display_status or 'Unpaid' in display_status or 'No Bill' in display_status:
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            elif appt['status'] == 'Cancelled':
                status_item.setForeground(Qt.GlobalColor.red)
            elif appt['status'] == 'No Show':
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            else:
                status_item.setForeground(Qt.GlobalColor.blue)
            self.table.setItem(row_num, 4, status_item)
            # Notes — uses pre-enriched combined_notes from controller
            combined_notes = appt.get('combined_notes', appt.get('notes', '') or '')
            notes_item = QTableWidgetItem(combined_notes)
            notes_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 5, notes_item)
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
            
            # Show "Mark as Complete" only for Scheduled appointments
            if appt['status'] == 'Scheduled':
                complete_action = QAction("✓ Mark as Complete", menu)
                complete_action.triggered.connect(lambda _, aid=appt['id']: self._mark_complete_callback(aid) if hasattr(self, '_mark_complete_callback') else None)
                menu.addAction(complete_action)
                menu.addSeparator()
            
            archive_action = QAction("Archive", menu)
            archive_action.triggered.connect(lambda _, aid=appt['id']: self._archive_callback(aid) if hasattr(self, '_archive_callback') else None)
            menu.addAction(archive_action)
            
            action_btn.setMenu(menu)
            action_layout.addWidget(action_btn)
            
            self.table.setCellWidget(row_num, 6, action_widget)
            self.table.setRowHeight(row_num, 60)
    
    def _on_cell_clicked(self, row, column):
        """Show full notes in a popup when clicking the Notes column."""
        if column == 5:  # Notes column
            item = self.table.item(row, column)
            notes_text = item.text() if item else ''
            if not notes_text:
                return
            patient_item = self.table.item(row, 0)
            patient_name = patient_item.text() if patient_item else 'Unknown'
            
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Notes — {patient_name}")
            dialog.setMinimumSize(450, 300)
            dialog.setStyleSheet("QDialog { background-color: #FFFFFF; }")
            layout = QVBoxLayout(dialog)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(12)
            
            title = QLabel(f"Notes for {patient_name}")
            title.setObjectName("section_title")
            layout.addWidget(title)
            
            notes_display = QTextBrowser()
            notes_display.setStyleSheet(
                "QTextBrowser { background: #F8FBFC; border: 1px solid #D4E6E9; "
                "border-radius: 8px; padding: 12px; font-size: 14px; color: #263238; }"
            )
            # Format notes nicely — split by | separator
            parts = notes_text.split(' | ')
            html_parts = []
            for part in parts:
                part = part.strip()
                if part.startswith('[') and ']' in part:
                    bracket_end = part.index(']')
                    service = part[1:bracket_end]
                    note = part[bracket_end+1:].strip()
                    html_parts.append(
                        f'<p><span style="color: #1A6E7A; font-weight: 600;">{service}:</span> {note}</p>'
                    )
                else:
                    html_parts.append(f'<p>{part}</p>')
            notes_display.setHtml(''.join(html_parts))
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


class AppointmentDialog(QDialog):
    """Dialog for booking/editing appointments."""
    
    def __init__(self, parent=None, appt_data=None, patients=None, dentists=None):
        super().__init__(parent)
        self.appt_data = appt_data
        self._patients = patients or []
        self._dentists = dentists or []
        self.setWindowTitle("Edit Appointment" if appt_data else "Book New Appointment")
        self.setMinimumWidth(500)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)
        
        title = QLabel("Edit Appointment" if self.appt_data else "Book New Appointment")
        title.setObjectName("section_title")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(10)
        
        # Patient dropdown
        self.patient_combo = QComboBox()
        self.patient_combo.setMinimumHeight(38)
        for p in self._patients:
            self.patient_combo.addItem(f"{p['first_name']} {p['last_name']}", p['id'])
        form.addRow(self._label("Patient *"), self.patient_combo)
        
        # Dentist dropdown
        self.dentist_combo = QComboBox()
        self.dentist_combo.setMinimumHeight(38)
        for d in self._dentists:
            self.dentist_combo.addItem(f"Dr. {d['first_name']} {d['last_name']} ({d['specialization']})", d['id'])
        form.addRow(self._label("Dentist *"), self.dentist_combo)
        
        # Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setMinimumHeight(38)
        form.addRow(self._label("Date *"), self.date_input)
        
        # Time
        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("hh:mm AP")
        self.time_input.setTime(QTime(9, 0))
        self.time_input.setMinimumHeight(38)
        form.addRow(self._label("Time *"), self.time_input)
        
        # Status (only for edit)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Scheduled", "Completed", "Cancelled", "No Show"])
        self.status_combo.setMinimumHeight(38)
        if not self.appt_data:
            self.status_combo.setEnabled(False)
        form.addRow(self._label("Status"), self.status_combo)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional notes (optional)")
        self.notes_input.setMaximumHeight(70)
        form.addRow(self._label("Notes"), self.notes_input)
        
        layout.addLayout(form)
        
        # Pre-fill
        if self.appt_data:
            # Select patient
            for i in range(self.patient_combo.count()):
                if self.patient_combo.itemData(i) == self.appt_data.get('patient_id'):
                    self.patient_combo.setCurrentIndex(i)
                    break
            # Select dentist
            for i in range(self.dentist_combo.count()):
                if self.dentist_combo.itemData(i) == self.appt_data.get('dentist_id'):
                    self.dentist_combo.setCurrentIndex(i)
                    break
            # Date
            ad = self.appt_data.get('appointment_date')
            if ad:
                self.date_input.setMinimumDate(QDate(2000, 1, 1))
                self.date_input.setDate(QDate.fromString(str(ad), "yyyy-MM-dd"))
            # Time
            at = self.appt_data.get('appointment_time')
            if at:
                time_str = str(at)
                parts = time_str.split(':')
                if len(parts) >= 2:
                    self.time_input.setTime(QTime(int(parts[0]), int(parts[1])))
            # Status
            idx = self.status_combo.findText(self.appt_data.get('status', 'Scheduled'))
            if idx >= 0:
                self.status_combo.setCurrentIndex(idx)
            # Notes
            self.notes_input.setPlainText(self.appt_data.get('notes', '') or '')
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("  Cancel")
        cancel_btn.setObjectName("outline_btn")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("  Save Appointment")
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
        if self.patient_combo.count() == 0:
            QMessageBox.warning(self, "Error", "No patients found. Please add a patient first.")
            return
        if self.dentist_combo.count() == 0:
            QMessageBox.warning(self, "Error", "No dentists found. Please add a dentist first.")
            return
        self.accept()
    
    def get_data(self):
        return {
            'patient_id': self.patient_combo.currentData(),
            'dentist_id': self.dentist_combo.currentData(),
            'appointment_date': self.date_input.date().toString("yyyy-MM-dd"),
            'appointment_time': self.time_input.time().toString("HH:mm:ss"),
            'status': self.status_combo.currentText(),
            'notes': self.notes_input.toPlainText().strip()
        }
