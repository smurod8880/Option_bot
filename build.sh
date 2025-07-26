#!/bin/bash
set -e

echo "📦 Установка quotexpy из GitHub..."
pip install git+https://github.com/SantiiRepair/quotexpy.git@main#egg=quotexpy

echo "📦 Установка остальных зависимостей..."
pip install -r requirements.txt
