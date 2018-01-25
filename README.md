# AAVSO-analysis
Small set of Python tools to manipulate variable star data obtained from 
the AAVSO.  Uses the following packages: pandas, numpy, matplotlib.pyplot.

Update: 2018 January 23 -- aavso-2.0 now available as pip-installable package:
use 
'''

pip install git+https://github.com/seasidesparrow/AAVSO-analysis.git

''' 
to install.  You can then import all the functions using  
'''

>>> import aavso.aavso as aa
>>> help(aa)

'''
-----------------------------------------------------------------------------

Variable star data from the American Association of Variable Star Observers
can be an incredible resource for those investigating individual variable 
stars or star classes.  These tools are designed to load data files obtained
from the AAVSO's Data Download feature into Pandas DataFrames, and provide 
simple tools to let you manipulate, edit, and plot the data.  From there,
you can use the time-series analysis tools of your choice using Python.  
