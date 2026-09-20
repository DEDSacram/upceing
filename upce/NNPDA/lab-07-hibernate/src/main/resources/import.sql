INSERT INTO authors (id, name, country) VALUES (1, 'George Orwell', 'United Kingdom');
INSERT INTO authors (id, name, country) VALUES (2, 'J.R.R. Tolkien', 'United Kingdom');
INSERT INTO books (id, title, year, price, author_id) VALUES (1, '1984', 1949, 299.0, 1);
INSERT INTO books (id, title, year, price, author_id) VALUES (2, 'Animal Farm', 1945, 249.0, 1);
INSERT INTO books (id, title, year, price, author_id) VALUES (3, 'The Hobbit', 1937, 349.0, 2);
-- H2 only: advance identity sequences past the seeded ids so runtime inserts do not collide.
ALTER TABLE authors ALTER COLUMN id RESTART WITH 100;
ALTER TABLE books ALTER COLUMN id RESTART WITH 100;
