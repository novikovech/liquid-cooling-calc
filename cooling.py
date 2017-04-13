# -*- coding: utf-8 -*-
import locale
os_encoding = locale.getpreferredencoding()
#let's figure out our cooling loop!

#user settings:

pump_flow = 100 #l/h
pump_head = 2 #meters H2O
power = 500 #W, max power dissipated by the cooling system. 
ethanol = True #Are you using ethanol coolant instead of water?
fan_cfm = 100 # cfm of the fans cooling the radiator (add cfm's of all parallel fans)

#advanced user settings:
restriction_power = 1.4 #exponent used in the equation governing loop restriction, default is 1.4
flow_c = 0.0006565 #multiplier used in the equation governing loop restriction, default is 0.0006565
#Note: above default values were obtained by averaging performance of some mid-range 120x3 radiators. 
#Change this only if you have better data about your actual radiator or loop. 
# pressure difference (in m H2O) = flow_c * flow (ml/s) ^ restriction_power

flow_override = 0 #if you know the actual flow in your loop, you can set this value. This will ignore pump specs above





































#helper functions:
def degrees(deg):
	return "%.1f%sC"%(deg, u"\u00b0")
	
def H2O():
	return "%s"%u"H\u00B2O"
	
	
	
#some constants:
kg_in_foot = 0.0366 #kilograms in a cubic foot of air.
cp_air = 1.004 #kJ/kg.K
cp_water = 4.184 #kJ/kg.K
cp2_ethanol = 2.44 #kJ/kg.K
p_ethanol = 0.789 #kg/l
cp_ethanol = 2.44*0.789 #kJ/l.K to have the unit compatible with water
max_flow = (0.0+pump_flow)/3.6 #ml/s 
power=0.0+power #watts
max_head=0.0+pump_head #m H2O
delta = u"Δ".encode(os_encoding, "replace")

#calculations

#let's try to brute force Q!
b=max_head/flow_c
a=b/max_flow

Q=max_flow #reasonable guess for the start
for i in range(100):
	Q = Q - (Q**restriction_power+Q*a-b)/(restriction_power*Q**(restriction_power-1)+a)

flow = Q #Thanks, Newton and math.stackexchange.com
# now the rest of the values

if flow_override>0:
	flow = flow_override
pressure = max_head * (1 - flow/max_flow) #m H2O

#NOTE: we are assuming a linear P-Q curve for the pump. Actual performance is typically better than that.

cfs = (0.0+fan_cfm)/60 *0.5 #about right, based on some research I saw. 
capacity = cp_water
if ethanol:
	capacity=cp_ethanol
air_cap = cp_air*kg_in_foot*cfs*1000
cooling_delta = power/capacity/flow
radiator_delta = power/air_cap



#print results
print "T1: Min "+delta+"T from components to coolant: "+degrees(cooling_delta)
print "T2: Min "+delta+"T from radiator to air: "+degrees(radiator_delta)
print "Flow: %.1f ml/s. %.0f%% of max."%(flow, (flow/max_flow*100))
print "Pressure at pump: %.3f m "%pressure + H2O()
print ""
print "Note: while the flow values may be correct, the delta_t values are given for perfect conditions. Real world results may vary."

