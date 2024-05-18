import sqlite3

def create_or_open_database():
    # Connect to the SQLite database. If it doesn't exist, it will be created.
    conn = sqlite3.connect('users.db')
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Create table as per requirement
    sql = '''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    '''
    cursor.execute(sql)
    conn.commit()
    return conn

def add_user_to_database(conn, username, password):
    try:
        # SQL command to insert the data in the users table
        sql = "INSERT INTO users (username, password) VALUES (?, ?);"
        # Execute the SQL command
        conn.execute(sql, (username, password))
        # Commit changes in the database
        conn.commit()
        print(f"User {username} added successfully.")
    except sqlite3.IntegrityError:
        print("Error: That username already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Create or open database
    conn = create_or_open_database()
    # Input from user
    username = input("Enter username: ")
    password = input("Enter password: ")
    # Add user to the database
    add_user_to_database(conn, username, password)
    # Closing the connection
    conn.close()

if __name__ == "__main__":
    main()
