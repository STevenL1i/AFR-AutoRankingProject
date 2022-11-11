def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesnt exist"


def second_To_laptime(laptime_sec:float):
    return f'{int(laptime_sec//60)}:{laptime_sec - int(laptime_sec//60)*60:.3f}'


def laptime_To_second(laptime:str):
    minute = int(laptime[:laptime.find(":")])
    second = float(laptime[laptime.find(":")+1:])

    return minute*60 + second
