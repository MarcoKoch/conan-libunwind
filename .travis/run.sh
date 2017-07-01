#!/bin/bash

set -e
set -x

# Darwin is not supported by libunwind
#if [[ "$(uname -s)" == 'Darwin' ]]; then
#    if which pyenv > /dev/null; then
#        eval "$(pyenv init -)"
#    fi
#    pyenv activate conan
#fi

# Only upload packages from the master or stable release branches.
# This prevents us from spamming the 'testing' repo with packages from
# feature branches.
if ! [[ $TRAVIS_PULL_REQUEST = "false" && $TRAVIS_BRANCH =~ (^master$)|(^v[0-9]+(\.[0-9]+)*-stable$) ]] ; then
    unset CONAN_UPLOAD
fi

python build.py
