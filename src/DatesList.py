from typing import List, Dict

from datetime import datetime, timedelta


def add_dates_to_weekly_list(weekly_list: List, key_name: str) -> List[Dict]:
    """
    Converts a list of values to a list of dicts with a date string
    :param weekly_list: List of numbers, each number represents a value oor a week
    :param key_name: Dict key name of values
    :return: New list containing dicts
    """
    n_weeks = len(weekly_list)
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday())
    start_date = last_monday - timedelta(weeks=n_weeks - 1)
    list_with_dates = []
    for i in range(n_weeks):
        list_with_dates.append({
            key_name: weekly_list[i],
            "date": start_date,
        })
        start_date += timedelta(weeks=1)
    return list_with_dates

def list_values_only(cls, list_with_dates: List[Dict]) -> List[int]:
    """
    Simplifies a list of dicts containing a date and a value to values only
    :param list_with_dates: List containing Dicts with dates and values
    :return: List of values only
    """
    return list(
        map(
            lambda el: list(el.values())[0],
            list_with_dates,
        )
    )