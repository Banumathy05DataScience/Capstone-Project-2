import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json


#dataframe creation

# sql connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data",
                      password="banumathy"
                      )

cursor=mydb.cursor()

#aggree_insurance

cursor.execute("SELECT * FROM aggreated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurane=pd.DataFrame(table1 ,columns=("States","Years","Quarter",
                                             "Transcation_type","Transcation_count","Transcation_amount"))
                                            
                                                                                                                        
#aggree_transcation

cursor.execute("SELECT * FROM aggreated_transction")
mydb.commit()
table2=cursor.fetchall()

Aggre_tanscation=pd.DataFrame(table2 ,columns=("States","Years","Quarter","Transcation_type",
                                                "Transcation_count","Transcation_amount"))                                    
                                                                   

#aggree_user

cursor.execute("SELECT * FROM aggreated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3, columns=("States","Years","Quarter",
                                         "Brands","Transcation_count","Percentage"))                                    
                                            
                                                            
#map_insurance

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

Map_insurance=pd.DataFrame(table4, columns=("States","Years","Quarter",
                                            "Districts", "Transcation_count","Transcation_amount"))

                                            
#map_transcation

cursor.execute("SELECT * FROM map_transcation")
mydb.commit()
table5=cursor.fetchall()

Map_transcation=pd.DataFrame(table5, columns=("States","Years","Quarter",
                                            "Districts", "Transcation_count","Transcation_amount"))  

#map_user

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

Map_user=pd.DataFrame(table6, columns=("States","Years","Quarter",
                                            "Districts", "RegisteredUsers","AppOpens"))  

#top_insurance

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7, columns=("States","Years","Quarter",
                                            "Pincodes", "Transcation_count","Transcation_amount"))              


#top_transcation

cursor.execute("SELECT * FROM top_transcation")
mydb.commit()
table8=cursor.fetchall()

Top_transcation=pd.DataFrame(table8, columns=("States","Years","Quarter",
                                            "Pincodes", "Transcation_count","Transcation_amount"))  


 #top_user

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9, columns=("States","Years","Quarter",
                                     "Pincodes", "RegisteredUsers"))
           



def Transcation_amount_count_Y(df,year):
    
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transcation_count","Transcation_amount"]].sum()
    tacyg.reset_index(inplace=True)

    coll1,coll2=st.columns(2)
    with coll1:

        fig_amount=px.bar(tacyg,x="States", y="Transcation_amount",title=f"{year} TRANSCATION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.algae,height=650,width=600)
                    
        st.plotly_chart(fig_amount)

    with coll2:

        fig_count=px.bar(tacyg,x="States", y="Transcation_count",title=f"{year} TRANSCATION COUNT",
                          color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
                                                    
        st.plotly_chart(fig_count)

    coll1,coll2=st.columns(2)  
    with coll1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for features in data1["features"]:
            states_name.append(features["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transcation_amount", color_continuous_scale= "temps",
                                range_color=(tacyg["Transcation_amount"].min(), tacyg["Transcation_amount"].max()),
                                hover_name="States", title= f"{year} TRANSCATION AMOUNT", fitbounds="locations", height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with coll2:

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transcation_count", color_continuous_scale= "temps",
                                range_color=(tacyg["Transcation_count"].min(), tacyg["Transcation_count"].max()),
                                hover_name="States", title= f"{year} TRANSCATION COUNT", fitbounds="locations", height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transcation_amount_count_Y_Q(df,quarter):

    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transcation_count","Transcation_amount"]].sum()
    tacyg.reset_index(inplace=True)
    

    coll1,coll2=st.columns(2)
    with coll1:


        fig_amount=px.line(tacyg,x="States", y="Transcation_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSCATION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.algae,height=650,width=600)
                    
        st.plotly_chart(fig_amount)

    with coll2:


        fig_count=px.line(tacyg,x="States", y="Transcation_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSCATION COUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
                                                    
        st.plotly_chart(fig_count)

    coll1,coll2=st.columns(2)
    with coll1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for features in data1["features"]:
            states_name.append(features["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transcation_amount", color_continuous_scale= "temps",
                                range_color=(tacyg["Transcation_amount"].min(), tacyg["Transcation_amount"].max()),
                                hover_name="States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSCATION AMOUNT", fitbounds="locations", height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with coll2:

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transcation_count", color_continuous_scale= "temps",
                                range_color=(tacyg["Transcation_count"].min(), tacyg["Transcation_count"].max()),
                                hover_name="States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSCATION COUNT", fitbounds="locations", height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Aggre_Tran_Transcation_type(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Transcation_type")[["Transcation_count","Transcation_amount"]].sum()
    tacyg.reset_index(inplace=True)

    coll1,coll2=st.columns(2)
    with coll1:
        
        fig_pie_1=px.pie(data_frame=tacyg, names="Transcation_type", values="Transcation_amount",
                        width=600, title=f"{state.upper()} TRANSCATION AMOUNT", hole=0.5) 
        st.plotly_chart(fig_pie_1)

    with coll2:

        fig_pie_2=px.pie(data_frame=tacyg, names="Transcation_type", values="Transcation_count",
                        width=600, title=f"{state.upper()} TRANSCATION COUNT", hole=0.5) 
        st.plotly_chart(fig_pie_2)

#Aggre_user_analysis_1

def Aggre_user_plot(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transcation_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands", y="Transcation_count", title=f"{year} BRANDS AND TRANSCATION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

# Aggre_usser_Analysis 2

def Aggre_user_plot2(df,quarter):

    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transcation_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg,x="Brands", y="Transcation_count", title=f"{quarter} QUARTER BRANDS AND TRANSCATION COUNT",
                        width=1000, color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggre_user_analysis_3

def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"] == state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1=px.bar(auyqs, x="Brands",y="Transcation_count", hover_data="Percentage",
                    title=f"{state.upper()} BRANDS, TRANSCATION COUNTPERCENTAGE", width=1000)
    st.plotly_chart(fig_line_1)


#Map_insurance_district

def Map_insur_Districts(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Districts")[["Transcation_count","Transcation_amount"]].sum()
    tacyg.reset_index(inplace=True)

    coll1,coll2=st.columns(2)
    with coll1:

        fig_bar_1=px.bar(tacyg, x="Transcation_amount", y="Districts", orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSCATION AMOUNT", color_discrete_sequence=px.colors.sequential.Rainbow) 
        st.plotly_chart(fig_bar_1)

    with coll2:

        fig_bar_2=px.bar(tacyg, x="Transcation_count", y="Districts", orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSCATION COUNT", color_discrete_sequence=px.colors.sequential.Bluered) 
        st.plotly_chart(fig_bar_2)


# Map_user_plot_1
def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True,inplace=True)

    muyg=muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.scatter(muyg, x="States",y=["RegisteredUsers", "AppOpens"], 
                        title=f"{year} REGISTERED USER AND APPOPENS", width=1000,height=800)
    st.plotly_chart(fig_line_1)

    return muy

# Map_user_plot_2
def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqg=muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.scatter(muyqg, x="States",y=["RegisteredUsers", "AppOpens"], 
                        title=f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER AND APPOPENS", width=1000,height=800,
                        color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_line_1)

    return muyq

#Map_user_plot_3
def map_user_plot_3(df,states):

    muyqs=df[df["States"]==states]
    muyqs.reset_index(drop=True,inplace=True)
    
    coll1,coll2=st.columns(2)
    with coll1:

        fig_map_user_bar_1=px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation='h',
                                title=f"{states.upper()} REGISTERED USER",height=800, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_map_user_bar_1)

    with coll2:

        fig_map_user_bar_2=px.bar(muyqs, x="AppOpens", y="Districts", orientation='h',
                                title=f"{states.upper()} APPOPENS",height=800, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

#Top_insurance_plot_1
def Top_insurance_plot_1(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True,inplace=True)

    coll1,coll2=st.columns(2)

    with coll1:

        fig_top_insur_bar_1=px.bar(tiy, x="Quarter", y="Transcation_amount", hover_data="Pincodes",
                                    title="TRANSCATION AMOUNT",height=650, color_discrete_sequence=px.colors.sequential.Bluered)
        st.plotly_chart(fig_top_insur_bar_1)

    with coll2:

        fig_top_insur_bar_2=px.bar(tiy, x="Quarter", y="Transcation_count", hover_data="Pincodes",
                                    title="TRANSCATION COUNT",height=650, color_discrete_sequence=px.colors.sequential.Magenta)
        st.plotly_chart(fig_top_insur_bar_2)


def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)
    
    fig_top_plot_1=px.bar(tuyg,x="States", y="RegisteredUsers", color="Quarter", width=650,height=650,
                        color_discrete_sequence=px.colors.sequential.Blugrn, hover_name="States",
                        title=f"{year} REGISTERED USER")
    st.plotly_chart(fig_top_plot_1)
    return tuy


# top_user_plot_2
def top_user_plot_2(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_pot_2= px.bar(tuys,x="Quarter",y="RegisteredUsers", title="REGISTERED USERS, PINCODES, QUARTERS", 
                        width=650,height=650,color="RegisteredUsers", hover_data="Pincodes",color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2) 

    
# sql connection(Transcation Amount)

def top_chart_transcation_amount(table_name):

    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="banumathy"
                        )

    #Plot_1
    query1= f''' SELECT states, SUM(transcation_amount)AS transcation_amount 
                FROM {table_name}
                GROUP BY states
                ORDER BY transcation_amount DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states", "transcation_amount"))

    coll1,coll2=st.columns(2)
    with coll1:

        fig_amount=px.bar(df_1,x="states", y="transcation_amount", title=" TOP 10 OF TRANSCATION AMOUNT",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.Rainbow,hover_name="states")
        st.plotly_chart(fig_amount)


    #Plot_2

    query2= f''' SELECT states, SUM(transcation_amount)AS transcation_amount 
                FROM {table_name}
                GROUP BY states
                ORDER BY transcation_amount
                LIMIT 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states", "transcation_amount"))

    with coll2:

        fig_amount_2=px.bar(df_2,x="states", y="transcation_amount", title=" LAST 10 OF TRANSCATION AMOUNT",
                            width=600,height=650,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="states")
        st.plotly_chart(fig_amount_2)


    #Plot_3

    query3= f''' SELECT states, AVG(transcation_amount)AS transcation_amount 
                FROM {table_name}
                GROUP BY states
                ORDER BY transcation_amount;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states", "transcation_amount"))

    fig_amount_3=px.bar(df_3,y="states", x="transcation_amount", title=" AVERAGE OF TRANSCATION AMOUNT",
                        width=1000,height=800,color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name="states",orientation="h")
    st.plotly_chart(fig_amount_3)

#SQL QUERY FOR TRANSCATION COUNT

def top_chart_transcation_count(table_name):

    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="banumathy"
                        )

    #Plot_1
    query1= f''' SELECT states, SUM(transcation_count)AS transcation_count 
                FROM {table_name}
                GROUP BY states
                ORDER BY transcation_count DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states", "transcation_count"))

    coll1,coll2=st.columns(2)
    with coll1:

        fig_amount=px.bar(df_1,x="states", y="transcation_count", title=" TOP 10 CHART OF TRANSCATION COUNT",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.Rainbow,hover_name="states")
        st.plotly_chart(fig_amount)


    #Plot_2

    query2= f''' SELECT states, SUM(transcation_count) AS transcation_count 
                FROM {table_name}
                GROUP BY states
                ORDER BY transcation_count
                LIMIT 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states", "transcation_count"))

    with coll2:

        fig_amount_2=px.bar(df_2,x="states", y="transcation_count", title=" LAST TO CHART OF TRANSCATION COUNT",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="states")
        st.plotly_chart(fig_amount_2)


    #Plot_3

    query3= f''' SELECT states, AVG(transcation_count) AS transcation_count 
                FROM {table_name}
                GROUP BY states
                ORDER BY transcation_count;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states", "transcation_count"))

    fig_amount_3=px.bar(df_3,y="states", x="transcation_count", title="AVERAGE 10 CHART OF TRANSCATION COUNT",
                        width=1000,height=800,color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name="states",orientation="h")
    st.plotly_chart(fig_amount_3)



# sql connection(Query part RU)

def top_chart_registered_User(table_name, state):

    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="banumathy"
                        )

    #Plot_1
    query1= f''' SELECT districts, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts 
                ORDER BY registeredusers DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts", "registeredusers"))

    coll1,coll2=st.columns(2)
    with coll1:

        fig_amount=px.bar(df_1,x="districts", y="registeredusers", title="TOP 10 OF REGISTERED USER",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.haline,hover_name="districts")
        st.plotly_chart(fig_amount)


    #Plot_2

    query2= f''' SELECT districts, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts 
                ORDER BY registeredusers 
                LIMIT 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts", "registeredusers"))

    with coll2:

        fig_amount_2=px.bar(df_2,x="districts", y="registeredusers", title=" LAST 10 OF REGISTERED USER",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="districts")
        st.plotly_chart(fig_amount_2)


    #Plot_3

    query3= f''' SELECT districts, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts 
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts", "registeredusers"))

    fig_amount_3=px.bar(df_3,y="districts", x="registeredusers", title=" AVERAGE OF REGISTERED USER",
                        width=1000,height=800,color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name="districts",orientation="h")
    st.plotly_chart(fig_amount_3)


    
# sql connection(Query part AppOpens)

def top_chart_appopens(table_name, state):

    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="banumathy"
                        )

    #Plot_1
    query1= f''' SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts 
                ORDER BY appopens DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts", "appopens"))

    coll1,coll2=st.columns(2)
    with coll1:

        fig_amount=px.bar(df_1,x="districts", y="appopens", title="TOP 10 OF APPOPENS",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.haline,hover_name="districts")
        st.plotly_chart(fig_amount)


    #Plot_2

    query2= f''' SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts 
                ORDER BY appopens 
                LIMIT 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts", "appopens"))

    with coll2:

        fig_amount_2=px.bar(df_2,x="districts", y="appopens", title=" LAST 10 OF APPOPENS",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="districts")
        st.plotly_chart(fig_amount_2)


    #Plot_3

    query3= f''' SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts 
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts", "appopens"))
    

    fig_amount_3=px.bar(df_3,y="districts", x="appopens", title=" AVERAGE OF APPOPENS",
                        width=1000,height=800,color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name="districts",orientation="h")
    st.plotly_chart(fig_amount_3)

    
# sql connection(Query part RUS)

def top_chart_registered_Users(table_name):

    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="banumathy"
                        )

    #Plot_1
    query1= f''' SELECT states,SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states", "registeredusers"))
    coll1,coll2=st.columns(2)
    with coll1:

        fig_amount=px.bar(df_1,x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.haline,hover_name="states")
        st.plotly_chart(fig_amount)


    #Plot_2

    query2= f''' SELECT states,SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers 
                LIMIT 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states", "registeredusers"))
    with coll2:

        fig_amount_2=px.bar(df_2,x="states", y="registeredusers", title=" LAST 10 OF REGISTERED USERS",
                            width=600,height=600,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="states")
        st.plotly_chart(fig_amount_2)


    #Plot_3

    query3= f''' SELECT states,AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3=px.bar(df_3,y="states", x="registeredusers", title=" AVERAGE OF REGISTERED USER",
                        width=1000,height=800,color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name="states",orientation="h")
    st.plotly_chart(fig_amount_3)



#  streamlit

st.set_page_config(layout="wide")
st.title(" BANUMATHY'S PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select=option_menu("Menu",["Home","Data Exploration","Top Charts"])

if select=="Home":
    coll1,coll2=st.columns(2)
    with coll1:
        st.header("PHONEPE")
        st.subheader("INDIA'S FIRST TRANSCATION APP")
        st.markdown("Phonepe is an Indian digital payments and financial technology company")
        st.download_button("DOWNLAOD NOW","https://www.phonepe.com/app-download/")
    with coll2:
        st.image((r"C:\Users\Admin\Desktop/images3.jpg"),width=600)

    coll3,coll4=st.columns(2)
    with coll3:
        st.image((r"C:\Users\Admin\Desktop/images2.jpg"),width=600)
        


elif select=="Data Exploration":

    tab1,tab2,tab3=st.tabs(["Aggreated Analysis", "Map Analysis","Top Analaysis"])

    with tab1:
         
        method=st.radio("Choose the Method",["Aggreated Insurance", "Aggreated Transcation ","Aggreated User"])

        if method == "Aggreated Insurance":

            coll1,coll2=st.columns(2)
            with coll1:
             
                years= st.slider("Select The Year", Aggre_insurane["Years"].min(),Aggre_insurane["Years"].max(),Aggre_insurane["Years"].min())
            tac_y= Transcation_amount_count_Y(Aggre_insurane, years)

            coll1,coll2=st.columns(2)
            with coll1:

                quarters= st.slider("Select The Quarter",tac_y ["Quarter"].min(),tac_y["Quarter"].max(),tac_y["Quarter"].min())
            Transcation_amount_count_Y_Q(tac_y, quarters)

        elif method == "Aggreated Transcation ":

            coll1,coll2=st.columns(2)
            with coll1:
                
                years= st.slider("Select The Year", Aggre_tanscation["Years"].min(),Aggre_tanscation["Years"].max(),Aggre_tanscation["Years"].min())
            Aggre_tran_tac_Y= Transcation_amount_count_Y(Aggre_tanscation,years)
            
            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State", Aggre_tran_tac_Y["States"].unique())
                
            Aggre_Tran_Transcation_type(Aggre_tran_tac_Y,states)

            coll1,coll2=st.columns(2)
            with coll1:

                quarters= st.slider("Select The Quarter",Aggre_tran_tac_Y ["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transcation_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_Ty",Aggre_tran_tac_Y_Q["States"].unique())
                
            Aggre_Tran_Transcation_type(Aggre_tran_tac_Y_Q, states)


                
        elif method=="Aggreated User":

            coll1,coll2=st.columns(2)
            with coll1:
             
                years= st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot(Aggre_user,years)

            coll1,coll2=st.columns(2)
            with coll1:

                quarters= st.slider("Select The Quarter",Aggre_user_Y ["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot2(Aggre_user_Y,quarters)
            
            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select The State",Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q,states)

            

    with tab2:
         
         method_2=st.radio("Choose the method",["Map Insurance", "Map Transcation","Map User"])
         
         if method_2=="Map Insurance":
             
            coll1,coll2=st.columns(2)
            with coll1:
                
                years= st.slider("Select The Year_M_I", Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            map_insur_tac_Y= Transcation_amount_count_Y(Map_insurance,years)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_MI", map_insur_tac_Y["States"].unique())
                
            Map_insur_Districts(map_insur_tac_Y,states)

            coll1,coll2=st.columns(2)
            with coll1:

                quarters= st.slider("Select The Quarter_MQ",map_insur_tac_Y ["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q=Transcation_amount_count_Y_Q(map_insur_tac_Y, quarters)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_M_Ty",map_insur_tac_Y_Q["States"].unique())
                
            Map_insur_Districts(map_insur_tac_Y_Q, states)


         
         elif method_2=="Map Transcation":
             
            coll1,coll2=st.columns(2)
            with coll1:
                
                years= st.slider("Select The Year", Map_transcation["Years"].min(),Map_transcation["Years"].max(),Map_transcation["Years"].min())
            map_tran_tac_Y= Transcation_amount_count_Y(Map_transcation,years)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_MT", map_tran_tac_Y["States"].unique())
                
            Map_insur_Districts(map_tran_tac_Y,states)

            coll1,coll2=st.columns(2)
            with coll1:

                quarters= st.slider("Select The Quarter",map_tran_tac_Y ["Quarter"].min(),map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q=Transcation_amount_count_Y_Q(map_tran_tac_Y, quarters)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_MTy",map_tran_tac_Y_Q["States"].unique())
                
            Map_insur_Districts(map_tran_tac_Y_Q, states)

         
         elif method_2=="Map User":
             
            coll1,coll2=st.columns(2)
            with coll1:
                
                years= st.slider("Select The Year_MUY",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_Y= map_user_plot_1(Map_user,years)

            coll1,coll2=st.columns(2)
            with coll1:

                quarters= st.slider("Select The Quarter_MUQ",map_user_Y ["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            mmap_user_Y_Q=map_user_plot_2(map_user_Y, quarters)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_MU",mmap_user_Y_Q["States"].unique())
                
            map_user_plot_3(mmap_user_Y_Q, states)

             
     
    with tab3:
         
         method_3=st.radio("Choose the method",["Top Insurance", "Top Transcation","Top User"])
         
         if method_3=="Top Insurance":
             
            coll1,coll2=st.columns(2)
            with coll1:
                
                years= st.slider("Select The Year_T_I", Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            top_insur_tac_Y= Transcation_amount_count_Y(Top_insurance,years)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_TI",top_insur_tac_Y["States"].unique())
                
            Top_insurance_plot_1(top_insur_tac_Y, states)

            coll1,coll2=st.columns(2)
            with coll1:

                quarters= st.slider("Select The Quarter_MUQ",top_insur_tac_Y ["Quarter"].min(),top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q=Transcation_amount_count_Y_Q(top_insur_tac_Y, quarters)


         
         elif method_3=="Top Transcation":
             
            coll1,coll2=st.columns(2)
            with coll1:
                
                years= st.slider("Select The Year_T_T", Top_transcation["Years"].min(),Top_transcation["Years"].max(),Top_transcation["Years"].min())
            top_tran_tac_Y= Transcation_amount_count_Y(Top_transcation,years)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_TN",top_tran_tac_Y["States"].unique())
                
            Top_insurance_plot_1(top_tran_tac_Y, states)

            coll1,coll2=st.columns(2)
            with coll1:

                quarters= st.slider("Select The Quarter_TTQ",top_tran_tac_Y ["Quarter"].min(),top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q=Transcation_amount_count_Y_Q(top_tran_tac_Y, quarters)

         
         elif method_3=="Top User":
            coll1,coll2=st.columns(2)
            with coll1:
                
                years= st.slider("Select The Year_TU", Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            top_user_Y= top_user_plot_1(Top_user,years)

            coll1,coll2=st.columns(2)
            with coll1:
                states=st.selectbox("Select the State_T_U",top_user_Y["States"].unique())
                
            top_user_plot_2(top_user_Y, states)
             
         
elif select=="Top Charts":   
    question=st.selectbox("Select the question", ["1.Transcation Amount and Count of Aggreated Insurance",
                                                  "2.Transcation Amount and Count of Map Insurance",
                                                  "3.Transcation Amount and Count of Top Insurance",
                                                  "4.Transcation Amount and Count of Aggreated Transcation",
                                                  "5.Transcation Amount and Count of Map Transcation",
                                                  "6.Transcation Amount and Count of Top Transcation",
                                                  "7.Transcation Count of Aggreated User",
                                                  "8.Registered Users of Map User",
                                                  "9.App opens of Map User",
                                                  "10.Registered Users of Top User"])

    if question == "1.Transcation Amount and Count of Aggreated Insurance":

        st.subheader("TRANSCATION AMOUNT")
        top_chart_transcation_amount("aggreated_insurance")

        st.subheader("TRANSCATION COUNT")
        top_chart_transcation_count("aggreated_insurance")

    elif question == "2.Transcation Amount and Count of Map Insurance":

        st.subheader("TRANSCATION AMOUNT")
        top_chart_transcation_amount("map_insurance")

        st.subheader("TRANSCATION COUNT")
        top_chart_transcation_count("map_insurance")

    elif question == "3.Transcation Amount and Count of Top Insurance":

        st.subheader("TRANSCATION AMOUNT")
        top_chart_transcation_amount("top_insurance")

        st.subheader("TRANSCATION COUNT")
        top_chart_transcation_count("top_insurance")

    elif question == "4.Transcation Amount and Count of Aggreated Transcation":

        st.subheader("TRANSCATION AMOUNT")
        top_chart_transcation_amount("aggreated_transction")

        st.subheader("TRANSCATION COUNT")
        top_chart_transcation_count("aggreated_transction")

    elif question == "5.Transcation Amount and Count of Map Transcation":

        st.subheader("TRANSCATION AMOUNT")
        top_chart_transcation_amount("map_transcation")

        st.subheader("TRANSCATION COUNT")
        top_chart_transcation_count("map_transcation")

    elif question == "6.Transcation Amount and Count of Top Transcation":

        st.subheader("TRANSCATION AMOUNT")
        top_chart_transcation_amount("top_transcation")

        st.subheader("TRANSCATION COUNT")
        top_chart_transcation_count("top_transcation")

    elif question == "7.Transcation Count of Aggreated User":

        st.subheader("TRANSCATION COUNT")
        top_chart_transcation_count("aggreated_user")

    elif question == "8.Registered Users of Map User":

        states=st.selectbox("Select The State MUQ", Map_user["States"].unique())

        st.subheader("REGISTERED USERS")
        top_chart_registered_User("map_user", states)

    elif question == "9.App opens of Map User":

        states=st.selectbox("Select The State AS", Map_user["States"].unique())

        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question == "10.Registered Users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_Users("top_user")

    
         
