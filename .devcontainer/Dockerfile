FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Atnaujiname paketų sąrašą
RUN apt-get update -y

# Įdiegiame Python ir pip
RUN apt-get install -y python3 python3-pip

# Įdiegiame PHP ir Composer
RUN apt-get install -y php-cli composer

# Įdiegiame SQLite
RUN apt-get install -y sqlite3 libsqlite3-dev

# Python: pagrindinės duomenų analizės bibliotekos
RUN pip3 install pandas numpy

# Python: vizualizacijos
RUN pip3 install matplotlib seaborn

# Python: mašininis mokymasis
RUN pip3 install scikit-learn

# Python: duomenų šaltiniai ir API
RUN pip3 install yfinance requests

# Python: darbui su CSV, JSON, SQL (įskaitant SQLite per pandas)
RUN pip3 install sqlalchemy

# Python: interaktyvi aplinka
RUN pip3 install jupyterlab

# Nustatome darbo katalogą
WORKDIR /workspaces/2025-Open-Data/students

# Bash kaip numatytasis shell
