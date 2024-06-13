import pandas as pd
import streamlit as st
import plotly_express as px
import matplotlib.pyplot as plt
def medal_telly(df):
    tel_medal = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])

    tel_medal = tel_medal.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values(by="Gold",
                                                                                                ascending=False).reset_index()
    tel_medal["Total Medal"] = tel_medal["Gold"] + tel_medal["Silver"] + tel_medal["Bronze"]

    # Now we have to convert to the integer

    tel_medal["Gold"]=tel_medal["Gold"].astype("int")                  # "astype()" Function is use to change the Datatype
    tel_medal["Silver"] = tel_medal["Silver"].astype("int")
    tel_medal["Bronze"] = tel_medal["Bronze"].astype("int")
    tel_medal["Total Medal"] = tel_medal["Total Medal"].astype("int")

    return tel_medal

def country_year_list(df):
    years = df["Year"].unique().tolist()                   # tolist() Function is use to to change the data into the list
    years.sort()
    years.insert(0, "Overall")

    country=list(df["region"].dropna().unique())
    country.sort()
    country.insert(0, "Overall")

    return years,country

def fetch_country_year(df,y,c):
    medal_df= df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    flag=0
    if y=="Overall" and c=="Overall":
        tem_df=medal_df
    elif y=="Overall" and c!="Overall":
        flag=1
        tem_df=medal_df[medal_df["region"]==c]
    elif y!="Overall" and c=="Overall":
        tem_df=medal_df[medal_df["Year"]==y]
    elif y!="Overall" and c!="Overall":
        tem_df=medal_df[(medal_df["Year"]==y) & (medal_df["region"]==c)]
    if flag==1:
        x = tem_df.groupby("Year").sum()[["Gold","Silver","Bronze"]].sort_values(by="Year").reset_index()
    else:
        x = tem_df.groupby("region").sum()[["Gold","Silver","Bronze"]].sort_values(by="Gold",ascending=False).reset_index()
    x["Total Medal"]=x["Gold"]+x["Silver"]+x["Bronze"]

    x["Gold"]=x["Gold"].astype("int")                  # "astype()" Function is use to change the Datatype
    x["Silver"] = x["Silver"].astype("int")
    x["Bronze"] = x["Bronze"].astype("int")
    x["Total Medal"] = x["Total Medal"].astype("int")

    return x

def country_participated(df,col):
    gra1 = df.drop_duplicates(["Year", col])[["Year"]].value_counts().sort_index().reset_index()
    gra1.rename(columns={0: col}, inplace=True)
    return gra1

def best_ath_spo(df,spo,co):
    x = df.groupby("Name")[["Medal"]].count().merge(df, on="Name", how="right")[
        ["Name", "Medal_x", "Sport", "region"]].sort_values(by="Medal_x", ascending=False)
    x.drop_duplicates(["Name"], inplace=True)                                            # delete the duplicates
    x.reset_index(inplace=True)                                                      # reset_index
    x.drop(["index"], axis=1, inplace=True)                                         # drop the index column
    x.rename(columns={"Medal_x": "Total Medals", "region": "Region"}, inplace=True)
    x = x[x["Total Medals"] >= 1]
    if spo=="Overall" and co=="Overall":
        tem=x.head(25)
    elif spo!="Overall" and co=="Overall":
        tem=x[x["Sport"]==spo].reset_index().head(15).drop(["index"],axis=1)
    elif spo=="Overall" and co!="Overall":
        tem=x[x["Region"]==co].reset_index().head(15).drop(["index"],axis=1)
    elif spo!="Overall" and co!="Overall":
        tem=x[(x["Region"]==co) & (x["Sport"]==spo)].reset_index().head(15).drop(["index"],axis=1)
    return tem

def country_wise_analysis(df,country):
    temp=df.dropna(subset=["Medal"])
    temp.drop_duplicates(subset=["Year","Team","NOC","Games","City","Sport","Event","Medal"],inplace=True)
    if country=="Overall":
        pass
    elif country!="Overall":
        temp=temp[temp["region"]==country]
    final_df=temp.groupby("Year").count()[["Medal"]].reset_index()
    return final_df

def heatmap_country_analysis(df,country):
    temp=df.dropna(subset=["Medal"])
    temp.drop_duplicates(subset=["Year","Team","NOC","Games","City","Sport","Event","Medal"],inplace=True)
    if country=="Overall":
        pass
    elif country!="Overall":
        temp=temp[temp["region"]==country]
    return temp

def top_ath(df,country):
    if country=="Overall":
        x=df
    elif country!="Overall":
        x=df[df["region"]==country]
    x=x.groupby("Name")[["Medal"]].count().merge(df,on="Name",how="left").sort_values(by="Medal_x",ascending=False)
    x.drop_duplicates(["Name"],inplace=True)
    x.rename(columns={"Medal_x":"Medal"},inplace=True)
    x=x[["Name","Sport","Medal"]].reset_index().head(10)
    x.drop(["index"],axis=1,inplace=True)
    x=x[x["Medal"]>=1]
    return x

def zero_med(df):
    zero_medal = df.groupby("region").count()[["Medal"]]
    zero_medal = zero_medal[zero_medal["Medal"] == 0]
    zero_medal = zero_medal.index.tolist()
    return zero_medal

def age_distribution(df,selected):
    fig = plt.figure(figsize=(10, 6))
    age_data=df.drop_duplicates(subset=["Name","region"])
    age_data=age_data[["Age","Medal"]]
    age_data.Age.dropna(inplace=True)
    for i in selected:
        if i=="Overall":
            x1=age_data["Age"]
            plt.hist(x1,bins="auto",label="Age Distribution",color="Blue")
        if i=="Gold":
            x2=age_data[age_data["Medal"]=="Gold"]["Age"]
            plt.hist(x2,bins="auto",label="Gold Medal",color="Gold")
        if i=="Silver":
            x3=age_data[age_data["Medal"]=="Silver"]["Age"]
            plt.hist(x3,bins="auto",label="Silver Medal",color="Silver")
        if i=="Bronze":
            x4=age_data[age_data["Medal"]=="Bronze"]["Age"]
            plt.hist(x4,bins="auto",label="Bronze Medal",color="Brown")
    plt.legend()
    plt.xlabel("Age of Athlete",size=10)
    plt.ylabel("Number of Persons",size=10)
    return fig

def age_dist_top_10(df,selected):
    fig = plt.figure(figsize=(10, 6))
    top_spo=df["Sport"].value_counts().head(10)
    top_spo=top_spo.index.tolist()
    d=pd.DataFrame()
    for i in range(len(top_spo)):
        temp=df[df["Sport"]==top_spo[i]][["Age","Medal","Sport"]]
        d=pd.concat([d,temp])
    d.Age.dropna(inplace=True)
    for i in selected:
        if i=="Overall":
            x1=d["Age"]
            plt.hist(x1,bins="auto",label="Age Distribution",color="Blue")
        if i=="Athletics":
            x2=d[d["Sport"]=="Athletics"]["Age"]
            plt.hist(x2,bins="auto",label="Athletics",color="Red")
        if i=='Gymnastics':
            x3=d[d["Sport"]=='Gymnastics']["Age"]
            plt.hist(x3,bins="auto",label='Gymnastics',color="Yellow")
        if i=='Swimming':
            x4=d[d["Sport"]=='Swimming']["Age"]
            plt.hist(x4,bins="auto",label='Swimming',color="Green")
        if i=='Shooting':
            x4=d[d["Sport"]=='Shooting']["Age"]
            plt.hist(x4,bins="auto",label='Shooting',color="Pink")
        if i=='Cycling':
            x4=d[d["Sport"]=='Cycling']["Age"]
            plt.hist(x4,bins="auto",label='Cycling',color="Violet")
        if i=='Fencing':
            x4=d[d["Sport"]=='Fencing']["Age"]
            plt.hist(x4,bins="auto",label='Fencing')
        if i=='Rowing':
            x4=d[d["Sport"]=='Rowing']["Age"]
            plt.hist(x4,bins="auto",label='Rowing')
        if i=='Wrestling':
            x4=d[d["Sport"]=='Wrestling']["Age"]
            plt.hist(x4,bins="auto",label='Wrestling')
        if i=='Football':
            x4=d[d["Sport"]=='Football']["Age"]
            plt.hist(x4,bins="auto",label='Football')
        if i=='Sailing':
            x4=d[d["Sport"]=='Sailing']["Age"]
            plt.hist(x4,bins="auto",label='Sailing')
    plt.legend()
    plt.xlabel("Age of Athlete",size=10)
    plt.ylabel("Number of Persons",size=10)
    return fig

def male_fem_comp_part(df):
    fig = plt.figure(figsize=(10, 6))
    gender_age=df[["Age","Sex","Medal"]]
    boy_age=gender_age[gender_age["Sex"]=="M"]["Age"]
    girl_age=gender_age[gender_age["Sex"]=="F"]["Age"]
    plt.hist(boy_age,label="Male",color="blue",bins="auto")
    plt.hist(girl_age,label="Female",color="red",bins="auto")
    plt.legend()
    plt.xlabel("Year",size=10)
    plt.ylabel("Number of Persons",size=10)
    return fig

def gold_ath(df):
    fig = plt.figure(figsize=(10, 6))
    go=df[df["Medal"]=="Gold"][["Height","Weight"]]
    plt.scatter(x=df.Weight,y=df.Height,marker="d",c=df.Height,alpha=1.0,label="Athlete in Olympics")
    plt.scatter(x=go.Weight,y=go.Height,marker="h",c="Gold",alpha=0.7,label="Gold Medalist")
    plt.legend()
    plt.xlabel("Weight in kg",size=10)
    plt.ylabel("Height in cm",size=10)
    return fig

def male_fem_gold_comp(df,selected):
    fig = plt.figure(figsize=(10, 6))
    go_m=df[(df["Medal"]=="Gold") & (df["Sex"]=="M")][["Height","Weight"]]
    go_f=df[(df["Medal"]=="Gold") & (df["Sex"]=="F")][["Height","Weight"]]
    for i in selected:
        if i=="Overall":
            plt.scatter(x=df.Weight, y=df.Height, marker="d", c=df.Height, alpha=1.0, label="Athlete in Olympics")
        if i=="Male":
            plt.scatter(x=go_m.Weight,y=go_m.Height,marker="h",c="c",alpha=0.7,label="Male")
        if i=="Female":
            plt.scatter(x=go_f.Weight,y=go_f.Height,marker="^",c="r",alpha=0.7,label="Female")
    plt.legend()
    plt.xlabel("Weight in kg",size=10)
    plt.ylabel("Height in cm",size=10)
    return fig

def participation_in_genders(df):
    x=df.drop_duplicates(subset=["Year","Name","Team"])
    male_part=x[x["Sex"]=="M"].groupby("Year").count()["Name"].reset_index()
    female_part=x[x["Sex"]=="F"].groupby("Year").count()["Name"].reset_index()
    parti=male_part.merge(female_part,on="Year",how="left")
    parti.fillna(0,inplace=True)
    parti.rename(columns={"Name_x":"Male","Name_y":"Female"},inplace=True)
    x=px.line(x="Year",y=["Male","Female"],data_frame=parti)
    return x