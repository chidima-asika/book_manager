## BookManager

Our project is a console-based book management system designed to assist readers in organizing their book collections. Users can keep track of the books they are currently reading, write reviews, join book clubs, and follow other users. The user interface is simple and intuitive, allowing users to interact with the system. Users can retrieve details about a specific book, including authors and reviews. The database is self-managed by users, as it puts trust in readers. This application is ideal for book lovers looking for a convenient way to manage their reading experience.
 

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running-Program](#Running-Program)
- [Configuration](#configuration)
- [How to Use](#how-to-use)

## Prerequisites

Before running the project, make sure you have the following software and libraries installed:

- MySQL Server: Download and install MySQL Server from the [official website](https://dev.mysql.com/downloads/). Follow the installation instructions provided.
- MySQL Connector/J: Download the JDBC driver for MySQL from the [MySQL website](https://dev.mysql.com/downloads/connector/j/). Choose the appropriate version for your system and follow the installation instructions.

## Installation

To install the project, follow these steps:

1. Clone or download the project source code from the repository.
2. Open your preferred IDE.
3. Build the project using the appropriate build command or IDE feature. 

please install the following dependcies forfor beggining

`pip3 install mysql-connector-python`
`pip3 install pymysql`

## Running Program

within terminal window run

`python3 application.py` 

## Configuration

Before running the project, you need to configure the database connection:

1. Open the project in your IDE.
2. Locate the database connection configuration file. It might be named something like "dbconfig.properties" or "application.properties."
3. Update the configuration file with your MySQL server details, including the host, port, username, and password.


## How to Use

1. Start the program and login with your account or create a new account.
2. Once logged in, you will see a menu with the following options:
   - Books: View, search, and manage books.
   - Book Clubs: Join book clubs, create new clubs, and interact with club members.
   - Authors: Explore authors and their books.
   - Genres: Browse books by genres.
   - Logout: Exit the program and logout from your account.
3. Choose an option from the menu by entering the corresponding number.
4. Follow the prompts and interact with the program based on the chosen option.

.

