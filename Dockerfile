# Building angular static files
FROM node:18-alpine as build-angular

WORKDIR /frontend

COPY ./app/frontend/package*.json ./
RUN npm install
COPY ./app/frontend .
RUN npm run build
RUN ls -al /frontend/dist

# Building FastAPI appication
FROM python:3.11

WORKDIR /pyparking

COPY ./requirements.txt /pyparking/requirements.txt
COPY ./alembic.ini /pyparking/alembic.ini
COPY ./alembic /pyparking/alembic

RUN pip install --no-cache-dir --upgrade -r /pyparking/requirements.txt

COPY ./app /pyparking/app
RUN rm -rf /pyparking/app/frontend
COPY --from=build-angular /frontend/dist/frontend /pyparking/app/frontend/dist/frontend

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
# CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--workers", "4"] # TODO: docker logs with 4 workers is not working