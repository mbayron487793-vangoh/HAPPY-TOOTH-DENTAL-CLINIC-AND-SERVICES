# =============================================================================
# Happy Tooth Dental Clinic and Services
# Patient History Dialog — Full medical history in one view
# =============================================================================

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QWidget, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
import qtawesome as qta


class PatientHistoryDialog(QDialog):
    """Full patient medical history — appointments, treatments, and bills."""

    def __init__(self, parent=None, patient_data=None, history_data=None):
        super().__init__(parent)
        self.patient = patient_data or {}
        self._history = history_data or {}
        patient_name = f"{self.patient.get('first_name', '')} {self.patient.get('last_name', '')}"
        self.setWindowTitle(f"Medical History — {patient_name}")
        self.setMinimumSize(900, 640)
        self.setStyleSheet("QDialog { background-color: #F8FBFC; border-radius: 16px; }")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # ---- Patient Info Header ----
        info_card = QFrame()
        info_card.setObjectName("stat_card")
        info_card.setStyleSheet("""
            QFrame#stat_card {
                background-color: white;
                border: 1px solid #E8F0F2;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        info_layout = QHBoxLayout(info_card)
        info_layout.setSpacing(36)

        # Left: patient info
        left_info = QVBoxLayout()
        patient_name = f"{self.patient.get('first_name', '')} {self.patient.get('last_name', '')}"
        name_label = QLabel(patient_name)
        name_label.setStyleSheet("font-size: 22px; font-weight: 600; color: #1A6E7A; letter-spacing: 0.3px;")
        left_info.addWidget(name_label)

        details = []
        if self.patient.get('gender'):
            details.append(f"Sex: {self.patient['gender']}")
        if self.patient.get('birthdate'):
            details.append(f"Birthdate: {self.patient['birthdate']}")
            # Calculate age
            try:
                from datetime import date, datetime
                bd = self.patient['birthdate']
                if isinstance(bd, str):
                    bd = datetime.strptime(bd, "%Y-%m-%d").date()
                today = date.today()
                age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
                details.append(f"Age: {age}")
            except Exception:
                pass
        if self.patient.get('contact_number'):
            details.append(f"Contact: {self.patient['contact_number']}")
        if self.patient.get('email'):
            details.append(f"Email: {self.patient['email']}")

        detail_label = QLabel("  |  ".join(details))
        detail_label.setStyleSheet("color: #78909C; font-size: 12px;")
        detail_label.setWordWrap(True)
        left_info.addWidget(detail_label)

        if self.patient.get('address'):
            addr_label = QLabel(f"Address: {self.patient['address']}")
            addr_label.setStyleSheet("color: #78909C; font-size: 11px;")
            left_info.addWidget(addr_label)

        if self.patient.get('medical_history'):
            med_label = QLabel(f"Medical Notes: {self.patient['medical_history']}")
            med_label.setStyleSheet("color: #E65100; font-size: 11px; font-weight: bold;")
            med_label.setWordWrap(True)
            left_info.addWidget(med_label)

        info_layout.addLayout(left_info, 3)

        # Right: quick stats
        right_stats = QVBoxLayout()
        right_stats.setAlignment(Qt.AlignmentFlag.AlignTop)

        pid = self.patient.get('id')
        appointments = self._history.get('appointments', [])
        treatments = self._history.get('treatments', [])
        billings = self._history.get('billings', [])
        appt_count = len(appointments)
        treat_count = len(treatments)

        # Billing stats from controller
        total_billed = self._history.get('total_billed', 0.0)
        bill_count = len(billings)

        for label_text, value, color in [
            ("Appointments", str(appt_count), "#2AACB8"),
            ("Treatments", str(treat_count), "#1A6E7A"),
            ("Total Billed", f"₱{total_billed:,.2f}", "#2E7D32"),
        ]:
            stat = QLabel(f"<span style='font-size:22px; font-weight:bold; color:{color};'>{value}</span>"
                          f"<br><span style='font-size:11px; color:#78909C;'>{label_text}</span>")
            stat.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stat.setStyleSheet("padding: 4px;")
            right_stats.addWidget(stat)

        info_layout.addLayout(right_stats, 1)
        layout.addWidget(info_card)

        # ---- Tabbed sections ----
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #D4E6E9; border-radius: 8px; background: white; }
            QTabBar::tab { padding: 10px 20px; font-size: 13px; font-weight: 600; }
            QTabBar::tab:selected { background: #2AACB8; color: white; border-radius: 6px 6px 0 0; }
            QTabBar::tab:!selected { background: #E0F4F5; color: #1A6E7A; }
        """)

        # Tab 1: Appointments
        appt_tab = QWidget()
        appt_layout = QVBoxLayout(appt_tab)
        self.appt_table = QTableWidget()
        self.appt_table.setColumnCount(4)
        self.appt_table.setHorizontalHeaderLabels(["Date", "Time", "Dentist", "Status"])
        self.appt_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.appt_table.setAlternatingRowColors(True)
        self.appt_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.appt_table.verticalHeader().setVisible(False)
        self._load_appointments()
        appt_layout.addWidget(self.appt_table)
        tabs.addTab(appt_tab, qta.icon('fa5s.calendar-check', color='#2AACB8'), f"  Appointments ({appt_count})")

        # Tab 2: Treatments
        treat_tab = QWidget()
        treat_layout = QVBoxLayout(treat_tab)
        self.treat_table = QTableWidget()
        self.treat_table.setColumnCount(6)
        self.treat_table.setHorizontalHeaderLabels(["Date", "Service", "Tooth #", "Dentist", "Amount", "Notes"])
        self.treat_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.treat_table.setAlternatingRowColors(True)
        self.treat_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.treat_table.verticalHeader().setVisible(False)
        self._load_treatments()
        treat_layout.addWidget(self.treat_table)
        tabs.addTab(treat_tab, qta.icon('fa5s.notes-medical', color='#1A6E7A'), f"  Treatments ({treat_count})")

        # Tab 3: Billing
        bill_tab = QWidget()
        bill_layout = QVBoxLayout(bill_tab)
        self.bill_table = QTableWidget()
        self.bill_table.setColumnCount(6)
        self.bill_table.setHorizontalHeaderLabels(["Date", "Total", "Paid", "Balance", "Method", "Status"])
        self.bill_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bill_table.setAlternatingRowColors(True)
        self.bill_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bill_table.verticalHeader().setVisible(False)
        self._load_billings()
        bill_layout.addWidget(self.bill_table)
        tabs.addTab(bill_tab, qta.icon('fa5s.file-invoice-dollar', color='#2E7D32'), f"  Billing ({bill_count})")

        layout.addWidget(tabs)

        # ---- Close Button ----
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("  Close")
        close_btn.setObjectName("outline_btn")
        close_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    @staticmethod
    def _format_time_ampm(raw_time):
        try:
            time_str = str(raw_time)
            parts = time_str.split(':')
            if len(parts) >= 2:
                hour, minute = int(parts[0]), int(parts[1])
                period = "AM" if hour < 12 else "PM"
                display_hour = hour % 12 or 12
                return f"{display_hour}:{minute:02d} {period}"
        except Exception:
            pass
        return str(raw_time)

    def _load_appointments(self):
        appointments = self._history.get('appointments', [])
        self.appt_table.setRowCount(0)
        for row, appt in enumerate(appointments):
            self.appt_table.insertRow(row)
            self.appt_table.setItem(row, 0, QTableWidgetItem(str(appt.get('appointment_date', ''))))
            self.appt_table.setItem(row, 1, QTableWidgetItem(self._format_time_ampm(appt.get('appointment_time', ''))))
            self.appt_table.setItem(row, 2, QTableWidgetItem(appt.get('dentist_name', '')))
            status = appt.get('status', '')
            status_item = QTableWidgetItem(status)
            if status == 'Completed':
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif status == 'Cancelled':
                status_item.setForeground(Qt.GlobalColor.red)
            elif status == 'Scheduled':
                status_item.setForeground(Qt.GlobalColor.blue)
            self.appt_table.setItem(row, 3, status_item)
            self.appt_table.setRowHeight(row, 38)

    def _load_treatments(self):
        treatments = self._history.get('treatments', [])
        self.treat_table.setRowCount(0)
        for row, t in enumerate(treatments):
            self.treat_table.insertRow(row)
            self.treat_table.setItem(row, 0, QTableWidgetItem(str(t.get('appointment_date', ''))))
            self.treat_table.setItem(row, 1, QTableWidgetItem(t.get('service_name', '')))
            self.treat_table.setItem(row, 2, QTableWidgetItem(t.get('tooth_number', '-') or '-'))
            self.treat_table.setItem(row, 3, QTableWidgetItem(t.get('dentist_name', '')))
            price = float(t.get('price', 0))
            price_item = QTableWidgetItem(f"₱{price:,.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.treat_table.setItem(row, 4, price_item)
            self.treat_table.setItem(row, 5, QTableWidgetItem(t.get('notes', '') or ''))
            self.treat_table.setRowHeight(row, 38)

    def _load_billings(self):
        billings = self._history.get('billings', [])
        self.bill_table.setRowCount(0)
        for row, b in enumerate(billings):
            self.bill_table.insertRow(row)
            self.bill_table.setItem(row, 0, QTableWidgetItem(str(b.get('appointment_date', ''))))

            total = float(b.get('total_amount', 0))
            total_item = QTableWidgetItem(f"₱{total:,.2f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.bill_table.setItem(row, 1, total_item)

            paid = float(b.get('amount_paid', 0))
            paid_item = QTableWidgetItem(f"₱{paid:,.2f}")
            paid_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.bill_table.setItem(row, 2, paid_item)

            balance = float(b.get('balance', 0))
            bal_item = QTableWidgetItem(f"₱{balance:,.2f}")
            bal_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if balance > 0:
                bal_item.setForeground(Qt.GlobalColor.red)
            else:
                bal_item.setForeground(Qt.GlobalColor.darkGreen)
            self.bill_table.setItem(row, 3, bal_item)

            self.bill_table.setItem(row, 4, QTableWidgetItem(b.get('payment_method', '')))

            status = b.get('payment_status', 'Unpaid')
            status_item = QTableWidgetItem(status)
            if status == 'Paid':
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif status == 'Partial':
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.bill_table.setItem(row, 5, status_item)
            self.bill_table.setRowHeight(row, 38)
