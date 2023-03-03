import streamlit as st
from streamlit_extras import buy_me_a_coffee
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.badges import badge
from streamlit_lottie import st_lottie
import openai
from utils import load_lottie_url
from api_key import load_api_key, reset_key_button
from internet_search import *
from assistant import *
from gpt_api import find_top_similar_results
from auth import authenticate_user, logout_button
from database import delete_user_button

st.set_page_config(page_title='Star Atlas FAQ')
st.title("Star Atlas FAQ")
st.markdown('Introducing our webpage featuring a ChatGPT-powered chatbot for quick and accurate responses to FAQs.  \
    With a user-friendly interface, simply type in your question and get an instant response. \
        Our constantly-learning chatbot can handle multiple queries at once, ensuring the best experience for support. Try it out now!')

#authenticate_user()

openai.api_key = load_api_key()

if 'settings' not in st.session_state:
    st.session_state['settings'] = {}

# App layout
tab1, tab2, tab3, tab4 = st.tabs(["Have a conversation", "Internet search", "Create your Assistant", "Settings"])

# Have a conversation tab
with tab1:
    response = st.container()
    chat = st.container()

# Section where user inputs directly to GPT
with chat:
    with st.form('Chat'):
        user_chat_text = st.text_area(label="Ask the Assistant")
        col1, col2 = st.columns(2)
        chat_submitted = col1.form_submit_button("Submit")
        settings = assistant_settings(chat_submitted, col2)



# User input is used here to process and display GPT's response
with response:
    if 'archetype' not in settings:
        archetypes, default_setting_index = load_assistant_settings()
        default_setting = list(archetypes.keys())[default_setting_index]
        settings['archetype'] = archetypes[default_setting]
    starting_conversation = settings['archetype']['starting_conversation']
    load_conversation(starting_conversation)
    display_chat_history(starting_conversation)
    if chat_submitted:
        submit_user_message(settings, user_chat_text, chat_submitted)

add_vertical_space(4)

col1, col2, col3 = st.columns(3)
with col1:
    url = 'https://play.staratlas.com/market/?oid=3&affid=141'
if st.button('Market Place', key='Market Place'):
    st.markdown(f'<a href="{url}" target="_blank">Link</a>', unsafe_allow_html=True)
with col2:
    st.container()
with col3:
    st.container()
