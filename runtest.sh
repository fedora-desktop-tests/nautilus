#!/bin/bash
sudo service gdm stop
env GIT_SSL_NO_VERIFY=true git submodule update --init --recursive
# Here we store exit code for the task in tmp file
# Because we need a report
# TODO: write a better rhts-run-simple-test
sudo -u test dogtail-run-headless-next "behave -t $1 -k -f html -o /tmp/report_$TEST.html -f plain"; rc=$?
RESULT="FAIL"
if [ $rc -eq 0 ]; then
  RESULT="PASS"
fi
rhts-report-result $TEST $RESULT "/tmp/report_$TEST.html"
exit $rc
