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

pushd "${OFFICE}" >/dev/null 2>&1

git pull >/dev/null 2>&1

popd >/dev/null 2>&1

echo "Content-Length: 2"
echo ""
echo "OK"
