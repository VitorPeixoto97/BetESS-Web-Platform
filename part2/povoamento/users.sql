INSERT INTO "public"."auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES 
('1', 'pbkdf2_sha256$150000$i3wOqhttA85F$f4FMnK5s99qZvzZ3WegoxmogH9ylhmE9AlyS/2VnsRI=', '2019-06-06 23:36:00.081593+01', 't', 'admin', '', '', 'vitor-peixoto@outlook.pt', 't', 't', '2019-06-06 23:35:17.71104+01'),
('2', 'pbkdf2_sha256$150000$WYYjjZfgq5T0$ekRuqpIDUP8DJ5EIgI1d3lHHbO6OIIY/saUMvhKVIgc=', NULL, 'f', 'vitorpeixoto@mail.com', '', '', '', 'f', 't', '2019-06-06 23:37:34.935947+01'),
('3', 'pbkdf2_sha256$150000$Xts3wTIlKKEd$2zghmsQ/fUylgL4nNaQNDpAl2HT1xdj8zAOGd8dkVJY=', NULL, 'f', 'antoniolopes@mail.com', '', '', '', 'f', 't', '2019-06-06 23:38:30.268315+01'),
('4', 'pbkdf2_sha256$150000$wmA6qF4kifau$CN3TAsGLNaqaYXTEuI8t7Hu6JAHaCWYj5qKAwz4TZX8=', NULL, 'f', 'catarinamendes@mail.com', '', '', '', 'f', 't', '2019-06-06 23:38:46.639358+01'),
('5', 'pbkdf2_sha256$150000$PCwwv0TYpQbP$uum5VwzszPwh/DnD+IcpXXtzMwyTBSc+6M8mfJgaIfc=', NULL, 'f', 'danielmaia@mail.com', '', '', '', 'f', 't', '2019-06-06 23:39:21.408394+01'),
('6', 'pbkdf2_sha256$120000$1fif4KJf2el4$vXUQwd/5jKw0w2mSKbvdZBOLUL70YtSU7OFizDACGFQ=', NULL, 'f', 'joaocarlos@mail.com', '', '', '', 'f', 't', '2019-06-12 15:51:50.709762+01');

INSERT INTO "public"."app_user" ("id", "username", "email", "name", "coins", "type") VALUES ('0', 'vitorpeixoto', 'vitor-peixoto@outlook.pt', 'Vitor Peixoto', '32', '0'),
('1', 'antoniolopes', 'antoniolopes@mail.com', 'António Lopes', '20', '1'),
('2', 'catarinamendes', 'catarinamendes@mail.com', 'Catarina Mendes', '12', '0'),
('3', 'danielmaia', 'danielmaia@mail.com', 'Daniel Maia', '35', '1');

INSERT INTO "public"."app_admin"("id", "email")VALUES ('1', 'joaocarlos@mail.com');

