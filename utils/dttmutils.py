from datetime import datetime, timedelta


def next_saturday_at_3pm(ref: datetime = datetime.now()) -> datetime:
    days_until_saturday = (5 - ref.weekday() + 7) % 7
    next_saturday = ref + timedelta(days=days_until_saturday)
    return next_saturday.replace(hour=15, minute=0, second=0, microsecond=0)


def format_dttm_no_minutes(dttm: datetime) -> str:
    return dttm.strftime('%Y-%m-%dT%H:%M')


def to_dttm_no_minutes(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M")
