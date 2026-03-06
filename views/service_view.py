# =============================================================================
# Happy Tooth Dental Clinic and Services
# Service View — Dental services / price list management
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QTextEdit, QDoubleSpinBox, QMessageBox, QMenu
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
import qtawesome as qta


class ServiceView(QWidget):
    """Service management page."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.tools', color='#1A6E7A').pixmap(24, 24))
        title_icon.setStyleSheet("background: transparent;")
        header_layout.addWidget(title_icon)
        
        title = QLabel("Dental Services")
        title.setObjectName("section_title")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Search services...")
        self.search_input.setMaximumWidth(320)
        self.search_input.setMinimumHeight(44)
        header_layout.addWidget(self.search_input)
        
        self.add_btn = QPushButton("  Add Service")
        self.add_btn.setObjectName("primary_btn")
        self.add_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(self.add_btn)
        
        layout.addLayout(header_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Service Name", "Description", "Price (₱)", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 80)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
    
    def load_table(self, services):
        self.table.setRowCount(0)
        for row_num, svc in enumerate(services):
            self.table.insertRow(row_num)
            
            name_item = QTableWidgetItem(svc['service_name'])
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 0, name_item)
            
            desc_item = QTableWidgetItem(svc.get('description', '') or '')
            desc_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num, 1, desc_item)
            
            price_item = QTableWidgetItem(f"₱{float(svc['price']):,.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_num, 2, price_item)
            
            status = "Active" if svc.get('is_active', 1) else "Inactive"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(Qt.GlobalColor.darkGreen if status == "Active" else Qt.GlobalColor.red)
            self.table.setItem(row_num, 3, status_item)
            
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
                QPushButton {
                    background: #FFFFFF;
                    border: 1px solid #D4E6E9;
                    border-radius: 6px;
                    padding: 0px;
                    text-align: center;
                }
                QPushButton:hover {
                    background: #E8F4F5;
                    border-color: #1A6E7A;
                }
                QPushButton::menu-indicator {
                    image: none;
                    width: 0px;
                }
            """)
            
            menu = QMenu(action_btn)
            menu.setStyleSheet("""
                QMenu {
                    background: white;
                    border: 1px solid #D4E6E9;
                    border-radius: 8px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 8px 20px;
                    border-radius: 4px;
                }
                QMenu::item:selected {
                    background: #E8F4F5;
                    color: #1A6E7A;
                }
            """)
            
            edit_action = QAction("Edit", menu)
            edit_action.triggered.connect(lambda _, sid=svc['id']: self._edit_callback(sid) if hasattr(self, '_edit_callback') else None)
            menu.addAction(edit_action)
            
            delete_action = QAction("Delete", menu)
            delete_action.triggered.connect(lambda _, sid=svc['id']: self._delete_callback(sid) if hasattr(self, '_delete_callback') else None)
            menu.addAction(delete_action)
            
            action_btn.setMenu(menu)
            action_layout.addWidget(action_btn)
            
            self.table.setCellWidget(row_num, 4, action_widget)
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


class ServiceDialog(QDialog):
    """Dialog for adding/editing a service."""
    
    def __init__(self, parent=None, service_data=None):
        super().__init__(parent)
        self.service_data = service_data
        self.setWindowTitle("Edit Service" if service_data else "Add New Service")
        self.setMinimumWidth(480)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)
        
        title = QLabel("Edit Service" if self.service_data else "Add New Service")
        title.setObjectName("section_title")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(10)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Tooth Cleaning")
        self.name_input.setMinimumHeight(38)
        form.addRow(self._label("Service Name *"), self.name_input)
        
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Brief description of the service")
        self.desc_input.setMaximumHeight(80)
        form.addRow(self._label("Description"), self.desc_input)
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix("₱ ")
        self.price_input.setMaximum(999999.99)
        self.price_input.setDecimals(2)
        self.price_input.setMinimumHeight(38)
        form.addRow(self._label("Price *"), self.price_input)
        
        layout.addLayout(form)
        
        if self.service_data:
            self.name_input.setText(self.service_data.get('service_name', ''))
            self.desc_input.setPlainText(self.service_data.get('description', '') or '')
            self.price_input.setValue(float(self.service_data.get('price', 0)))
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("  Cancel")
        cancel_btn.setObjectName("outline_btn")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#2AACB8'))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("  Save Service")
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
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Service name is required.")
            return
        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Price must be greater than zero.")
            return
        self.accept()
    
    def get_data(self):
        return {
            'service_name': self.name_input.text().strip(),
            'description': self.desc_input.toPlainText().strip(),
            'price': self.price_input.value()
        }
