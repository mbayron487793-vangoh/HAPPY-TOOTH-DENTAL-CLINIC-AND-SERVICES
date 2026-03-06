# =============================================================================
# Happy Tooth Dental Clinic and Services
# Service Controller
# =============================================================================

from database import Database
from models.service_model import ServiceModel
from views.service_view import ServiceDialog


class ServiceController:
    def __init__(self, view):
        self.view = view
        self.db = Database()
        self._connect_signals()
    
    def _connect_signals(self):
        self.view.add_btn.clicked.connect(self.add_service)
        self.view.search_input.textChanged.connect(self.search_services)
        self.view._edit_callback = self.edit_service
        self.view._delete_callback = self.delete_service
        self.view._toggle_callback = self.toggle_service_status

    def toggle_service_status(self, service_id):
        # Only admin can change service status
        user_data = getattr(self.view, 'user_data', None)
        if not user_data or user_data.get('role') != 'Admin':
            self.view.show_warning("Access Denied", "Only admin can change service status.")
            return
        result = self.db.execute_query(ServiceModel.Q_TOGGLE_STATUS, (service_id,))
        if result:
            self.view.show_info("Success", "Service status updated.")
            self.load_services()
        else:
            self.view.show_warning("Error", "Failed to update service status.")
    
    def load_services(self):
        services = self.db.fetch_all(ServiceModel.Q_SELECT_ALL)
        self.view.load_table(services)
    
    def search_services(self, keyword):
        if keyword.strip():
            search = f"%{keyword}%"
            services = self.db.fetch_all(ServiceModel.Q_SEARCH, (search, search))
        else:
            services = self.db.fetch_all(ServiceModel.Q_SELECT_ALL)
        self.view.load_table(services)
    
    def add_service(self):
        dialog = ServiceDialog(self.view)
        if dialog.exec():
            data = dialog.get_data()
            result = self.db.execute_query(
                ServiceModel.Q_INSERT,
                (data['service_name'], data['description'], data['price'])
            )
            if result:
                self.view.show_info("Success", "Service added successfully!")
                self.load_services()
            else:
                self.view.show_warning("Error", "Failed to add service.")
    
    def edit_service(self, service_id):
        service = self.db.fetch_one(ServiceModel.Q_SELECT_BY_ID, (service_id,))
        if not service:
            self.view.show_warning("Error", "Service not found.")
            return
        dialog = ServiceDialog(self.view, service)
        if dialog.exec():
            data = dialog.get_data()
            result = self.db.execute_query(
                ServiceModel.Q_UPDATE,
                (data['service_name'], data['description'], data['price'], service_id)
            )
            if result:
                self.view.show_info("Success", "Service updated successfully!")
                self.load_services()
            else:
                self.view.show_warning("Error", "Failed to update service.")
    
    def delete_service(self, service_id):
        if self.view.show_confirm("Confirm Delete", "Are you sure you want to delete this service?"):
            result = self.db.execute_query(ServiceModel.Q_DELETE, (service_id,))
            if result:
                self.view.show_info("Deleted", "Service deleted successfully.")
                self.load_services()
            else:
                self.view.show_warning("Error", "Failed to delete service.")
