FROM python:3.12-slim

# Create a non-root user
RUN useradd -m -u 1000 webhook

WORKDIR /usr/src

RUN pip install --no-cache-dir poetry==2.0.1 && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root --no-interaction --no-ansi

COPY ./webhook ./webhook

# Change ownership of the working directory
RUN chown -R webhook:webhook /usr/src

# Switch to non-root user
USER webhook

CMD ["python", "-m", "webhook"]
