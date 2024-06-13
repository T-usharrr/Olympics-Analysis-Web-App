import streamlit as st       # for the web creation
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import Preprocessor as p
import Helper as h
import Statements as sta
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")

# We First create the side bar radio buttons
# st.sidebar.title("Olympics")
st.sidebar.image("https://colorlib.com/wp/wp-content/uploads/sites/2/2014/02/Olympic-logo.png")
#st.sidebar.title("Olympics")

with st.sidebar:
    ch=option_menu(menu_title="Main Menu",options=["Medal Telly"
                                        ,"Overall Analysis"
                                        ,"Country Wise Analysis"
                                        ,"Athlete Wise Analysis"],menu_icon="cast",icons=["house","bar-chart-fill","globe","person-walking"]
                   ,styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"},
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#77FF4B"},
    })




#ch=st.sidebar.radio("Choose your Options",("Medal Telly"
 #                                       ,"Overall Analysis"
  #                                      ,"Country-Wise Analysis"
   #                                     ,"Athlete-Wise Analysis"))

# Gaving the title to the sidebar

# st.sidebar.divider()

# "streamlit run app.py" statement will run on the terminal for the web server show

df=p.process(df,region_df)

# st.dataframe(df)

# all the part of the Medal Telly
if ch == "Medal Telly":
    st.title("Olympic Games")
    st.write(sta.sta1(1))
    st.image("https://globallygrounded.com/wp-content/uploads/2016/08/olympic-games.jpg")
    st.sidebar.title("Olyampics Analysis")
    st.sidebar.header("Medal Telly")
    years,country=h.country_year_list(df)

    # "Sidebar.selectbox()" function is used for the drop down menu
    selected_year = st.sidebar.selectbox("Select the Year",years)
    selected_country = st.sidebar.selectbox("Select the Country",country)

    if selected_year=="Overall" and selected_country=="Overall":
        st.title("Overall Telly in Olyampics")
    elif selected_year == "Overall" and selected_country!="Overall":
        st.title(f"{selected_country}'s Overall Performance in Olyampics")
    elif selected_year != "Overall" and selected_country == "Overall":
        st.title(f"Medal Telly Olyampics in {str(selected_year)}")
    elif selected_year!= "Overall" and selected_country != "Overall":
        st.title(f"{selected_country}'s Performance in {selected_year} in Olyampics")

    st.write(sta.sta1(2))

    # TO make the selectbox work we have to make a function for it

    med_t=h.fetch_country_year(df,selected_year,selected_country)

    # Tabel function is use to gave the data in the tabular format
    st.table(med_t)
    st.title("")
    st.text(sta.sta1(3))

if ch == "Overall Analysis":
    st.sidebar.title("**DID YOU KNOW?**")
    st.sidebar.write(sta.sta1(8))
    st.title("Top Statistics")

    # basic numbers for the analysis
    ed=df["Year"].unique().size-1
    spo=df["Sport"].unique().size
    eve=df["Event"].unique().size
    ci=df["City"].unique().size
    na=df["Name"].unique().size
    co=df["region"].unique().size

    # columns() takes no of divisions for the container to make small size columns
    c1,c2,c3=st.columns(3)

    # "with" is use for every container in a single line
    with c1:
        st.header("Sports")
        st.subheader(spo)
    with c2:
        st.header("Events")
        st.subheader(eve)
    with c3:
        st.header("Hosts")
        st.subheader(ci)

    c4, c5, c6=st.columns(3)

    with c4:
        st.header("Athletes")
        st.subheader(na)
    with c5:
        st.header("Nations")
        st.subheader(co)
    with c6:
        st.header("Editions")
        st.subheader(ed)

    # Now Show the overall Charts of Olyampics

    # total countries
    st.title("")
    st.title("Number of Countries Participated over Years")
    gra1=h.country_participated(df,"region")
    g1 = px.line(gra1, x="Year", y="region", height=470, width=650)
    st.plotly_chart(g1)
    st.subheader("Reasons for Major Delcine in Olympics")
    st.write(sta.sta1(4))

    # total events
    st.title("Number of Events occur over Years")
    gra2=h.country_participated(df,"Event")
    g2 = px.bar(data_frame=gra2, x="Year", y="Event",color="Event")
    st.plotly_chart(g2)
    st.write(sta.sta1(5))

    # heatmap every sport
    st.title("Every Sport Event over Time")
    fi=plt.figure(figsize=(21,16))
    x = df.drop_duplicates(["Year", "Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"),
                annot=True)
    plt.xlabel("Year",size=20)
    plt.ylabel("Sport",size=20)
    st.pyplot(fi)                               # sns and plt can work together
                                                     # by gaving only the figure the value is also taken in st
    st.write(sta.sta1(6))

    # Overall Athledes and sort by sports
    st.title("Top Athletes is Olympics")
    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")
    st.write(sta.sta1(7))

    c1,c2=st.columns(2)
    with c1:
        selected_sport=st.selectbox("Select the Sport",sports_list)
    with c2:
        year,country=h.country_year_list(df)
        selected_co=st.selectbox("Select the Country",country)


    ath_tab=h.best_ath_spo(df, selected_sport,selected_co)
    st.table(ath_tab)

if ch=="Country Wise Analysis":
    st.sidebar.title("**DID YOU KNOW?**")
    st.sidebar.write(sta.sta1(9))
    st.title("Country Wise Analysis")
    year,country=h.country_year_list(df)
    selected_country_analysis=st.selectbox("Choose the Country",country)
    if selected_country_analysis=="Overall":
        st.header("All Country Analysis")
    elif selected_country_analysis!="Overall":
        st.header(f"{selected_country_analysis} Country Analysis")
    data=h.country_wise_analysis(df,selected_country_analysis)
    g4 = px.line(x="Year", y="Medal", data_frame=data)
    st.plotly_chart(g4)

    if selected_country_analysis == "Overall":
        st.header("All Sport Medals Analysis")
    elif selected_country_analysis != "Overall":
        st.header(f"{selected_country_analysis} Sport Medal Analysis")
    data=h.heatmap_country_analysis(df, selected_country_analysis)
    try:
        fig=plt.figure(figsize=(21,16))
        g5=sns.heatmap(data.pivot_table(columns="Year",index="Sport",values="Medal",aggfunc="count").fillna(0).astype("int"),annot=True)
        plt.xlabel("Year",size=20)
        plt.ylabel("Sports",size=20)
        st.pyplot(fig)
    except:
        st.title("Heat Map can't be Possible for this Country")

    if selected_country_analysis == "Overall":
        st.header("Top 10 Athletes")
    elif selected_country_analysis != "Overall":
        st.header(f"{selected_country_analysis}'s Top Athletes")
    data3=h.top_ath(df,selected_country_analysis)
    st.table(data3)


if ch=="Athlete Wise Analysis":
    st.sidebar.title("**DID YOU KNOW?**")
    st.sidebar.write(sta.sta1(10))
    st.title("Athlete Wise Analysis")
    st.header("Age Distribution in Olympics")
    sele_data=st.multiselect("Select the Options",["Overall","Gold","Silver","Bronze"],default=["Overall"])
    g6=h.age_distribution(df,sele_data)
    st.pyplot(g6)
    st.write(sta.sta1(11))

    st.header("Top 10 Sport Athletes Age Distribution")
    top_spo=df["Sport"].value_counts().head(10)
    top_spo=top_spo.index.tolist()
    top_spo.insert(0,"Overall")
    st.write(sta.sta1(12))
    sele_top_spo=st.multiselect("Select the Sports",top_spo,default=['Athletics'])
    g7=h.age_dist_top_10(df,sele_top_spo)
    st.pyplot(g7)

    st.header("Gender Wise Age Distribution")
    g8=h.male_fem_comp_part(df)
    st.pyplot(g8)
    st.write(sta.sta1(13))

    st.header("Weight to Height Analysis of Gold Medalists")
    g9=h.gold_ath(df)
    st.pyplot(g9)
    st.write(sta.sta1(14))

    st.header("Different Gender Gold Medalists Analysis")
    selected_gender=st.multiselect("Select the Gender",["Male","Female","Overall"],default=["Male","Female"])
    g10=h.male_fem_gold_comp(df,selected_gender)
    st.pyplot(g10)
    st.write(sta.sta1(15))

    st.header("Different Gender Participation over Years")
    g11=h.participation_in_genders(df)
    st.plotly_chart(g11)
    st.write(sta.sta1(16))

