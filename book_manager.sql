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
	num_books INT DEFAULT 0

);

CREATE TABLE author
(
	first_last_name VARCHAR(100) PRIMARY KEY,
	num_books INT DEFAULT 0
    
);

CREATE TABLE book
(
	bookId INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    num_pages INT NOT NULL,
    publication_year YEAR NOT NULL,
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
    description VARCHAR(500) DEFAULT NULL,
    num_reviews INT DEFAULT 0
);


CREATE TABLE book_club
(

    club_name VARCHAR(100) PRIMARY KEY,
    active TINYINT(1) DEFAULT 1,
    bookId INT,
    librarian VARCHAR(30),
    num_members INT DEFAULT 1,

	FOREIGN KEY (bookId) REFERENCES book (bookId),
    FOREIGN KEY (librarian) REFERENCES librarian (lib_username)
    
);


CREATE TABLE book_user
(
	bookId INT,
    username VARCHAR(30),
    status VARCHAR(30) DEFAULT NULL,
    
    FOREIGN KEY (bookId) REFERENCES book (bookId),
    FOREIGN KEY (username) REFERENCES user (username)
    
);

CREATE TABLE book_club_members
(
	club_name VARCHAR(100),
    member VARCHAR(30),
    
    FOREIGN KEY (club_name) REFERENCES book_club (club_name),
    FOREIGN KEY (member) REFERENCES user (username)
    
);


CREATE TABLE user_follows_user
(
	username VARCHAR(30),
    following_username VARCHAR(30),
    
    FOREIGN KEY (username) REFERENCES user (username),
    FOREIGN KEY (following_username) REFERENCES user (username)
    
);


CREATE TABLE user_review_book
(
	bookId INT,
    username VARCHAR(30),
    reviewId INT,
    
    FOREIGN KEY (bookId) REFERENCES book (bookId),
    FOREIGN KEY (username) REFERENCES user (username),
    FOREIGN KEY (reviewId) REFERENCES reviews (reviewId)
    
);


# Data dump

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

INSERT INTO genre (name) VALUES
('Historical Fiction'), ('Science Fiction'), ('Fantasy');

INSERT INTO book (title, num_pages, publication_year, book_genre, author, librarian_username) VALUES 
('The Great Gatsby', 180, 1925, 'Historical Fiction', 'F. Scott Fitzgerald', 'test_librarian'),
('To Kill a Mocking Bird', 323, 1960, 'Historical Fiction', 'Harper Lee', 'test_librarian'),
('1984', 368, 1949, 'Science Fiction', 'George Orwell', 'test_librarian'),
('Harry Potter and the Deathly Hallows', 759, 2007, 'Fantasy', 'J.K. Rowling', 'test_librarian');

INSERT INTO book_club (club_name, bookId, librarian) VALUES
('PotterHeads', 4, 'test_librarian'),
('Classics Lovers', 1, 'test_librarian');

INSERT INTO book_club_members (club_name, member) VALUES
('PotterHeads', 'test_user'),
('Classics Lovers', 'jane_doe_22');

INSERT INTO book_user (bookId, username, status) VALUES
(1, 'jane_doe_22', 'Read'),
(2, 'jane_doe_22', 'Read'),
(1, 'test_user', 'Want to Read'),
(2, 'test_user', 'Currently Reading'),
(3, 'test_user', 'Want to Read'),
(4, 'test_user', 'Want to Read');

