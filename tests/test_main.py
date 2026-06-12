"""Tests for main module."""

import subprocess
import sys


def test_output():
    expected = """\
0 : Multiple of 5
1 : {"player": {"first_name": "Sergio", "last_name": "Ramos", "Age": 34}, "team": "Real Madrid", "even": false}
2 : {"player": {"first_name": "Kylian", "last_name": "Mbappé", "Age": 22}, "team": "PSG", "even": true}
3 : Nothing to display
4 : Nothing to display
5 : Multiple of 5
6 : {"player": {"first_name": "Luis", "last_name": "Suárez", "Age": 34}, "team": "Atlético Madrid"}.
7 : Nothing to display
8 : Process_9000_suc$esfully_run
9 : Nothing to display
10 : Multiple of 5
11 : Nothing to display
12 : Match_95687_has_fin$shed
13 : {"player": {"first_name": "Jamie", "last_name": "Vardy", "Age": 34}, "team": "Leicester", "even": false}
14 : Nothing to display
15 : Multiple of 5
16 : Process 498758 succesfully run.
"""

    result = subprocess.run(
        [sys.executable, "main.py", "data.log"],
        capture_output=True,
        text=True,
    )

    assert result.stdout == expected
