# aiohttp test application

## Application demo instructions
1. Install mysql `sudo apt install mysql-server`, `sudo mysql_secure_installation`
1. Create user/database for use in application `CREATE USER 'tstech'@'localhost' IDENTIFIED BY 'tstech';`, `GRANT ALL PRIVILEGES ON *.* TO 'tstech'@'localhost';`, `CREATE DATABASE tstech;`
1. `git clone https://github.com/km445/aiohttp_tstech.git`
1. Create a virtual environment, activate it and install requirements.txt.
1. `cd aiohttp_tstech`
1. Initialize the database and run application with `python user_processing/init_db.py`, `python user_processing/main.py`
1. Go to `http://localhost:8080/` to use the application.
1. Run some tests with `python user_processing/tests.py`
