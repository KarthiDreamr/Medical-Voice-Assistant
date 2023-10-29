import json
from difflib import get_close_matches
import speech_recognition as sr
import googletrans
import gtts
import playsound
import os


def speak(trans_text, lang):
    converted_audio = gtts.gTTS(trans_text,lang=lang)
    converted_audio.save("hello.mp3")
    playsound.playsound("hello.mp3")
    if os.path.exists('hello.mp3'):
        os.remove('hello.mp3')
     
def listen(lang):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language = lang)
        print(f"You: {command}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return "None"

    return command

def translate(text,dest_lang):
    translator = googletrans.Translator()
    translation = translator.translate(text,dest=dest_lang)
    return translation.text

def load_knowledge_base(file_path):
    with open(file_path,'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path,data):
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)
        
def find_best_match(user_question,questions):
    matches = get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question,knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        

def chat_bot():
    lang = 'ml'
    wel_msg = translate("Hello! Voice assistant at your service! Is the current language acceptable? Or would you prefer to change it to one of the following language? Hindi,malayalam,english,tamil",lang)
    knowledge_base = load_knowledge_base('knowledge_base.json')
    speak(wel_msg,lang)
    while True:
        user_input = listen(lang)
        user_input = translate(user_input,'en')
        
        if "tamil" in user_input.lower():
            lang = 'ta'
            break
        elif "english" in user_input.lower():
            lang = 'en'
            break
        elif "malayalam" in user_input.lower():
            lang = 'ml'
            break
        elif "hindi" in user_input.lower():
            lang = 'hi'
            break
        else:
            repeat_msg = "Sorry. Can you please repeat?"
            speak(translate(repeat_msg,lang),lang)
    
    issue = "Can you please tell the issue you face?"
    speak(translate(issue,lang),lang)
    
    while True:
        user_input = listen(lang)
        user_input = translate(user_input,'en')
        
         
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        
        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            speak(translate(answer,lang),lang)
            print(f"Bot: {answer}")
            if 'doctor' in answer.lower():
                break
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer = input('Type the answer or "skip" to skip: ')
             
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print('Bot: Thank you! I learned a new response!')
                
                
            
if __name__ == '__main__':
    chat_bot()
