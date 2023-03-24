# Привет ✋.

Для запуска проекта выполните следующие шаги:

1. Скопируйте репозиторий:

git clone https://github.com/RezuanDzibov/qortex-test-assignment


2. Перейдите в директорию проекта:

cd qortex-test-assignment


3. Создайте файл `.env` и заполните его или использовать `.env.example` следующей командой:

Windows
copy .env.example .env

Linux/MacOS
cp .env.example .env


4. Запустите проект:

docker-compose up --build


В проекте есть тестовый админ пользователь и несколько тестовых объектов:

- `username: admin`
- `password: admin`

Для доступа к админке перейдите по ссылке: http://127.0.0.1:8000/admin/

Чтобы использовать Swagger API, перейдите по ссылке: http://127.0.0.1:8000/swagger/

Желаем вам хорошего дня!