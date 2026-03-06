# =============================================================================
# Happy Tooth Dental Clinic and Services
# Login Controller — Handles login logic
# =============================================================================

import bcrypt
from database import Database
from models.user_model import UserModel


class LoginController:
    """Controller for login authentication."""
    
    def __init__(self, view):
        self.view = view
        self.db = Database()
        self._connect_signals()
    
    def _connect_signals(self):
        """Connect view signals to controller methods."""
        self.view.login_btn.clicked.connect(self.handle_login)
    
    def handle_login(self):
        """Process login attempt."""
        username, password = self.view.get_credentials()
        
        # Validate inputs
        if not username:
            self.view.show_error("Please enter your username.")
            return
        if not password:
            self.view.show_error("Please enter your password.")
            return
        
        # Authenticate — fetch user and compare hashed password
        user = self.db.fetch_one(UserModel.Q_SELECT_BY_USERNAME, (username,))
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Successful login — emit signal with user data
            self.view.login_success.emit(user)
        else:
            self.view.show_error("Invalid username or password.")
