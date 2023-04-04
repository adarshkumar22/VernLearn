import streamlit as st
from pytube import YouTube
import os
import requests
from zipfile import ZipFile
from googletrans import Translator
from dotenv import load_dotenv

translator = Translator()

load_dotenv()
api_key = os.getenv("API_KEY")

st.markdown('# 📝 **VernLearn**')
bar = st.progress(0)

# https://www.youtube.com/watch?v=c2Sn-pP3uxo

# Custom functions 

# 2. Retrieving audio file from YouTube video
def get_yt(URL):
    video = YouTube(URL)
    yt = video.streams.get_audio_only()
    yt.download()

    #st.info('2. Audio file has been retrieved from YouTube video')
    bar.progress(10)

# 3. Upload YouTube audio file to AssemblyAI
def transcribe_yt():

    current_dir = os.getcwd()

    for file in os.listdir(current_dir):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(current_dir, file)
            #print(mp4_file)
    filename = mp4_file
    bar.progress(20)
    
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))
    
    audio_url = response.json()["upload_url"]

    #st.info('3. YouTube audio file has been uploaded to AssemblyAI')
    bar.progress(30)

    # 4. Transcribe uploaded audio file
    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
    "audio_url": audio_url
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    transcript_input_response = requests.post(endpoint, json=json, headers=headers)

    #st.info('4. Transcribing uploaded file')
    bar.progress(40)

    # 5. Extract transcript ID
    transcript_id = transcript_input_response.json()["id"]
    #st.info('5. Extract transcript ID')
    bar.progress(50)

    # 6. Retrieve transcription results
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }
    transcript_output_response = requests.get(endpoint, headers=headers)
    #st.info('6. Retrieve transcription results')
    bar.progress(60)

    # Check if transcription is complete
    from time import sleep
    msgShow = 'Transcription is processing ...'
    st.warning(msgShow)
    while transcript_output_response.json()['status'] != 'completed':
        transcript_output_response = requests.get(endpoint, headers=headers)
    msgShow = 'Transcription is processed!'
    bar.progress(100)

    # 7. Print transcribed text
    

    englishText = transcript_output_response.json()["text"]
    englishText = str(englishText)
    english = translator.translate(englishText, dest='en')
    hindi = translator.translate(englishText, dest='hi')
    bengali = translator.translate(englishText, dest='bn')
    tamil = translator.translate(englishText, dest='ta')
    telugu = translator.translate(englishText, dest='te')
    gujrati = translator.translate(englishText, dest='gu')
    malayalam = translator.translate(englishText, dest='ml')
    marathi = translator.translate(englishText, dest='mr')
    urdu = translator.translate(englishText, dest='ur')
    
    selectedLang = ""

    if option == 'English':
        st.header('Output English')
        st.success(english.text)
        selectedLang = english.text
    elif option == 'Hindi':
        st.header('Output Hindi')
        st.info(hindi.text)
        selectedLang = hindi.text
    elif option == 'Bengali':
        st.header('Output Bengali')
        st.success(bengali.text)
        selectedLang = bengali.text
    elif option == 'Tamil':
        st.header('Output Tamil')
        st.info(tamil.text)
        selectedLang = tamil.text
    elif option == 'Telugu':
        st.header('Output Telugu')
        st.success(telugu.text)
        selectedLang = telugu.text
    elif option == 'Gujrati':
        st.header('Output Gujrati')
        st.info(gujrati.text)
        selectedLang = gujrati.text
    elif option == 'Malayalam':
        st.header('Output Malayalam')
        st.success(malayalam.text)
        selectedLang = malayalam.text
    elif option == 'Marathi':
        st.header('Output Marathi')
        st.info(marathi.text)
        selectedLang = marathi.text
    elif option == 'Urdu':
        st.header('Output Urdu')
        st.success(urdu.text)
        selectedLang = urdu.text


    # 8. Save transcribed text to file

    # Save as TXT file
    yt_txt = open('yt.txt', 'w', encoding="utf-8")
    yt_txt.write(selectedLang)
    yt_txt.close()

    zip_file = ZipFile('transcription.zip', 'w')
    zip_file.write('yt.txt')
    zip_file.close()


# Sidebar
st.sidebar.header('Input parameter')
option = st.sidebar.selectbox(
    'Select language?',
    ('English', 'Hindi', 'Bengali', 'Tamil', 'Telugu', 'Gujrati', 'Malayalam',
    'Marathi', 'Urdu'))
st.write('Language selected:', option)
with st.sidebar.form(key='my_form'):
	URL = st.text_input('Enter URL of YouTube video:')
	submit_button = st.form_submit_button(label='Go')


st.warning('Awaiting URL input in the sidebar.')

# Run custom functions if URL is entered
if submit_button:

    get_yt(URL)
    transcribe_yt()

    with open("transcription.zip", "rb") as zip_download:
        btn = st.download_button(
            label="Download ZIP",
            data=zip_download,
            file_name="transcription.zip",
            mime="application/zip"
        )
