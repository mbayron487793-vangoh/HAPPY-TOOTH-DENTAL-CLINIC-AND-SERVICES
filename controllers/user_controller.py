# =============================================================================
# Happy Tooth Dental Clinic and Services
# User Controller — Manages user accounts (Admin only)
# =============================================================================

import bcrypt
from database import Database
from models.user_model import UserModel
from models.dentist_model import DentistModel
from views.user_view import UserDialog, ResetPasswordDialog
from views.change_password_dialog import ChangePasswordDialog


class UserController:
    """Controller for User/Staff Management."""
    
    def __init__(self, view):
        self.view = view
        self.db = Database()
        self._connect_signals()
    
    def _connect_signals(self):
        self.view.add_btn.clicked.connect(self.add_user)
        self.view.search_input.textChanged.connect(self.search_users)
        self.view._edit_callback = self.edit_user
        self.view._toggle_callback = self.toggle_user
        self.view._reset_callback = self.reset_password
        self.view._delete_callback = self.delete_user
    
    def load_users(self):
        """Load all users into the table."""
        users = self.db.fetch_all(UserModel.Q_SELECT_ALL)
        self.view.load_table(users)
    
    def search_users(self, keyword):
        """Filter users by keyword."""
        users = self.db.fetch_all(UserModel.Q_SELECT_ALL)
        if keyword.strip():
            keyword_lower = keyword.lower()
            users = [
                u for u in users
                if keyword_lower in u['username'].lower()
                or keyword_lower in u['first_name'].lower()
                or keyword_lower in u['last_name'].lower()
                or keyword_lower in u['role'].lower()
            ]
        self.view.load_table(users)
    
    def add_user(self):
        """Add a new user with any role."""
        dialog = UserDialog(self.view)
        if dialog.exec():
            data = dialog.get_data()
            # Check if username already exists
            existing = self.db.fetch_one(UserModel.Q_CHECK_USERNAME, (data['username'],))
            if existing:
                self.view.show_warning("Error", "Username already taken. Please choose a different username.")
                return
            
            password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            result = self.db.execute_query(
                UserModel.Q_INSERT,
                (data['username'], password_hash.decode('utf-8'),
                 data['first_name'], data['last_name'], data['role'])
            )
            if result:
                # If role is Dentist, also create a dentist record linked to this user
                if data['role'] == 'Dentist':
                    user = self.db.fetch_one(UserModel.Q_GET_ID_BY_USERNAME, (data['username'],))
                    if user:
                        self.db.execute_query(
                            DentistModel.Q_INSERT,
                            (data['first_name'], data['last_name'],
                             'General Dentist', '', '', user['id'])
                        )
                self.view.show_info("Success", "User account created successfully!")
                self.load_users()
            else:
                self.view.show_warning("Error", "Failed to create user account.")
    
    def edit_user(self, user_id):
        """Edit an existing user."""
        user = self.db.fetch_one(UserModel.Q_SELECT_BY_ID, (user_id,))
        if not user:
            self.view.show_warning("Error", "User not found.")
            return
        
        old_role = user.get('role')
        dialog = UserDialog(self.view, user_data=user)
        if dialog.exec():
            data = dialog.get_data()
            # Check if username is taken by another user
            existing = self.db.fetch_one(
                UserModel.Q_CHECK_USERNAME_EXCLUDE, (data['username'], user_id)
            )
            if existing:
                self.view.show_warning("Error", "Username already taken by another user.")
                return
            
            result = self.db.execute_query(
                UserModel.Q_UPDATE,
                (data['username'], data['first_name'], data['last_name'], data['role'], user_id)
            )
            
            # If role changed TO Dentist, create a linked dentist record if one doesn't exist
            if data['role'] == 'Dentist' and old_role != 'Dentist':
                existing_dentist = self.db.fetch_one(DentistModel.Q_SELECT_BY_USER_ID, (user_id,))
                if not existing_dentist:
                    self.db.execute_query(
                        DentistModel.Q_INSERT,
                        (data['first_name'], data['last_name'],
                         'General Dentist', '', '', user_id)
                    )
            
            # Update password if provided
            if 'password' in data:
                password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                self.db.execute_query(
                    UserModel.Q_UPDATE_PASSWORD,
                    (password_hash.decode('utf-8'), user_id)
                )
            
            if result:
                self.view.show_info("Success", "User updated successfully!")
                self.load_users()
            else:
                self.view.show_warning("Error", "Failed to update user.")
    
    def toggle_user(self, user_id):
        """Toggle user active/inactive status."""
        user = self.db.fetch_one(UserModel.Q_SELECT_BY_ID, (user_id,))
        if not user:
            return
        
        action = "deactivate" if user.get('is_active') else "activate"
        if self.view.show_confirm(
            "Confirm",
            f"Are you sure you want to {action} user '{user['username']}'?"
        ):
            result = self.db.execute_query(UserModel.Q_TOGGLE_STATUS, (user_id,))
            if result:
                self.view.show_info("Success", f"User {action}d successfully!")
                self.load_users()
            else:
                self.view.show_warning("Error", f"Failed to {action} user.")
    
    def reset_password(self, user_id):
        """Reset a user's password."""
        user = self.db.fetch_one(UserModel.Q_SELECT_BY_ID, (user_id,))
        if not user:
            return
        
        dialog = ResetPasswordDialog(self.view, user['username'])
        if dialog.exec():
            new_password = dialog.get_password()
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            result = self.db.execute_query(
                UserModel.Q_UPDATE_PASSWORD,
                (password_hash.decode('utf-8'), user_id)
            )
            if result:
                self.view.show_info("Success", f"Password for '{user['username']}' has been reset!")
            else:
                self.view.show_warning("Error", "Failed to reset password.")
    
    def delete_user(self, user_id):
        """Delete a user account."""
        user = self.db.fetch_one(UserModel.Q_SELECT_BY_ID, (user_id,))
        if not user:
            return
        
        if user['username'] == 'admin':
            self.view.show_warning("Protected", "The default admin account cannot be deleted.")
            return
        
        if self.view.show_confirm(
            "Confirm Delete",
            f"Are you sure you want to permanently delete user '{user['username']}'?\n"
            "This action cannot be undone."
        ):
            # If user is a dentist, delete linked dentist record
            if user.get('role') == 'Dentist':
                dentist = self.db.fetch_one(DentistModel.Q_SELECT_BY_USER_ID, (user_id,))
                if dentist:
                    self.db.execute_query(DentistModel.Q_DELETE, (dentist['id'],))
            result = self.db.execute_query(UserModel.Q_DELETE, (user_id,))
            if result:
                self.view.show_info("Deleted", "User account deleted successfully.")
                self.load_users()
            else:
                self.view.show_warning("Error", "Failed to delete user account.")
    
    def change_password(self, parent_widget, user_data):
        """Open change password dialog and process the password change."""
        dialog = ChangePasswordDialog(parent_widget, user_data)
        if dialog.exec():
            data = dialog.get_data()
            # Verify current password
            user = self.db.fetch_one(UserModel.Q_SELECT_BY_ID, (user_data.get('id'),))
            if not user:
                self.view.show_warning("Error", "User not found.")
                return
            if not bcrypt.checkpw(
                data['current_password'].encode('utf-8'),
                user['password_hash'].encode('utf-8')
            ):
                self.view.show_warning("Error", "Current password is incorrect.")
                return
            # Hash and save new password
            hashed = bcrypt.hashpw(
                data['new_password'].encode('utf-8'), bcrypt.gensalt()
            ).decode('utf-8')
            result = self.db.execute_query(UserModel.Q_UPDATE_PASSWORD, (hashed, user['id']))
            if result:
                self.view.show_info("Success", "Password changed successfully!")
            else:
                self.view.show_warning("Error", "Failed to change password.")
