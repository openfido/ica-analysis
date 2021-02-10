set -u
set -e
set -x

for VAR in $DEFAULT_VARLIST; do
	gridlabd template config set $VAR $(printenv $VAR)
done
cp ${OPENFIDO_INPUT}/* .
for MODEL in $(ls -1 ${MODELNAME:-*.glm}); do
	if [ -z "${MODEL}" -a ! -f "${MODEL}" ]; then
		error $E_NOTFOUND "file '${MODEL}' is not found"
	elif [ "${MODEL}" != "${GLMCONFIG}" -a "${MODEL}" != "${TEMPLATE}" -a "${MODEL}" != "${GLMRECORD}"  ]; then
		gridlabd -D OUTPUT=${OPENFIDO_OUTPUT} ${GLMCONFIG} "${MODEL}" ${GLMRECORD} "ica_analysis.glm"
	fi
done