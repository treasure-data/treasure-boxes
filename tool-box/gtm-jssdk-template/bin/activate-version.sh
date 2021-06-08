#!/usr/bin/env bash

DRYRUN='--dryrun'
VERSION=''
WAIT=''
BUCKET='td-cdn-experiment'
REGION="--region us-east-2"
PROD=''
FOLDER='gtm'

while [ $# -gt 0 ]; do
  case "$1" in
    -f|--force)
      DRYRUN=""
      ;;
    --prod)
      BUCKET='td-cdn'
      REGION=''
      PROD='--prod'
      ;;
    --version=*)
      VERSION="${1#*=}"
      ;;
    --wait)
      WAIT='--wait'
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done

if [ "$VERSION" = "" ]; then
  echo "You must supply a --version"
  exit 1
fi

TO_VERSION=$(echo $VERSION | sed 's/\.[-a-zA-Z0-9]*$//g')

set -euo pipefail

aws --profile dev-frontend                      \
  s3 sync "s3://${BUCKET}/${FOLDER}/${VERSION}/" "s3://${BUCKET}/${FOLDER}/${TO_VERSION}/" \
    ${DRYRUN}                                   \
    ${REGION}                                   \
    --acl 'public-read'                         \
    --cache-control 'public, max-age=315360000' \

if [ "$DRYRUN" != '' ]; then
  exit 0
fi

./bin/invalidate-release.sh --version=${TO_VERSION} ${PROD} ${WAIT}
