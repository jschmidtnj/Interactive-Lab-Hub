#!/bin/bash

# required argument - relative to base path to folder with the project to build

# abort on errors
set -e

source_folder="lib"
output="dist.zip"

cp package.json "$source_folder"

cd "$source_folder"
yarn install --prod
cd - > /dev/null

rm -f "$output"
cd "$source_folder"
zip -r "$output" *
mv "$output" ..
rm -rf node_modules yarn.lock package.json
cd - > /dev/null

exit 0
