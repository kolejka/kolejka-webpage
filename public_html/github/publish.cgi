#!/bin/bash
# vim:ts=4:sts=4:sw=4:expandtab

MYSELF="$(readlink -f "$(which "${0}")")"
OFFICE="$(dirname "${MYSELF}")"

SECRET="$(cat ~/github_secret)"

if [ "${QUERY_STRING}" != "secret=${SECRET}" ]; then
    echo "Content-Length: 4"
    echo ""
    echo "FAIL"
    exit
fi

screen -dmS publish /home/kolejka/bin/kolejka-publish

echo "Content-Length: 2"
echo ""
echo "OK"
