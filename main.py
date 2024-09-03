import streamlit as st
from pyht import Client, TTSOptions, Format
from io import BytesIO
import base64
import streamlit.components.v1 as components
from kratos import Kratos
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------- Environment Variables ------------------ #

USER_ID = os.environ["PLAYHT_ID"]
API_KEY = os.environ["PLAYHT_API_KEY"]

# ------------------- Initialize AI Model -------------------- #
kratos = Kratos()

# ------------------------ PlayHT TTS ------------------------ #

# Initialize PlayHT API with your credentials
client = Client(user_id=USER_ID, api_key=API_KEY)

# Configure your TTS options
options = TTSOptions(
    voice="s3://voice-cloning-zero-shot/78a93d00-1e21-4d84-816e-25e34c9842e4/original/manifest.json",  # Replace with Kratos voice ID
    sample_rate=44_100,
    format=Format.FORMAT_MP3,
    speed=0.8,
)

# --------------------- Streamlit Website --------------------- #

st.markdown("<h1 style='text-align: left; color: white;'>Kratos - <span style='color: #FF3131;'>GPT</span></h1>", unsafe_allow_html=True)

# Initialize Chatbot
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initial Chat Icons
avatars = {
    "user": "./atreus.jpg",
    "assistant": "./kratos.jpg"
}

# Display messages in session state
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars.get(message["role"], "")):
        st.markdown(message["content"])

# Take Input for Chat
prompt = st.chat_input("Speak, boy.")
if prompt:

    # Display user inputted prompt as user message
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)

    # Append user message to messages in session state
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Get Response from AI model using prompt
    response = kratos.get_response(prompt)
    
    try:
        # Audio Conversion for html embedding
        audio_chunks = client.tts(text=response, voice_engine="PlayHT2.0-turbo", options=options)
        audio_stream = audio_stream = BytesIO(b''.join(audio_chunks))
        audio_base64 = base64.b64encode(audio_stream.getvalue()).decode("ascii")

        # Play, Copy and Download Functionality (js/html/css)
        functionality = f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <!-- Speaker Icon (Replay) -->
            <button onclick="document.getElementById('audio').play()" style="
                border: none;
                background: none;
                cursor: pointer;
                font-size: 8px;  /* Smaller icon size */
                color: white;
                margin-left: 10px; /* Move icon slightly to the right */
            ">
                <i class="fa fa-volume-up" style="color: white; font-size: 18px;"></i>
            </button>

            <!-- Copy Button -->
            <button onclick="copyText()" style="
                border: none;
                background: none;
                cursor: pointer;
                font-size: 8px;  /* Smaller icon size */
                color: white;
                margin-left: 3px; /* Move icon slightly to the right */
            ">
                <i class="fa fa-copy" style="color: white; font-size: 18px;"></i>
            </button>

            <!-- Save Button -->
            <a href="data:audio/mp3;base64,{audio_base64}" download="response.mp3" style="
                border: none;
                background: none;
                cursor: pointer;
                font-size: 8px;  /* Smaller icon size */
                color: white;
                margin-left: 5px; /* Move icon slightly to the right */
            ">
                <i class="fa fa-download" style="color: white; font-size: 18px;"></i>
            </a>
        </div>
        <audio id="audio" src="data:audio/mp3;base64,{audio_base64}" autoplay></audio>
        <script>
            function copyText() {{
                const textToCopy = `{response}`;
                navigator.clipboard.writeText(textToCopy).then(() => {{
                    alert('Text copied to clipboard!');
                }});
            }}
        </script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        """
        with st.chat_message("assistant", avatar=avatars["assistant"]):
            st.markdown(response)

        st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

        #Play Audio and Spawn Buttons
        components.html(functionality, height=30) 

    # Error Handling
    except Exception as e:
        st.write(f"An error occured: {e}")