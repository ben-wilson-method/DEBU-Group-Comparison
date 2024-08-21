import streamlit as st

#Import the standard modules
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import matplotlib.pyplot as plt
import pickle


#Import the data
#df = pd.read_excel('Japanese_(DEBU)トランスフォーメーションに向けたサーベイ(1-696).xlsx',sheet_name='Sheet1')
uploaded_file = st.file_uploader("Choose the english version of the Survey file")
uploaded_dictionary = st.file_uploader("Upload the dictionary file")

if uploaded_file is not None:
    df_eng = pd.read_excel(uploaded_file,sheet_name='Sheet1')
    #df.columns = df_eng.columns
    
    #Add the manager key
    #df['Manager'] = [True if ('a.' in i) or ('b.' in i) or ('c.' in i) else False for i in df_eng['What is your job title?'].tolist()]
    df_eng['Manager'] = [True if ('a.' in i) or ('b.' in i) or ('c.' in i) else False for i in df_eng['What is your job title?'].tolist()]
    
    #Process the data
    AP_index = df_eng[df_eng['What department are you in?']=='a. (AP)'].index.tolist()
    DX_index = df_eng[df_eng['What department are you in?']!='a. (AP)'].index.tolist()
    
    df_eng_other_removed = df_eng[df_eng['What is your job title?'].str.contains('f. Others') == False]
    
    Manager_index = df_eng_other_removed[df_eng_other_removed['Manager']].index.tolist()
    Non_Manager_index = df_eng_other_removed[df_eng_other_removed['Manager'] == False].index.tolist()
    
    AP_Manager_index = df_eng_other_removed[df_eng_other_removed['Manager']][df_eng_other_removed['What department are you in?']=='a. (AP)'].index.tolist()
    AP_Non_Manager_index = df_eng_other_removed[df_eng_other_removed['Manager'] == False][df_eng_other_removed['What department are you in?']=='a. (AP)'].index.tolist()
    DX_Manager_index = df_eng_other_removed[df_eng_other_removed['Manager']][df_eng_other_removed['What department are you in?']!='a. (AP)'].index.tolist()
    DX_Non_Manager_index = df_eng_other_removed[df_eng_other_removed['Manager'] == False][df_eng_other_removed['What department are you in?']!='a. (AP)'].index.tolist()
    OJT_first_index = df_eng[df_eng['d. OJT']=='1st place'].index.tolist()
    OJT_second_index = df_eng[df_eng['d. OJT']=='2nd place'].index.tolist()
    OJT_third_index = df_eng[df_eng['d. OJT']=='Third'].index.tolist()
    OJT_selected_index = df_eng[((df_eng['d. OJT']=='1st place') | (df_eng['d. OJT']=='2nd place') | (df_eng['d. OJT']=='Third')) == True].index.tolist()
    OJT_NA_index = df_eng[((df_eng['d. OJT']=='1st place') | (df_eng['d. OJT']=='2nd place') | (df_eng['d. OJT']=='Third')) == False].index.tolist()
    
    group_dic = {'AP Managers':AP_Manager_index,
    'AP Non-Managers':AP_Non_Manager_index,
    'DX Managers':DX_Manager_index,
    'DX Non-Managers':DX_Non_Manager_index,
    'Managers':Manager_index,
    'Non-Managers':Non_Manager_index,
    'AP':AP_index,
    'DX':DX_index,
    'OJT first:':OJT_first_index,
    'OJT second:':OJT_second_index,
    'OJT third:':OJT_third_index,
    'OJT selected':OJT_selected_index,
    'OJT not selected:':OJT_NA_index,}
    
    Question_num = st.sidebar.selectbox("Which question to analyse",('Question 6','Question 7','Question 8','Question 19','Question 20','Question 23','Question 24','Question 27','Question 28','Question 31','Question 32','Question 33','Question 34'))
    
    if uploaded_dictionary is not None:
        with uploaded_dictionary as file: 
      
            # Call load method to deserialze 
            Question_dic = pickle.load(file)
    
    
        Question = Question_dic[Question_num]
        
        st.sidebar.write('Which groups would you like to compare?')
        group_list = []
        for key in group_dic.keys():
            if st.sidebar.checkbox(key,key=key):
                group_list.append(key)
                
                
        
        st.subheader(Question_num)
        st.write(Question_dic[Question_num])
        if group_list == []:
            st.write('#')
            st.subheader('Waiting for you to select which groups to compare')
        else:
            fig,ax = plt.subplots()
            #group_list = ['AP','DX']
            num_groups = len(group_list)
            
            
            label_dic = {key:i for i,key in enumerate(sorted(df_eng[Question].value_counts().keys()))}
            #label_dic = label_dic
            width = 1/(num_groups+1)
            multiplier = 0
            for group in group_list:
                working_dic = df_eng.iloc[group_dic[group]][Question].value_counts()
                x_axis = np.array([label_dic[key] for key in working_dic.keys()])
                offset = width * multiplier
                ax.bar(x_axis+offset,working_dic.values/sum(working_dic.values),width = width,label=group)
                multiplier += 1
            
            ax.set_xticks(np.array(list(label_dic.values())) + width*(len(group_list)-1), label_dic.keys(),rotation=90)
            ax.legend()
            ax.grid()
            st.pyplot(fig)
    else:
        st.write("##")
        st.subheader('Waiting for Dictionary')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
