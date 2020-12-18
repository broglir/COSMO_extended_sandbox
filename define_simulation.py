#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 13:52:48 2018

@author: jvergara
"""

import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os.path
import os
import sys
import numpy as np
import calendar
# =============================================================================
# Define chain for simulation
# =============================================================================
name_run='testing_sandbox'

postprocessing=True
store_system='/project/pr94/robro/cosmo_out'
saving_folder=store_system+'/'+name_run+'/'
scratch_folder= os.environ['SCRATCH']+'/'+name_run

#set name run in run_daint
os.system("sed -i 's/.*NAME_RUN=.*/NAME_RUN=\"%s\"/' run_daint.sh"%name_run)

# =============================================================================
# Creating directories
# =============================================================================

os.makedirs(saving_folder, exist_ok=True)
os.makedirs(scratch_folder, exist_ok=True)
os.makedirs(scratch_folder+'/input', exist_ok=True)
os.makedirs(scratch_folder+'/output', exist_ok=True)

#Initial date
LM_YYYY_INI='2004'
LM_MM_INI='11'
LM_DD_INI='01'
LM_ZZ_INI='00'

#end of chained dates
LM_YYYY_END_CHAIN='2004'
LM_MM_END_CHAIN='12'
LM_DD_END_CHAIN='01'
LM_ZZ_END_CHAIN='00'


main_simulation_step='2_lm_c'
#main_simulation_step='4_lm_f'

d_ini=datetime.datetime(int(LM_YYYY_INI),int(LM_MM_INI),int(LM_DD_INI),int(LM_ZZ_INI))

d_end_chain=datetime.datetime(int(LM_YYYY_END_CHAIN),int(LM_MM_END_CHAIN),int(LM_DD_END_CHAIN),int(LM_ZZ_END_CHAIN))


months_per_step=1
days_per_step=0 #If >0, this will overwrite months_per_step
last_step=0

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

months_in_between=diff_month(d_end_chain,d_ini)
steps=months_in_between/months_per_step

if months_in_between%months_per_step:
    raise NameError('Number of months is not divisible by the specified months per step')


def diff_days(d1, d2):
    return (d1-d2).days
if days_per_step:
    days_in_between=diff_days(d_end_chain,d_ini)
    steps=days_in_between/days_per_step
    if days_in_between%days_per_step:
        last_step=days_in_between%days_per_step
    
def get_dt(step=main_simulation_step):
    with open(step+'/run') as f: lines = f.read().splitlines()
    num=np.nan
    for line in lines:
        if line.startswith('DT='):
            num = float(line.split('=')[-1].strip()[:])
            print (num)
    return num

def get_idbg(step=main_simulation_step):
    with open(step+'/run') as f: lines = f.read().splitlines()
    num=np.nan
    for line in lines:
        if line.startswith('  idbg_level ='):
            num = int(float(line.split('=')[-1].strip()[:-1]))
            print (num)
    return num

def multiply_idbg(n=10,step=main_simulation_step):
    number=get_idbg(step=step)
    new_number=number*n
    a=os.system("sed -i 's/  idbg_level = %i/  idbg_level = %i/g' %s/run"%(number,new_number,step))


def time():
    return datetime.datetime.now().strftime('%y/%m/%d-%H:%M:%S')






dt=get_dt()
idbg=get_idbg()

columns=['step','start_date', 'end_date', 'h_str', 'h_end', 'status','dt','idbg_level','last_update']
name_control_dataframe='Dataframe_'+name_run
# =============================================================================
# Create chain
# =============================================================================
if __name__=='__main__':
    print('Linking input/output folders to SCRATCH')
    os.system('ln -s '+scratch_folder+'/output output')

    os.system('ln -s '+scratch_folder+'/input input')

    if not os.path.isfile(name_control_dataframe):
        print('Creating dataframe')
        dataframe=pd.DataFrame(columns=columns)
        
        d_end=d_ini
        for i in range(int(steps)):
            d_str=d_end
            if not days_per_step:
                if months_per_step==0.5:
                    if d_end.day<15:
                        d_end=d_end+ relativedelta(days=15-d_end.day)
                    else:
                        days_in_month=calendar.monthrange(d_end.year, d_end.month)[1]
                        d_end=d_end+ relativedelta(days=days_in_month-d_end.day+1)
                else:d_end=d_end+ relativedelta(months=months_per_step)
            else:
                d_end=d_end+ relativedelta(days=days_per_step)
            print(d_end)    
            h_str=(d_str-d_ini).days*24
            h_end=(d_end-d_ini).days*24
            status=0
            run_setup = pd.DataFrame([[i,d_str.isoformat()[:10],d_end.isoformat()[:10],h_str,h_end,status,dt,idbg,time()]], columns=columns)
            dataframe=dataframe.append(run_setup)
        if last_step:
            d_str=d_end
            d_end=d_end+ relativedelta(days=last_step)
            h_str=(d_str-d_ini).days*24
            h_end=(d_end-d_ini).days*24
            status=0
            run_setup = pd.DataFrame([[int(steps),d_str.isoformat()[:10],d_end.isoformat()[:10],h_str,h_end,status,dt,idbg,time()]], columns=columns)
            dataframe=dataframe.append(run_setup)
            
            
        dataframe.to_csv(name_control_dataframe,mode = 'w',sep="\t", index=False)
    else:
        print("Dataframe was already created")
