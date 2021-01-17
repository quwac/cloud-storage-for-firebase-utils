ARG VARIANT="3.6"
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}
LABEL name="python-env"
LABEL version="1.0.0"

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/erbium"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Install tig and Poetry
ENV POETRY_HOME=/home/vscode/.poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends bash-completion git tig curl \
    # Install Poetry
    && echo Install Poetry ... \
    && su vscode -c "umask 0002 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - " \
    && poetry completions bash > /etc/bash_completion.d/poetry.bash-completion \
    # Clean
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts


CMD ["/bin/bash"]
ENTRYPOINT [ "/bin/bash" ]
