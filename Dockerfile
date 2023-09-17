FROM python:3.9-slim
WORKDIR /srv
RUN pip install pip==22.0.4 && pip install pipenv==2020.11.15 && pip install setuptools
COPY ./Pipfile* ./
RUN pipenv install --dev --system
COPY . .