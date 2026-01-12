from datetime import timedelta, datetime

def generate_time_slots(start, end, interval=30):
    slots = []
    current = datetime.combine(datetime.today(), start)

    while current.time() < end:
        slots.append(current.time())
        current += timedelta(minutes=interval)

    return slots
