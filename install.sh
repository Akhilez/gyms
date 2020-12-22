#!/bin/bash
set -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

ENV_NAME=$1

if [[ $ENV_NAME == "" ]]; then
  echo "Please pass the gym environment name"
  exit 1
fi

cd $DIR/$ENV_NAME

pip install -e .
