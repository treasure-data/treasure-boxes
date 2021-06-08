#!/usr/bin/env bash

set -euo pipefail
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
VERSION=$(jq -r '.version' < "${ROOT_DIR}/package.json")
WAIT=0
FOLDER='gtm'
BUILT_FILE='td-gtm.js'

PRODUCTION_OPTIONS='--distribution-id E2L8AHDWNOCKE'
TEST_OPTIONS="--distribution-id E1F7ECRVBF3EX2 --region us-east-2"
PROD=''

DISTRIBUTION_OPTIONS=$TEST_OPTIONS

while [ $# -gt 0 ]; do
  case "$1" in
    --version=*)
      VERSION="${1#*=}"
      ;;
    --wait)
      WAIT=1
      ;;
    --prod)
      DISTRIBUTION_OPTIONS=${PRODUCTION_OPTIONS}
      PROD='--prod'
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done

JSON=$(aws --profile dev-frontend                            \
  cloudfront create-invalidation                             \
    ${DISTRIBUTION_OPTIONS}                                  \
    --paths /${FOLDER}/${VERSION}/${BUILT_FILE})

INVALIDATION_ID=$(echo $JSON | jq -r '.Invalidation.Id')
echo Created Invalidation: $INVALIDATION_ID

if [ $WAIT -eq 1 ]; then
  echo "Waiting until invalidation complete"
  ./bin/check-invalidation.sh --id=$INVALIDATION_ID ${PROD}
fi
