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


def delimiter_string(string:str, length:int):
    outputString = f' {string} '
    while len(outputString) < length:
        outputString = "-" + outputString + "-"
    
    outputString = outputString[:length]
    return outputString


def get_LPdict(LPsettings:dict) -> dict:
    LPdict = {}
    allkey = LPsettings.keys()
    allkey_list = []
    for key in allkey:
        allkey_list.append(int(key))
    allkey_list.sort()
    for i in range(0,len(allkey_list)):
        try:
            for j in range(int(allkey_list[i]), int(allkey_list[i+1])):
                LPdict[j] = LPsettings[str(allkey_list[i])]
        except IndexError:
            pass
    
    return LPdict
