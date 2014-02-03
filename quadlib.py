##Walt Nixon
##2014
##QuadCopter Calculation Library
import tabulate



def Watts(volts, amps):
    """returns watts given volts and amps as inputs"""
    return volts * amps

def Amps(watts, volts):
    """returns Amps (Current) give watts (Power) and volts (Voltage)"""
    return watts / volts

#Continuous AMP draw = (mah * 0.001) * (C continuous rating)
def ContiniousAmpDraw (mah, Crating):
    """returns the continious aperage a battery can provide given its capacity (mah) and it'c C-rating"""
    return Crating * mah * 0.001

#Motor's max amp x 1.5 is normally my thumb rule for ESC 
def getESC_rating(motorMaxAmp):
    """returns the proper ESC rating for a motor given the motor's max amperage (A)"""
    return motorMaxAmp * 1.5

def RPM(Kv, volts):
    """Kv = voltage propConstant,   volts = voltage"""
    return Kv*volt

def FeetToInches(measurement):
    return measurement * 12.0

def InchesToFeet(measurement):
    return measurement / 12.0

def getKp(propType):
    """returns the propeller contant for the below listed types of props"""
    if propType == 'generic':
        return 1.31
    elif propType == 'APC':
        return 1.11
    elif prorType == 'carbon':
        return 1.18


def Power_watts(Kp, D, P, RPM):
    """Kp = propConstant,   D = Diameter in Feet,   P = Pitch in Feet, 
    RPM = Rev. Per Minute (specified in Thousands)"""
    return (Kp*(D**4)*P*(RPM**3))

def PredictCurrentDraw(Kv, D, P):
    """For a motor with a given Kv value and a prop with a diameter (D) in inches and pitch (P) in inches,
     show a table of Power, Voltage and Current"""
    cases = []
    for RPM in (4000,6000,8000,10000,12000,14000):
        power = Power_watts(getKp('APC'), InchesToFeet(D), InchesToFeet(P), RPM/1000.0)
        voltage = RPM / Kv
        current = power * voltage
        cases.append((RPM, power, voltage, current))
    print "{0}    {1}     {2}   {3}". format('RPM', 'POWER', 'VOLTAGE', 'CURRENT')
    print tabulate.tabulate(cases)
    
PredictCurrentDraw(1500, 8.0, 4.0) 
