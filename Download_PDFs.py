#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests as req
import sys


# In[2]:


path_dir = sys.argv[1]


# In[3]:


# change each file name to avoid overwriting files
urls = []
outs = []
for i in range(11,19):  # years that UW has proper formatted content of admissions 
    url = "https://grad.uw.edu/wp-content/uploads/2019/06/admissions"
    url = "{u}{i}.pdf".format(u=url,i=i)
    urls.append(url)
    outs.append("admissions" + str(i) + ".pdf")


# In[4]:


for i in range(len(urls)):
    r = req.get(urls[i])
    with open(str(path_dir+outs[i]), 'wb') as f: #  wb = write, bytes
        f.write(r.content)

