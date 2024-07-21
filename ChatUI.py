import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
from server import index


def chatting(UUID,Chat_id ):
    st.markdown("<h1 style='text-align: center;'>Chat placeholder</h1>", unsafe_allow_html=True)
    uuid = UUID
    chat_id = Chat_id
    if 'user_input' not in st.session_state and 'past' in st.session_state:
            del st.session_state.past[:]
            del st.session_state.generated[:]
    def on_input_change():
        user_input = st.session_state.user_input
        st.session_state.past.append(user_input)
        response = index(uuid=uuid, u_input=user_input, chat_id=chat_id)
        response['message'] = response['message'].replace("```html", "").replace("```", "")
        print('response by LLM recived at ChatUI ++++  ++++++ ++++',response)
        st.session_state[uuid] = response['chat_id']
        st.session_state.generated.append(response)
        st.session_state.user_input = ''

    def on_btn_click():
        del st.session_state.past[:]
        del st.session_state.generated[:]

    st.session_state.setdefault(
        'past', 
        []
    )
    st.session_state.setdefault(
        'generated', 
        []
    )

    chat_placeholder = st.empty()
    with chat_placeholder.container():    
        for i in range(len(st.session_state['past'])):                
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
            message(
                st.session_state['generated'][i]['message'], 
                key=f"{i}", 
                allow_html=True
            )
        st.button("Clear message", on_click=on_btn_click)


    with st.container():
        uinput = st.text_input("User Input:", on_change=on_input_change, key="user_input")

