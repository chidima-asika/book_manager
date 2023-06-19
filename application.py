import pymysql

def get_database_credentials():
    db_user = input("Database Username: ")
    db_password = input("Database Password: ")
    return db_user, db_password

# Establish a connection to the database
def connect_to_database():
    db_host = 'localhost'
    db_name = 'BookManager'

    db_user, db_password = get_database_credentials()

    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)
        return connection
    except pymysql.Error as e:
        print("Failed to connect to the database:", e)

def login():
    connection = connect_to_database()

    if connection:
        username = input("Username: ")
        password = input("Password: ")

        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM librarian WHERE lib_username = %s AND password = %s"
                cursor.execute(query, (username, password))
                librarian = cursor.fetchone()

                if librarian:
                    print("Logged in as librarian")
                    librarian_menu()
                else:
                    query = "SELECT * FROM user WHERE username = %s AND password = %s"
                    cursor.execute(query, (username, password))
                    user = cursor.fetchone()

                    if user:
                        print("Logged in as user")
                        user_menu(user['username'])
                    else:
                        print("Invalid credentials")
        
        except Exception as e:
            print("Error occurred during login:", e)

def librarian_menu():
    while True:
        print("Menu:")
        print("1. Delete Book")
        print("2. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            book_id = input("Enter the Book ID to delete: ")
            delete_book(book_id)
        elif choice == "2":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")

def delete_book(book_id):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM book_user WHERE bookId = %s"
            cursor.execute(query, (book_id,))
            connection.commit()
            print("Book deleted successfully")
    
    except Exception as e:
        print("Error occurred while deleting the book:", e)

def user_menu(username):
    while True:
        print("Menu:")
        print("1. Add Book")
        print("2. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            book_id = input("Enter the Book ID to add: ")
            add_book(book_id, username)
        elif choice == "2":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")

def add_book(book_id, username):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO book_user (bookId, username, status) VALUES (%s, %s, 'unread')"
            cursor.execute(query, (book_id, username))
            connection.commit()
            print("Book added successfully")
    
    except Exception as e:
        print("Error occurred while adding the book:", e)

login()
