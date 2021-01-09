#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 09:42:40 2020

@author: saraborchers
"""
import gridlabd
import sys

for arg in sys.argv:
	gridlabd.command(arg)
gridlabd.start("wait")
