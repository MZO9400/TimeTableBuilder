def get_time(time):
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
        print("Time string malformed")
        return None
