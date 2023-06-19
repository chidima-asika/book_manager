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
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.Error as e:
        print("Failed to connect to the database:", e)

table_mapping = {
    "book": ("book", "bookId"),
    "review": ("reviews", "reviewId"),
    "book_club": ("book_clubs", "club_name"),
    "author": ("authors", "first_last_name"),
    "genre": ("genres", "name"),
}

# view book for user is from book_user table
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
                    librarian_menu(connection, username)
                else:
                    query = "SELECT * FROM user WHERE username = %s AND password = %s"
                    cursor.execute(query, (username, password))
                    user = cursor.fetchone()

                    if user:
                        print("Logged in as user")
                        user_menu(connection, username)
                    else:
                        print("Invalid credentials")

        except Exception as e:
            print("Error occurred during login:", e)


def librarian_menu(connection, username):
    while True:
        print("Menu:")
        print("1. Books")
        print("2. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            librarian_books_menu(connection,username)
        elif choice == "2":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")


def librarian_books_menu(connection, username):
    while True:
        print("Books Menu:")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. View Book")
        print("4. Go Back")
        choice = input("Enter your choice: ")
        if choice != "1":
            book_id = input("Enter the Book ID: ")

        if choice == "1":
            create_book(connection, username)
        elif choice == "2":
            # delete_book(connection, book_id)
            delete_item(connection, "book", book_id)
        elif choice == "3":
            view_item(connection, "book", book_id)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def create_book(connection, username):
    try:
        with connection.cursor() as cursor:
            title = input("Enter the title: ")
            author = input("Enter the authorID: ")
            
            # Check if the author exists
            query = "SELECT * FROM author WHERE first_last_name = %s"
            cursor.execute(query, (author,))
            result = cursor.fetchone()
            
            if not result:
                print("Author not found in the database. Please create the author before creating a book.")
                return
            
            num_pages = int(input("Enter the number of pages: "))
            publication_year = int(input("Enter the publication year: "))
            book_genre = input("Enter the genre name: ")
            
            # Check if the genre exists
            query = "SELECT * FROM genre WHERE name = %s"
            cursor.execute(query, (book_genre,))
            result = cursor.fetchone()
            
            if not result:
                print("Genre not found in the database. Please create the genre before creating a book.")
                return
            
            librarian_username = username

            # Check if the book already exists
            query = "SELECT * FROM book WHERE title = %s AND author = %s"
            cursor.execute(query, (title, author))
            result = cursor.fetchone()

            if result:
                print("The book already exists in the database.")
                return

            query = "INSERT INTO book (title, author, num_pages, publication_year, book_genre, librarian_username) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (title, author, num_pages, publication_year, book_genre, librarian_username))
            connection.commit()
            print("Book created successfully")
    except Exception as e:
        print("Error occurred while creating the book:", e)



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



def view_item(connection, entity, id):
    table_name, id_column = table_mapping.get(entity)
    if table_name and id_column:
        try:
            with connection.cursor() as cursor:
                query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
                cursor.execute(query, (id,))
                item = cursor.fetchone()

                if item:
                    print("Item Details:")
                    for key, value in item.items():
                        print(f"{key}: {value}")
                else:
                    print("Item not found")
        except Exception as e:
            print("Error occurred while viewing the item:", e)
    else:
        print("Invalid entity. Please try again.")

def delete_item(connection, entity, key):
    table_name, id_column = table_mapping.get(entity)
    if table_name and id_column:
        try:
            with connection.cursor() as cursor:
                query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
                cursor.execute(query, (key,))
                connection.commit()
                print("Item deleted successfully")
        except Exception as e:
            print("Error occurred while deleting the item:", e)
    else:
        print("Invalid entity. Please try again.")


def user_menu(connection, username):
    while True:
        print("Menu:")
        print("1. Books")
        print("2. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_books_menu(connection, username)
        elif choice == "2":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")


def user_books_menu(connection, username):
    while True:
        print("Books Menu:")
        print("1. View Books")
        print("2. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_books(connection, username)
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")


def view_books(connection, username): # change to view  user
    try:
        with connection.cursor() as cursor:
            query = "SELECT book.* FROM book JOIN book_user ON book.bookId = book_user.bookId WHERE book_user.username = %s"
            cursor.execute(query, (username,))
            books = cursor.fetchall()

            if books:
                print("Books:")
                for book in books:
                    print(f"Title: {book['title']}, Author: {book['author']}")
            else:
                print("No books found")

    except Exception as e:
        print("Error occurred while fetching books:", e)


# Call the login function to start the login process
login()
