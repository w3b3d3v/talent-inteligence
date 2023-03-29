from dateStore import LastDate, save_last_date, load_last_date
import datetime
import os
import pytest

FILENAME = "test.pkl"


def test_last_date_creation():
    now_ = datetime.datetime.now()
    last_date = LastDate()
    assert last_date.last_date == now_


def test_last_date_not_null():
    try:
        LastDate()
    except TypeError:
        assert TypeError is not None


def test_last_save_dating():
    last_date = LastDate(datetime.datetime.now())
    save_last_date(last_date, FILENAME)
    assert os.path.exists(FILENAME)


def test_last_save_reading():
    now_ = datetime.datetime.now()
    last_date = LastDate(now_)
    save_last_date(last_date, FILENAME)
    loaded_obj = load_last_date(FILENAME)
    assert type(loaded_obj) == LastDate
    assert loaded_obj.last_date == now_


@pytest.fixture(autouse=True)
def cleanup(request):
    yield  # run tests before this
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
