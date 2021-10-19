#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import seaborn as sns 
import numpy
import os
import re


# In[37]:


#Дополнительный проект
#В папке subsid (shared/homeworks/python_ds_miniprojects/5_subsid) находятся файлы (tm_sales_1, tm_sales_2, ...) 
#с продажами продуктов через телемаркетинг.
#Каждый файл содержит, как минимум, 4 колонки (поля): FILIAL_ID, SUBS_ID, PROD_ID, ACT_DTTM.

#Суть задачи в том, чтобы проверить подключения продуктов определенным пользователям, соединив файлы о продажах 
#с логами по подключениям в системе.

#Особенности данных:

#сотрудники телемаркетинга не всегда указывают полный id, если 'id' нет в начале SUBS_ID, то нужно его добавить
#поля в файлах могут быть расположены абсолютно случайным образом, но названия полей статичны
#продажа не засчитывается, если отключение (END_DTTM) произошло меньше чем через 5 минут после подключения 
#(START_DTTM)
#если в файле с продажами встречается строка без указанного SUBS_ID, она пропускается
#Сохраните результат в датафрэйм с разделителем ;, содержащий корректные подключения.

#Note: обратите внимание на то, как pandas переводит дату из строки, возможно вам понадобится параметр format


# In[38]:


df0=pd.read_csv('/home/jupyter-a.chicherova-13/shared/homeworks/python_ds_miniprojects/5_subsid/subsid/prod_activations_logs.csv', sep=';')


# In[39]:


df1=pd.read_csv('/home/jupyter-a.chicherova-13/shared/homeworks/python_ds_miniprojects/5_subsid/subsid/tm_sales_1.csv', sep=';')


# In[40]:


df2=pd.read_csv('/home/jupyter-a.chicherova-13/shared/homeworks/python_ds_miniprojects/5_subsid/subsid/tm_sales_2.csv', sep=';')


# In[41]:


df3=pd.read_csv('/home/jupyter-a.chicherova-13/shared/homeworks/python_ds_miniprojects/5_subsid/subsid/tm_sales_3.csv', sep=';')


# In[42]:


full_df=pd.concat([df1, df2, df3])


# In[43]:


full_df


# In[44]:


full_df=full_df.dropna()


# In[45]:


full_df.dtypes


# In[46]:


def id_adder(value):
    if value.startswith('id'):
        return value
    return 'id' + value


# In[47]:


full_df.SUBS_ID=full_df.SUBS_ID.apply(id_adder)


# In[48]:


final_data=full_df.merge(df0, how='inner', on=['SUBS_ID', 'PROD_ID'])


# In[49]:


final_data


# In[50]:


final_data['ACT_DTTM']=final_data['ACT_DTTM'].apply(pd.to_datetime, format='%d-%m-%Y %H:%M')


# In[51]:


final_data['START_DTTM']=final_data['START_DTTM'].apply(pd.to_datetime, format='%d-%m-%Y %H:%M')


# In[52]:


final_data['END_DTTM']=final_data['END_DTTM'].apply(pd.to_datetime, format='%d-%m-%Y %H:%M')


# In[53]:


final_data['delta']=final_data.END_DTTM - final_data.START_DTTM


# In[54]:


final_data


# In[55]:


final_data.query('delta>"00:05:00"').sort_values('SUBS_ID').SUBS_ID.tolist()


# In[56]:


final_data = final_data.query('delta>"00:05:00"').sort_values('SUBS_ID')


# In[59]:


final_data.to_csv('final_data.csv')


# In[60]:


final_data


# In[ ]:




