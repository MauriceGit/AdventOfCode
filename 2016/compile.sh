#!/usr/bin/env bash

allCPP="*.cpp"
if [ "$1" -a "$1" != "clean" ]; then
    allCPP="$1"
fi

for f in $allCPP; do
    exe=$(basename -s .cpp "$f")
    if [ "$1" == "clean" ]; then
        rm -f "$exe"
    else
        g++-12 -o "$exe" "$f" -std=c++2b -O3 -lfmt
    fi
done
