#!/usr/bin/env bash

for locale in locales/**/LC_MESSAGES/hexagon.po; do
  (cat "$locale"; echo) \
    | awk '/^msgstr ""$/{getline;print NR-1":"$0}' \
    | awk -v fname="$locale" '/^[0-9]*:\s*$/{print fname":"$0"translation string should not be empty"}' >> errors.txt
done

if [ -s errors.txt ]; then
  echo "Some translation files contain errors"
  cat errors.txt
  exit 1
else
  echo "🥳 all strings have a translation 🗺"
  exit 0
fi
