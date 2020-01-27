# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Import packages

# %%
import os
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import re

# %% [markdown]
# # Define Functions

# %%
def CallAPI(url):
    r = requests.get(url)
    content = json.loads(r.content.decode('utf-8'))
    
    while 'accounts' not in content.keys():
        # Extract waiting time from error message
        stop_Num = float(re.findall(r"\d+\.?\d*",content['error'])[-1]) + 0.01
        time.sleep(stop_Num)
        r = requests.get(url)
        content = json.loads(r.content.decode('utf-8'))

    Accounts_Detail = content['accounts']

    return Accounts_Detail


# %%
def Create_DataFrame(ExistingDF, New_Account):
    # Create a dataframe for new account record 
    Feature_List = list(New_Account.keys())
    Account_Value = list(New_Account.values())
    New_Account_DF = pd.DataFrame([Account_Value], columns=Feature_List)
    ExistingDF = ExistingDF.append(New_Account_DF)

    return ExistingDF


# %%
# Check if all history records have been fully downloaded
def Check_Full_History(check_Full, Accounts_Detail, End_Time_Str):
    Accounts_Detail_Last = Accounts_Detail
    while check_Full != True:
        if len(Accounts_Detail_Last) < 1000:
            check_Full = True
        else:
            Last_Time = datetime.strptime(Accounts_Detail[-1]['inception'], '%Y-%m-%dT%H:%M:%SZ')+ timedelta(seconds=1)
            Last_Time_Str = Last_Time.strftime('%Y-%m-%dT%H:%M:%SZ')
            API_url = 'https://data.ripple.com/v2/accounts/?start=' + Last_Time_Str + '&end=' + End_Time_Str + '&limit=1000'
            Accounts_Detail_Last = CallAPI(API_url)
            temp = len(Accounts_Detail_Last)
            print(Last_Time_Str, temp)
            if len(Accounts_Detail_Last) == 0:
                check_Full = True
            else:
                Accounts_Detail.extend(Accounts_Detail_Last)
    return Accounts_Detail

# %%
def Write_New_CSV(DF, Local_Path):
    DF.to_csv(Local_Path,index=False)

# %%
def Write_Existing_CSV(DF, Local_Path):
    DF.to_csv(Local_Path, index=False, mode='a', header=False)

# %% [markdown]
# # Determine time interval

# %%
NumOFday = 365

# %%
# Current time
Current_Time = datetime.utcnow()
# End at 00:00
Current_Time = datetime.combine(Current_Time, datetime.min.time())

# Start time for the whole time range
Start_Time_All = Current_Time + timedelta(days=0)

# End time for the whole time range
End_Time_All = Start_Time_All + timedelta(days=-NumOFday)

# %% [markdown]
# # Start download
# %% [markdown]
# ## Reason for half day: records limitation for returns (200)

# %%
day = 1
Accounts_DF = pd.DataFrame()
while day <= NumOFday:
    check_Full = False
    # End time
    # while i = 1, End_Time = Start_Time_All
    End_Time = Start_Time_All + timedelta(days=-day+1)
    End_Time_Str = End_Time.strftime('%Y-%m-%dT%H:%M:%SZ')
    # Start time
    # while i = 1, Start_Time = Start_Time_All - 1 day
    Start_Time = End_Time + timedelta(days=-1)
    Start_Time_Str = Start_Time.strftime('%Y-%m-%dT%H:%M:%SZ')

    print(Start_Time_Str)
    # API url
    API_url = 'https://data.ripple.com/v2/accounts/?start=' + Start_Time_Str + '&end=' + End_Time_Str + '&limit=1000'

    # Download Data for that 'day'
    Accounts_Detail = CallAPI(API_url)
    
    # Check if the full history has been returned 
    Accounts_Detail = Check_Full_History(check_Full, Accounts_Detail, End_Time_Str)

    Accounts_DF_Day = pd.DataFrame(Accounts_Detail)
    Accounts_DF = Accounts_DF.append(Accounts_DF_Day)
    Accounts_DF = Accounts_DF.reset_index(drop=True)
    
    day += 1

#%%
# Data transformation
Accounts_DF['DateTime'] = Accounts_DF['inception'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
del Accounts_DF['inception']
Accounts_DF.sort_values(by=['DateTime'], inplace=True, ascending=False)
Accounts_DF = Accounts_DF.reset_index(drop=True)
print(len(Accounts_DF))


# %%
cwd = os.path.dirname(os.path.realpath(__file__))
FilePath = cwd + '\\Create_Accounts_Num.csv'

if os.path.exists(FilePath):
    Write_Existing_CSV(Accounts_DF, FilePath)
else:
    Write_New_CSV(Accounts_DF, FilePath)

