# Copyright 2017  Lars Wirzenius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =*= License: GPL-3+ =*=


all: yarns.html

yarns.pdf: $(yarns) Makefile
	pandoc --chapters --toc -o yarns.pdf *.yarn

yarns.html: $(yarns) Makefile ugly.css
	pandoc -H ugly.css -f markdown+smart --toc \
		--top-level-division=chapter --number-sections \
                -V geometry:lettersize \
		--standalone --self-contained -o yarns.html *.yarn
