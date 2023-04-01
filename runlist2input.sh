#!/usr/bin/env bash

runlist=$1; shift

tail -n +2 $runlist | awk '{print $2}' | sort | uniq
