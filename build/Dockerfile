FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPYCACHEPREFIX /tmp/pyc

RUN apt-get update && apt-get install -y \
    git \
    openssh-client \
    systemd; \
    rm -rf /var/lib/apt/lists/*

# Access GitHub to pull in dependencies.
RUN mkdir /root/.ssh
ARG SSH_PRIVATE_KEY
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN eval `ssh-agent &` && ssh-add /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Install dependencies.
RUN pip3 --no-cache-dir --no-input -q install -U pip pipenv && rm -rf /tmp/pyc

COPY Pipfile Pipfile.lock ./

RUN pipenv install --ignore-pipfile --deploy --system && rm -rf /root/.cache && rm -rf /tmp/pyc

# Destroy credentials.
RUN rm -rf /root/.ssh

COPY . .

WORKDIR pipelines

# Apply run permissions to entrypoint script
RUN chmod +x /build/entrypoint.sh
ENTRYPOINT ["/build/entrypoint.sh"]
