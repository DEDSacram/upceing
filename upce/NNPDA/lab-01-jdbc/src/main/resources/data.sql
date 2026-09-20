INSERT INTO students (first_name, last_name, email) VALUES
    ('Alice', 'Novak', 'alice.novak@example.com'),
    ('Bob', 'Svoboda', 'bob.svoboda@example.com'),
    ('Cyril', 'Dvorak', 'cyril.dvorak@example.com')
ON CONFLICT (email) DO NOTHING;
