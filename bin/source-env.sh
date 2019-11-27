#!/usr/bin/env sh

# shellcheck disable=SC2046
export $(grep -Ev '^#' .flaskenv | xargs)
