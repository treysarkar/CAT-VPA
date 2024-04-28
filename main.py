import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from mptpkg import print_say, voice_to_text, alarm
import google.generativeai as genai # to tell us about something, this would also be our last resort, incase nothing works
import wolframalpha #gebn ai only takes over when wolfram fails
import smtplib
import os
import platform

from io import BytesIO
#import requests
import bs4
from pygame import mixer


import webbrowser # so that we can open the web browser and look for for that which is being asked of us
import requests # to seek for the news from news api






def email():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("saugata604@gmail.com", "ihnl ulep ylhn ggmf")
    # message to be sent
    display_message("Tell us the receipient's email address:","left")
    print_say("Tell us the receiver's addresss over the terminal:\n")
    receiver=voice_to_text()
    if "trey" in receiver:
        receiver="treysarkar@gmail.com"
    elif "me" in receiver:
        receiver="saugata604@gmail.com"
    else:
        receiver="saugat604@gmail.com"    
    display_message("Tell us the message:","left")
    print_say("The message to send")
    
    message =voice_to_text()
    display_message("Message body\n\n"+message,"left")
    # sending the mail
    s.sendmail("saugat604@gmail.com", receiver, message)
    # terminating the session
    s.quit()




def fetch_news(api_key, country='us', category=None):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': country,
        'apiKey': api_key
    }
    if category:
        params['category'] = category
    
    response = requests.get(url, params=params)
    data = response.json()
    count=0
    if data['status'] == 'ok':
        articles = data['articles']
        for article in articles:
            if(count%3==0 and count!=0):
                display_message("Continue?","left")
                print_say("Continue:")
                inp=voice_to_text()
                display_message(inp,"right")
                if "no" in inp:
                    break
            if(article['title']!="[removed]"):
                display_message(article['title'],"left")
                print_say(article['title'])
                #display_message(article['title']","left")
                display_message("Description:\n\n"+ article['description'],"left")
                print_say(article["description"])
                #display_message(f"{article['description']}","left")
                display_message("-" * 50,"left")
                count+=1
    else:
        print("Failed to fetch news:", data['message'])
        print_say("Cant find news")


def news_brief():
    # Locate the website for the NPR news brief
    url = 'https://www.npr.org/podcasts/500005/npr-news-now'
    # Convert the source code to a soup string
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # Locate the tag that contains the mp3 files
    casts = soup.findAll('a', {'class': 'audio-module-listen'})
    # Obtain the web link for the mp3 file
    cast = casts[0]['href']
    # Remove the unwanted components in the link
    mp3 = cast.find("?")
    mymp3 = cast[0:mp3]
    # Play the mp3 using the pygame module
    mymp3 = requests.get(mymp3)
    voice = BytesIO()
    voice.write(mymp3.content)
    voice.seek(0)
    mixer.init()
    mixer.music.load(voice)
    mixer.music.play()


def get_voice_input():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        # Capture the audio input
        audio = recognizer.listen(source)

    try:
        # Recognize the audio input
        text = recognizer.recognize_google(audio) #input audio is text
        # Display the recognized text on the screen
        display_message(text, "right")
        text=text.lower()
        
        
        if "browse" in text or "open the browser" in text or "google" in text:
            text=text.replace("browser","")
            text=text.replace("open the browser","")
            text=text.replace("google","")
            # everything you do is going to be googled and googled only
            output="Googling "+text
            display_message(output,"left")
            print_say(output)
            webbrowser.open("https://www.google.com/search?q="+text)
        
        
        
        elif "read news" in text or "tell me the news" in text:
            category=""
            country="in"
            api_key="197280ae85fd425fa0dcea0feda8d744"
            display_message("Would you like to hear some specific news?","left")
            #print_say("Would you like to hear some specific news?")
            print("...")
            inp2=voice_to_text()
            display_message(inp2,"right")
            inp2=inp2.lower()

            print(inp2)
            if "yes" in inp2 or "i would" in inp2:
                display_message("Category please","left")
                print_say("Category Please")
                #print_say("Category please:")
                inp3=voice_to_text()
                print("the category is ",inp3)
                display_message(inp3,"right")
                category=inp3
            fetch_news(api_key,country,category)

        elif "newscast" in text or "news cast" in text:
            news_brief()
            display_message("Just say Stop Playing to exit from this","left")
            # Python listens in the background
            while True:
                
                background = voice_to_text().lower()
                # Stops playing if you say "stop playing"
                if "stop" in background:
                    mixer.music.stop()
                    break
                continue 
        
        elif "alarm for" in text and ("a.m." in text or "p.m." in text):
            alarm(text)

        elif "send" in text and "email" in text:
            email()
        
        
        else:
            # first the query ges for wolfram alpha and in case it fails the generative AI takes over
            
            #WOLFRAM BLOCK STARTS FROM HERE
            try:
                APIkey = "GLEREV-R465LW56KH" 
                wolf = wolframalpha.Client(APIkey)
                # Enter your query 
                inp = text.lower()
                # Send your query to WolframAlpha and get a response
                response = wolf.query(inp)
                # Retrieve the text from the response
                res = next(response.results).text 
                # Print out the response
                display_message(res,"left")
                print_say(res) 
            except:
                try:
                    #GEN AI BLACK STARTS HERE
                    API_KEY="AIzaSyAMyIjpe7ubv90wIC5dnhfLSJxkI5EkjsU"
                    genai.configure(api_key=API_KEY)
                    model=genai.GenerativeModel("gemini-pro")
                    if "paragraph" in text or "poem" in text:
                        prompt=f"{text}"
                    else:
                        prompt=f"{text}, write me a summary about it in paragraph format not more than 100 words make it interesting" #, if we are talking about a movie title please provide the rotten tomatoes and the imdb rating"
                    response=model.generate_content(prompt)
                    display_message(response.text,"left")
                    print_say(response.text)
                except:
                    display_message("OOPSSS!! Im still learning, I can't answer that","left")
                    print_say("OOPSSS!! Im still learning, I can't answer that")

    except sr.UnknownValueError:
        # Handle unrecognized speech
        display_message("Sorry, could not understand audio", "left")
    except sr.RequestError as e:
        # Handle errors with the API request
        display_message("Error: {0}".format(e), "left")

def display_message(message, side):
    # Determine background color based on side
    if side == "left":
        bg_color = "#dcf8c6"  # Light green for received messages
        align = "w"
    else:
        bg_color = "#e5e5ea"  # Light gray for sent messages
        align = "e"
    
    # Create a label for the message
    message_label = tk.Label(chat_frame, text=message, bg=bg_color, wraplength=300, font=("Arial", 12), padx=20, pady=5)
    message_label.grid(sticky=align)
    
    # if side=="left":
    #     print_say(message)
    
    # Update the chat window
    chat_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(2.0)  # Scroll to the bottom
     
# Create the tkinter window
window = tk.Tk()
window.title("CAT CHAT")

# Create a canvas with scrollbar
canvas = tk.Canvas(window)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create a frame to hold the chat messages
chat_frame = ttk.Frame(scrollable_frame)
chat_frame.grid(sticky="nsew")

# Create a button to trigger voice input
button = tk.Button(window, text="Speak", command=get_voice_input, font=("Arial", 14))
button.pack(side="bottom", pady=10)

# Run the tkinter event loop
window.mainloop()
