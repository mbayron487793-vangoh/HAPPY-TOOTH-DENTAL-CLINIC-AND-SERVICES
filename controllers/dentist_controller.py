# =============================================================================
# Happy Tooth Dental Clinic and Services
# Dentist Controller
# =============================================================================

import bcrypt
from database import Database
from models.dentist_model import DentistModel
from models.user_model import UserModel
from views.dentist_view import DentistDialog


class DentistController:
    """Controller for Dentist management."""
    
    def __init__(self, view):
        self.view = view
        self.db = Database()
        self._connect_signals()
    
    def _connect_signals(self):
        self.view.add_btn.clicked.connect(self.add_dentist)
        self.view.search_input.textChanged.connect(self.search_dentists)
        self.view._edit_callback = self.edit_dentist
        self.view._delete_callback = self.delete_dentist
    
    def load_dentists(self):
        dentists = self.db.fetch_all(DentistModel.Q_SELECT_ALL)
        self.view.load_table(dentists)
    
    def search_dentists(self, keyword):
        if keyword.strip():
            search = f"%{keyword}%"
            dentists = self.db.fetch_all(DentistModel.Q_SEARCH, (search, search, search))
        else:
            dentists = self.db.fetch_all(DentistModel.Q_SELECT_ALL)
        self.view.load_table(dentists)
    
    def add_dentist(self):
        dialog = DentistDialog(self.view)
        if dialog.exec():
            data = dialog.get_data()
            user_id = None
            
            # Create user login account if requested
            if data.get('create_account'):
                # Check if username already exists
                existing = self.db.fetch_one(UserModel.Q_CHECK_USERNAME, (data['username'],))
                if existing:
                    self.view.show_warning(
                        "Error",
                        f"Username '{data['username']}' is already taken.\n"
                        f"Please try a different username."
                    )
                    return
                password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                user_result = self.db.execute_query(
                    UserModel.Q_INSERT,
                    (data['username'], password_hash.decode('utf-8'),
                     data['first_name'], data['last_name'], 'Dentist')
                )
                if not user_result:
                    self.view.show_warning("Error", "Failed to create user account.")
                    return
                # Get the new user's ID
                user_row = self.db.fetch_one(UserModel.Q_GET_ID_BY_USERNAME, (data['username'],))
                user_id = user_row['id'] if user_row else None
            
            result = self.db.execute_query(
                DentistModel.Q_INSERT,
                (data['first_name'], data['last_name'], data['specialization'],
                 data['contact_number'], data['email'], user_id)
            )
            if result:
                msg = "Dentist added successfully!"
                if data.get('create_account'):
                    msg += f"\n\nLogin account created:\n  Username: {data['username']}\n  Password: {data['password']}"
                self.view.show_info("Success", msg)
                self.load_dentists()
            else:
                self.view.show_warning("Error", "Failed to add dentist.")
    
    def edit_dentist(self, dentist_id):
        dentist = self.db.fetch_one(DentistModel.Q_SELECT_BY_ID, (dentist_id,))
        if not dentist:
            self.view.show_warning("Error", "Dentist not found.")
            return
        dialog = DentistDialog(self.view, dentist)
        if dialog.exec():
            data = dialog.get_data()
            user_id = dentist.get('user_id')  # keep existing linked account
            
            # If creating a new account during edit
            if data.get('create_account'):
                existing = self.db.fetch_one(UserModel.Q_CHECK_USERNAME, (data['username'],))
                if existing:
                    self.view.show_warning(
                        "Error",
                        f"Username '{data['username']}' is already taken.\n"
                        f"Please try a different username."
                    )
                    return
                password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                user_result = self.db.execute_query(
                    UserModel.Q_INSERT,
                    (data['username'], password_hash.decode('utf-8'),
                     data['first_name'], data['last_name'], 'Dentist')
                )
                if not user_result:
                    self.view.show_warning("Error", "Failed to create user account.")
                    return
                user_row = self.db.fetch_one(UserModel.Q_GET_ID_BY_USERNAME, (data['username'],))
                user_id = user_row['id'] if user_row else None
            
            result = self.db.execute_query(
                DentistModel.Q_UPDATE,
                (data['first_name'], data['last_name'],
                 data['specialization'], data['contact_number'],
                 data['email'], user_id, dentist_id)
            )
            if result:
                msg = "Dentist updated successfully!"
                if data.get('create_account'):
                    msg += f"\n\nLogin account created:\n  Username: {data['username']}\n  Password: {data['password']}"
                self.view.show_info("Success", msg)
                self.load_dentists()
            else:
                self.view.show_warning("Error", "Failed to update dentist.")
    
    def delete_dentist(self, dentist_id):
        if self.view.show_confirm(
            "Confirm Delete",
            "Are you sure you want to delete this dentist?"
        ):
            result = self.db.execute_query(DentistModel.Q_DELETE, (dentist_id,))
            if result:
                self.view.show_info("Deleted", "Dentist deleted successfully.")
                self.load_dentists()
            else:
                self.view.show_warning("Error", "Failed to delete dentist.")
