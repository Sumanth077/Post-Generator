import streamlit as st
import time
from steamship import Steamship
from steamship.base import TaskState

api_key="35739754-99DE-4585-86E4-DD10706414F3"

instance = Steamship(st.secrets["apikey"]).use(package_handle = "audio-description", instance_handle="new-instance")

st.title('Post Generator ❤️')
st.text("")
st.header('Are you a Content Creator and want to generate Social Media Posts \
          Describing your New Video ? 🎥 '
       )
st.text("")
st.text("")


def refresh_state():
	st.session_state['status'] = 'submitted'

url = st.text_input('Place the Link of your Video here and see the magic 🪄',value='https://youtu.be/n8NgvECmq-M',on_change=refresh_state)
st.text("")
st.button('Generate')

st.video(url)

@st.cache
def generate(link):
    transcribe_task = instance.invoke("analyze_youtube", url=str(link))
    task_id = transcribe_task["task_id"]
    status = transcribe_task["status"]
    retries = 0
    while retries <= 100 and status != TaskState.succeeded:
        response = instance.invoke("status", task_id=task_id)
        status = response["status"]
        if status == TaskState.failed:
            print(f"[FAILED] {response['status_message']}")
            break

        print(f"[Try {retries}] Transcription {status}.")
        if status == TaskState.succeeded:
            break
        time.sleep(2)
        retries += 1
    return response

response = generate(url)


output = response['file']
st.write(output)
