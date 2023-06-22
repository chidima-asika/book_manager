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
    "book_user": ("book_user", "username"),
    "user": ("user", "username")
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

## ________________________ LIBRARIAN FUNCTIOANLITY  ________________________ ##


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
            librarian_author_menu(connection, username)
        elif choice == "4":
            librarian_genre_menu(connection, username)
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
            num_pages = int(input("Enter the number of pages: "))
            publication_year = int(input("Enter the publication year: "))
            author = input("Enter the author's full name: ")
            book_genre = input("Enter the genre name: ")
            librarian_username = username

            if not validate_instance_exists(connection, 'author', 'first_last_name', author):
                print("Author not found in the database. Please create the author before creating a book.")
                return

            if not validate_instance_exists(connection, 'genre', 'name', book_genre):
                print("Genre not found in the database. Please create the genre before creating a book.")
                return

            if validate_instance_exists(connection, 'book', 'title', title):
                print("The book already exists in the database.")
                return

            cursor.callproc('create_book', (title, num_pages, publication_year, author, book_genre, librarian_username))
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


def librarian_author_menu(connection, username):
    while True:
        print("Authors Menu:")
        print("1. View an Author")
        print("2. View All Authors")
        print("3. Add New Author")
        print("4. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            author_name = input("Enter the author's name: ")
            view_item(connection, "author", author_name)
        elif choice == "2":
            view_item(connection, "author")
        elif choice == "3":
            create_author(connection)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

# _______________________ unique librarian_author_menu FUNCTIONS  _________________________#

def create_author(connection):
    try:
        with connection.cursor() as cursor:
            author_name = input("Enter the author's full name: ")

            if validate_instance_exists(connection, 'author', 'first_last_name', author_name):
                print("Author already exists in the database.")
                return

            cursor.callproc('create_author', (author_name,))
            connection.commit()
            print("Author created successfully")

    except Exception as e:
        print("Error occurred while creating the author:", e)

# _______________________ unique librarian_author_menu FUNCTIONS END _________________________#


def librarian_genre_menu(connection):
    while True:
        print("Genres Menu:")
        print("1. View a Genre")
        print("2. View All Genres")
        print("3. Add New Genre")
        print("4. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            genre_name = input("Enter the genre name: ")
            view_item(connection, "genre", genre_name)
        elif choice == "2":
            view_item(connection, "genre")
        elif choice == "3":
            create_genre(connection)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

# _______________________ unique librarian_genre_menu FUNCTIONS  _________________________#

def create_genre(connection):
    try:
        with connection.cursor() as cursor:
            genre_name = input("Enter the genre name: ")

            if validate_instance_exists(connection, 'genre', 'name', genre_name):
                print("Genre already exists in the database.")
                return

            description = input("Enter the genre description: ")

            cursor.callproc('create_genre', (genre_name, description))
            connection.commit()
            print("Genre created successfully")

    except Exception as e:
        print("Error occurred while creating the genre:", e)


# _______________________ unique librarian_genre_menu FUNCTIONS END _________________________#

## ________________________ LIBRARIAN FUNCTIOANLITY END ________________________ ##

## ____________________________ USER FUNCTIOANLITY ____________________________ ##


def user_menu(connection, username):
    while True:
        print("Menu:")
        print("1. Books")
        print("2. Reviews")
        print("3. Book Clubs")
        print("4. Authors")
        print("5. Genres")
        print("6. Users")
        print("7. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_books_menu(connection, username)
        elif choice == "2":
            user_reviews_menu(connection, username)
        elif choice == "3":
            user_book_clubs_menu(connection, username)
        elif choice == "4":
            user_author_menu(connection, username)
        elif choice == "5":
            user_genre_menu(connection, username)
        elif choice == "6":
            other_users_menu(connection, username)
        elif choice == "7":
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
            if add_book(connection, username, book_id):
                update_status(connection, username, book_id)
        elif choice == "4":
            view_item(connection, "book_user", username)
        elif choice == "5":
            update_status(connection, username, book_id)
        elif choice == "6":
            # delete_item_junction here
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
            query = "INSERT INTO book_user (bookId, username) VALUES (%s, %s)"
            cursor.execute(query, (book_id, username))
            connection.commit()
            print("Book added successfully")
            return True

    except Exception as e:
        print("Error occurred while adding the book:", e)
        return False


# Call the login function to start the login process
def update_status(connection, username, book_id):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM book_user WHERE username = %s AND bookId = %s"
            cursor.execute(query, (username, book_id))
            result = cursor.fetchone()

            if result is None:
                print("No book found for the provided username and book ID.")
                print("Please add the book before updating the status.")
                return

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

            cursor.callproc('update_status', (status, username, book_id))
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


def user_author_menu(connection, username):
    while True:
        print("Authors Menu:")
        print("1. View an Author")
        print("2. View All Authors")
        print("3. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            author_name = input("Enter the author's name: ")
            view_item(connection, "author", author_name)
        elif choice == "2":
            view_item(connection, "author")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            
            
def user_genre_menu(connection):
    while True:
        print("Genres Menu:")
        print("1. View a Genre")
        print("2. View All Genres")
        print("3. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            genre_name = input("Enter the genre name: ")
            view_item(connection, "genre", genre_name)
        elif choice == "2":
            view_item(connection, "genre")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


def user_reviews_menu(connection, username):
    while True:
        print("Reviews Menu:")
        print("1. Write a Review for a Book")
        print("2. View All Reviews")
        print("3. View a Review")
        print("4. Delete a Review")
        print("5. Go Back")
        choice = input("Enter your choice: ")

        if choice in ["1"]:
            book_id = input("Enter Book ID: ")
        elif choice in ["3", "4"]:
            review_id = input("Enter Review ID: ")

        if choice == "1":
            create_review(connection, username, book_id)
        elif choice == "2":
            view_item(connection, "reviews")
        elif choice == "3":
            view_item(connection, "rewiews", review_id)
        elif choice == "4":
            break
            # delete_item_junction here
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


# _______________________ unique user_reviews_menu FUNCTIONS  _________________________#

def create_review(connection, username, book_id):
    try:
        with connection.cursor() as cursor:
            while True:
                rating = int(input("Enter a rating (1-5): "))
                if rating < 1 or rating > 5:
                    print("Invalid rating. Please enter a number between 1 and 5.")
                else:
                    break

            description = input("Enter a description for the review: ")

            cursor.callproc('create_review', (rating, description, book_id, username))
            connection.commit()

            print("Review added successfully")

    except Exception as e:
        print("Error occurred while writing the review:", e)

# _______________________ unique user_reviews_menu FUNCTIONS END _________________________#


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

def other_users_menu(connection, username):
    while True:
        print("Other Users Menu:")
        print("1. View All Users")
        print("2. View Users You Follow")
        print("3. View Users Who Follow You")
        print("4. View Number of Users You Follow")
        print("5. View Number of Followers")
        print("7. Unfollow a User")
        print("8. Go Back")
        choice = input("Enter your choice: ")

        if choice in ["5", "6"]:
            second_username = input("Enter the user's username: ")

            if second_username == username:
                print("Cannot enter your own username. Please try again.")
                return

            if not validate_instance_exists(connection, 'users', 'username', second_username):
                print("User does not exist. Please try again.")
                return

        if choice == "1":
            view_item(connection)
        elif choice == "2":
            view_column_items(connection, "following_username", "user_follows_user", "username", item_id=username)
        elif choice == "3":
            view_column_items(connection, "username", "user_follows_user", "following_username", item_id=username)
        elif choice == "4":
            view_column_items(connection, "num_folowing", "user", "username", item_id=username)
        elif choice == "5":
            view_column_items(connection, "num_followers", "user", "username", item_id=username)
        elif choice == "6":
            follow_user(connection, username, second_username)
        elif choice == "7":
            unfollow_user(connection, username, second_username)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

#_____________________  unique other_users_menu FUNCTIONS _____________________# 

def follow_user(connection, username, second_username):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('follow_user_proc', (username, second_username))
            connection.commit()
            print(f"You are now following {second_username}")
    except Exception as e:
        print("Error occurred while following the user:", e)
        
        
def unfollow_user(connection, username, second_username):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('unfollow_user_proc', (username, second_username))
            connection.commit()
            print(f"You have unfollowed {second_username}")
    except Exception as e:
        print("Error occurred while unfollowing the user:", e)

#_____________________  unique other_users_menu FUNCTIONS END _____________________# 


## __________________________ USER FUNCTIOANLITY END __________________________ ##


# _______________________ GENERAL FUNCTIONS _________________________#


def view_item(connection, entity, item_id=None):
    table_name, id_column = table_mapping.get(entity)
    if table_name and id_column:
        try:
            with connection.cursor() as cursor:
                cursor.callproc('view_item_proc', (entity, id_column, item_id))
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
# need to add validation that the entity exists


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

def delete_item_junction(connection, table_name, key1_name, key1_value, key2_name, key2_value, key3_name=None, key3_value=None):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('delete_item_junction', (table_name, key1_name, key1_value, key2_name, key2_value, key3_name, key3_value))
            result = cursor.fetchone()
            if result:
                print(result["message"])
            else:
                print("Deletion failed")

    except Exception as e:
        print("Error occurred while deleting the item:", e)



# _______________________ GENERAL FUNCTIONS END _________________________#

login()
