#!/usr/bin/env python
# coding: utf-8

# In[95]:




import requests
import praw
import pandas as pd
import datetime
import streamlit as st
import altair as alt
import numpy as np


# In[96]:


user_agent = 'fraud/u/kjohnmunene'


# In[97]:


reddit = praw.Reddit(client_id = '5MHaJDf-ZFXK9t66TUFLTg',
                     client_secret = 'V8zAivIlJwcrL_xaNqOv9BJf4cci2g',
                     user_agent = user_agent
                 
                    )

# Set up Streamlit app
st.title('Reddit_Mobile_Theft_News')


# In[98]:


def get_data():
    headlines = []
    author = []
    date = []
    # Login to redit andselect data whose title contains the name 'theft'
    for submission in reddit.subreddit('theft').new(limit=100000):
        #colect the colums on title, author and date
        headlines.append(submission.title)
        author.append(submission.author)
        date.append(submission.created_utc)
    
#store the above data as a dataframe

    df= pd.DataFrame({"Title": headlines , "author": author, 'Unit_time':date})

# Data cleaning and transformation
#convert unit time to actual time
    df['Actua_date'] = pd.to_datetime(df["Unit_time"], unit="s")

#get only date

    df['Date'] = pd.DatetimeIndex(df.Actua_date).normalize()

#filter phone theft only
    df2 = df[df['Title'].str.contains("phone")].reset_index(drop=True)

#drop unneccessary columns

    data=df2.drop(['Unit_time','Actua_date'], axis=1)
    return (data)


# In[99]:



#prepare data for drawing a bar graph
def draw(data):
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
    data['Year'] = data['Date'].dt.strftime('%Y')    
    data2 = data.groupby(['Year'])['Title'].count().reset_index(name='counts_of_news_per_year')
    data2 = data2.set_index('Year')


    return(data2)


# In[100]:


# Call function to get data from API
data = get_data()
data2 = draw(data)

# Display data in Streamlit app
st.write(data)

#repersent count of news on phone theft per year on a bar graph
st.bar_chart(data2)


# In[ ]:




