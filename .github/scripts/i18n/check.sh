#!/usr/bin/env bash

set -e

errors_file="i18n_errors.txt"
rm -f $errors_file

# Check that all translation ids start with one of: msg, action, error, icon
translations_template="locales/hexagon.pot"
(
  cat "$translations_template"
  echo
) |
  awk '/^msgid/{gsub(/"/, "", $2);print NR":"$2}' | tail -n +2 | awk -F'.' '{print $1}' |
  awk -v fname="$translations_template" -F':' '/^[0-9]*:[^msg|actions|error|icon]/{print fname":"$1":Invalid keyword `"$2"` translation id should start with one of: msg,action,error,icon"}' >>$errors_file

# Check that no translation string is empty
for locale in locales/**/LC_MESSAGES/hexagon.po; do
  (
    cat "$locale"
    echo
  ) |
    awk '/^msgstr ""$/{getline;print NR-1":"$0}' |
    awk -v fname="$locale" '/^[0-9]*:\s*$/{print fname":"$0"translation string should not be empty"}' >>$errors_file
done

# Check that no translation string is fuzzy (#, fuzzy)
for locale in locales/**/LC_MESSAGES/hexagon.po; do
  (
    cat "$locale"
    echo
  ) |
    awk '/^#, fuzzy$/{getline;print NR-1":"$0}' |
    awk -v fname="$locale" -F':' '/^[0-9]+:/{print fname":"$1":translation string is fuzzy"}' >>$errors_file
done

if [ -s $errors_file ]; then
  echo "Some translation files contain errors"
  cat $errors_file
  exit 1
else
  echo "🥳 all strings have a translation 🗺"
  exit 0
fi
