#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[29]:


l = []
base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for pages in range(0,30,10):
#     print(base_url + str(pages) + ".html",)
    r = requests.get(base_url + str(pages) + ".html",headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c)
    all = soup.find_all("div",{"class":"propertyRow"})
    pages = soup.find_all("a",{"class":"Page"})[-1].text
    
    for item in all:
        d = {}
        d["price"]=item.find("h4",{"class":"propPrice"}).text.replace(" ","").replace("\n","")#price
        d["Address"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text#address1
        d["Locality"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text#address2
        try:
            d["Beds"]=item.find("span",{"class":"infoBed"}).find("b").text#bed
        except:
            d["Beds"]="Not Available"

        try:
            d["Full Bath"]=item.find("span",{"class":"infoValueFullBath"}).find("b").text#full bath
        except:
            d["Full Bath"]="Not Available"

        try:
            d["Half Bath"]=item.find("span",{"class":"infoValueHalfBath"}).find("b").text#half bath
        except:
            d["Half Bath"]="Not Available"


        try:
            d["Area"]=item.find("span",{"class":"infoSqFt"}).find("b").text#area 
        except:
             d["Area"]="Not Available"


        for columngroup in item.find_all("div",{"class":"columnGroup"}):
            for feature_group , feature_name in zip(columngroup.find_all("span",{"class":"featureGroup"}),columngroup.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                     d["Lot Size"]=feature_name.text

        l.append(d)


# In[23]:


import pandas

df = pandas.DataFrame(l)
df


# In[25]:


df.to_csv("out.csv")


# In[ ]:




