import streamlit as st
from utils import *
from io import StringIO, BytesIO
from tempfile import NamedTemporaryFile
import os
from openai import OpenAI


openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
chunk_overlap = st.sidebar.number_input("The number of characters that a piece of context may have", value=200)

uploaded_file = None
if openai_key != '' and chunk_overlap is not None:
    uploaded_file = st.file_uploader("Upload your file here...", type=['pdf'])

if uploaded_file is not None:
    if 'documents' not in st.session_state:
        print('loading uploaded_file')
        bytes_data = uploaded_file.read()
        with NamedTemporaryFile(delete=False) as tmp:  
            tmp.write(bytes_data)     
            st.session_state['documents'] = load_pdf_file(tmp.name, chunk_overlap)      
        os.remove(tmp.name)   

    exact_match_key_phrases = st.text_area(label='Exactly matched phrases (seperated by ending line)', height=100)
    exact_match_key_phrases = [x for x in exact_match_key_phrases.split('\n') if x !='']
    instruction = st.text_area(label='Instruction', height=50)
    if st.button('Ask GPT'):
        document_list_result = [document for document in st.session_state['documents'] if any([x in document.page_content for x in exact_match_key_phrases])]
        context = "\n-------\n".join([document.page_content for document in document_list_result])
        prompt = f'You have to do the task describe in the instruction, base on the information in context:\n\ninstruction:\n[start ninstruction]\n{instruction}\n[end ninstruction]\n\n\context:\n[start context]\n{context}\n[end context]\n'
        client = OpenAI(
            api_key=openai_key,
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo-1106",
            temperature=0
        )
        st.text_area(label="Answer", value=chat_completion.choices[0].message.content, height= 300)
        st.write([document.page_content for document in document_list_result])
    

