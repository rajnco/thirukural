FROM python:3.11.10-slim-bookworm as poetry-base
#FROM python:3.11.10-bookworm as poetry-base

# set environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# install poetry  
RUN pip install poetry==1.8.2

# Add demo user thiruvalluvar
RUN adduser  thiruvalluvar && \
    mkdir -p /home/thiruvalluvar/app && \
    chown thiruvalluvar:thiruvalluvar /home/thiruvalluvar/app

WORKDIR /home/thiruvalluvar/app

USER thiruvalluvar

WORKDIR /home/thiruvalluvar/app


COPY ./pyproject.toml ./poetry.lock* /home/thiruvalluvar/app/

# poetry complains if there is no README file
RUN touch README.md

# install without dev dependencies + remove poetry cache
RUN poetry install --no-dev && rm -rf $POETRY_CACHE_DIR


#FROM python:3.11.10-bookworm as runtime
FROM python:3.11.10-slim-bookworm as runtime

# Add demo user thiruvalluvar
RUN adduser  thiruvalluvar && \
    mkdir -p /home/thiruvalluvar/app && \
    chown thiruvalluvar:thiruvalluvar /home/thiruvalluvar/app

WORKDIR /home/thiruvalluvar/app

#USER thiruvalluvar

#WORKDIR /home/thiruvalluvar/app

# set environment variables
ENV VIRTUAL_ENV=.venv \
    PATH="/home/thiruvalluvar/app/.venv/bin:$PATH"

COPY --from=poetry-base /home/thiruvalluvar/app/${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY  ./app /home/thiruvalluvar/app
# COPY --chmod=777 ./app /home/thiruvalluvar/app

RUN find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

RUN chown -R thiruvalluvar:thiruvalluvar  /home/thiruvalluvar/app

RUN ls -la /home/thiruvalluvar/app

# RUN rm -rf /var/lib/apt/lists/* -- 0 effect
RUN apt-get clean


USER thiruvalluvar

# RUN chown -R thiruvalluvar:thiruvalluvar  /home/thiruvalluvar/app
# RUN chmod -R u+rwx /home/thiruvalluvar/app
# RUN ls -la /home/thiruvalluvar/app
# RUN chmod -R 777 /home/thiruvalluvar/app
# RUN rm -rf /var/lib/apt/lists/* -- 0 effect
# RUN apt-get clean


#EXPOSE 8000
EXPOSE 9090
EXPOSE 9100

#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
#ENTRYPOINT [ "python", "/home/thiruvalluvar/app/app/app.py"  ]
ENTRYPOINT [ "/bin/bash", "-e", "/home/thiruvalluvar/app/start.sh"  ]
