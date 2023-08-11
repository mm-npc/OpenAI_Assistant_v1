import os
import time
import pyaudio
import playsound
from gtts import gTTS
import openai
import speech_recognition as sr
from pydub import AudioSegment
import time

lang = 'en'
api_key = ""
openai.api_key = api_key

while True:
    def get_audio():
        r = sr.Recognizer()
        print("Mic Check...", end=" ")
        with sr.Microphone(device_index=1) as source:
            print("Done")
            print("Ready...")
            myTTS("Ready for input")
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)

                print("You said...:", end=" ")
                print(said)

                if "Maris" in said:
                    print("Detected keyword")
                    # myTTS("Okay, got it. Give me a second, please")
                    myTTS("Just a sec")
                    if "tell me about your name" in said:
                        completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "user", "content": "in 30 words or less, describe maris brood"}
                            ]
                        )
                        text = completion.choices[0].message.content
                        myTTS(text)
                        time.sleep(5)
                        return

                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": said}
                        ]
                    )

                    # completion = openai.ChatCompletion.create(
                    #     model="gpt-3.5-turbo",
                    #     messages=[
                    #         {"role": "user", "content": "say aww, skeet, skeet"}
                    #     ]
                    # )

                    text = completion.choices[0].message.content
                    print(text)
                    speech = gTTS(text=text, lang=lang, slow=False, tld="com")
                    speech.save("msg.mp3")
                    playsound.playsound("msg.mp3")
                    time.sleep(5)

            except Exception:
                print("[Exception] Now exiting...")
                if said == "":
                    myTTS("You're not talking. So, I'm leaving")
                exit()

        # exit()
        return said

    def myTTS(txt):
        if txt == "Ready for input":
            playsound.playsound("ready_for_input.mp3")
        elif txt == "You're not talking. So, I'm leaving":
            playsound.playsound("youre_not_talking_so_im_leaving.mp3")
        else:
            speech = gTTS(text=txt, lang=lang, slow=False, tld="com")
            speech.save("gen_msg.mp3")
            playsound.playsound("gen_msg.mp3")

        # Attempt to speed up the voice:
        # audio = AudioSegment.from_mp3("gen_msg.mp3")
        # audio.speedup(playback_speed=2.0)  # speed up by 2x
        # audio.export("gen_msg_2x.mp3", format="mp3")
        # playsound.playsound("gen_msg_2x.mp3")

    get_audio()
