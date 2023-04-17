import openai
import sqlite3
import gtts
from playsound import playsound

# Set up the OpenAI API client
openai.api_key = "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"

# Set up the model and prompt
model_engine = "text-davinci-003"
prompt = ""


while prompt != "Exit":


    prompt = input("Enter a message: ")

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text.lstrip()
    print(f"\n{response}\n")

    tts = gtts.gTTS(response)
    tts.save("tts.mp3")
    playsound("tts.mp3")


