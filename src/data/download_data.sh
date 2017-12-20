#!/usr/bin/env bash
set -euo pipefail

mkdir -p 'data/raw'
mkdir -p 'data/cleaned'

cd 'data/raw'

echo "-- Download data from www.transparence.sante.gouv.fr"
wget "https://www.transparence.sante.gouv.fr/exports-etalab/exports-etalab.zip" -O tmp.zip

echo "-- Unzip data"
unzip tmp.zip
rm tmp.zip