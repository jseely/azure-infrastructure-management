#!/usr/bin/env bash -u
pushd $REPO &>/dev/null
if [[ "$(git status)" == "On branch"* ]]
then
  export BRANCH="$(echo $(git status) | awk '{print $3}')"
else
  export BRANCH="$(echo $(git status) | awk '{print $4}')"
fi
  echo "BRANCH=$BRANCH"
popd &>/dev/null

export DEPLOY_NAME="$PROJECT_SHORTNAME-$BRANCH"
echo "DEPLOY_NAME=$DEPLOY_NAME"
export KEYVAULT="$PROJECT_SHORTNAME-kv"
echo "KEYVAULT=$KEYVAULT"
