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

##TODO Calculate Current Directly (A = Kp * D^4 * P * Kv ^ 3 * V^2)

##TODO  have an Ideal Motor with a Kv of 750 and a 12x10 propeller.  I want to get 3 minutes of full throttle duration out of my Ideal Cells (1 Ah).  How many cells should I use?

# This is a very challenging question. To answer it, you will first need to combine our two different power equations. Namely:

# Power = Volts x Amps
# Power = Kp * D^4 * P * RPM^3

# Into:

# Volts x Amps = Kp * D ^ 4 * P * RPM ^ 3

# Then, consider the fact that the RPM is equal to the input voltage times the motor Kv:

# RPM = Volts x Kv
# Volts x Amps = Kp * D ^ 4 * P * RPM ^ 3

# Therefore:

# Volts x Amps = Kp * D ^ 4 * P * (Volts x Kv) ^ 3
# Volts x Amps = Kp * D ^ 4 * P * Volts ^ 3 * Kv ^ 3
# 1 / Volts ^ 2 = ( Kp * D ^ 4 * P * Kv ^ 3 ) / Amps
# Volts ^ 2 = Amps / (Kp * D ^ 4 * P * Kv ^ 3)

# Lets go ahead and add in our values:

# Volts ^ 2 = Amps / (1.25 * 1 ^ 4 * .833 * .75 ^ 3)
# Volts ^ 2 = Amps / .44

# To determine the current draw we simply have to use our duration equation:

# Duration = 60 / Current
# Current = 60 / Duration
# Current = 60 / 3
# Current = 20

# Plugging in 20 amps, we get:

# Volts ^ 2 = 20 / .44
# Volts ^ 2 = 45.5
# Volts = 6.75


##TODO Implement this:
# Answering the question based on a given motor

# It is a little more common for a modeler to design an airplane around a motor than it is a propeller, isn't it?  To answer the question this way we can approach it using the following steps:

# Select a motor and note its Kv value.
# Select a current draw.
# Compute the number of cells required to create the desired power given the amperage you selected.
# Multiply the number of cells by the Kv to determine the RPM.
# Select a propeller based on the RPM and power.  This step requires some juggling.
# For my answer I will select a motor with a Kv of 1000.  I will choose a current draw of 25 amps.  How many cells do I need to produce 500 watts?

# Power = Volts x Amps
# Power = Ideal Cells x Amps
# Ideal Cells = Power / Amps
# Ideal Cells = 500 / 25
# Ideal Cells = 20

# Now I can determine how fast my motor will be spinning the propeller based on the cell count and the motor's Kv.

# RPM = Voltage x Kv
# RPM = 20 x 1000
# RPM = 20000

# Now, the tricky part.  We need to choose a propeller that will absorb 500 watts at 20000 RPM.  Look at our power formula and see what we have:

# Power (Watts) = Kp * D^4 * P * RPM^3
# 500 = 1.25 * D ^ 4 * P * (20 ^ 3)
# 500 = 1.25 * D ^ 4 * P * 8000
# 500 = 10000 * D ^ 4 * P
# D ^ 4 * P = .05

# The problem is that we can't go any farther without picking a pitch or a diameter.   If we pick poorly the first time we will have to keep trying until we get a propeller that makes sense.  For example, if I pick "10" for my pitch and compute the diameter, I will find:

# D ^ 4 * P = .05
# D ^ 4 * .833 = .05
# D ^ 4 = .06
# D = .49

# Remember that we are specifying diameter in pitch in feet.  So the above tells us that a 10 inch pitch propeller must have a 6 inch diameter to absorb 500 watts at 20000 RPM.  If you stop there then you have answered the original question satisfactorily because we are still operating in the Ideal World, but in the real world where you and I fly our airplanes, nobody manufactures a 6x10 propeller!  We'll have to try again using a lower value for pitch.  Lets try a 5 inch pitch propeller and see what diameter we come up with:

# D ^ 4 * P = .05
# D ^ 4 * .42 = .05
# So a 7x5 inch propeller will work.  Putting it all together we have determined that a motor with a Kv of 1000 will require 20 cells at 25 amps to spin a 7x5 inch propeller at 20000 RPM, producing 500 watts.
# D ^ 4 =  .12
# D = .59 feet = 7 inches
