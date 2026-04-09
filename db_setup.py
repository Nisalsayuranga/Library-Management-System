import mysql.connector

def setup_database():
    try:
        # Connect to MySQL (Assuming XAMPP defaults: root, no password)
        print("Connecting to MySQL...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        
        # 1. Create Database
        cursor.execute("CREATE DATABASE IF NOT EXISTS library_system")
        print("[OK] Database 'library_system' created or already exists.")
        
        # Use the DB
        cursor.execute("USE library_system")
        
        # 2. Create Admin Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        
        # Insert default admin if table is empty
        cursor.execute("SELECT * FROM admin WHERE username='admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin123')")
            print("[OK] Default Admin created.")
            
        # 3. Create Books Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'Available',
                added_date DATE
            )
        """)
        
        # 4. Create Members Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                address TEXT NOT NULL,
                joined_date DATE
            )
        """)
        
        # 5. Create Issue Records (Transactions) Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issue_records (
                issue_id INT AUTO_INCREMENT PRIMARY KEY,
                book_id INT,
                member_id INT,
                issue_date DATE,
                due_date DATE,
                return_date DATE NULL,
                fine INT DEFAULT 0,
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            )
        """)
        
        conn.commit()
        print("[OK] All tables created successfully!")
        print("\n[SUCCESS] Database setup is complete!")
        print("-> Default Login -> Username: admin | Password: admin123")
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        print("කරුණාකර XAMPP හි MySQL ක්‍රියාත්මක (Start) කර ඇති දැයි තහවුරු කරගන්න.")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
