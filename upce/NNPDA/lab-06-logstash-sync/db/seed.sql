INSERT INTO products (name, description, price) VALUES
  ('Wireless Headphones', 'Wireless over-ear headphones with noise cancellation', 199.99),
  ('Bluetooth Speaker', 'Portable wireless bluetooth speaker with deep bass', 89.90),
  ('Mechanical Keyboard', 'RGB mechanical keyboard with tactile switches', 129.00),
  ('Wireless Mouse', 'Ergonomic wireless mouse with silent clicks', 39.99),
  ('Espresso Machine', 'Compact espresso machine with milk frother', 249.00),
  ('Chef Knife', 'Stainless steel chef knife, razor sharp', 59.50),
  ('Running Shoes', 'Lightweight running shoes for daily training', 119.95),
  ('Yoga Mat', 'Non-slip yoga mat with carrying strap', 29.99)
ON CONFLICT DO NOTHING;
