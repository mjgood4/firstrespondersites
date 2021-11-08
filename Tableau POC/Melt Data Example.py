#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df=pd.read_csv('allegheny_rand_data.csv')


# In[3]:


df


# In[4]:


df=df.melt(id_vars=['selected_zone'],var_name="zone_value").sort_values


# In[6]:


df.sort_values(by='selected_zone')


# In[7]:


df.to_csv('melted_data.csv')


# In[ ]:




