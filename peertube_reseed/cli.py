"""
peertube-reseed
Copyright (C) 2021 LoveIsGrief

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
from typing import List


class CommaSeparatedOption(object):
    def __init__(self, options: List[str]):
        self.options = options

    def __call__(self, string: str) -> List[str]:
        result = []
        for separated in string.split(","):
            separated = separated.strip()
            if separated not in self.options:
                raise argparse.ArgumentTypeError("Option is not allowed")
            result.append(separated)

        return result
