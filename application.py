import pymysql
import getpass


def get_database_credentials():
    db_user = input("Database Username: ")
    db_password = getpass.getpass("Database Password: ")
    return db_user, db_password


def connect_to_database():
    db_host = 'localhost'
    db_name = 'BookManager'

    db_user, db_password = get_database_credentials()

    try:
        connection = pymysql.connect(
            host=db_host, user=db_user, password=db_password, db=db_name, cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.Error as e:
        print("Failed to connect to the database:", e)


table_mapping = {
    "book": ("book", "bookId"),
    "review": ("reviews", "reviewId"),
    "book_club": ("book_club", "club_name"),
    # "book_club_members": ("book_club_members", "member"),
    "author": ("author", "first_last_name"),
    "genre": ("genre", "name"),
    "book_user": ("book_user", "username")
}


def check_existing_user(connection, username):
    with connection.cursor() as cursor:
        # Check if the username already exists in both user and librarian tables
        query = "SELECT username FROM user WHERE username = %s UNION SELECT username FROM librarian WHERE username = %s"
        cursor.execute(query, (username, username))
        existing_user = cursor.fetchone()

        return existing_user is not None


def create_user(connection, user_type):
    
    if user_type == "librarian":
        secret_passphase = input(
                "If you really want to become a librarian, answer this: What powers the words?")
        if secret_passphase in ("Books", "books"):
            pass
        else:
            print("Incorrect!")
            return
    username = input("Enter a new username: ")

    if check_existing_user(connection, username):
        print(
            "Username already exists. Please choose a different username.")
    else:
        password = input("Enter a new password: ")
        first_name = input("Enter the first name: ")
        last_name = input("Enter the last name: ")

        try:
            with connection.cursor() as cursor:
                query = "CALL create_users_proc(%s, %s, %s, %s, %s)"
                cursor.execute(
                    query, (username, password, first_name, last_name, user_type))
                connection.commit()
                print(f"New {user_type} account created successfully")

        except Exception as e:
            print(
                f"Error occurred while creating a new {user_type} account:", e)


def login():
    connection = connect_to_database()

    if connection:
        print("1. Sign In")
        print("2. Create New User Account")
        print("3. Become A Librarian")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")

            try:
                with connection.cursor() as cursor:
                    query = "SELECT * FROM librarian WHERE username = %s AND password = %s"
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

        elif choice == "2":
            create_user(connection, "user")

        elif choice == "3":
            create_user(connection, "librarian")

        else:
            print("Invalid choice")


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
            authors_menu(connection, username)
        elif choice == "4":
            genres_menu(connection, username)
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
        if choice not in ["1", "4", "5"]:
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

# _______________________ unique librarian_books_menu FUNCTIONS _________________________#


def create_book(connection, username):
    try:
        with connection.cursor() as cursor:
            title = input("Enter the title: ")
            author = input("Enter the author's full name: ")

            if not validate_instance_exists(connection, 'author', 'first_last_name', author):
                print(
                    "Author not found in the database. Please create the author before creating a book.")
                return

            book_genre = input("Enter the genre name: ")

            if not validate_instance_exists(connection, 'genre', 'name', book_genre):
                print(
                    "Genre not found in the database. Please create the genre before creating a book.")
                return

            num_pages = int(input("Enter the number of pages: "))
            publication_year = int(input("Enter the publication year: "))

            librarian_username = username

            if validate_instance_exists(connection, 'book', 'title', title):
                print("The book already exists in the database.")
                return

            query = "INSERT INTO book (title, author, num_pages, publication_year, book_genre, librarian_username) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (title, author, num_pages, publication_year, book_genre, librarian_username))
            connection.commit()
            print("Book created successfully")

    except Exception as e:
        print("Error occurred while creating the book:", e)


# _______________________ unique librarian_books_menu FUNCTIONS END _________________________#

def librarian_book_clubs_menu(connection, username):
    while True:
        print("Book Clubs Menu:")
        print("1. Create a Book Club")
        print("2. View a Book Club")
        print("3. View All Book Clubs")
        print("4. View Book Club Members")
        print("5. Delete a Book Club")
        print("6. Go Back")
        choice = input("Enter your choice: ")
        if choice not in ["1", "3", "6"]:
            bc_name = input("Enter Book Club name: ")

        if choice == "1":
            create_book_club(connection, username)
        elif choice == "2":
            view_item(connection, "book_club", bc_name)
        elif choice == "3":
            view_item(connection, "book_club")
        elif choice == "4":
            view_column_items(connection, "member", "book_club_members", "club_name", bc_name)
        elif choice == "5":
            delete_item(connection, "book_club", bc_name)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

# _______________________ unique librarian_book_clubs_menu FUNCTIONS _________________________#


def create_book_club(connection, librarian_username):
    club_name = input("Enter the Book Club name: ")
    book_id = input("Enter the Book ID associated with the Book Club: ")

    try:
        with connection.cursor() as cursor:
            # Perform validation using the validate_instance_exists function
            if validate_instance_exists(connection, 'book_club', 'club_name', club_name):
                print("Book Club already exists")
            else:
                if not validate_instance_exists(connection, 'book', 'bookId', book_id):
                    print("Book does not exist")
                    return

                # Call the stored procedure
                cursor.callproc('create_book_club_proc',
                                (club_name, book_id, librarian_username))
                result = cursor.fetchone()

                if result:
                    print(result["message"])
    except Exception as e:
        print("Error occurred while creating the Book Club:", e)


# _______________________ unique librarian_book_clubs_menu FUNCTIONS END _________________________#


def user_menu(connection, username):
    while True:
        print("Menu:")
        print("1. Books")
        print("2. Reviews")
        print("3. Book Clubs")
        print("4. Authors")
        print("5. Genres")
        print("6. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_books_menu(connection, username)
        elif choice == "2":
            break
            user_reviews_menu(connection, username)
        elif choice == "3":
            user_book_clubs_menu(connection, username)
        elif choice == "4":
            authors_menu(connection, username)
        elif choice == "5":
            genres_menu(connection, username)
        elif choice == "6":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")


def user_books_menu(connection, username):
    while True:
        print("Books Menu:")
        print("1. View All Books")
        print("2. View a Book")
        print("3. Add a Book")
        print("4. View your Books")
        print("5. Update Status of your Book")
        print("6. Delete a book from your Books")
        print("7. Go Back")
        choice = input("Enter your choice: ")

        if choice not in ["1", "4"]:
            book_id = input("Enter book id: ")

        if choice == "1":
            view_item(connection, "book")
        elif choice == "2":
            view_item(connection, "book", book_id)
        elif choice == "3":
            add_book(connection, username, book_id)
            # these can be one function b/c one error should stop function
            update_status(connection, username, book_id)
        elif choice == "4":
            view_item(connection, "book_user", username)  # this is wrong
        elif choice == "5":
            # need to validate that book exists (we should extrapoalte this)
            update_status(connection, username, book_id)
        elif choice == "6":
            # primary key is two values, need delete_item_junction function
            delete_item(connection, "book_user", book_id)
            delete_book_user(connection, username, book_id)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

# _______________________ unique user_books_menu FUNCTIONS _________________________#


def add_book(connection, username, book_id):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO book_user (bookId, username) VALUES (%s, '%')"
            cursor.execute(query, (book_id, username))
            connection.commit()
            print("Book added successfully")

    except Exception as e:
        print("Error occurred while adding the book:", e)


def view_book_user(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM book_user WHERE username = %s"
            cursor.execute(query, (username,))
            books = cursor.fetchall()

            if books:
                print("Your Books:")
                for book in books:
                    print("Book ID:", book["bookId"])
                    print("Status:", book["status"])
                    print("-----")
            else:
                print(f"No books found for {username}")

    except Exception as e:
        print("Error occurred while fetching user books:", e)


# Call the login function to start the login process
def update_status(connection, username, book_id):
    try:
        with connection.cursor() as cursor:
            print("Book Status Options:")
            print("1: Read")
            print("2: Currently Reading")
            print("3: Want to Read")

            book_status = input("Enter your choice: ")

            if book_status == "1":
                status = "Read"
            elif book_status == "2":
                status = "Currently Reading"
            elif book_status == "3":
                status = "Want to Read"
            else:
                print("Invalid choice. Please try again.")
                return

            query = "UPDATE book_user SET status = %s WHERE username = %s AND bookId = %s"
            cursor.execute(query, (status, username, book_id))
            connection.commit()

            if cursor.rowcount > 0:
                print("Status updated successfully")
            else:
                print("No book found for the provided username and book ID")

    except Exception as e:
        print("Error occurred while updating book status:", e)


def delete_book_user(connection, username, book_id):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM book_user WHERE username = %s AND bookId = %s"
            cursor.execute(query, (username, book_id))
            connection.commit()
            print("Book removed from your books successfully")
    except Exception as e:
        print("Error occurred while deleting book:", e)


# _______________________ unique user_books_menu FUNCTIONS END _________________________#

def user_reviews_menu(connection, username):
    while True:
        print("Reviews Menu:")
        print("1. Write a Review for a Book")
        print("2. View All Reviews")
        print("3. View a Review")
        print("4. Update a Review")
        print("5. Delete a Review")
        print("6. Go Back")
        choice = input("Enter your choice: ")

        if choice not in ["2"]:
            book_id = input("Enter Book ID: ")

        if choice == "1":
            write_review(connection, username, book_id)
        elif choice == "2":
            view_item(connection, "reviews")
            view_all_reviews(connection)
        elif choice == "3":
            view_reviews_with_condition(connection)
        elif choice == "4":
            review_id = input("Enter the Review ID: ")
            update_review(connection, username, review_id)
        elif choice == "5":
            book_id = input("Enter the Book ID: ")
            delete_review(connection, username, book_id)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

    # stopped here


# _______________________ unique user_books_menu FUNCTIONS END _________________________#

def user_book_clubs_menu(connection, username):
    while True:
        print("Book Clubs Menu:")
        print("1. View All Book Clubs")
        print("2. View a Book Clubs")
        print("3. View Book Club Members")
        print("4. View your Book Clubs")
        print("5. Join a Book Club")
        print("6. Leave a Book Club")
        print("7. Go Back")
        choice = input("Enter your choice: ")

        if choice not in ["1", "4", "7"]:
            bc_name = input("Enter Book Club name: ")

        if choice == "1":
            view_item(connection, "book_club")
        elif choice == "2":
            view_item(connection, "book_club", bc_name)
        elif choice == "3":
            view_column_items(connection, "member", "book_club_members", "club_name", bc_name)
        elif choice == "4":
            view_column_items(connection, "club_name", "book_club_members", "member", username)
        elif choice == "5":
            join_book_club(connection, username, bc_name)
        elif choice == "6":
            leave_book_club(connection, username, bc_name)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

# _______________________ unique user_book_clubs_menu FUNCTIONS _________________________#


def join_book_club(connection, username, bc_name):
    try:
        with connection.cursor() as cursor:
            # Call the stored procedure
            cursor.callproc('join_book_club_proc', (username, bc_name))

            # Fetch the result message
            result = cursor.fetchone()

            if result:
                print(result['message'])
            else:
                print("Error occurred while joining the book club")
    except Exception as e:
        print("Error occurred while joining the book club:", e)


def leave_book_club(connection, username, bc_name):
    try:
        with connection.cursor() as cursor:
            # Call the stored procedure
            cursor.callproc('leave_book_club_proc', (username, bc_name))

            # Fetch the result message
            result = cursor.fetchone()

            if result:
                print(result['message'])
            else:
                print("Error occurred while leaving the book club")
    except Exception as e:
        print("Error occurred while leaving the book club:", e)


# _______________________ unique user_book_clubs_menu FUNCTIONS END _________________________#


# =============================================================================
# def user_reviews_menu(connection, username):
#     while True:
#         print("Reviews Menu:")
#         print("1. View All Reviews")
#         print("2. View a Review")
#         print("3. Write a Review")
#         choice = input("Enter your choice: ")
#
#         if choice not in ["1", "4"]:
#             bc_name = input("Enter Book Club name: ")
#
#         if choice == "1":
#             view_item(connection, "book_club")
#         elif choice == "2":
#             view_item(connection, "book_club", bc_name)
#         elif choice == "3":
#             view_book_club_members(connection, bc_name)
#         elif choice == "4":
#             view_book_club_personal(connection, username)
#         elif choice == "5":
#             join_book_club(connection, username, bc_name)
#         elif choice == "6":
#             leave_book_club(connection, username, bc_name)
#         elif choice == "7":
#             break
#         else:
#             print("Invalid choice. Please try again.")
# =============================================================================

# _______________________ GENERAL FUNCTIONS _________________________#


def view_item(connection, entity, item_id=None):
    table_name, id_column = table_mapping.get(entity)
    if table_name and id_column:
        try:
            with connection.cursor() as cursor:
                cursor.callproc('view_item_proc', (entity, item_id, id_column))
                results = cursor.fetchall()

            if results:
                print("Item Details:")
                for item in results:
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print("-----")
            else:
                print(f"{entity} not found")
        except Exception as e:
            print("Error occurred while viewing the item:", e)


def view_column_items(connection, select_col, entity, id_column, item_id=None):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('view_column_items_proc',
                            (select_col, entity, id_column, item_id))
            results = cursor.fetchall()

        if results:
            print("Item Details:")
            for item in results:
                for key, value in item.items():
                    print(f"{key}: {value}")
                print("-----")
        else:
            print(f"{entity} not found")
    except Exception as e:
        print("Error occurred while viewing the item:", e)


def delete_item(connection, entity, id):
    table_name, id_column = table_mapping.get(entity)
    if table_name and id_column:
        try:
            with connection.cursor() as cursor:
                cursor.callproc('delete_item_proc', (entity, id, id_column))
                connection.commit()
                print("Item deleted successfully")
        except Exception as e:
            print("Error occurred while deleting the item:", e)
    else:
        print("Invalid entity or id. Please try again.")


def validate_instance_exists(connection, table_name, column_name, value):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
            cursor.execute(query, (value,))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        print("Error occurred while validating instance:", e)
        return False


# _______________________ GENERAL FUNCTIONS END _________________________#

login()
