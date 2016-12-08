#!/bin/bash
#
# Test RAML with Abao (https://github.com/cybertk/abao).
#
#  * install abao and all dependencies
#  * set CEAGLE_ENDPOINT
#  * run this script to get RAML verified

if ! test "${CEAGLE_ENDPOINT}"
then
	cat << EOF

CEAGLE_ENDPOINT must be set to Ceagle API endpoint, for example:

    export CEAGLE_ENDPOINT=http://127.0.0.1:5000

EOF
	exit 1
fi

if ! which abao >/dev/null
then
	cat << EOF

Abao tool is not available.
Follow instructions on https://github.com/cybertk/abao to get it installed.

EOF
	exit 1
fi

WDIR=$(dirname "${0}")
cd "${WDIR}/../.."

RAML=raml/api.raml
HOOKS=raml/validation/abao_hooks.js
ABAO_VERSION=$(abao --version)

echo
echo RAML: ${RAML}
echo Abao version: ${ABAO_VERSION}
echo Start testing for API endpoint ${CEAGLE_ENDPOINT}

abao "${RAML}" --server "${CEAGLE_ENDPOINT}" --hookfiles "${HOOKS}"
RETCODE=${?}

exit ${RETCODE}
