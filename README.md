This app was lifted from the Python Language Projects book by Laura Casell and Alan Gauld.

Please see Chapter 5 in the book for more information on how the code works.

The app employs flask with a simple sqlite db. I thought this would make the best example
to learn how to dockerize applications.

The devops-project in my repo will also utilize this app to demonstrate basic ci/cd workflows
when I add/modify the codebase.

lendy.db:
.schema item
CREATE TABLE item (
ID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Description TEXT NOT NULL,
OwnerID INTEGER NOT NULL REFERENCES member(ID),
Price NUMERIC,
Condition TEXT,
DateRegistered TEXT);


.schema loan
CREATE TABLE loan (
ID INTEGER PRIMARY KEY,
ItemID INTEGER NOT NULL REFERENCES item(ID),
BorrowerID INTEGER NOT NULL REFERENCES member(ID),
DateBorrowed TEXT NOT NULL,
DateReturned TEXT);

.schema member
CREATE TABLE member (
ID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Email TEXT);
