DROP DATABASE IF EXISTS BookManager;
CREATE DATABASE IF NOT EXISTS BookManager;

USE BookManager;


CREATE TABLE user
(
	username VARCHAR(30) PRIMARY KEY,
    password VARCHAR(30),
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    num_followers INT DEFAULT 0,
    num_following INT DEFAULT 0

);

CREATE TABLE librarian
(
	lib_username VARCHAR(30) PRIMARY KEY,
    password VARCHAR(30),
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
    

	FOREIGN KEY (book_genre) REFERENCES genre (name),
	FOREIGN KEY (author) REFERENCES author (first_last_name),
    FOREIGN KEY (librarian_username) REFERENCES librarian (lib_username)
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

	FOREIGN KEY (bookId) REFERENCES book (bookId),
    FOREIGN KEY (librarian) REFERENCES librarian (lib_username)
    
);


CREATE TABLE book_user
(
	bookId INT,
    username VARCHAR(30),
    status VARCHAR(30) DEFAULT NULL,
    
    FOREIGN KEY (bookId) REFERENCES book (bookId),
    FOREIGN KEY (username) REFERENCES user (username),
    
    PRIMARY KEY (bookId, username)
    
);

CREATE TABLE book_club_members
(
	club_name VARCHAR(100),
    member VARCHAR(30),
    
    FOREIGN KEY (club_name) REFERENCES book_club (club_name),
    FOREIGN KEY (member) REFERENCES user (username),
    
    PRIMARY KEY (club_name, member)
    
);


CREATE TABLE user_follows_user
(
	username VARCHAR(30),
    following_username VARCHAR(30),
    
    FOREIGN KEY (username) REFERENCES user (username),
    FOREIGN KEY (following_username) REFERENCES user (username),
    
    PRIMARY KEY (username, following_username)
    
);


CREATE TABLE user_review_book
(
	bookId INT,
    username VARCHAR(30),
    reviewId INT,
    
    FOREIGN KEY (bookId) REFERENCES book (bookId),
    FOREIGN KEY (username) REFERENCES user (username),
    FOREIGN KEY (reviewId) REFERENCES reviews (reviewId),
    
    PRIMARY KEY (bookId, username, reviewId)
    
);


-- Triggers to update counter variables (num_following, num_books, num_members, etc.)


DELIMITER //

DROP TRIGGER IF EXISTS update_num_books_insert;
CREATE TRIGGER update_num_books_insert AFTER INSERT ON book
FOR EACH ROW
BEGIN
    DECLARE author_name VARCHAR(100);
    DECLARE genre_name VARCHAR(100);
    
    SET author_name = NEW.author;
    SET genre_name = NEW.book_genre;
    
    IF author_name IS NOT NULL THEN
        UPDATE author
        SET num_books = num_books + 1
        WHERE first_last_name = author_name;
    END IF;
    
    IF genre_name IS NOT NULL THEN
        UPDATE genre
        SET num_books = num_books + 1
        WHERE name = genre_name;
    END IF;
END //

DELIMITER ;


DELIMITER //

DROP TRIGGER IF EXISTS update_num_books_delete;
CREATE TRIGGER update_num_books_delete AFTER DELETE ON book
FOR EACH ROW
BEGIN
    DECLARE author_name VARCHAR(100);
    DECLARE genre_name VARCHAR(100);
    
    SET author_name = OLD.author;
    SET genre_name = OLD.book_genre;
    
    IF author_name IS NOT NULL THEN
        UPDATE author
        SET num_books = num_books - 1
        WHERE first_last_name = author_name;
    END IF;
    
    IF genre_name IS NOT NULL THEN
        UPDATE genre
        SET num_books = num_books - 1
        WHERE name = genre_name;
    END IF;
END //

DELIMITER ;



DELIMITER //

DROP TRIGGER IF EXISTS update_num_following_insert;
CREATE TRIGGER update_num_following_insert AFTER INSERT ON user_follows_user
FOR EACH ROW
BEGIN
    -- update num_following for the user who initiated the follow
    UPDATE user
    SET num_following = num_following + 1
    WHERE username = NEW.username;
    
    -- update num_followers for the user who is being followed
    UPDATE user
    SET num_followers = num_followers + 1
    WHERE username = NEW.following_username;
END //

DELIMITER ;


DELIMITER //

DROP TRIGGER IF EXISTS update_num_following_delete;
CREATE TRIGGER update_num_following_delete AFTER DELETE ON user_follows_user
FOR EACH ROW
BEGIN
    -- update num_following for the user who initiated the follow
    UPDATE user
    SET num_following = num_following - 1
    WHERE username = OLD.username;
    
    -- update num_followers for the user who is being followed
    UPDATE user
    SET num_followers = num_followers - 1
    WHERE username = OLD.following_username;
END //

DELIMITER ;


DELIMITER //

DROP TRIGGER IF EXISTS update_book_review_info_insert;
CREATE TRIGGER update_book_review_info_insert AFTER INSERT ON user_review_book
FOR EACH ROW
BEGIN
    
    UPDATE book
    SET num_reviews = (SELECT COUNT(*) FROM user_review_book WHERE bookId = NEW.bookId)
    WHERE bookId = NEW.bookId;
    
    
    UPDATE book
    SET ave_rating =
        (SELECT IFNULL(SUM(reviews.rating) / book.num_reviews, NULL)
        FROM reviews
        JOIN user_review_book ON reviews.reviewId = user_review_book.reviewId
        WHERE user_review_book.bookId = NEW.bookId)
    WHERE bookId = NEW.bookId;
END //

DELIMITER ;


DELIMITER //

DROP TRIGGER IF EXISTS update_book_review_info_delete;
CREATE TRIGGER update_book_review_info_delete AFTER DELETE ON user_review_book
FOR EACH ROW
BEGIN
    
    UPDATE book
    SET num_reviews = (SELECT COUNT(*) FROM user_review_book WHERE bookId = OLD.bookId)
    WHERE bookId = OLD.bookId;
    
    
    UPDATE book
    SET ave_rating =
        (SELECT IFNULL(SUM(reviews.rating) / book.num_reviews, NULL)
        FROM reviews
        JOIN user_review_book ON reviews.reviewId = user_review_book.reviewId
        WHERE user_review_book.bookId = OLD.bookId)
    WHERE bookId = OLD.bookId;
END //

DELIMITER ;




-- Data dump

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
(2, 'Could be better');

INSERT INTO book_club (club_name, bookId, librarian) VALUES
('PotterHeads', 4, 'test_librarian'),
('Classics Lovers', 1, 'test_librarian');

INSERT INTO book_club_members (club_name, member) VALUES
('PotterHeads', 'test_user'),
('Classics Lovers', 'test_user'),
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
(4, 'jane_doe_22', 4);


