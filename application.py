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
        print("2. Book Clubs")
        print("3. Authors")
        print("4. Genres")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            librarian_books_menu(connection, username)
        elif choice == "2":
            librarian_book_clubs_menu(connection, username)
        elif choice == "3":
            break
            # librarian_authors_menu(connection)
        elif choice == "4":
            break
            # librarian_genres_menu(connection)
        elif choice == "5":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")



def librarian_books_menu(connection, username):
    while True:
        print("Books Menu:")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. View a Book")
        print("4. View All Books")
        print("5. Go Back")
        choice = input("Enter your choice: ")
        if choice != "1" and choice != "4":
            book_id = input("Enter the Book ID: ")

        if choice == "1":
            create_book(connection, username)
        elif choice == "2":
            delete_item(connection, "book", book_id)
        elif choice == "3":
            view_item(connection, "book", book_id)
        elif choice == "4":
            view_item(connection, "book")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

# _______________________ llibrarian_books_menu FUNCTIONS _________________________#

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

# _______________________ llibrarian_books_menu FUNCTIONS END _________________________#

def librarian_book_clubs_menu(connection, username):
    while True:
        print("Book Clubs Menu:")
        print("1. Create a Book Club")
        print("2. View a Book Clubs")
        print("3. View All Book Clubs")
        print("4. View Book Club Members")
        print("5. Delete a Book Club")
        print("6. Go Back")
        choice = input("Enter your choice: ")
        if choice != 1:
            bc_name = input("Enter Bookclub ID: ")

        if choice == "1":
            create_book_club(connection, username)
        elif choice == "2":
            view_item(connection, "bookclub", bc_name)
        elif choice == "3":
            view_item(connection, "bookclub")
        elif choice == "4":
            view_book_club_members(connection, bc_name)
        elif choice == "5":
            delete_item(connection, "bookclub", bc_name)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

# _______________________ librarian_book_clubs_menu FUNCTIONS _________________________#

def create_book_club(connection, librarian_username):
    club_name = input("Enter the Book Club name: ")
    book_id = input("Enter the Book ID associated with the Book Club: ")

    try:
        with connection.cursor() as cursor:
            # Check if the book club already exists
            query = "SELECT club_name FROM book_club WHERE club_name = %s"
            cursor.execute(query, (club_name,))
            existing_club = cursor.fetchone()

            if existing_club:
                print("Book Club already exists")
            else:
                query = "INSERT INTO book_club (club_name, bookId, librarian) VALUES (%s, %s, %s)"
                cursor.execute(query, (club_name, book_id, librarian_username))
                connection.commit()
                print("Book Club created successfully")
    except Exception as e:
        print("Error occurred while creating the Book Club:", e)

def view_book_club_members(connection, club_name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT member FROM book_club_members WHERE club_name = %s"
            cursor.execute(query, (club_name,))
            members = cursor.fetchall()

            if members:
                print("Book Club Members:")
                for member in members:
                    print(member["member"])
            else:
                print(f"No members found for the Book Club: {club_name}")

    except Exception as e:
        print("Error occurred while fetching book club members:", e)

# _______________________ librarian_book_clubs_menu FUNCTIONS END _________________________#

# def add_book(connection, book_id):
#     try:
#         with connection.cursor() as cursor:
#             query = "INSERT INTO book_user (bookId, username, status) VALUES (%s, 'librarian', 'unread')"
#             cursor.execute(query, (book_id,))
#             connection.commit()
#             print("Book added successfully")

#     except Exception as e:
#         print("Error occurred while adding the book:", e)

# _______________________ GENERAL FUNCTION _________________________#
def view_item(connection, entity, id=None):
    table_name, id_column = table_mapping.get(entity)
    if table_name and id_column:
        try:
            with connection.cursor() as cursor:
                if id is None:
                    query = f"SELECT * FROM {table_name}"
                    cursor.execute(query)
                    items = cursor.fetchall()
                else:
                    query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
                    cursor.execute(query, (id,))
                    items = cursor.fetchone()

                if items:
                    print("Item Details:")
                    if isinstance(items, dict):  # Single item
                        items = [items]
                    for item in items:
                        for key, value in item.items():
                            print(f"{key}: {value}")
                        print("-----")
                else:
                    print("Item not found")
        except Exception as e:
            print("Error occurred while viewing the item:", e)
    else:
        print("Invalid entity. Please try again.")


def view_item2(connection, entity, id):
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

# _______________________ GENERAL FUNCTION END _________________________#

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
