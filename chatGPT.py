import openai
import sqlite3
import pyttsx3

text_speech = pyttsx3.init()
# Set up the OpenAI API client
openai.api_key = ""
oldPrompt = "x"
switch = 0
initMessage = ""
startMessage = ""
# Set up the model and prompt



while True:
    model_engine = "text-davinci-003"
    prompt = ""

    sqliteConnection = sqlite3.connect(r'C:\Users\Maxwe\DroneProjectv2\Assets\gestures.db')
    cursor = sqliteConnection.cursor()
    for row in cursor.execute('SELECT * FROM chatGPTinput ORDER BY rowid DESC LIMIT 1;'):
        prompt = row


    if oldPrompt != prompt:

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
        text_speech.say(response )
        text_speech.runAndWait()
        oldPrompt = prompt
        cursor.close()







