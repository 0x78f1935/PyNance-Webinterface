ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'pynanny'@'%' IDENTIFIED BY 'PyNanny';
GRANT ALL PRIVILEGES ON *.* TO 'pynanny'@'%';
FLUSH PRIVILEGES;