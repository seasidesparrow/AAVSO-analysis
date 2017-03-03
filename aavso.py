import pandas as pd
import numpy as np
import math


def fainterthans_repair(df):
  """
    Wherever the Magnitude has a leading "<", remove it, and modify the
    value of Band to add a trailing "-fainter"
  """
  df.loc[df.Magnitude.str.contains('<')==True,'Band']= df.loc[df.Magnitude.str.contains('<')==True,'Band']+'-fainter'
  df.loc[df.Magnitude.str.contains('<')==True,'Magnitude']=df.loc[df.Magnitude.str.contains('<')==True,'Magnitude'].str.replace('<','')
  return df

def fainterthans_delete(df):
  """
    Takes input data frame, and returns a Pandas DataFrame "df" having
    only positive data, with no fainter-than estimates.
  """
  df=fainterthans_repair(df)
  df=df.loc[df.Band.str.endswith('-fainter')==False]
  return df

def nonstandard_filter_delete(df):
  """
    Removes data from several archaic or undefined filters that occasionally
    appear in AAVSO data:  Blue-Vis.,Green-Vis.,Red-Vis.,Orange,Yellow-Vis.,
    "O" (for other), and "" (blank, which is a translation of "NA" which
    occasionally appears in AAVSO data).

    See https://www.aavso.org/filters for a list of filters.
  """
  fcut=['Blue-Vis.','Green-Vis.','Red-Vis.','Orange','Yellow-Vis.','O','']
  for f in fcut:
    df=df.loc[df.Band!=f]
  return df
  
def jd_decimalyear_convert(df):
  """
    WARNING: SUITABLE FOR PLOTTING ONLY.
    Takes the input Pandas DataFrame "df" and converts the 'JD' column
    to an approximate floating point Year.  Useful for making more readable
    light curves, but is not strictly accurate to more than a decimal
    place in the day fraction as the equation is only approximate.
  """
  df.loc[:,'JD']=(1900.+(df.loc[:,'JD']-2415020.0)/365.25)
  return df


def jd_truncate(df,offset=2400000.0):
  """
    Takes the input Pandas DataFrame "df" and subtracts an offset.  The
    default offset is 2400000.0, but if an optional parameter "offset"
    is given, that will be used instead (e.g. "2400000.5")
  """
  df.loc[:,'JD']=df.loc[:,'JD']-offset
  return df


def aavso_csv_load(infile):
  """
    Loads an AAVSO CSV data file into a Pandas DataFrame "df".  Any
    empty values in any (row,column) will be converted from NaN 
    (the default) to empty string ''.  If infile is given without 
    path, it is assumed to be in your current working directory.
  """
  df=pd.read_csv(infile,low_memory=False)
  df.fillna('',inplace=True)
  
  return df


def observer_only(df,o):
  """
    Takes input data frame, and returns a Pandas DataFrame "df" having
    *only* the data from obscode in "o".  Note that if that observer 
    code has no data, you will get an empty DataFrame returned!
  """
  df=df.loc[df['Observer Code']==o]
  return df


def observer_delete(df,o):
  """
    Takes input data frame, and returns a Pandas DataFrame "df" having 
    none of the data from the AAVSO Observer Code in "o".
  """
  df=df.loc[df['Observer Code']!=o]
  return df


def visual_estimates_only(df):
  """
    Takes input data frame, and returns a Pandas DataFrame "df" having
    only visual estimates.  May include fainter-than observations,
    so for visual positives only, you must also run fainterthans_delete.
  """
  df=df.loc[df.Band.str.contains('Vis.')]
  return df

def transformed_only(df):
  """
    Takes input data frame, and returns a Pandas DataFrame "df" having
    only transformed, instrumental measures in standard filters. NOTE: 
    there is a typo in the header row of aavso .CSV files as of 2017 
    March 01, so the column name is "Transfomed" rather than the correct
    "Transformed".  This will be edited if/when the issue is fixed.
  """
  df=df.loc[df.Transfomed==1]
  return df


def invalids_delete(df):
  """
    Takes input data frame, and returns a Pandas DataFrame "df" with
    only data marked with the Validation flags 'V' or 'Z'.  For a
    description of AAVSO Validation flags and their meanings, see:
  """
  mask=((df['Validation Flag']=='V') | (df['Validation Flag']=='Z'))
  return df[mask]

def differentials_delete(df):
  """
    Takes input data frame, and returns it with any data having a
    Measurement Method of "DIFF" removed.  Useful if you didn't 
    deselect DIFF-STEP data when you were downloading.
  """
  mask=((df['Measurement Method']!='DIF'))
  return df[mask]

def differentials_keep(df):
  """
    Takes input data frame, and returns a data frame having
    *only* data with a Measurement Method of "DIFF" removed.
    Useful for many binaries and pulsating stars with lots of
    available differential data.
  """
  mask=((df['Measurement Method']=='DIF'))
  return df[mask]

def steps_delete(df):
  """
    Takes input data frame, and returns it with any data having a
    Measurement Method of "STEP" removed.  Useful if you didn't 
    deselect DIFF-STEP data when you were downloading.
  """
  mask=((df['Measurement Method']!='STEP'))
  return df[mask]

def filterlist_get(df):
  """
    Returns an array with a list of filters found in the DataFrame
  """
  f=df.Band.unique()
  return f

def observerlist_get(df):
  """
    Returns an array with all Observer Codes in the DataFrame
  """
  obs=df['Observer Code'].unique()
  obs=sorted(sorted(obs))
  return obs

def observercounts_dict(df):
  """
    Returns a dictionary with keys of observer codes, and values of
    the number of observations they contributed to this data set.
  """
  ol=observerlist_get(df)
  ot=df['Observer Code'].value_counts()
  obstab={}
  for o in ol:
    obstab[o]=ot[o]
  return obstab


def midpoint_get(df):
  """
    Returns the midpoint of JD in the dataset.  Can be used to set
    an offset t(0) suitable for time-series analysis
  """
  jdmax=max(df.JD)
  jdmin=min(df.JD)
  jdmid=(jdmax+jdmin)/2.
  return jdmid


def multipanel_file(df,nplots=4,xlabel='JD',ylabel='Mag.',title='',dts=300,imtype='png',outf='lightcurve.png'):
  """
    Make a .png image file out of a multipanel lightcurve.  Output will be
    to the directory you launched python from, unless you use an absolute
    path.
  """
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  plotf=multipanel_lc(df,plt,nplots,xlabel,ylabel,title)
  if(imtype=='png'):
    plotf.savefig(outf,format=imtype,dpi=dts)
  else:
    if(nplots>4):
      ori='portrait'
    else:
      ori='landscape'
    plotf.savefig(outf,format=imtype,orientation=ori)
  plt.close(plotf)

  return


def multipanel_screen(df,nplots=4,xlabel='JD',ylabel='Mag.',title=''):
  """
    Make a .png image file out of a multipanel lightcurve.  Output will be
    to the directory you launched python from, unless you use an absolute
    path.
  """
  import matplotlib.pyplot as plt

  plotf=multipanel_lc(df,plt,nplots,xlabel,ylabel,title)
  plt.show()

  return


def multipanel_lc(df,plt,np,xl,yl,ti):
  """
    Create a light curve with vertically stacked panels.  This is not called
    directly by the user; use "multipanel_screen" for interactive plots, or
    "multipanel_file" for image file output to PNG, PS, or PDF.
  """
  plotparm={'Vis.-fainter':('black','v',8),
    'Vis.' :('black','o',1),
    'U'    :('purple','o',2),
    'B'    :('blue','o',2),
    'V'    :('green','o',2),
    'R'    :('red','o',2),
    'I'    :('orange','o',2),
    'TG'   :('green','s',8),
    'TB'   :('blue','s',8),
    'TR'   :('red','s',8),
    'CV'   :('green','+',8),
    'CR'   :('red','+',8),
    ''     :('white','+',1),
    '-fainter' :('white','v',8),
    'V-fainter':('green','v',8),
    'Green-Vis.':('green','h',20)
  }

  font={'family' : 'Serif','weight' : 'normal','size' : 8}
  plt.rc('font',**font)

  filters=filterlist_get(df)

  jdmax=max(df.JD)
  jdmin=min(df.JD)
  magmax=min(df.Magnitude)
  magmin=max(df.Magnitude)
  jdspan=jdmax-jdmin
  tdelta=0.01*jdspan
  jdmax=jdmax+tdelta
  jdmin=jdmin-tdelta
  ptspan=jdspan/np

  p,ax=plt.subplots(nrows=np,sharex=False)

  ax[0].set_title(ti)
  for i in range(0,np):
    for f in filters:
      jd=df.loc[df.Band==f].JD
      mag=df.loc[df.Band==f].Magnitude
      ax[i].scatter(jd,mag,s=plotparm[f][2],marker=plotparm[f][1],color=plotparm[f][0])

    ax[i].set_ylim(ax[i].get_ylim()[::-1])
    ax[i].set_xlim((jdmin+(i*ptspan)),(jdmin+((i+1)*ptspan)))
    ax[i].set_ylabel(yl)
    ax[i].set_autoscale_on(False)
  ax[(np-1)].set_xlabel(xl)
  p.subplots_adjust(hspace=0.5)
  return p
