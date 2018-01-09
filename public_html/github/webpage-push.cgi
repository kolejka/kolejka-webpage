#!/bin/bash
# vim:ts=4:sts=4:sw=4:expandtab

if [ "${HOME}" == "" ]; then
    HOME="$(getent passwd |grep "^$(whoami):" |cut -d : -f 6)"
    export HOME
fi

SECRET="$(cat ${HOME}/github_secret)"

if [ "${QUERY_STRING}" != "secret=${SECRET}" ]; then
    echo "Status: 403 Forbidden"
    echo "Content-Length: 4"
    echo ""
    echo "FAIL"
    exit 
fi

screen -dmS github-push-webpage "${HOME}/bin/github-push-webpage"

echo "Content-Length: 2"
echo ""
echo "OK"
