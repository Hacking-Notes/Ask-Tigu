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

st.set_page_config(page_title='Star Atlas FAQ', page_icon='https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://staratlas.help&size=16')
st.title("Star Atlas FAQ")
st.markdown('Introducing our webpage featuring a ChatGPT-powered chatbot for quick and accurate responses to FAQs.  \
    With a user-friendly interface, simply type in your question and get an instant response. \
        Our constantly-learning chatbot can handle multiple queries at once, ensuring the best experience for support. Try it out now!')

#authenticate_user()

openai.api_key = "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"

if 'settings' not in st.session_state:
    st.session_state['settings'] = {}

# App layout
tab1, tab2, tab3, tab4 = st.tabs(["Ask a question", "Internet search", "Create your Assistant", "Settings"])

# Have a conversation tab
with tab1:
    response = st.container()
    chat = st.container()
    
# Internet search tab
with tab2:
    st.markdown("<span style='font-size:2em'>\
        Tell the Assistant what to research about.</span>", unsafe_allow_html=True)
    st.markdown("This tab allows you to give information from across the internet to the Assistant AI. \
        Once you've told it all the topics to search for, you can have a conversation with it in the \
            'Have a conversation' tab.")
    with st.spinner("Getting search history..."):
        google_history = get_user_search_history()
    unique_searches = google_history['query'].unique().tolist()
    unique_searches.insert(0,'')
    initial_search = st.selectbox('Search history', unique_searches, index=0)
    search = st.container()

with tab3:
    st.write("<span style='font-size:2em'>Comming soon...</span>", unsafe_allow_html=True)
    st.write("In this page you will be able to create custom Assistant archetypes.")

with tab4:
    #logout_button()
    reset_key_button()
    #delete_history_button()
    #delete_user_button()


# Google search section
with search:
    with st.form('Google'):
        user_query_text = st.text_input(label='Google search',value=initial_search, help="This tab \
            allows you to give information from across the internet to the Assistant AI. Once you've \
                told it all the topics to search for, you can have a conversation with it in the \
                    'Have a conversation' tab.")
        google_submitted = st.form_submit_button("Submit")

        # If the user pressed submit to make a new search or selected an existing one from history
        if (google_submitted and user_query_text != '') or initial_search != '':
            google_findings, links = make_new_internet_search(user_query_text)
            
            display_search_results(user_query_text, google_findings, links)

# Section where user inputs directly to GPT
with chat:
    with st.form('Chat'):
        user_chat_text = st.text_area(label="Ask the Assistant")
        col1, col2 = st.columns(2)
        chat_submitted = col1.form_submit_button("Submit")
        settings = assistant_settings(chat_submitted, col2)
    add_searches(settings)
        
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

add_vertical_space(2)

col1, col2, col3 = st.columns(3)
with col1:
    url = 'https://play.staratlas.com/market/?oid=3&affid=141'
if st.button('🛒 ---> Star Atlas Market Place', key='Market Place'):
    st.markdown(f'<a href="{url}" target="_blank">Link</a>', unsafe_allow_html=True)
with col2:
    st.container()
with col3:
    st.container()

st.markdown('<style>.css-1lsmgbg.egzxvld0 {display: none;}</style>', unsafe_allow_html=True)
st.markdown('<style>a.viewerBadge_container__1QSob {font-size: .001rem !important;}</style>', unsafe_allow_html=True)
st.markdown('<style>.row-widget.stCheckbox{visibility:hidden;display:none;}</style>', unsafe_allow_html=True)
st.markdown('<style>#tabs-bui3-tab-1 {visibility:hidden;display:none;}</style>', unsafe_allow_html=True)
st.markdown('<style>#tabs-bui3-tab-2 {visibility:hidden;display:none;}</style>', unsafe_allow_html=True)
st.markdown('<style>#tabs-bui3-tab-3 {visibility:hidden;display:none;}</style>', unsafe_allow_html=True)
st.markdown('<style>.css-1fcdlhc.e1s6o5jp0 {display:none !important;}</style>', unsafe_allow_html=True)
