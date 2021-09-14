#!/bin/bash

# required argument - relative to base path to folder with the project to build

# abort on errors
set -e

source_folder="src"

# delete gitignored files
cd "$source_folder"
git clean -xdf
cd - > /dev/null

dist_folder="dist"

rm -rf "$dist_folder"
mkdir "$dist_folder"

cp -LR "$source_dir/." "$dist_folder"

exit 0
