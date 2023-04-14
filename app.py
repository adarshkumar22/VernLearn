import streamlit as st
from pytube import YouTube
import os
import requests
from zipfile import ZipFile
from googletrans import Translator
from dotenv import load_dotenv
from summa import summarizer

translator = Translator()

load_dotenv()
# api_key = os.getenv("API_KEY")
api_key = "bf5c2c11c6734283bbe513d01a0e8cee"

st.markdown('# 📝 **VernLearn**')
bar = st.progress(0)

ratio = st.slider(
    "Summarization fraction", min_value=0.0, max_value=1.0, value=0.2, step=0.01
)

# 5 minute https://www.youtube.com/watch?v=c2Sn-pP3uxo
# 20 secon https://www.youtube.com/watch?v=0VLxWIHRD4E

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

    summarized_list = summarizer.summarize(
        englishText, ratio=ratio, language="english", split=True, scores=True
    )

    summarized_text = ""
    for i in summarized_list:
        summarized_text = summarized_text + i[0] + " "
    
    if(option == 'English'):
        english = translator.translate(englishText, dest='en')
        senglish = translator.translate(summarized_text, dest='en')
    elif(option == 'Hindi'):
        hindi = translator.translate(englishText, dest='hi')
        shindi = translator.translate(summarized_text, dest='hi')
    elif(option == 'Bengali'):
        bengali = translator.translate(englishText, dest='bn')
        sbengali = translator.translate(summarized_text, dest='bn')
    elif(option == 'Tamil'):
        tamil = translator.translate(englishText, dest='ta')
        stamil = translator.translate(summarized_text, dest='ta')
    elif(option == 'Telugu'):
        telugu = translator.translate(englishText, dest='te')
        stelugu = translator.translate(summarized_text, dest='te')
    elif(option == 'Gujrati'):
        gujrati = translator.translate(englishText, dest='gu')
        sgujrati = translator.translate(summarized_text, dest='gu')
    elif(option == 'Malayalam'):
        malayalam = translator.translate(englishText, dest='ml')
        smalayalam = translator.translate(summarized_text, dest='ml')
    elif(option == 'Marathi'):
        marathi = translator.translate(englishText, dest='mr')
        smarathi = translator.translate(summarized_text, dest='mr')
    elif(option == 'Urdu'):
        urdu = translator.translate(englishText, dest='ur')
        surdu = translator.translate(summarized_text, dest='ur')
    
    selectedLang = ""

    if option == 'English':
        st.header('Output English')
        st.success(english.text)
        st.header('Summary')
        st.info(senglish.text)
        selectedLang = english.text
    elif option == 'Hindi':
        st.header('Output Hindi')
        st.info(hindi.text)
        st.header('Summary')
        st.success(shindi.text)
        selectedLang = hindi.text
    elif option == 'Bengali':
        st.header('Output Bengali')
        st.success(bengali.text)
        st.header('Summary')
        st.info(sbengali.text)
        selectedLang = bengali.text
    elif option == 'Tamil':
        st.header('Output Tamil')
        st.info(tamil.text)
        st.header('Summary')
        st.success(stamil.text)
        selectedLang = tamil.text
    elif option == 'Telugu':
        st.header('Output Telugu')
        st.success(telugu.text)
        st.header('Summary')
        st.info(stelugu.text)
        selectedLang = telugu.text
    elif option == 'Gujrati':
        st.header('Output Gujrati')
        st.info(gujrati.text)
        st.header('Summary')
        st.success(sgujrati.text)
        selectedLang = gujrati.text
    elif option == 'Malayalam':
        st.header('Output Malayalam')
        st.success(malayalam.text)
        st.header('Summary')
        st.info(smalayalam.text)
        selectedLang = malayalam.text
    elif option == 'Marathi':
        st.header('Output Marathi')
        st.info(marathi.text)
        st.header('Summary')
        st.success(smarathi.text)
        selectedLang = marathi.text
    elif option == 'Urdu':
        st.header('Output Urdu')
        st.success(urdu.text)
        st.header('Summary')
        st.info(surdu.text)
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
    'Select output language?',
    ('English', 'Hindi', 'Bengali', 'Tamil', 'Telugu', 'Gujrati', 'Malayalam',
    'Marathi', 'Urdu'))
st.write('Language selected:', option)

with st.sidebar.form(key='my_form'):
	URL = st.text_input('Enter URL of YouTube video:')
	submit_button = st.form_submit_button(label='Go')

st.sidebar.header('Made By-')
st.sidebar.write('Shubham Sharma')
st.sidebar.write('Nikhil Kumar')
st.sidebar.write('Adarsh Kumar')


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