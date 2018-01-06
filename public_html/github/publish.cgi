#!/bin/bash
# vim:ts=4:sts=4:sw=4:expandtab

SECRET="$(cat ${HOME}/github_secret)"

if [ "${QUERY_STRING}" != "secret=${SECRET}" ]; then
    echo "Content-Length: 4"
    echo ""
    echo "FAIL"
    exit
fi

screen -dmS github-publish-kolejka "${HOME}/bin/github-publish-kolejka"

echo "Content-Length: 2"
echo ""
echo "OK"
