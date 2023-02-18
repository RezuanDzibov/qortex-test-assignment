FROM python:3

ENV APP_HOME=/home/app

RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

RUN apt update && apt install python3 netcat -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $WEB_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

RUN pip install -r $APP_HOME/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:${WEB_HOME}"

RUN chmod +x /home/app/entrypoint.sh
ENTRYPOINT ["/home/app/entrypoint.sh"]