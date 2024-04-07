# Copyright (C) 2023-present The Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from cl.runtime.configuration.package_aliases import PackageAliases


def test_smoke():
    """Test package aliases."""

    # Add using __init__
    obj = PackageAliases(
        {
            "abc": "a",
            "def.ghi": "d"
        }
    )

    # Add using methods
    obj.add_alias("uvw.*.xyz", "u")
    obj.add_alias("qrs?.*", "q")
    obj.add_alias("a123", "n")

    # Try adding invalid patterns
    with pytest.raises(RuntimeError):
        obj.add_alias("Abc", "u")
        obj.add_alias(".abc", "u")
        obj.add_alias("abc.", "u")
        obj.add_alias("abc..def.", "u")

    assert obj.get_alias("abc") == "a"
    assert obj.get_alias("abc.def") == "a"
    assert obj.get_alias("abcdef") is None

    assert obj.get_alias("def.ghi") == "d"
    assert obj.get_alias("def.ghi.jkl") == "d"
    assert obj.get_alias("def.ghijkl") is None

    assert obj.get_alias("uvw.xyz") is None
    assert obj.get_alias("uvw.abc.xyz") == "u"
    assert obj.get_alias("uvw.abc.def.xyz") == "u"

    assert obj.get_alias("qrs") is None
    assert obj.get_alias("qrs.abc") is None
    assert obj.get_alias("qrst") is None
    assert obj.get_alias("qrst.abc") == "q"

    assert obj.get_alias("a123") == "n"
    assert obj.get_alias("a123.def") == "n"
    assert obj.get_alias("a123def") is None

    with pytest.raises(RuntimeError):
        obj.get_alias("Abc")
        obj.get_alias(".abc")
        obj.get_alias("abc.")
        obj.get_alias("abc..def.")
        obj.get_alias("abc.*.def")
        obj.get_alias("abc?.def")
        obj.get_alias("abc[.]def")


if __name__ == "__main__":
    pytest.main([__file__])
