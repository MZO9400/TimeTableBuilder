import threading

DAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
DATA_LIST = ('room', 'day', 'section', 'course', 'instructor', 'time')


def time_comparator(t):
    """
    Time comparator function that converts hh:mm to integer-based minutes for comparison
    :param t: time object
    :return: integer based hour+minute sum
    """
    return t['hours'] * 60 + t['minutes']


def get_times(data):
    """
    Given a knowledgebase from prolog, this returns all the times in the db
    :param data: Prolog knoweldgebase query
    :return: List of times as objects
    """
    time_objs = map(lambda r: str_to_time(r['TIME']), data)
    times = []
    for time in time_objs:
        if time['start'] not in times:
            times += [time['start']]
        if time['end'] not in times:
            times += [time['end']]
    return sorted(times, key=time_comparator)


def str_to_time(time):
    """
    Converts string based time to dictionary based object
    :param time: a prolog time string
    :return: a time object
    """
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
    """
    Converts time object to string
    :param time_obj: a dictionary based time object
    :return: a time string for saving in prolog
    """
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


def time_input_to_str(input_str):
    """
    Converts input string to time string
    :param input_str: Time in hh:mm-hh:mm format
    :return: Time in prolog string format
    """
    try:
        start, end = input_str.split('-')
        if not is_time_valid(start) or not is_time_valid(end):
            raise Exception("Time is invalid")
        start_h, start_m = start.split(':')
        end_h, end_m = end.split(':')
        return 'time(:({}, {}), :({}, {}))'.format(start_h, start_m, end_h, end_m)
    except:
        return False


def is_time_valid(time):
    """
    Checks validity of time string
    :param time: hh:mm based time string
    :return: boolean
    """
    try:
        hour, minutes = time.split(':')
        hour = int(hour)
        minutes = int(minutes)
        return 0 <= hour < 24 and 0 <= minutes < 60
    except:
        return False


def pretty_string_time(time_obj):
    """
    Converts time object to hh:mm - hh:mm
    :param time_obj: Time object
    :return: Pretty string for time format
    """
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
    """
    Converts string to titlecase and removes underscores
    :param string: input form knowledgebase
    :return: pretty titlecase string
    """
    return string.replace('_', ' ').title()


def verify_time(room, day, section, course, instructor, time):
    """
    Verifies if input is in correct format
    :param room: classroom
    :param day: day from DAYS
    :param section: class/section
    :param course: course name
    :param instructor: instructor name
    :param time: time object
    :return: boolean
    """
    return day.lower() in DAYS and time_to_str(time) is not None and type_checking([room, section, course, instructor],
                                                                                   str)


def type_checking(values, test_type):
    """
    Check if all values are of type test_type
    :param values: list of variables to check
    :param test_type: type to check against
    :return: boolean
    """
    return all([isinstance(type(value), test_type) for value in values])


def run_thread(func, args=None):
    """
    Multithreading
    :param func: function ref
    :param args: arguments list
    :return: None
    """
    if args is None:
        args = []
    th = threading.Thread(target=func, args=args)
    th.start()
