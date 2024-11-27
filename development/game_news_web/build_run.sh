#!/bin/bash

# Vue 빌드 실행
echo "Building Vue project..."
cd frontend
npm run build || { echo "Vue build failed"; exit 1; }

# 빌드된 파일을 Django로 복사
echo "Copying Vue build files to Django static directory..."
rm -rf ../backend/static
cp -r dist ../backend/static

# Django 서버 실행
echo "Starting Django server..."
cd ../backend
python manage.py runserver