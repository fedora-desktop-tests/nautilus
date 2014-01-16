#!/bin/env python
# This cleans existing nautilus data

import shutil
import sys

if len(sys.argv) > 1:
    shutil.rmtree(sys.argv[1])
