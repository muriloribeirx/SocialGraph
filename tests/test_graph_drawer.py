import os
from graph_drawer import safe_filename


def test_safe_filename_removes_forbidden_chars():
    a = 'Inteligência Artificial: riscos, benefícios e uso responsável'
    b = 'Explainable AI: Interpreting, Explaining and Visualizing *Deep* Learning?'
    fname = safe_filename(a, b)
    # should end with .html
    assert fname.endswith('.html')
    # should not contain characters invalid on Windows
    for c in '<>:"/\\|?*':
        assert c not in fname


def test_safe_filename_short_and_hash():
    long_a = 'a' * 400
    long_b = 'b' * 400
    fname = safe_filename(long_a, long_b, maxlen=120)
    assert len(fname) <= 120
    assert '_' in fname
