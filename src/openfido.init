set -u
set -e
set -x

# Defaults
export DEFAULT_MODELNAME="*.glm"
export DEFAULT_GLMCONFIG=""
export DEFAULT_GLMRECORD=""
export DEFAULT_TEMPLATE="ica_analysis.zip"
export DEFAULT_VARLIST="GITHUBUSERCONTENT ORGANIZATION GITUSER GITREPO GITBRANCH"

# Check and load startup environment
getconfig MODELNAME "$DEFAULT_MODELNAME"
getconfig GLMCONFIG "$DEFAULT_GLMCONFIG"
getconfig GLMRECORD "$DEFAULT_GLMRECORD"
getconfig TEMPLATE "$DEFAULT_TEMPLATE"
for VAR in $DEFAULT_VARLIST; do
	getconfig $VAR $(gridlabd template config get $VAR)
done

