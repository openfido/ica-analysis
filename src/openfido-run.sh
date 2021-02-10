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
	elif [ "${MODEL}" != "${GLMCONFIG}" -a "${MODEL}" != "${TEMPLATE}.glm" -a "${MODEL}" != "${GLMRECORD}"  ]; then
		export GLPATH="$(gridlabd --version=install)/share/gridlabd/template/$ORGANIZATION"
		if [ -d "${GLPATH}/${TEMPLATE}" ]; then
			export GLPATH="$(gridlabd --version=install)/share/gridlabd/template/$ORGANIZATION/${TEMPLATE}"
		elif [ ! -f "${GLPATH}/${TEMPLATE}.glm" ]; then
			error $E_NOTFOUND "template '${TEMPLATE}' is not found in '${GLPATH}"
		fi
		cp "$GLPATH/$TEMPLATE".* .
		gridlabd -D OUTPUT=${OPENFIDO_OUTPUT} ${GLMCONFIG} "${MODEL}" ${GLMRECORD} ${TEMPLATE}.glm
	fi
done
