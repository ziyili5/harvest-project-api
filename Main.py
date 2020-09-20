from Calculate import Cal
from Figure import Fig
#from Curve_fit import Fit

#Curve fitting function is not used at this stage, when we collected the real field-experiment data, we could add this module


# Calculate the MRTN results and give input(fertilizer and corn price,rotation and district)
fpr=0.4 #nitrogen fertilizer price 0.4 $/lb N
cpr=4 #corn price 4 $/bu
rot='cc'#rotation cc:continuous corn; cs:corn-soybean rotation
dis=1 #district: 1-9 means districts 1-9; 10-13 means northern, lsw region, central and southern Illinois

Rlt=Cal(rot,fpr,cpr,dis)


# Draw the corresponding figures
tp=4 # figure type: 1 means "Return to N"; 2 means "% of Max Yield"; 3 means "ENOR Frequency" and 4 means "ENOR vs. Yield"
# there is a more clear discription at the website below for each figure
# http://cnrc.agron.iastate.edu/nRate.aspx
yn=Rlt[0]# parameters calculated in the previous step
En=Rlt[1]# parameters calculated in the previous step
Opy=Rlt[2]# parameters calculated in the previous step
Fig(tp, yn,cpr,fpr,En,Opy)