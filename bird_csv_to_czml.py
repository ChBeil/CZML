
# coding: utf-8

# In[1]:

from czml import czml

# Initialize a document
doc = czml.CZML()


# In[2]:

clock = {
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "range": "LOOP_STOP",
            "multiplier": 2160000,
            "interval": "2015-01-01/2015-12-31",
            "currentTime": "2015-01-01"
    }


# In[3]:

# Create and append the document packet
packet1 = czml.CZMLPacket(id='document',version='1.0',clock=clock)


# In[4]:

packet1.dumps()


# In[5]:

doc.packets.append(packet1)


# In[6]:

packet2 = czml.CZMLPacket(id='flycatcher', availability="2015-01-01/2015-12-31")


# In[7]:

packet2.dumps()


# In[8]:

point={
        "color": {
            "rgba": [
                255, 255, 0, 255
            ]
        },
        "outlineWidth": 0,
        "pixelSize": 10,
        "show": True
    }


# In[9]:

packet2.point = point


# ## Read the actual Bird Data CSV

# # Convert Cornell Bird Migration CSV files to CZML
# Trying out the CZML python package.  Installed from PIP until we can build our own conda package

# In[10]:

import pandas as pd
import datetime as dt
import numpy as np


# In[11]:

# parser to convert integer yeardays to datetimes in 2015
def parse(day):
    date = dt.datetime(2015,1,1,0,0) + dt.timedelta(days=(day.astype(np.int32)-1))
    return date


# In[12]:

def csv_to_position(file='Acadian_Flycatcher.csv'):
    df = pd.read_csv(file, parse_dates=True, date_parser=parse, index_col=0, na_values='NA')
    df.dropna(how="all", inplace=True) 
    df['z']=0.0
    df['str']= df.index.strftime('%Y-%m-%d')
    df2 = df.ix[:,[3,0,1,2]]
    a = df2.values.tolist()
    return {'cartographicDegrees':[val for sublist in a for val in sublist]}


# In[13]:

import glob


# In[14]:

csv_files = glob.glob('*.csv')


# In[15]:

for csv_file in csv_files:
    bird = csv_file.split('.')[0]
    packet = czml.CZMLPacket(id=bird, availability="2015-01-01/2015-12-31")
    packet.point = point
    pos = csv_to_position(file=csv_file)
    packet.position = pos
    desc = czml.Description(string=bird)
    packet.description = desc
    doc.packets.append(packet)

    


# In[16]:

# inspect the last packet
packet.dumps()


# In[17]:

# Write the CZML document to a file
filename = "all_birds.czml"
doc.write(filename)

