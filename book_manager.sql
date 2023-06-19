CREATE TABLE Book (
    bookId INT PRIMARY KEY,
    title VARCHAR(255),
    numPages INT,
    publicationYear INT,
    numReviews INT,
    averageRating DECIMAL(3,2)
);

CREATE TABLE Author (
    first_last_name VARCHAR(255) PRIMARY KEY,
    numBooks INT
);

CREATE TABLE Genre (
    name VARCHAR(255) PRIMARY KEY,
    description TEXT,
    numBooks INT
);

CREATE TABLE Review (
    reviewId INT PRIMARY KEY,
    rating INt(3,2), 
    description TEXT
);

CREATE TABLE BookClub (
    name VARCHAR(255) PRIMARY KEY,
    active BOOLEAN,
    numMembers INT
);

CREATE TABLE User (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255),
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    numFollowers INT,
    numFollowing INT,
    status VARCHAR(255)
);

CREATE TABLE Librarian (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255),
    firstName VARCHAR(255),
    lastName VARCHAR(255)
);
