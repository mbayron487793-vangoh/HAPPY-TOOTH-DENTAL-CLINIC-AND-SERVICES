# =============================================================================
# Happy Tooth Dental Clinic and Services
# Database Connection Helper
# =============================================================================

import pymysql
from pymysql import Error
from config import DB_CONFIG


class Database:
    """Handles all database connections and operations."""
    
    _instance = None  # Singleton instance
    
    def __new__(cls):
        """Singleton pattern - only one database connection."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
            cls._instance.current_user_id = None
        return cls._instance
    
    def set_user(self, user_id):
        """Store the current logged-in user ID and set MySQL session variable."""
        self.current_user_id = user_id
        try:
            conn = self.connect()
            if conn and conn.open:
                cursor = conn.cursor()
                cursor.execute("SET @app_user_id = %s", (user_id,))
                cursor.close()
        except Exception:
            pass

    def connect(self):
        """Establish connection to MySQL database."""
        try:
            if self.connection is None or not self.connection.open:
                self.connection = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
                # Restore session variable on reconnect
                if self.current_user_id is not None:
                    cursor = self.connection.cursor()
                    cursor.execute("SET @app_user_id = %s", (self.current_user_id,))
                    cursor.close()
            return self.connection
        except Error as e:
            print(f"[Database Error] Failed to connect: {e}")
            return None
    
    def disconnect(self):
        """Close database connection."""
        try:
            if self.connection and self.connection.open:
                self.connection.close()
                self.connection = None
        except Error as e:
            print(f"[Database Error] Failed to disconnect: {e}")
    
    def execute_query(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE queries (parameterized)."""
        try:
            conn = self.connect()
            if conn is None:
                return False
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id if last_id else True
        except Error as e:
            print(f"[Database Error] Query failed: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def fetch_one(self, query, params=None):
        """Fetch a single row from the database."""
        try:
            conn = self.connect()
            if conn is None:
                return None
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"[Database Error] Fetch failed: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        """Fetch all rows from the database."""
        try:
            conn = self.connect()
            if conn is None:
                return []
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"[Database Error] Fetch failed: {e}")
            return []
    
    def create_database(self):
        """Create the database if it doesn't exist."""
        try:
            config_no_db = DB_CONFIG.copy()
            db_name = config_no_db.pop('database')
            conn = pymysql.connect(**config_no_db)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            cursor.close()
            conn.close()
            print(f"[Database] Database '{db_name}' ready.")
            return True
        except Error as e:
            print(f"[Database Error] Cannot create database: {e}")
            return False
    
    def initialize_tables(self):
        """Create all required tables if they don't exist."""
        try:
            conn = self.connect()
            if conn is None:
                return False
            
            cursor = conn.cursor()
            
            # ---- Users Table ----
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    role ENUM('Admin', 'Dentist', 'Staff') NOT NULL DEFAULT 'Staff',
                    is_active TINYINT(1) DEFAULT 1,
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # ---- Patients Table ----
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    gender ENUM('Male', 'Female', 'Other') NOT NULL,
                    birthdate DATE NOT NULL,
                    contact_number VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    medical_history TEXT,
                    date_registered DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # ---- Dentists Table ----
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dentists (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    specialization VARCHAR(100) DEFAULT 'General Dentistry',
                    contact_number VARCHAR(20),
                    email VARCHAR(100),
                    user_id INT,
                    is_active TINYINT(1) DEFAULT 1,
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # ---- Services Table ----
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS services (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    service_name VARCHAR(150) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                    is_active TINYINT(1) DEFAULT 1,
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # ---- Appointments Table ----
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    dentist_id INT NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status ENUM('Scheduled', 'Completed', 'Cancelled', 'No Show') DEFAULT 'Scheduled',
                    notes TEXT,
                    created_by INT,
                    is_archived TINYINT(1) DEFAULT 0,
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
                    FOREIGN KEY (dentist_id) REFERENCES dentists(id) ON DELETE CASCADE,
                    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # ---- Treatments Table ----
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS treatments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    appointment_id INT NOT NULL,
                    service_id INT NOT NULL,
                    tooth_number VARCHAR(10),
                    notes TEXT,
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
                    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # ---- Billings Table ----
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS billings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    appointment_id INT NOT NULL,
                    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                    amount_paid DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                    payment_method ENUM('Cash', 'GCash', 'Card', 'Bank Transfer', 'Other') DEFAULT 'Cash',
                    payment_status ENUM('Paid', 'Partial', 'Unpaid') DEFAULT 'Unpaid',
                    date_paid DATETIME,
                    generated_by INT,
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
                    FOREIGN KEY (generated_by) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            conn.commit()
            
            # ---- Trigger: auto-fill generated_by from MySQL session variable ----
            try:
                cursor = conn.cursor()
                cursor.execute("DROP TRIGGER IF EXISTS trg_billing_set_generated_by")
                cursor.execute("""
                    CREATE TRIGGER trg_billing_set_generated_by
                    BEFORE INSERT ON billings
                    FOR EACH ROW
                    BEGIN
                        IF NEW.generated_by IS NULL THEN
                            SET NEW.generated_by = @app_user_id;
                        END IF;
                    END
                """)
                conn.commit()
                cursor.close()
            except Exception:
                pass
            
            # ---- Migrations for existing databases ----
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "ALTER TABLE appointments ADD COLUMN is_archived TINYINT(1) DEFAULT 0"
                )
                conn.commit()
                cursor.close()
                print("[Database] Added is_archived column to appointments.")
            except Exception:
                pass  # Column already exists
            
            # Add processed_by field to track who processed payments
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "ALTER TABLE billings ADD COLUMN processed_by INT"
                )
                cursor.execute(
                    "ALTER TABLE billings ADD FOREIGN KEY (processed_by) REFERENCES users(id) ON DELETE SET NULL"
                )
                conn.commit()
                cursor.close()
                print("[Database] Added processed_by column to billings.")
            except Exception:
                pass  # Column already exists
            
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "ALTER TABLE billings ADD COLUMN generated_by INT"
                )
                conn.commit()
                cursor.close()
                print("[Database] Added generated_by column to billings.")
            except Exception:
                pass  # Column already exists
            
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "ALTER TABLE billings ADD FOREIGN KEY (generated_by) REFERENCES users(id) ON DELETE SET NULL"
                )
                conn.commit()
                cursor.close()
            except Exception:
                pass  # FK already exists
            
            print("[Database] All tables created successfully.")
            return True
            
        except Error as e:
            print(f"[Database Error] Table creation failed: {e}")
            return False
    
    def insert_default_admin(self):
        """Insert default user accounts if no users exist."""
        import bcrypt
        
        existing = self.fetch_one("SELECT id FROM users LIMIT 1")
        if existing is None:
            default_users = [
                ('admin', 'admin123', 'System', 'Administrator', 'Admin'),
                ('dentist', 'dentist123', 'Juan', 'Dela Cruz', 'Dentist'),
                ('staff', 'staff123', 'Maria', 'Santos', 'Staff'),
            ]
            for username, password, first, last, role in default_users:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                self.execute_query(
                    """INSERT INTO users (username, password_hash, first_name, last_name, role) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (username, password_hash.decode('utf-8'), first, last, role)
                )
            
            # Also create a default dentist profile linked to the dentist user
            dentist_user = self.fetch_one("SELECT id FROM users WHERE username = 'dentist'")
            if dentist_user:
                self.execute_query(
                    """INSERT INTO dentists (first_name, last_name, specialization, contact_number, user_id)
                       VALUES (%s, %s, %s, %s, %s)""",
                    ('Juan', 'Dela Cruz', 'General Dentistry', '09171234567', dentist_user['id'])
                )
            
            print("[Database] Default accounts created successfully.")
        else:
            # Ensure existing dentist users have a linked dentist profile
            self._ensure_dentist_profiles_linked()
    
    def _ensure_dentist_profiles_linked(self):
        """Ensure all users with role 'Dentist' have a linked dentist profile."""
        # Find dentist users without a linked dentist profile
        unlinked_dentists = self.fetch_all("""
            SELECT u.id, u.first_name, u.last_name 
            FROM users u
            LEFT JOIN dentists d ON d.user_id = u.id
            WHERE u.role = 'Dentist' AND u.is_active = 1 AND d.id IS NULL
        """)
        
        for user in unlinked_dentists:
            # Check if a dentist with the same name exists but isn't linked
            existing_dentist = self.fetch_one(
                """SELECT id FROM dentists 
                   WHERE first_name = %s AND last_name = %s AND user_id IS NULL""",
                (user['first_name'], user['last_name'])
            )
            
            if existing_dentist:
                # Link existing dentist record to the user
                self.execute_query(
                    "UPDATE dentists SET user_id = %s WHERE id = %s",
                    (user['id'], existing_dentist['id'])
                )
                print(f"[Database] Linked dentist '{user['first_name']} {user['last_name']}' to their user account.")
            else:
                # Create a new dentist profile for this user
                self.execute_query(
                    """INSERT INTO dentists (first_name, last_name, specialization, contact_number, user_id)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (user['first_name'], user['last_name'], 'General Dentistry', '', user['id'])
                )
                print(f"[Database] Created dentist profile for user '{user['first_name']} {user['last_name']}'.")
    
    def insert_default_services(self):
        """Insert default dental services if none exist."""
        existing = self.fetch_one("SELECT id FROM services LIMIT 1")
        if existing is None:
            default_services = [
                ('Dental Consultation', 'Oral examination and assessment', 300.00),
                ('Tooth Cleaning (Prophylaxis)', 'Scaling and polishing of teeth', 800.00),
                ('Tooth Extraction (Simple)', 'Simple removal of a tooth', 1000.00),
                ('Tooth Extraction (Surgical)', 'Complex removal requiring surgery', 3500.00),
                ('Dental Filling (Composite)', 'Tooth-colored composite filling', 1200.00),
                ('Dental Filling (Amalgam)', 'Silver amalgam filling', 800.00),
                ('Root Canal Treatment', 'Endodontic treatment for infected tooth', 5000.00),
                ('Tooth Whitening / Bleaching', 'Cosmetic teeth whitening', 4000.00),
                ('Dental X-Ray (Periapical)', 'Single tooth X-ray', 350.00),
                ('Panoramic X-Ray', 'Full mouth panoramic X-ray', 800.00),
                ('Dental Crown', 'Cap placed over a damaged tooth', 8000.00),
                ('Dental Bridge', 'Replacement for missing teeth', 12000.00),
                ('Dentures (Complete)', 'Full set of removable false teeth', 15000.00),
                ('Dentures (Partial)', 'Partial removable false teeth', 8000.00),
                ('Orthodontic Braces (Metal)', 'Traditional metal braces', 30000.00),
                ('Retainer', 'Post-braces retainer appliance', 5000.00),
                ('Fluoride Treatment', 'Preventive fluoride application', 500.00),
                ('Pit and Fissure Sealant', 'Preventive sealant per tooth', 600.00),
            ]
            for name, desc, price in default_services:
                self.execute_query(
                    "INSERT INTO services (service_name, description, price) VALUES (%s, %s, %s)",
                    (name, desc, price)
                )
            print("[Database] Default dental services inserted.")
