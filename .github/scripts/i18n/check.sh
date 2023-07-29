#!/usr/bin/env bash

set -e

translations_template="locales/hexagon.pot"
(
  cat "$translations_template"
  echo
) |
  awk '/^msgid/{gsub(/"/, "", $2);print NR":"$2}' | tail -n +2 | awk -F'.' '{print $1}' |
  awk -v fname="$translations_template" -F':' '/^[0-9]*:[^msg|action|error|icon]/{print fname":"$1":Invalid keyword `"$2"` translation id should start with one of: msg,action,error,icon"}' >>errors.txt

for locale in locales/**/LC_MESSAGES/hexagon.po; do
  (
    cat "$locale"
    echo
  ) |
    awk '/^msgstr ""$/{getline;print NR-1":"$0}' |
    awk -v fname="$locale" '/^[0-9]*:\s*$/{print fname":"$0"translation string should not be empty"}' >>errors.txt
done

if [ -s errors.txt ]; then
  echo "Some translation files contain errors"
  cat errors.txt
  exit 1
else
  echo "🥳 all strings have a translation 🗺"
  exit 0
fi
