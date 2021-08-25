from datetime import datetime


def ts2dt(v) -> datetime:
    return datetime.fromtimestamp(v)
