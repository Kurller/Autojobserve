from datetime import datetime, timedelta

def parse_relative_time(relative_time):
    if 'just now' in relative_time.lower():
        return datetime.now()
    elif 'minute' in relative_time.lower():
        minutes_ago = int(relative_time.split()[0])
        return datetime.now() - timedelta(minutes=minutes_ago)
    elif 'hour' in relative_time.lower():
        hours_ago = int(relative_time.split()[0])
        return datetime.now() - timedelta(hours=hours_ago)
    elif 'day' in relative_time.lower():
        days_ago = int(relative_time.split()[0])
        return datetime.now() - timedelta(days=days_ago)
    else:
        return None