#!/bin/bash
set -ex

workdir=$(dirname $0)
yamllint -c $workdir/ramllint.yaml $(find . -not -path '*/\.*' -type f -name '*.raml')
