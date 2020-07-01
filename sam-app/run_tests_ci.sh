# This script takes three arguments:
# EXIT_IF_FAILURE: 0 = don't exist upon errors from testing, 1 = exit upon errors from testing
# RUN_LINT: 0 = don't lint, 1 = lint the code
# RUN_FORMATTER_CHECK: 0 = don't check formatting, 1 = check formatting


export EXIT_IF_FAILURE=$1
export RUN_LINT=$2
export RUN_FORMATTER_CHECK=$3


# Setup virtual env and install requirements
TMSP=$(date +"%Y_%m_%d_%H_%M_%S")
python3 -m venv venv_ci_testing
. venv_ci_testing/bin/activate
pip install -r requirements_ci_testing.txt

if [ $RUN_FORMATTER_CHECK -eq 1 ]
then
    echo "Running the black Python formatter"
    black --check --exclude "/.*venv.*|/.*.aws-sam.*" .
    if [ $? -ne 0 ]
    then
        if [ $EXIT_IF_FAILURE -eq 1 ]
        then
        echo "Some fails don't match the black format"
            exit 1
        else
            return
        fi
    fi
else
    echo "Skipping formatter"
fi

if [ $RUN_LINT -eq 1 ]
then
    echo "Linting Python but without stopping the build"
    pylint --exit-zero -ry --rcfile=tests/.pylintrc add_cw_log_error_metric add_ec2_alarms analyze_metric_frequency auto_tagger fake_cw_log_errors log_sns_message process_alarms process_cw_log_error_metric_alarm process_pipeline_failures process_pipeline_successful_events process_selected_infra_change_events > pylint_results_$TMSP.txt
    cat pylint_results_$TMSP.txt
else
    echo "Skipping Linting"
fi
sleep 1

export TESTS_FAILED=0
if [ -z ${DONT_EXIT+x} ];
then
    DONT_EXIT=0
fi

# Run the unit tests first and short circuit if they fail
SOURCE_DIRS=lutil_s3_text_lines_to_sns,hello_world
FILE_FILTER=*.py # Update this file filter to run specific test files

echo "*** SOURCE_DIRS: $SOURCE_DIRS"
echo "*** FILE_FILTER: $FILE_FILTER"

coverage run  --source $SOURCE_DIRS -m unittest discover -s tests/unit -p $FILE_FILTER
if [ $? -ne 0 ]
then
    echo "Unit tests failed, checking exit failure: $EXIT_IF_FAILURE "
    TESTS_FAILED=1
    if [ $EXIT_IF_FAILURE -eq 1 ]
    then
        echo "Stopping build"
        exit 1
    fi
fi

# Run the integration tests 
coverage run --append --source $SOURCE_DIRS -m unittest discover -s tests/integration  -p $FILE_FILTER
if [ $? -ne 0 ]
then
    echo "Integration tests failed, checking exit failure: $EXIT_IF_FAILURE "
    TESTS_FAILED=1
    if [ $EXIT_IF_FAILURE -eq 1 ]
    then
        exit 1
    fi
fi
 
# Create the coverage reports
coverage report > test_coverage_results_$TMSP.txt
cat  test_coverage_results_$TMSP.txt
coverage html

echo "Tests failed: $TESTS_FAILED"
if [ $TESTS_FAILED -eq 1 ] 
then
    echo "*** SOME TESTS FAILED"
fi


