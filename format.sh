#!/bin/sh

set -eu

pandoc \
    --self-contained \
    --standalone \
    --css vmdb2.css \
    --toc \
    --number-sections \
    -o vmdb2.html \
    vmdb2.mdwn vmdb/plugins/*.mdwn

pandoc \
    --pdf-engine=xelatex \
    --toc \
    --number-sections \
    -Vdocumentclass=report \
    -Vgeometry:a4paper \
    -Vfontsize:12pt \
    -Vmainfont:FreeSerif \
    -Vsansfont:FreeSans \
    -Vmonofont:FreeMonoBold \
    '-Vgeometry:top=2cm, bottom=2.5cm, left=2cm, right=1cm' \
    -o vmdb2.pdf \
    vmdb2.mdwn vmdb/plugins/*.mdwn
