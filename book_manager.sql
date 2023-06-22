DROP DATABASE IF EXISTS BookManager;
CREATE DATABASE IF NOT EXISTS BookManager;

USE BookManager;

-- need to add PK some of these have non
-- Need to add deletion contraints depending on the entity 
-- need to add ability to create users

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
	lib_username VARCHAR(30) PRIMARY KEY,
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
    

	FOREIGN KEY (book_genre) REFERENCES genre (name) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (author) REFERENCES author (first_last_name) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (librarian_username) REFERENCES librarian (lib_username) ON UPDATE CASCADE ON DELETE SET NULL
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
    FOREIGN KEY (librarian) REFERENCES librarian (lib_username) ON UPDATE CASCADE ON DELETE SET NULL
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

DELIMITER //
CREATE PROCEDURE view_item_proc(IN entity VARCHAR(100), IN item_id VARCHAR(100), IN id_column VARCHAR(100))
BEGIN
    SET @query = CONCAT('SELECT * FROM ', entity);
    IF item_id IS NOT NULL THEN
        SET @query = CONCAT(@query, ' WHERE ', id_column, ' = ', item_id);
    END IF;
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



-- ---------------------------------- DATA DUMP ----------------------------------

INSERT INTO librarian (lib_username, password, first_name, last_name) VALUES
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
('Historical Fiction', 'Historical fiction is a literary genre in which the plot takes place in a setting located in the past'),
('Science Fiction', 'Science fiction is a genre of speculative fiction that typically deals with imaginative and futuristic concepts'),
('Fantasy', 'Fantasy is a genre of speculative fiction set in a fictional universe, often inspired by myth and folklore');


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
('PotterHeads', 'jane_doe_22'),
('Classics Lovers', 'jane_doe_22');

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

-------------------------------- DATA DUMP END --------------------------------

