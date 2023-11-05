#!/usr/bin/env bash

set -e

printer_path="hexagon/support/output/printer/en.py"

if [ "$1" = "fallback" ]; then
  echo "copying en to printer location: $printer_path"
  cp "locales/en/LC_MESSAGES/hexagon.mo" "$printer_path"
  exit 0
fi

rm -f "$printer_path"

pygettext3 -d hexagon -o locales/hexagon.pot hexagon
for locale in locales/**/LC_MESSAGES/hexagon.po; do
  l=$(echo "$locale" | cut -d/ -f2)
  echo "merging messages to $locale"
  msgmerge --update "$locale" locales/hexagon.pot
  echo "formatting messages to $locale"
  msgfmt -o "locales/$l/LC_MESSAGES/hexagon.mo" "$locale"
done

echo "copying en to printer location: $printer_path"
cp "locales/en/LC_MESSAGES/hexagon.mo" "$printer_path"
