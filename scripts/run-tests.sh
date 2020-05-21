#!/bin/sh

export POWERTOOLS_TRACE_DISABLED=1

pytest --cov=src --cov-report=html tests/