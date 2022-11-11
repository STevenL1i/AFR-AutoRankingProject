import math
from statistics import mean

def standard_deviation(data:list) -> int:
    total = 0
    avgl = sum(data) / len(data)
    for i in range(0, len(data)):
        total += pow(data[i] - avgl, 2)
    sd = math.sqrt(total / len(data))

    return sd


def laptimeToStr(lt:float) -> str:
    laptimeStr = ""
    laptimeStr += f'{int(lt/60)}:'
    laptimeStr += f'{int(lt - int(lt/60)*60):02d}'
    laptimeStr += str(lt)[str(lt).find("."):str(lt).find(".")+4]
    return laptimeStr


def strToLaptime(laptimeStr:str) -> float:
    laptime = 0
    laptime = int(laptimeStr[:laptimeStr.find(":")]) * 60
    laptime += int(laptimeStr[laptimeStr.find(":")+1:laptimeStr.find(".")])
    laptime += int(laptimeStr[laptimeStr.find(".")+1:]) / 1000

    return laptime