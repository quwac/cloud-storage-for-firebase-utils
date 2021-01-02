#!/bin/bash

# Install Visual Studio Code Extensions
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension donjayamanne.python-extension-pack
code --install-extension himanoa.Python-autopep8
code --install-extension bungcip.better-toml
code --install-extension foxundermoon.shell-format
code --install-extension timonwong.shellcheck

# Install Python
python_version=$(head -1 ".python-version")
installed=$(pyenv versions --bare | grep "$python_version")
if [ "$python_version" != "$installed" ]; then
    tmp=$python_version
    tmp="${tmp#[vV]}"
    python_version_minor="${tmp#*.}"
    python_version_minor="${python_version_minor%.*}"
    if [ "$python_version_minor" == "6" ] || [ "$python_version_minor" == "7" ]; then
        CPPFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix bzip2)/include  -L$(brew --prefix zlib)/include  -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" \
        LDFLAGS="-L$(brew --prefix openssl)/lib     -L$(brew --prefix bzip2)/lib      -L$(brew --prefix zlib)/lib      -L$(brew --prefix readline)/lib     -L$(xcrun --show-sdk-path)/usr/lib" \
            pyenv install --patch "$python_version" \
            < <(curl -sSL https://github.com/python/cpython/commit/8ea6353.patch\?full_index\=1)
    else
        LDFLAGS="-L$(xcrun --show-sdk-path)/usr/lib" pyenv install "$python_version"
    fi
fi

# Install Python modules
if [ -e ".venv" ]; then
    rm -rf .venv
fi
poetry install

# Install Node.js modules for Pyright
if [ -e "node_modules" ]; then
    rm -rf node_modules
fi
npm install
