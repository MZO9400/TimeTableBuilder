import threading

DAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')


def str_to_time(time):
    try:
        time_arr = time.split('time')[1][1:-1].split(',')
        time_arr = [
            int(time_str.replace(':', '').replace(')', '').replace('(', '').strip())
            for time_str in time_arr
        ]
        time_obj = {
            'start': {
                'hours': time_arr[0],
                'minutes': time_arr[1]
            },
            'end': {
                'hours': time_arr[2],
                'minutes': time_arr[3]
            }
        }
        return time_obj
    except (ValueError, IndexError, AttributeError):
        if time_to_str(time):
            return time
        return None


def time_to_str(time_obj):
    try:
        return 'time(:({}, {}), :({}, {}))'.format(
            time_obj['start']['hours'],
            time_obj['start']['minutes'],
            time_obj['end']['hours'],
            time_obj['end']['minutes'],
        )
    except (ValueError, IndexError, AttributeError):
        if str_to_time(time_obj):
            return time_obj
        return None


def pretty_string_time(time_obj):
    try:
        return '{}:{} - {}:{}'.format(
            time_obj['start']['hours'],
            time_obj['start']['minutes'],
            time_obj['end']['hours'],
            time_obj['end']['minutes']
        )
    except (ValueError, IndexError, AttributeError):
        return None


def pretty_string_name(string):
    return string.replace('_', ' ').title()


def verify_time(room, day, section, course, instructor, time):
    return day in DAYS and time_to_str(time) is not None and type_checking([room, section, course, instructor], str)


def type_checking(values, test_type):
    return all([isinstance(type(value), test_type) for value in values])


def run_thread(func, args=None):
    if args is None:
        args = []
    th = threading.Thread(target=func, args=args)
    th.start()
