# =============================================================================
# Happy Tooth Dental Clinic and Services
# Configuration File
# =============================================================================

# Database Configuration (XAMPP MySQL)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default XAMPP MySQL has no password
    'database': 'happy_tooth_db',
    'port': 3306
}

# Application Configuration
APP_CONFIG = {
    'name': 'Happy Tooth Dental Clinic and Services',
    'version': '1.0.0',
    'window_width': 1200,
    'window_height': 700
}

# Color Theme (Matching Logo - Teal/White/Green)
COLORS = {
    'primary': '#2AACB8',        # Teal (from logo)
    'primary_dark': '#1B8FA0',   # Dark teal (hover)
    'primary_darker': '#157080', # Darker teal (sidebar bg)
    'sidebar_bg': '#1A6E7A',     # Sidebar background
    'sidebar_hover': '#2AACB8',  # Sidebar hover
    'sidebar_active': '#35C4D0', # Sidebar active item
    'accent_green': '#2E7D32',   # Success/confirm
    'light_green': '#66BB6A',    # Badges/positive
    'white': '#FFFFFF',          # Cards/inputs
    'off_white': '#F0F6F7',      # Main background
    'dark_text': '#263238',      # Primary text
    'gray_text': '#78909C',      # Secondary text
    'border': '#D4E6E9',         # Borders
    'danger': '#E53935',         # Delete/cancel
    'warning': '#FB8C00',        # Pending/warning
    'light_teal': '#E0F4F5'      # Light teal background
}

# Global session — stores the currently logged-in user
CURRENT_USER = {}
