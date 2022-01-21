#!/usr/bin/env bash

pygettext3 -d hexagon -o locales/hexagon.pot hexagon
for locale in locales/**/LC_MESSAGES/hexagon.po; do
  l=$(echo "$locale" | cut -d/ -f2)
  echo "merging messages to $locale"
  msgmerge --update "$locale" locales/hexagon.pot
  echo "formatting messages to $locale"
  msgfmt -o "locales/$l/LC_MESSAGES/hexagon.mo" "$locale"
done
