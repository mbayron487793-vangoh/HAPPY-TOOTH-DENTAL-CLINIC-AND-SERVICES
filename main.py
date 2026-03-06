# =============================================================================
# Happy Tooth Dental Clinic and Services
# Main Entry Point — Application launcher
# =============================================================================

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtCore import Qt

# Ensure the project root is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Database
from views.login_view import LoginView
from views.main_window import MainWindow
from controllers.login_controller import LoginController


class HappyToothApp:
    """Main application class — manages login and main window lifecycle."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Happy Tooth Dental Clinic and Services")
        
        # Set application icon
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            self.app.setWindowIcon(QIcon(logo_path))
        
        # Load Poppins font
        self._load_fonts()
        
        # Load QSS theme
        self._load_styles()
        
        # Initialize database
        if not self._init_database():
            QMessageBox.critical(
                None, "Database Error",
                "Could not connect to the database.\n\n"
                "Please make sure:\n"
                "1. XAMPP is running\n"
                "2. MySQL/MariaDB service is started\n"
                "3. Check config.py for correct settings\n\n"
                "The application will now close."
            )
            sys.exit(1)
        
        # Start with login screen
        self.login_view = None
        self.main_window = None
        self.show_login()
    
    def _load_fonts(self):
        """Load custom fonts (Poppins)."""
        fonts_dir = os.path.join(os.path.dirname(__file__), 'assets', 'fonts')
        poppins_fonts = [
            'Poppins-Regular.ttf',
            'Poppins-Medium.ttf',
            'Poppins-SemiBold.ttf',
            'Poppins-Bold.ttf',
            'Poppins-Light.ttf'
        ]
        
        fonts_loaded = 0
        if os.path.exists(fonts_dir):
            for font_file in poppins_fonts:
                font_path = os.path.join(fonts_dir, font_file)
                if os.path.exists(font_path):
                    font_id = QFontDatabase.addApplicationFont(font_path)
                    if font_id != -1:
                        fonts_loaded += 1
        
        # Set default application font
        if fonts_loaded > 0:
            app_font = QFont('Poppins', 10)
            self.app.setFont(app_font)
            print(f"[App] Loaded {fonts_loaded} Poppins font variants.")
        else:
            # Fallback to Segoe UI if Poppins not available
            app_font = QFont('Segoe UI', 10)
            self.app.setFont(app_font)
            print("[App] Using fallback font (Segoe UI). For best experience, add Poppins fonts to assets/fonts/")
    
    def _load_styles(self):
        """Load the QSS stylesheet."""
        qss_path = os.path.join(os.path.dirname(__file__), 'assets', 'styles.qss')
        try:
            if os.path.exists(qss_path):
                with open(qss_path, 'r') as f:
                    self.app.setStyleSheet(f.read())
                print("[App] QSS theme loaded successfully.")
            else:
                print(f"[App] QSS file not found at: {qss_path}")
        except Exception as e:
            print(f"[App] Failed to load QSS: {e}")
    
    def _init_database(self):
        """Initialize database and create tables."""
        try:
            db = Database()
            
            # Create database if it doesn't exist
            if not db.create_database():
                return False
            
            # Connect and create tables
            if not db.connect():
                return False
            
            if not db.initialize_tables():
                return False
            
            # Insert default data
            db.insert_default_admin()
            db.insert_default_services()
            
            print("[App] Database initialized successfully.")
            return True
        except Exception as e:
            print(f"[App] Database initialization failed: {e}")
            return False
    
    def show_login(self):
        """Show the login screen."""
        # Close main window if open
        if self.main_window:
            # Instead of .close(), use .deleteLater() to avoid triggering closeEvent
            self.main_window.logout_signal.disconnect(self.on_logout)
            self.main_window.deleteLater()
            self.main_window = None
        
        self.login_view = LoginView()
        self.login_controller = LoginController(self.login_view)
        self.login_view.login_success.connect(self.on_login_success)
        self.login_view.setWindowTitle("Happy Tooth Dental Clinic — Login")
        self.login_view.setMinimumSize(500, 650)
        self.login_view.showMaximized()
    
    def on_login_success(self, user_data):
        """Handle successful login — switch to main window."""
        print(f"[App] Login successful: {user_data['username']} ({user_data['role']})")
        
        # Store in global session so all controllers can access it
        import config
        config.CURRENT_USER = dict(user_data)
        
        # Set user on Database singleton — also sets MySQL session variable
        from database import Database
        db = Database()
        db.set_user(user_data.get('id'))
        
        # Close login view
        if self.login_view:
            self.login_view.close()
            self.login_view = None
        
        # Open main window
        self.main_window = MainWindow(user_data)
        self.main_window.logout_signal.connect(self.on_logout)
        self.main_window.showMaximized()
    
    def on_logout(self):
        """Handle logout — return to login screen."""
        print("[App] User logged out.")
        self.show_login()
    
    def run(self):
        """Start the application event loop."""
        return self.app.exec()


# =============================================================================
# Run the application
# =============================================================================
if __name__ == '__main__':
    app = HappyToothApp()
    sys.exit(app.run())
