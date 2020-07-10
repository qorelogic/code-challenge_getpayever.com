#!/bin/bash

for fp in `ls *.css`; do html5-print -s 4 -t css ${fp}  2> /dev/null > ${fp}.html5print; echo "${fp} done"; done
cat *.html5print > all.css.html5print
cat *.css > all.css
