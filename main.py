from dotenv import load_dotenv, find_dotenv
import requests
import os
import streamlit as st
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

# print(torch.cuda.is_available())

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.getenv("token")
headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}

def img2text(path):

    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()

    output = query(path)[0]['generated_text']

    print(output)
    return output



def generate_story(scene):
    template = f'''
                You are a poet;
                You can generate a poem from a simple narrative, understand the theme, and use proper rhyming words.
                The poem should not be longer than 16 lines.

                Scenario: {scene}

                Write a poem based on the provided scenario.
                '''

    print(template)

    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    story = query({
        "inputs": template,
    })

    story = str(story[0]['generated_text'])
    story = story[152:]

    print(story)
    return story

def gen_audio(message):

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler_tts_mini_v0.1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1")

    prompt = message
    description = "A female speaker with a slightly low-pitched, quite expressive voice delivers her words at a normal  pace in a poetic manner with proper pauses while speaking inside a confined space with very clear audio."

    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    sf.write("audio.wav", audio_arr, model.config.sampling_rate)


def main():
    st.set_page_config(page_title="img 2 poem", page_icon="🤖")
    st.header("Trun image into poem")
    uploaded_file = st.file_uploader("choose an image.....", type=["png","jpg","jpeg","svg"])

    if uploaded_file is not None:
        print(uploaded_file)
        bytes_data = uploaded_file.getvalue()
        print(bytes_data)
        with open(uploaded_file.name, "wb") as file:
            file.write(bytes_data)

        st.image(uploaded_file, caption="Uploaded Image")

        scenario = img2text(uploaded_file.name)
        story = generate_story(scenario)
        gen_audio(story)

        with st.expander("Scenario"):
            st.write(scenario)
        with st.expander("Poem"):
            st.write(story)

        st.audio("audio.wav")

if __name__ == "__main__":
    # main()
    scene = img2text("couples.jpg")
    story = generate_story(scene)
    gen_audio(story)

















