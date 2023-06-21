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
                        user_menu(connection, username)
                    else:
                        print("Invalid credentials")

        except Exception as e:
            print("Error occurred during login:", e)


def librarian_menu(connection):
    while True:
        print("Menu:")
        print("1. Books")
        print("2. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            librarian_books_menu(connection)
        elif choice == "2":
            print("Logged out")
            break
        else:
            print("Invalid choice. Please try again.")


<<<<<<< Updated upstream
def librarian_books_menu(connection):
=======
def librarian_books_menu(connection, username):
>>>>>>> Stashed changes
    while True:
        print("Books Menu:")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            book_id = input("Enter the Book ID to add: ")
            add_book(connection, book_id)
        elif choice == "2":
            book_id = input("Enter the Book ID to delete: ")
            delete_book(connection, book_id)
        elif choice == "3":
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
<<<<<<< Updated upstream
=======
            view_item(connection, "book", book_id)
        elif choice == "3":
            add_book(connection, username, book_id)
            update_status(connection, username, book_id)
        elif choice == "4":
            view_item(connection, "book_user", username)
        elif choice == "5":
            update_status(connection, username, book_id)
        elif choice == "6":
<<<<<<< Updated upstream
            delete_item(connection, "book_user", book_id)
=======
            delete_book_user(connection, username, book_id)
>>>>>>> Stashed changes
        elif choice == "7":
>>>>>>> Stashed changes
            break
        else:
            print("Invalid choice. Please try again.")


def view_books(connection, username):
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


<<<<<<< Updated upstream
# Call the login function to start the login process
=======
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

        if choice not in ["1", "4"]:
            bc_name = input("Enter Book Club name: ")

        if choice == "1":
            view_item(connection, "book_club")
        elif choice == "2":
            view_item(connection, "book_club", bc_name)
        elif choice == "3":
            view_book_club_members(connection, bc_name) 
        elif choice == "4":
            view_book_club_personal(connection, username) 
        elif choice == "5":
            join_book_club(connection, username, bc_name)
        elif choice == "6":
            leave_book_club(connection, username, bc_name)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

# _______________________ unique user_book_clubs_menu FUNCTIONS _________________________#

def view_book_club_personal(connection, username):
    try:
        with connection.cursor() as cursor:
            query = "SELECT club_name FROM book_club_members WHERE member = %s"
            cursor.execute(query, (username,))
            book_clubs = cursor.fetchall()

            if book_clubs:
                print(f"Books Clubs {username} is a member of:")
                for book_club in book_clubs:
                    print(book_club["club_name"])
            else:
                print("No book clubs found for your username")

    except Exception as e:
        print("Error occurred while fetching book clubs:", e)


def join_book_club(connection, username, bc_name):
    try:
        with connection.cursor() as cursor:
            # Check if the user is already a member of the book club
            query = "SELECT club_name FROM book_club_members WHERE club_name = %s AND member = %s"
            cursor.execute(query, (bc_name, username))
            result = cursor.fetchone()

            if result:
                print("You are already a member of this book club")
            else:
                # Add the user as a member of the book club
                query = "INSERT INTO book_club_members (club_name, member) VALUES (%s, %s)"
                cursor.execute(query, (bc_name, username))
                connection.commit()
                print(f"Joined the book club {bc_name} successfully")

    except Exception as e:
        print("Error occurred while joining the book club:", e)

def leave_book_club(connection, username, bc_name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT club_name FROM book_club_members WHERE club_name = %s AND member = %s"
            cursor.execute(query, (bc_name, username))
            result = cursor.fetchone()

            if result:
                query = "DELETE FROM book_club_members WHERE club_name = %s AND member = %s"
                cursor.execute(query, (bc_name, username))
                connection.commit()
                print(f"Left the book club {bc_name} successfully")
            else:
                print(f"You are not a member of the {bc_name} book club")

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
                    if isinstance(items, dict):  # single item
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
        print("Invalid entity or id. Please try again.")

# =============================================================================
# def view_item2(connection, entity, id):
#     table_name, id_column = table_mapping.get(entity)
#     if table_name and id_column:
#         try:
#             with connection.cursor() as cursor:
#                 query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
#                 cursor.execute(query, (id,))
#                 item = cursor.fetchone()
# 
#                 if item:
#                     print("Item Details:")
#                     for key, value in item.items():
#                         print(f"{key}: {value}")
#                 else:
#                     print("Item not found")
#         except Exception as e:
#             print("Error occurred while viewing the item:", e)
#     else:
#         print("Invalid entity or id. Please try again.")
# =============================================================================

def delete_item(connection, entity, id):
    table_name, id_column = table_mapping.get(entity)
    if table_name and id_column:
        try:
            with connection.cursor() as cursor:
                query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
                cursor.execute(query, (id,))
                connection.commit()
                print("Item deleted successfully")
        except Exception as e:
            print("Error occurred while deleting the item:", e)
    else:
        print("Invalid entity or id. Please try again.")

# _______________________ GENERAL FUNCTIONS END _________________________#

>>>>>>> Stashed changes
login()
