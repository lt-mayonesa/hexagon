#!/usr/bin/env bash

# This script is used to test the bash module.
echo "bash_module from tests_e2e/execute_tool_relative_to_paths/.dotted_dir/level_2"
echo "arguments:"
for i in "$@"; do
    echo "$i"
done