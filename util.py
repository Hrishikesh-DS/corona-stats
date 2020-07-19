import csv
import pandas as pd
import numpy as np
import os

__states=None
__districts=None

def load_states():
    global __states
    df=pd.read_csv("sample.csv")
    __states=df['state'].unique()
    __states = __states.tolist()

def load_district(state):
    global __districts
    df=pd.read_csv("sample.csv")
    inpst=df.loc[df['state']==state]
    __districts=inpst.district.unique().tolist()
    return __districts

def get_states():
    return __states

def add_and_get_email(district,email):
    df=pd.read_csv("sample.csv")
    inpds=df.loc[df['district']==district]
    inpds['email']=email
    inpds.to_csv(r'userId.csv',mode='a',header=False,index=False,quoting=csv.QUOTE_NONNUMERIC)
    return inpds.values.tolist()

if __name__=='__main__':
    load_states()
    load_district()
    print(__states)
    print(__districts)