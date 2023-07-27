#!/bin/bash

# License
# Copyright (c) 2022
# Section I
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# The person obtaining a copy of the Software meets the Use-based restrictions
# as referenced in Section II paragraph 1.
# The person obtaining a copy of the Software accepts that the Model or
# Derivatives of the Model (as defined in the "CreativeML Open RAIL-M" license
# accompanying this License) are subject to Section II paragraph 1.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


set -Eeuox pipefail

mkdir -p /repositories/"$1"
cd /repositories/"$1"
git init
git remote add origin "$2"
git fetch origin "$3" --depth=1
git reset --hard "$3"
rm -rf .git
