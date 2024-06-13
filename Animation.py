import streamlit as st       # for the web creation
import json
import requests
import streamlit_lottie

def load_lottie(path):
    f=open(path,"r")
    return json.load(f)

def ani_lottie(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json
