import pymysql
import getpass


def get_database_credentials():
    db_user = input("Database Username: ")
    db_password = getpass.getpass("Database Password: ")
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
                    librarian_menu(connection)
                else:
                    query = "SELECT * FROM user WHERE username = %s AND password = %s"
                    cursor.execute(query, (username, password))
                    user = cursor.fetchone()

                    if user:
                        print("Logged in as user")
                        user_menu(connection)
                    else:
                        print("Invalid credentials")

        except Exception as e:
            print("Error occurred during login:", e)


def librarian_menu(connection):
    while True:
        print("Menu:")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            book_id = input("Enter the Book ID to add: ")
            add_book(connection, book_id)
        elif choice == "2":
            book_id = input("Enter the Book ID to delete: ")
            delete_book(connection, book_id)
        elif choice == "3":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")


def add_book(connection, book_id):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO book_user (bookId, username, status) VALUES (%s, 'librarian', 'unread')"
            cursor.execute(query, (book_id,))
            connection.commit()
            print("Book added successfully")

    except Exception as e:
        print("Error occurred while adding the book:", e)


def delete_book(connection, book_id):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM book_user WHERE bookId = %s"
            cursor.execute(query, (book_id,))
            connection.commit()
            print("Book deleted successfully")

    except Exception as e:
        print("Error occurred while deleting the book:", e)


def user_menu(connection):
    while True:
        print("Menu:")
        print("1. View Books")
        print("2. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_books(connection)
        elif choice == "2":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")


def view_books(connection):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM book_user"
            cursor.execute(query)
            books = cursor.fetchall()

            if books:
                print("Books:")
                for book in books:
                    print(f"Book ID: {book['bookId']}")
            else:
                print("No books found")

    except Exception as e:
        print("Error occurred while fetching books:", e)


# Call the login function to start the login process
login()
