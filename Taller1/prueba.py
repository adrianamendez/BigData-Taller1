#!/usr/bin/env python
# coding: utf-8

# In[79]:


import numpy as np
import pandas as pd
import json
import datetime


# In[43]:


data = pd.read_json('Prueba.json', orient = 'columns')
data.inserted_date = pd.to_datetime(data.inserted_date)

#Límites Bogotá

bogota = np.array([[-74.2891, 4.5745], [-73.9529, 4.8763]])


# In[44]:


bogota


# In[45]:


data.location = data.location.apply(str)


data2 = data.location.str.rsplit(':', expand = True)

data2 = data2.iloc[:,2].str.replace(']}', "").str.rsplit(', ', expand = True)
data2.iloc[:,0] = data2.iloc[:,0].str.replace('[', "")
data2.columns = ['long', 'lat']
data = pd.concat([data.drop(['location'], axis = 1), data2], axis = 1)
data[['long', 'lat']] = data[['long', 'lat']].astype(float).round(4)

data.head()


# In[35]:


data = data.sort_values(by='inserted_date')

data['minutes'] = [x.seconds/60 for x in data.date.diff()]


# In[91]:


data.head(5)


# In[ ]:





# In[ ]:




