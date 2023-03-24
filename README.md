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
# Hello ✋.

To run the project, follow these steps:

1. Clone the repository:

git clone https://github.com/RezuanDzibov/qortex-test-assignment

2. Navigate to the project directory:

cd qortex-test-assignment

3. Create a `.env` file and fill it with the necessary information or use `.env.example` by running the following command:

Windows
copy .env.example .env

Linux/MacOS
cp .env.example .env

4. Start the project:

docker-compose up --build

The project includes a test admin user and several test objects:

- `username: admin`
- `password: admin`

To access the admin panel, go to: http://127.0.0.1:8000/admin/

To use the Swagger API, go to: http://127.0.0.1:8000/swagger/

We wish you a good day!

Swagger screenshots:

![Swagger UI](./pics/Swagger%20UI.jpeg)

![Swagger UI Expandend Operation](./pics/Swagger%20UI%20expandend%20operation.png)

![Swagger UI Response Example](./pics/Swagger%20UI%20resoponse%20example.png)
