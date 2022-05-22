CREATE DATABASE IF NOT EXISTS replicatormanager;
CREATE DATABASE IF NOT EXISTS accessguard;

GRANT ALL ON `replicatormanager`.* TO 'user'@'%';
GRANT ALL ON `accessguard`.* TO 'user'@'%';
