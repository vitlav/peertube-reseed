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
from pathlib import Path
from typing import List


def list_dirs(directory: Path) -> List[Path]:
    """
  List directories in the given directory
  """
    return [path for path in directory.iterdir() if path.is_dir()]
