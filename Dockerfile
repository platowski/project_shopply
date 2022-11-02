FROM python:3.9

RUN mkdir /opt/app
WORKDIR /opt/app

RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-dev \
    libpq-dev

RUN export PATH=/usr/lib/postgresql/X.Y/bin/:$PATH

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock /opt/app/
RUN poetry lock --no-update
# Allow installing dev dependencies to run tests
RUN poetry install
COPY ./ /opt/app/


EXPOSE 8010

CMD ["/opt/app/start_app.sh"]

