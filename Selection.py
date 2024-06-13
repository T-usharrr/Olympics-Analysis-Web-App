import streamlit as st
from streamlit_option_menu import option_menu
def choice_bar():
    with st.sidebar:
        ch = option_menu(menu_title="Main Menu", options=["Medal Telly"
            , "Overall Analysis"
            , "Country-Wise Analysis"
            , "Athlete-Wise Analysis"], menu_icon="cast", icons=["house", "bar-chart-fill", "globe", "person-walking"]
                         , styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#77FF4B"},
            })
    li=["Medal Telly", "Overall Analysis", "Country-Wise Analysis", "Athlete-Wise Analysis"]
    ind=li.index(ch)
    ch = option_menu(menu_title="Main Menu", options=["Medal Telly"
        , "Overall Analysis"
        , "Country-Wise Analysis"
        , "Athlete-Wise Analysis"], default_index=ind, menu_icon="cast",
                     icons=["house", "bar-chart-fill", "globe", "person-walking"],orientation="horizontal"
                     , styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#77FF4B"},
        })
    return ch

def choice_bar_hor():
    ch = option_menu(menu_title="Main Menu", options=["Medal Telly"
        , "Overall Analysis"
        , "Country-Wise Analysis"
        , "Athlete-Wise Analysis"], default_index=0, menu_icon="cast",
                     icons=["house", "bar-chart-fill", "globe", "person-walking"],orientation="horizontal"
                     , styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#77FF4B"},
        })
    li = ["Medal Telly", "Overall Analysis", "Country-Wise Analysis", "Athlete-Wise Analysis"]
    ind = li.index(ch)
    with st.sidebar:
        ch = option_menu(menu_title="Main Menu", options=["Medal Telly"
            , "Overall Analysis"
            , "Country-Wise Analysis"
            , "Athlete-Wise Analysis"],default_index=ind, menu_icon="cast", icons=["house", "bar-chart-fill", "globe", "person-walking"]
                         , styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#77FF4B"},
            })
    return ch





