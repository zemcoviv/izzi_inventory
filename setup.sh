#!/bin/bash

# Обновление списка пакетов и установка необходимых системных зависимостей
echo "Updating package list and installing system dependencies..."
sudo apt-get update
sudo apt-get install -y libpq-dev python3-dev build-essential postgresql postgresql-contrib git

# Установка masscan из исходного кода
echo "Installing masscan..."
git clone https://github.com/robertdavidgraham/masscan.git
cd masscan
make
sudo make install
cd ..

# Установка виртуального окружения для Python
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Обновление pip и установка Python-зависимостей
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install Flask psycopg2-binary python-nmap

# Настройка PostgreSQL
echo "Setting up PostgreSQL database..."
sudo -u postgres psql -c "CREATE DATABASE network_inventory;"
sudo -u postgres psql -c "CREATE USER \"user\" WITH PASSWORD 'password';"
sudo -u postgres psql -c "ALTER ROLE \"user\" SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE \"user\" SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE \"user\" SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE network_inventory TO \"user\";"

echo "All done! To start using the virtual environment, run 'source venv/bin/activate'."
echo "You can now run 'python app.py' to start the application."
