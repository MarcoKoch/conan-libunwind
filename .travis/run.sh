#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate conan
fi

# Only upload packages from the master or release branches.
# This prevents us from spamming the 'testing' repo with packages from
# feature branches.
if ! [[ $TRAVIS_PULL_REQUEST = "false" && $TRAVIS_BRANCH =~ (^master$)|(^v.+) ]]
    unset CONAN_UPLOAD
fi

python build.py
