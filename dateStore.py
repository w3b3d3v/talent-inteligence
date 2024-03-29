import pickle
import datetime


class LastDate():
    def __init__(self, last_date: datetime.datetime) -> None:
        assert last_date is not None, "last date cannot be null"
        self.last_date = last_date


def save_last_date(obj: LastDate, filename: str = "last_date.pkl"):
    try:
        with open(filename, "wb") as f:
            pickle.dump(obj=obj, file=f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(e)


def load_last_date(filename: str = "last_date.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(e)
