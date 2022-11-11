
def flvalidator(resultlist:list):
    """
    parameter resultlist came from following query :
    query = f'SELECT driverName, team, driverGroup, GP, \
            startPosition, finishPosition, fastestLap, driverStatus \
            WHERE GP = "{race}" and driverGroup = "{drivergroup}" \
            ORDER BY finishPosition ASC;'
    """

    countdriver = len(resultlist)
    fl_list = resultlist[:int(len(resultlist)/4*3 + 0.8)]
    
    fl = "9:59.999"
    fldriver = ''
    flteam = ''
    validation = 0
    gp = ''
    group = ''

    for driver in fl_list:
        driver = list(driver)
        group = driver[2]
        gp = driver[3]
        finishposition = driver[5]
        status = driver[7]

        if driver[6] < fl: # driver[6] = thefl
            fl = driver[6]
            fldriver = driver[0]
            flteam = driver[1]
            
            if finishposition < countdriver/2 + 0.5 and status == "FINISHED":
                validation = 1
            else:
                validation = 0
    
    return fldriver, flteam, validation, gp, group