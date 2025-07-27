#!/bin/bash
set -e

echo "⚙️ Проверка версии Python..."
python3 --version

echo "📦 Установка зависимостей..."
pip install --upgrade pip
pip install git+https://github.com/SantiiRepair/quotexpy.git@main#egg=quotexpy
pip install -r requirements.txt
