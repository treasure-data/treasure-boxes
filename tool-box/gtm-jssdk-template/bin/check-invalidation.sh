#!/usr/bin/env bash

set -euo pipefail
ID=''

PRODUCTION_OPTIONS='--distribution-id E2L8AHDWNOCKE'
TEST_OPTIONS="--distribution-id E1F7ECRVBF3EX2 --region us-east-2"

DISTRIBUTION_OPTIONS=$TEST_OPTIONS

while [ $# -gt 0 ]; do
  case "$1" in
    --id=*)
      ID="${1#*=}"
      ;;
    --prod)
      DISTRIBUTION_OPTIONS=$PRODUCTION_OPTIONS
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done

while [ $(aws --profile dev-frontend     \
  cloudfront get-invalidation         \
    ${DISTRIBUTION_OPTIONS}           \
    --id ${ID} | jq -r '.Invalidation.Status') = "InProgress" ]; do
      printf '.'
      sleep 4
    done

echo Invalidation $(aws --profile dev-frontend     \
  cloudfront get-invalidation         \
    ${DISTRIBUTION_OPTIONS}           \
    --id ${ID} | jq -r '.Invalidation.Status')
