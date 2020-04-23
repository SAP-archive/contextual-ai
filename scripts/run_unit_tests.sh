#!/usr/bin/env bash

echo 'Running Unittests [nosetests] ...'
which python3.6
echo 'Python version'
echo $(which python3.6)
echo $(which python3.6)

echo $( $(which python3.6) --version)
echo $( $(which python3.6) --version)

$(which pip3) install virtualenv --user

V_ENV_DIR=nosetests-env
#virtualenv ${V_ENV_DIR} --python=/usr/bin/python3
$(which python3.6) -m virtualenv ${V_ENV_DIR} --python=$(which python3.6)
. ${V_ENV_DIR}/bin/activate

PYTHON_VENV_PATH=$(which python3.6)


echo 'Start...'
echo $(which python3.6)
PIP_VENV_PATH=$(which pip3)
echo $(which pip3)

echo 'End...'


$PYTHON_VENV_PATH $PIP_VENV_PATH install -r requirements.txt  \
    -i http://nexus.wdf.sap.corp:8081/nexus/content/groups/build.snapshots.pypi/simple/ \
    --trusted-host nexus.wdf.sap.corp
$PYTHON_VENV_PATH $PIP_VENV_PATH install mock responses nosexcover pylint==2.3.0  \
    --pre -i http://nexus.wdf.sap.corp:8081/nexus/content/groups/build.snapshots.pypi/simple/  \
    --trusted-host nexus.wdf.sap.corp

$PYTHON_VENV_PATH $PIP_VENV_PATH freeze

nosetests --tests=./tests \
    -v --nologcapture --exe --with-xunit --with-xcoverage \
    --cover-package=./xai \
    --cover-erase  --xunit-file=nosetests_result.xml


# save the exit code here, so we can exit the test later after the clean-up
test_exit_code=$?
echo "test exit code was ${test_exit_code}"

# ========== remove the virtual env folder
rm -r $V_ENV_DIR

exit ${test_exit_code}
