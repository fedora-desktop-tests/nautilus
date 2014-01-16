# -*- coding: UTF-8 -*-

import os
from behave_common_steps import dummy, App
from dogtail.config import config
from time import sleep, localtime, strftime
import problem
import shutil


def before_all(context):
    """Setup nautilus stuff
    Being executed before all features
    """

    try:
        # Cleanup abrt crashes
        [x.delete() for x in problem.list()]

        # Do the cleanup
        os.system("python cleanup.py > /dev/null")

        # Skip dogtail actions to print to stdout
        config.logDebugToStdOut = False
        config.typingDelay = 0.2

        # Include assertion object
        context.assertion = dummy()

        # Kill initial setup
        os.system("killall /usr/libexec/gnome-initial-setup")

        # Store scenario start time for session logs
        context.log_start_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

        context.app = App('nautilus', forceKill=False)

    except Exception as e:
        print("Error in before_all: %s" % e.message)


def after_step(context, step):
    """Teardown after each step.
    Here we make screenshot and embed it (if one of formatters supports it)
    """
    try:
        if problem.list():
            problems = problem.list()
            for crash in problems:
                if hasattr(context, "embed"):
                    context.embed('text/plain', "abrt has detected a crash: %s" % crash.reason)
                else:
                    print("abrt has detected a crash: %s" % crash.reason)

            # Crash was stored, so it is safe to remove it now
            [x.delete() for x in problems]

        # Make screnshot if step has failed
        if hasattr(context, "embed"):
            os.system("gnome-screenshot -f /tmp/screenshot.jpg")
            context.embed('image/jpg', open("/tmp/screenshot.jpg", 'r').read())

            # Test debugging - set DEBUG_ON_FAILURE to drop to ipdb on step failure
            if os.environ.get('DEBUG_ON_FAILURE'):
                import ipdb; ipdb.set_trace()  # flake8: noqa

    except Exception as e:
        print("Error in after_step: %s" % e.message)


def after_scenario(context, scenario):
    """Teardown for each scenario
    Kill nautilus (in order to make this reliable we send sigkill)
    """
    try:
        # Stop nautilus
        os.system("killall nautilus &> /dev/null")

        # Attach journalctl logs
        if hasattr(context, "embed"):
            os.system("sudo journalctl /usr/bin/gnome-session --no-pager -o cat --since='%s'> /tmp/journal-session.log" % context.log_start_time)
            data = open("/tmp/journal-session.log", 'r').read()
            if data:
                context.embed('text/plain', data)

        if hasattr(context, 'temp_dir'):
            shutil.rmtree(context.temp_dir)

        # Make some pause after scenario
        sleep(1)
    except Exception as e:
        # Stupid behave simply crashes in case exception has occurred
        print("Error in after_scenario: %s" % e.message)
