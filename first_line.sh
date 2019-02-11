#! /usr/bin/env sh
sed -e '/move to next layer (30)/,$d' $1 > gcode.gcode
echo ~/gcode.tail >> gcode.gcode
echo gcode.tmp
