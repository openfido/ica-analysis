#!/bin/bash
export OPENFIDO_AUTOINSTALL=no
export OPENFIDO_DEBUG=no
export OPENFIDO_INPUT
export OPENFIDO_OUTPUT
for OPENFIDO_INPUT in $(find $PWD/autotest -name 'input_*' -type d -print -prune); do
	OPENFIDO_OUTPUT=$PWD/autotest/output_${OPENFIDO_INPUT##*_}
	rm -rf $OPENFIDO_OUTPUT
	mkdir $OPENFIDO_OUTPUT
	echo "Running $OPENFIDO_INPUT..."
	( sh openfido.sh </dev/null 2>$OPENFIDO_OUTPUT/stderr || grep -v '^+' $OPENFIDO_OUTPUT/stderr ) | tee $OPENFIDO_OUTPUT/stdout
done
