import pytest


def test_context_works():
    from django_timetravel import timetravel, get_tt_ts
    assert get_tt_ts() is None

    with timetravel(314):
        assert get_tt_ts() == 314


def test_wrong_destination():
    from django_timetravel import timetravel
    with pytest.raises(Exception):
        with timetravel('wrong'):
            pass
