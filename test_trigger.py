import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import Database
db = Database()
# Reset singleton state for clean test
db.connection = None 
db.current_user_id = None
db.connect()
db.initialize_tables()
db.set_user(3)
# Insert with NULL generated_by - trigger should fill it
bill_id = db.execute_query(
    'INSERT INTO billings (appointment_id, total_amount, balance, payment_status, generated_by) VALUES (%s, %s, %s, %s, %s)',
    (6, 100, 100, 'Unpaid', None)
)
result = db.fetch_one('SELECT id, generated_by FROM billings WHERE id = %s', (bill_id,))
print(f"TRIGGER TEST: generated_by = {result['generated_by']} (expected 3)")
db.execute_query('DELETE FROM billings WHERE id = %s', (bill_id,))
if result['generated_by'] == 3:
    print("SUCCESS - Trigger works!")
else:
    print("FAIL - Trigger did not fill generated_by")
