DROP DATABASE IF EXISTS BookManager;
CREATE DATABASE IF NOT EXISTS BookManager;

USE BookManager;

-- need to add PK some of these have non
-- Need to add deletion contraints depending on the entity 
-- need to add ability to create users
-- remove active column from book club


DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS librarian;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS book_club;
DROP TABLE IF EXISTS book_user;
DROP TABLE IF EXISTS book_club_members;
DROP TABLE IF EXISTS user_follows_user;
DROP TABLE IF EXISTS user_review_book;

CREATE TABLE user
(
	username VARCHAR(30) PRIMARY KEY,
    password VARCHAR(30) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    num_followers INT DEFAULT 0,
    num_following INT DEFAULT 0
);

CREATE TABLE librarian
(
	username VARCHAR(30) PRIMARY KEY,
    password VARCHAR(30) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

CREATE TABLE genre
(
	name VARCHAR(100) PRIMARY KEY,
    description VARCHAR(500) DEFAULT NULL,
	num_books INT DEFAULT 1

);

CREATE TABLE author
(
	first_last_name VARCHAR(100) PRIMARY KEY,
	num_books INT DEFAULT 1

);

CREATE TABLE book
(
	bookId INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    num_pages INT NOT NULL,
    publication_year YEAR NOT NULL,
    num_reviews INT DEFAULT 0,
    ave_rating DECIMAL(3, 2) DEFAULT NULL,
    author VARCHAR(100) NOT NULL,
    book_genre VARCHAR(100) NOT NULL,
    librarian_username VARCHAR(30),

    UNIQUE(title,author),
	FOREIGN KEY (book_genre) REFERENCES genre (name) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (author) REFERENCES author (first_last_name) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (librarian_username) REFERENCES librarian (username) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE reviews
(
	reviewId INT AUTO_INCREMENT PRIMARY KEY,
    rating INT NOT NULL,
    description VARCHAR(500) DEFAULT NULL
    
);

CREATE TABLE book_club
(
    club_name VARCHAR(100) PRIMARY KEY,
    active TINYINT(1) DEFAULT 1,
    bookId INT,
    librarian VARCHAR(30),
    num_members INT DEFAULT 0,

	FOREIGN KEY (bookId) REFERENCES book (bookId) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (librarian) REFERENCES librarian (username) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE book_user
(
	bookId INT,
    username VARCHAR(30),
    status VARCHAR(30) DEFAULT NULL,
    
    PRIMARY KEY (bookId, username),
    
    FOREIGN KEY (bookId) REFERENCES book (bookId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES user (username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE book_club_members
(
	club_name VARCHAR(100),
    member VARCHAR(30),
    
    PRIMARY KEY (club_name, member),
    FOREIGN KEY (club_name) REFERENCES book_club (club_name) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (member) REFERENCES user (username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE user_follows_user (
    username VARCHAR(30),
    following_username VARCHAR(30),
    
    PRIMARY KEY (username, following_username),
    FOREIGN KEY (username) REFERENCES user (username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (following_username) REFERENCES user (username) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE user_review_book
(
	bookId INT,
    username VARCHAR(30),
    reviewId INT,
    
    PRIMARY KEY (bookId, username, reviewId),
    FOREIGN KEY (bookId) REFERENCES book (bookId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES user (username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (reviewId) REFERENCES reviews (reviewId) ON UPDATE CASCADE ON DELETE CASCADE
);


---------------------------------- TRIGGERRS ----------------------------------
-- update counter variables (num_following, num_books, num_members, etc.)


-- DELIMITER //

-- DROP TRIGGER IF EXISTS update_num_books_insert;
-- CREATE TRIGGER update_num_books_insert AFTER INSERT ON book
-- FOR EACH ROW
-- BEGIN
--     DECLARE author_name VARCHAR(100);
--     DECLARE genre_name VARCHAR(100);
    
--     SET author_name = NEW.author;
--     SET genre_name = NEW.book_genre;
    
--     IF author_name IS NOT NULL THEN
--         UPDATE author SET num_books = num_books + 1 WHERE first_last_name = author_name;
--     END IF;
    
--     IF genre_name IS NOT NULL THEN
--         UPDATE genre SET num_books = num_books + 1 WHERE name = genre_name;
--     END IF;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- DROP TRIGGER IF EXISTS update_num_books_delete;
-- CREATE TRIGGER update_num_books_delete AFTER DELETE ON book
-- FOR EACH ROW
-- BEGIN
--     DECLARE author_name VARCHAR(100);
--     DECLARE genre_name VARCHAR(100);
    
--     SET author_name = OLD.author;
--     SET genre_name = OLD.book_genre;
    
--     IF author_name IS NOT NULL THEN
--         UPDATE author SET num_books = num_books - 1 WHERE first_last_name = author_name;
--     END IF;
    
--     IF genre_name IS NOT NULL THEN
--         UPDATE genre SET num_books = num_books - 1 WHERE name = genre_name;
--     END IF;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- DROP TRIGGER IF EXISTS update_num_following_insert;
-- CREATE TRIGGER update_num_following_insert AFTER INSERT ON user_follows_user
-- FOR EACH ROW
-- BEGIN
--     -- update num_following for the user who initiated the follow
--     UPDATE user SET num_following = num_following + 1 WHERE username = NEW.username;
    
--     -- update num_followers for the user who is being followed
--     UPDATE user SET num_followers = num_followers + 1 WHERE username = NEW.following_username;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- DROP TRIGGER IF EXISTS update_num_following_delete;
-- CREATE TRIGGER update_num_following_delete AFTER DELETE ON user_follows_user
-- FOR EACH ROW
-- BEGIN
--     -- update num_following for the user who initiated the follow
--     UPDATE user SET num_following = num_following - 1 WHERE username = OLD.username;
    
--     -- update num_followers for the user who is being followed
--     UPDATE user SET num_followers = num_followers - 1 WHERE username = OLD.following_username;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- DROP TRIGGER IF EXISTS update_book_review_info_insert;
-- CREATE TRIGGER update_book_review_info_insert AFTER INSERT ON user_review_book
-- FOR EACH ROW
-- BEGIN
    
--     UPDATE book
--     SET num_reviews = (SELECT COUNT(*) FROM user_review_book WHERE bookId = NEW.bookId)
--     WHERE bookId = NEW.bookId;
    
--     UPDATE book
--     SET ave_rating =
--         (SELECT IFNULL(SUM(reviews.rating) / book.num_reviews, NULL)
--         FROM reviews
--         JOIN user_review_book ON reviews.reviewId = user_review_book.reviewId
--         WHERE user_review_book.bookId = NEW.bookId)
--     WHERE bookId = NEW.bookId;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- DROP TRIGGER IF EXISTS update_book_review_info_delete;
-- CREATE TRIGGER update_book_review_info_delete AFTER DELETE ON user_review_book
-- FOR EACH ROW
-- BEGIN
    
--     UPDATE book
--     SET num_reviews = (SELECT COUNT(*) FROM user_review_book WHERE bookId = OLD.bookId)
--     WHERE bookId = OLD.bookId;
    
--     UPDATE book
--     SET ave_rating =
--         (SELECT IFNULL(SUM(reviews.rating) / book.num_reviews, NULL)
--         FROM reviews
--         JOIN user_review_book ON reviews.reviewId = user_review_book.reviewId
--         WHERE user_review_book.bookId = OLD.bookId)
--     WHERE bookId = OLD.bookId;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- DROP TRIGGER IF EXISTS update_num_members_insert;
-- CREATE TRIGGER update_num_members_insert AFTER INSERT ON book_club_members
-- FOR EACH ROW
-- BEGIN
    
--     UPDATE book_club
--     SET num_members = (SELECT COUNT(*) FROM book_club_members WHERE club_name = NEW.club_name)
--     WHERE club_name = NEW.club_name;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- DROP TRIGGER IF EXISTS update_num_members_delete;
-- CREATE TRIGGER update_num_members_delete AFTER DELETE ON book_club_members
-- FOR EACH ROW
-- BEGIN

--     UPDATE book_club
--     SET num_members = (SELECT COUNT(*) FROM book_club_members WHERE club_name = OLD.club_name)
--     WHERE club_name = OLD.club_name;
-- END //

-- DELIMITER ;

-- ------------------------------TRIGGERRS END --------------------------------



-- ------------------------------ STORED PROCEDURES ------------------------------ 



-- ---------------------------- STORED PROCEDURES END ----------------------------

-- create_users_libs

DELIMITER //

CREATE PROCEDURE create_users_proc(
    IN username_p VARCHAR(30),
    IN password_p VARCHAR(30),
    IN first_name_p VARCHAR(30),
    IN last_name_p VARCHAR(30),
    IN user_type_p VARCHAR(30)
)
BEGIN
    DECLARE query VARCHAR(500);

    IF user_type_p = 'librarian' THEN
        SET @query = CONCAT('INSERT INTO librarian (username, password, first_name, last_name) VALUES (''', username_p, ''', ''', password_p, ''', ''', first_name_p, ''', ''', last_name_p, ''')');
    ELSE
        SET @query = CONCAT('INSERT INTO user (username, password, first_name, last_name) VALUES (''', username_p, ''', ''', password_p, ''', ''', first_name_p, ''', ''', last_name_p, ''')');
    END IF;

    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

DELIMITER ;


-- create_users_lib END


-- librarian_bookclub_menu
-- librarian_bookclub_menu END

-- librarian_books_menu
-- librarian_books_menu END

-- librarian_author_menu

DELIMITER //
CREATE PROCEDURE create_author(
    IN p_author_name VARCHAR(100)
)
BEGIN
    INSERT INTO author (first_last_name)
    VALUES (p_author_name);
END //
DELIMITER ;


-- librarian_author_menu END




-- librarian_bookclub_menu
DELIMITER //

CREATE PROCEDURE create_book_club_proc(
    IN club_name VARCHAR(100),
    IN book_id VARCHAR(100),
    IN librarian_username VARCHAR(30)
)
BEGIN
    -- Insert the Book Club
    INSERT INTO book_club (club_name, bookId, librarian)
    VALUES (club_name, book_id, librarian_username);

    SELECT 'Book Club created successfully' AS message;
END //

DELIMITER ;

-- librarian_bookclub_menu END

-- endn_bookclub_menu

DELIMITER //

CREATE PROCEDURE join_book_club_proc(IN username VARCHAR(30), IN bc_name VARCHAR(100))
BEGIN
    DECLARE is_member INT;
    
    -- Check if the user is already a member of the book club
    SELECT COUNT(*) INTO is_member
    FROM book_club_members
    WHERE club_name = bc_name AND member = username;

    IF is_member > 0 THEN
        SELECT 'You are already a member of this book club' AS 'message';
    ELSE
        -- Insert the user as a member of the book club
        INSERT INTO book_club_members (club_name, member)
        VALUES (bc_name, username);
        
        SELECT CONCAT('Joined the book club ', bc_name, ' successfully') AS 'message';
    END IF;
    
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE leave_book_club_proc(IN username VARCHAR(30), IN bc_name VARCHAR(100))
BEGIN
    DECLARE is_member INT;

    -- Check if the user is a member of the book club
    SELECT COUNT(*) INTO is_member
    FROM book_club_members
    WHERE club_name = bc_name AND member = username;

    IF is_member > 0 THEN
        -- Remove the user from the book club
        DELETE FROM book_club_members
        WHERE club_name = bc_name AND member = username;
        
        SELECT CONCAT('Left the book club ', bc_name, ' successfully') AS 'message';
    ELSE
        SELECT CONCAT('You are not a member of the ', bc_name, ' book club or book club does not exist') AS 'message';
    END IF;
    
END //

DELIMITER ;


-- end_bookclub_menu END

DELIMITER //

CREATE PROCEDURE update_status(
    IN p_status VARCHAR(20),
    IN p_username VARCHAR(30),
    IN p_book_id INT
)
BEGIN
    UPDATE book_user
    SET status = p_status
    WHERE username = p_username AND bookId = p_book_id;
END//

DELIMITER ;

-- user_book_menu END

-- user_review_menu

DELIMITER //

CREATE PROCEDURE create_review(
    IN p_rating INT,
    IN p_description TEXT,
    IN p_book_id INT,
    IN p_username VARCHAR(30)
)
BEGIN
    DECLARE review_id INT;

    INSERT INTO reviews (rating, description)
    VALUES (p_rating, p_description);

    SET review_id = LAST_INSERT_ID();

    INSERT INTO user_review_book (bookId, username, reviewId)
    VALUES (p_book_id, p_username, review_id);
END//

DELIMITER ;


-- user_review_menu END

-- other_users_menu

DELIMITER //

CREATE PROCEDURE follow_user_proc(
    IN p_username VARCHAR(30),
    IN p_second_username VARCHAR(30)
)
BEGIN
    SET @query = CONCAT('INSERT INTO user_follows_user (username, following_username) VALUES ("', p_username, '", "', p_second_username, '");');
    PREPARE statement FROM @query;
    EXECUTE statement;
    DEALLOCATE PREPARE statement;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE unfollow_user_proc(
    IN p_username VARCHAR(30),
    IN p_second_username VARCHAR(30)
)
BEGIN
    SET @query = CONCAT('DELETE FROM user_follows_user WHERE username = "', p_username, '" AND following_username = "', p_second_username, '";');
    PREPARE statement FROM @query;
    EXECUTE statement;
    DEALLOCATE PREPARE statement;
END //

DELIMITER ;


-- other_user_menu END

-- general procedures

DELIMITER //
CREATE PROCEDURE view_item_proc(IN entity VARCHAR(100), IN id_column VARCHAR(100), IN item_id VARCHAR(100))
BEGIN
    SET @query = CONCAT('SELECT * FROM ', entity);
    IF item_id IS NOT NULL THEN
        SET @query = CONCAT(@query, ' WHERE ',id_column, ' = "', item_id, '"');
    END IF;
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

DELIMITER //

-- view_column_items_proc', (select_col, entity, item_id, id_column))
DELIMITER //

CREATE PROCEDURE view_column_items_proc(IN select_col VARCHAR(100), IN entity VARCHAR(100), IN id_column VARCHAR(100), IN item_id VARCHAR(100))
BEGIN
    SET @query = CONCAT('SELECT ', select_col, ' FROM ', entity);
    IF item_id IS NOT NULL THEN
        SET @query = CONCAT(@query, ' WHERE ', id_column, ' = "', item_id, '"');
    END IF;
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE delete_item_proc(IN entity VARCHAR(100), IN item_id VARCHAR(100), IN id_column VARCHAR(100))
BEGIN
    SET @query = CONCAT('DELETE FROM ', entity, ' WHERE ', id_column, ' = ', item_id);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE delete_junction_instance(IN table_name VARCHAR(100), IN primary_key_columns VARCHAR(500), IN primary_key_values VARCHAR(500))
BEGIN
    SET @query = CONCAT('DELETE FROM ', table_name, ' WHERE ', primary_key_columns, ' = ', primary_key_values);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_items_proc(
    IN table_name VARCHAR(100),
    IN column_name VARCHAR(100),
    IN new_value VARCHAR(100),
    IN where_column VARCHAR(100),
    IN where_value VARCHAR(100)
)
BEGIN
    SET @query = CONCAT('UPDATE ', table_name, ' SET ', column_name, ' = "', new_value, '" WHERE ', where_column, ' = "', where_value, '"');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

DELIMITER //






-- ---------------------------------- DATA DUMP ----------------------------------

INSERT INTO librarian (username, password, first_name, last_name) VALUES
('test_librarian', 'tester123', 'Test', 'Librarian');

INSERT INTO user (username, password, first_name, last_name) VALUES
('test_user', 'tester456', 'Test', 'User'),
('jane_doe_22', 'doremefaso', 'Jane', 'Doe');

INSERT INTO author (first_last_name) VALUES 
('F. Scott Fitzgerald'), 
('Harper Lee'), 
('George Orwell'),
('J.K. Rowling');

INSERT INTO genre (name, description) VALUES
('Historical Fiction', 'Plot takes place in a setting located in the past'),
('Science Fiction', 'Deals with imaginative and futuristic concepts'),
('Fantasy', 'Set in a fictional universe, often inspired by myth and folklore'),
('Mystery', 'Involves the solving of a crime or puzzle'),
('Romance', 'Focuses on romantic relationships'),
('Thriller', 'Generates intense excitement, suspense, and anticipation'),
('Horror', 'Intends to frighten, scare, or startle its readers'),
('Adventure', 'Involves exciting journeys or experiences'),
('Biography', 'Tells the life story of a person'),
('Self-Help', 'Provides guidance and advice for personal improvement');


INSERT INTO book (title, num_pages, publication_year, author, book_genre, librarian_username) VALUES 
('The Great Gatsby', 180, 1925, 'F. Scott Fitzgerald', 'Historical Fiction', 'test_librarian'),
('To Kill a Mocking Bird', 323, 1960, 'Harper Lee', 'Historical Fiction', 'test_librarian'),
('1984', 368, 1949, 'George Orwell', 'Science Fiction', 'test_librarian'),
('Harry Potter and the Deathly Hallows', 759, 2007, 'J.K. Rowling', 'Fantasy', 'test_librarian');

INSERT INTO reviews (rating, description) VALUES
(5, NULL),
(4, 'Great book'),
(3, 'Not bad'),
(2, 'Could be better'),
(4, NULL);

INSERT INTO book_club (club_name, bookId, librarian) VALUES
('PotterHeads', 4, 'test_librarian'),
('Classics Lovers', 1, 'test_librarian');

INSERT INTO book_club_members (club_name, member) VALUES
('PotterHeads', 'test_user'),
('Classics Lovers', 'test_user'),
('PotterHeads', 'jane_doe_22');

INSERT INTO book_user (bookId, username, status) VALUES
(1, 'jane_doe_22', 'Read'),
(2, 'jane_doe_22', 'Read'),
(1, 'test_user', 'Want to Read'),
(2, 'test_user', 'Currently Reading'),
(3, 'test_user', 'Want to Read'),
(4, 'test_user', 'Want to Read');

INSERT INTO user_follows_user (username, following_username) VALUES
('test_user', 'jane_doe_22');

INSERT INTO user_review_book (bookId, username, reviewId) VALUES
(1, 'test_user', 1),
(2, 'jane_doe_22', 2),
(3, 'test_user', 3),
(4, 'jane_doe_22', 4),
(1, 'jane_doe_22', 5);



