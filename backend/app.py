from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
# Enable CORS to allow requests from frontend
CORS(app)

# Environment variables with sensible defaults
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpassword")
DB_NAME = os.getenv("DB_NAME", "calculator_db")

def get_db_connection():
    """Helper function to attempt MySQL connection with retries"""
    for attempt in range(5):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Database connection attempt {attempt + 1} failed: {err}")
            time.sleep(2)
    return None

def init_db():
    """Create database and calculations table on startup"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calculations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                num1 DOUBLE NOT NULL,
                num2 DOUBLE NOT NULL,
                operator VARCHAR(5) NOT NULL,
                result DOUBLE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and table verified successfully.")
    except mysql.connector.Error as err:
        print(f"Error during database initialization: {err}")

# --- Root Route (Fixes 404 on http://localhost:5000) ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "healthy",
        "service": "calculator-backend",
        "endpoints": {
            "root": "/",
            "calculate": "/calculate (POST)",
            "history": "/history (GET)"
        }
    })

# --- Calculation Route ---
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'num1' not in data or 'num2' not in data or 'operator' not in data:
        return jsonify({"error": "Invalid input data"}), 400

    try:
        n1 = float(data['num1'])
        n2 = float(data['num2'])
        op = data['operator']
    except (ValueError, TypeError):
        return jsonify({"error": "Numbers must be numeric"}), 400

    res = 0.0
    if op == '+':
        res = n1 + n2
    elif op == '-':
        res = n1 - n2
    elif op == '*':
        res = n1 * n2
    elif op == '/':
        if n2 == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400
        res = n1 / n2
    else:
        return jsonify({"error": "Unsupported operator"}), 400

    # Save calculation result to MySQL
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO calculations (num1, num2, operator, result) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (n1, n2, op, res))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Failed to insert calculation: {err}")

    return jsonify({"result": res})

# --- History Route ---
@app.route('/history', methods=['GET'])
def get_history():
    conn = get_db_connection()
    if not conn:
        return jsonify([])

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT num1, num2, operator, result, created_at FROM calculations ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except mysql.connector.Error as err:
        print(f"Failed to fetch history: {err}")
        return jsonify([])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)