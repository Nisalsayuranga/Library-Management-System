import mysql.connector

def update_db():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="library_system")
        cursor = conn.cursor()
        
        try:
            cursor.execute("ALTER TABLE members ADD COLUMN email VARCHAR(150) DEFAULT ''")
            print("Added email to members")
        except Exception as e:
            print("Column email might exist.", e)
            
        try:
            cursor.execute("ALTER TABLE books ADD COLUMN quantity INT DEFAULT 1")
            print("Added quantity to books")
        except Exception as e:
            print("Column quantity might exist.", e)

        conn.commit()
        conn.close()
        print("Database updated completely!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    update_db()
