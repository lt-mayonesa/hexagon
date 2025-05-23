#!/usr/bin/env bash

# This script is used to test the bash module.
echo "Hello from bash module!"
echo "arguments:"
for i in "$@"; do
    echo "$i"
done