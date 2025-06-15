import os
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, AsyncOpenAI
from agents.run import RunConfig
import asyncio


# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL="gemini-2.0-flash"

client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=gemini_api_key
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client,

)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

translator = Agent(name="Language Translator",instructions="You are a language translator.",model=model)


async def translate(text,lan):
    response = await Runner.run(translator,
            f"Translate {text} into {lang}",
            run_config=config
            )
    return response.final_output


# Supported Languages
languages = [
    "Urdu", "French", "Spanish", "German", "Chinese", "Japanese", "Korean", "Arabic",
    "Portuguese", "Russian", "Hindi", "Bengali", "Turkish", "Italian", "Dutch", "Greek",
    "Polish", "Swedish", "Thai", "Vietnamese", "Hebrew", "Malay", "Czech", "Romanian", "Finnish"
]

# Streamlit UI
st.set_page_config(page_title="Translator by Shahab", layout="centered")
st.markdown("""
    <style>
            .stApp {
            background: #8E2DE2;  /* fallback for old browsers */
background: -webkit-linear-gradient(to right, #4A00E0, #8E2DE2);  /* Chrome 10-25, Safari 5.1-6 */
background: linear-gradient(to right, #4A00E0, #8E2DE2); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

            }

    </style>        
""",unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>🌐 AI Translator </h1>",unsafe_allow_html=True)
st.write("Created by **Shahab** – Translate your English text into various languages using Gemini AI.")

text = st.text_area("Enter English text to translate:", height=150)
lang = st.selectbox("Select target language:", languages)
btn = st.button("Translate")

if btn and text:
    try:
        with st.spinner("Translation in process........."):
            translated_text = asyncio.run(translate(text,lang))
            st.success(f"Translated into {lang}")
            st.info(f"Origional Text: {text}")
            st.text_area("Translate text: ",value=translated_text,height=200)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")