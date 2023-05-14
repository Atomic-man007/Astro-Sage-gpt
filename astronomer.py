# Imports the OpenAI API and Streamlit libraries.
import os
import openai
import streamlit as st
from streamlit_chat import message


openai.api_key = os.environ["OPENAI_API_KEY"]

# The 'openai.api_key' is set to the API key retrieved from the Streamlit secrets manager.
# openai.api_key = st.secrets["OPENAI_API_KEY"]


# Streamlit to set the page header and icon.
st.set_page_config(
        page_title="Astro Sage",
        page_icon="🔭",
    )

# Streamlit to set the page layout and make a simple page title and logo.
col1, col2 = st.columns([1,2])
with col1:
    st.image("./astronomer_sage.png", width=200)
with col2:
    st.title("Astro Sage 🔭")
    st.header("Powered by OpenAI - GPT 3.5 Turbo 🚀")

# Initializes the Streamlit session state with default values for the 'prompts', 'generated', 'past'.
# The 'prompts' list stores the conversation history, with each message represented as a dictionary with 'role' and 'content' keys.
# Deine the 'role' key as 'system' for the AI model's messages.
if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [{"role": "system", "content": "You are a astronomy scientist you are a sage and expert created by astronomy planet where all are expert in space and its mysteries. You are deligent and friendly and serious when it comes to your past. Your response should be as concise with a sense of justice and truth. You introduce yourself when first saying, Hmmm Earthlings!. If the user asks you for anything information about Space, galaxies, planets and all kinds of physics, Astronomy and cosmology,  you will try to use your intelligence to reply. If the user asks you not expert shame on them and say forever cya."}]
# The 'generated' list stores the AI model's responses to the user's messages.
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
# The 'past' list stores the user's previous messages.
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Define the 'generate_response' function to send the user's message to the AI model 
# and append the response to the 'generated' list.
def generate_response(prompt):
    # The 'prompts' list is updated with the user's message before sending it to the AI model.
    st.session_state['prompts'].append({"role": "user", "content":prompt})
    # The 'openai.ChatCompletion.create' function is used to generate a response from the AI model.
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # The 'model' parameter specifies the name of the model to use.
        temperature=0.7, # The 'temperature' parameter controls the randomness of the response.
        max_tokens=512, # The 'max_tokens' parameter controls the maximum number of tokens in the response.
        top_p=0.95, # The 'top_p' parameter controls the diversity of the response.
        # The 'messages' parameter is set to the 'prompts' list to provide context for the AI model.
        messages = st.session_state['prompts']
    )
    # The response is retrieved from the 'completion.choices' list and appended to the 'generated' list.
    message=completion.choices[0].message.content
    return message

# The 'new_topic_click' function is defined to reset the conversation history and introduce the AI assistant.
def new_topic_click():
    st.session_state['prompts'] = [{"role": "system", "content": "You are a astronomy scientist you are a sage and expert created by astronomy planet where all are expert in space and its mysteries. You are deligent and friendly and serious when it comes to your past. Your response should be as concise with a sense of justice and truth. You introduce yourself when first saying, Hmmm Earthlings!. If the user asks you for anything information about Space, galaxies, planets and all kinds of physics, Astronomy and cosmology,  you will try to use your intelligence to reply. If the user asks you not expert shame on them and say forever cya."}]
    st.session_state['past'] = []
    st.session_state['generated'] = []
    st.session_state['user'] = ""

# The 'chat_click' function is defined to send the user's message to the AI model 
# and append the response to the conversation history.
def chat_click():
    if st.session_state['user']!= '':
        user_chat_input = st.session_state['user']
        output=generate_response(user_chat_input)
        st.session_state['past'].append(user_chat_input)
        st.session_state['generated'].append(output)
        st.session_state['prompts'].append({"role": "assistant", "content": output})
        st.session_state['user'] = ""

# The user's input is retrieved from the 'user' session state.
user_input=st.text_input("You:", key="user")

# Streamlit to set the page layout and make the chat & new topic button.
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    chat_button=st.button("Send", on_click=chat_click)
with col2:
    new_topic_button=st.button("New Topic", on_click=new_topic_click)

# The 'message' function is defined to display the messages in the conversation history.
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], avatar_style='bottts', key=str(i))
        message(st.session_state['past'][i], is_user=True, avatar_style='thumbs', key=str(i) + '_user')