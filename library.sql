-- Library Management System SQL
-- Creates database, tables and sample data

CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

CREATE TABLE IF NOT EXISTS Books (
  BookID INT AUTO_INCREMENT PRIMARY KEY,
  Title VARCHAR(200),
  Author VARCHAR(150),
  Genre VARCHAR(80),
  Quantity INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Members (
  MemberID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(150),
  Email VARCHAR(150),
  JoinDate DATE DEFAULT (CURRENT_DATE())
);

CREATE TABLE IF NOT EXISTS Borrow (
  BorrowID INT AUTO_INCREMENT PRIMARY KEY,
  BookID INT,
  MemberID INT,
  IssueDate DATE,
  DueDate DATE,
  ReturnDate DATE,
  Fine DECIMAL(10,2) DEFAULT 0,
  FOREIGN KEY (BookID) REFERENCES Books(BookID),
  FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Sample data
INSERT INTO Books (Title, Author, Genre, Quantity) VALUES
('Python for Data Science', 'Jake VanderPlas', 'Programming', 3),
('Clean Code', 'Robert C. Martin', 'Programming', 2),
('Design Patterns', 'Erich Gamma', 'Software Engineering', 1);

INSERT INTO Members (Name, Email) VALUES
('Komal Malekar', 'komal@example.com'),
('Amit Kumar', 'amit@example.com');

-- Example borrow (issue today, due in 14 days)
INSERT INTO Borrow (BookID, MemberID, IssueDate, DueDate, Fine) VALUES
(1, 1, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), 0);
