# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.191.1/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3.8"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Install additional OS-level dependencies for Python packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        libldap2-dev=2.4.57+dfsg-3 \
        libsasl2-dev

# Remove default utils that could be mistakenly used instead of poetry-controlled equivalents.
ARG DEFAULT_UTILS_TO_UNINSTALL="\
    pylint \
    flake8 \
    autopep8 \
    black \
    yapf \
    mypy \
    pydocstyle \
    pycodestyle \
    bandit"
RUN echo "${DEFAULT_UTILS_TO_UNINSTALL}" | xargs -n 1 pipx uninstall

RUN pipx install pre-commit

# Install Poetry for vscode user
RUN su vscode -c "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version 1.1.10 2>&1"
RUN su vscode -c "echo 'source ~/.poetry/env' >> ~/.zshrc 2>&1"
RUN su vscode -c "echo 'source ~/.poetry/env' >> ~/.bashrc 2>&1"

# Dock In Docker
# See: https://github.com/microsoft/vscode-dev-containers/blob/main/script-library/docs/docker-in-docker.md
# [Option] Enable non-root Docker access in container
# ARG ENABLE_NONROOT_DOCKER="true"
# # [Option] Use the OSS Moby Engine instead of the licensed Docker Engine
# ARG USE_MOBY="true"
# ARG USERNAME=automatic
# ARG USER_UID=1000
# ARG USER_GID=$USER_UID

# COPY bin/docker-in-docker-debian.sh /tmp/library-scripts/docker-in-docker-debian.sh
# RUN apt-get update && /bin/bash /tmp/library-scripts/docker-in-docker-debian.sh "${ENABLE_NONROOT_DOCKER}" "${USERNAME}" "${USE_MOBY}" \
#   # Cleanup
#   && apt-get autoremove -y && apt-get clean -y && rm -rf /tmp/library-scripts/


# ENTRYPOINT ["/usr/local/share/docker-init.sh"]

# VOLUME [ "/var/lib/docker" ]
# CMD ["sleep", "infinity"]
