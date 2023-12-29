#!/bin/bash

echo "Start script: $0"
echo "Arguments:"
echo "  First argument is: $1"
echo "  Second argument is: $2"

ppprint() {
	echo "Got *** $1 *** "
}

echo "Create Target Dir"
data_dir=$1
target_dir="${data_dir}/$2"
mkdir "${target_dir}"

echo "Contents of $data_dir"
find "${data_dir}" -iname  "Participant *.zip" | xargs -I "{}" unzip {} -d "${target_dir}"



