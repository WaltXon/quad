##Walt Nixon
##2014
##QuadCopter Calculation Library

def Watts(volts, amps):
	return volts * amps

#Continuous AMP draw = (mah * 0.001) * (C continuous rating)
def ContAmpDraw (mah, Crating):
	return Crating * mah * 0.001

#Motor's max amp x 1.5 is normally my thumb rule for ESC 
def getESCrating(motorMaxAmp):
	return motorMaxAmp * 1.5

def RPM(kv, volt):
	return kv*volt

	