import base64
from streamlit_card import card
import streamlit as st

def read_image(path):
    with open(path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data

def Card_layout(name, description, image_url,url,key):
    return card(
         title=name,
         text=description,
         image=image_url,
         url=url,
         key = key,
         styles={
            "card": {
            "width": "230px",
            "border-radius": "20px",
            "box-shadow": "0 0 10px rgba(0,0,0,0)"
              }
         },
        )