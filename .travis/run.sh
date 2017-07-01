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

# Only upload packages from release branches
# This prevents us from spamming the 'testing' repo with packages from
# feature branches.
if ! [[ $TRAVIS_PULL_REQUEST = "false" && $TRAVIS_BRANCH =~ ^v[0-9]+(\.[0-9]+)*$ ]] ; then
    unset CONAN_UPLOAD
fi

# Upload release tags to the stable channel and everything else to the testing
# channel.
if ! [[ $TRAVIS_TAG =~ ^v[0-9]+(\.[0-9]+)*-[0-9]+$ ]] ; then
    export CONAN_STABLE_BRANCH_PATTERN="a^" # match nothing
fi

python build.py
