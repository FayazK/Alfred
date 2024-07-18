import streamlit as st
from index import read_image
from server import show_records
from streamlit_card import card
import ChatUI
import FileUpload
import requests


def handle_card_click(record):
    link = record["link"]
    if link not in st.session_state:
        st.session_state[link] = ''
    if record["type"] == 'upload':
        st.experimental_set_query_params(page='upload', uuid='')
        st.session_state.current_screen = 'upload'
        st.session_state.UUID = ''

    
        # st.experimental_set_query_params(page='upload')
    elif record["type"] == 'chat':
        st.experimental_set_query_params(page='chat', uuid=record["link"])
        st.session_state.current_screen = 'chat'
        st.session_state.UUID = record["link"]
        st.session_state.chat_id = ''
        # st.experimental_set_query_params(page='chat', uuid=record["link"])
    
    st.experimental_rerun()


def data():
    recocrds = show_records()
    recocrds.append({'name': "", 'date': "Create Assistant!", 'image': 'static/plus.png','link': f'','key':0,'type':'upload'})
    return recocrds


def Home():
    st.markdown("<h1 style='text-align: center;'>Alfred</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    recocrds = data()
    for i, record in enumerate(recocrds):
        with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
            imagedata = read_image(path = record['image'])
            card_element = card(
            title=record["name"],
            text=record["date"],
            image=imagedata,
            url='',
            key = record["key"],
            styles={
                "card": {
                "width": "190px",
                "border-radius": "20px",
                "box-shadow": "0 0 10px rgba(0,0,0,0)"
                },
                "title": {
                "font-size": "20px" ,
                "position": "absolute",
                "top": "10px",
                "color":"#CACFD2 "
                 },
                 "text": {
                     "position": "absolute",
                    "bottom": "10px",
                    "left": "10px",
                    "right": "10px",
                 }

            },
            on_click=lambda r=record: handle_card_click(r)
        )



st.set_page_config(layout="wide", page_title="Alfred")

# Get all the assistants from databse

if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'home'

if 'UUID' not in st.session_state:
    st.session_state.UUID = ''
if 'chat_id' not in st.session_state:
    st.session_state.chat_id = ''

current_screen = st.experimental_get_query_params().get('page', ['home'])[0]
uuid = st.experimental_get_query_params().get('uuid', [''])[0]


if current_screen == 'home':
    Home()
elif current_screen == 'chat':
    if uuid not in st.session_state:
        st.session_state[uuid] = ''
    st.session_state.UUID = uuid
    ChatUI.chatting(UUID=st.session_state.UUID, Chat_id=st.session_state[st.session_state.UUID])
elif current_screen == 'upload':
    FileUpload.file_upload()