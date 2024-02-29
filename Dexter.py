
import speech_recognition as recognize
import os
import requests
import json
import winspeech
import time
import datetime
import random
import threading

#Key logger imports
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Controller
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

#image recognition imports
from ultralytics import YOLO
import cv2

#image generator imports
from PIL import ImageTk, Image

#music Player imports
import moviepy.editor as mp
from googleapiclient.discovery import build
from pytube import YouTube
import pygame

#Scrapper imports
from bs4 import BeautifulSoup
import pickle

#GUI imports
import tkinter
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import Tk, Canvas, Text, Button, PhotoImage, simpledialog,messagebox

# Assistant feature imports
import webbrowser as wb
import AppOpener


#global variables
chat = ""
mouse=Controller()
actions=[] #Variable to store user performed clicks

#image generator
image1_data, image2_data = "", ""
image_label_1,image_label_2="",""

#muisc player
video_name=[]
exit_mixer=False
music_status=""

speak_flag=0
gpt_in_use=0

# defining the dictionary which has website url
websites = {
    "google": "www.google.com",
    "youtube": "www.youtube.com",
    "amazon": "www.amazon.in",
    "flipkart": "www.flipkart.com",
    "wikipedia": "www.wikipedia.org",
    "instagram": "www.instagram.com",
    "facebook": "www.facebook.com",
    "whatsapp": "web.whatsapp.com",
    "snapchat": "web.snapchat.com",
    "telegram": "telegram.org",
    "bard": "bard.google.com",
    "chat gpt": "chat.openai.com",
    "microsoft": "www.microsoft.com",
    "linkedin": "www.linkedin.com",
    "netflix": "www.netflix.com",
    "amazon prime videos": "www.primevideo.com",
    "twitter": "twitter.com",
    "hotstar": "www.hotstar.com",
    "github": "github.com",
    "google meet": "meet.google.com",
    "discord": "discord.com",
    "stack overflow": "stackoverflow.com",
    "meesho": "www.meesho.com",
    "myntra": "www.myntra.com",
    "gst": "https://services.gst.gov.in/services/login"
}

#setting Path for source files
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH2 = OUTPUT_PATH / Path(r"assets\frame2")


def relative_to_assets2(path: str) -> Path:
    return ASSETS_PATH2 / Path(path)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1312x602") #window width and height
window.configure(bg="#000099")


canvas = Canvas(
    window,
    bg="#000099",
    height=602,
    width=1312,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

# code for scrollable chats
scroll = Canvas(
    window,
    bg="#000099",
    height=450,
    width=350,
    highlightthickness=0,
    relief="ridge"
)
scroll.place(x=900, y=10)

scrollbar = tk.Scrollbar(window, orient='vertical', command=scroll.yview)
scrollbar.pack(side="right", fill="y")
scroll.configure(yscrollcommand=scrollbar.set)

height=50
content_frame = tk.Frame(scroll,height=height,width=350,bg="#000099")
scroll.create_window((4,4), window=content_frame,  anchor="nw")

#AI Image
canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    555.0,
    247.0,
    image=image_image_1
)

#Listening text
canvas.create_text(
    479.0,
    396.0,
    anchor="nw",
    text=f"Listening....",
    fill="#CDCACA",
    font=("Inter Bold", 22 * -1),
    tags='status'
)

def set_status(current):
    canvas.after(0,lambda: canvas.itemconfig('status', text=current))
    print("Status setted as",current)

#code to display options
def show_options():
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=248,
        width=249,
        borderwidth=2,
        highlightthickness=2,
        relief="ridge"
    )
    canvas.place(x=10, y=20)

    option_button_1 = Button(
        text='Saved chats',
        borderwidth=2,
        highlightthickness=2,
        command=lambda: open_File('Saved-Chats'),
        relief="flat"
    )
    option_button_1.place(
        x=25.0,
        y=201.0,
        width=219.0,
        height=34.0
    )

    option_button_2 = Button(
        text='play recorded actions',
        borderwidth=2,
        highlightthickness=2,
        command=playback,
        relief="flat"
    )
    option_button_2.place(
        x=25.0,
        y=145.0,
        width=219.0,
        height=34.0
    )

    option_button_3 = Button(
        text='Analyzed Data',
        borderwidth=2,
        highlightthickness=2,
        command=lambda: open_File('website-analysis'),
        relief="flat"
    )
    option_button_3.place(
        x=25.0,
        y=89.0,
        width=219.0,
        height=34.0
    )

    option_button_4 = Button(
        text='Close',
        borderwidth=2,
        highlightthickness=2,
        command=lambda:close_options(canvas,option_button_1,option_button_2,option_button_3,option_button_4),
        relief="flat"
    )
    option_button_4.place(
        x=25.0,
        y=34.0,
        width=219.0,
        height=34.0
    )

def close_options(canvas,button1,button2,button3,button4):
    canvas.destroy()
    button1.destroy()
    button2.destroy()
    button3.destroy()
    button4.destroy()

def browse_folder():
    folder_path = filedialog.askdirectory()  # Opens a folder selection dialog
    return folder_path

def choose_playback_file(location):
   file = filedialog.askopenfile(initialdir=f'{location}/',mode='rb')
   if file:
      content = pickle.load(file)
      file.close()
      return content

def choose_file(location):
   file = filedialog.askopenfile(initialdir=f'{location}/',mode='r')
   if file:
       os.startfile(file.name)
       file.close()

def open_File(location):
    threading.Thread(target=choose_file,args=(location,)).start()

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command = lambda: show_options(),
    relief="flat"
)
button_1.place(
    x=34.0,
    y=42.0,
    width=86.0,
    height=64.0
)


#Code for input field
canvas.create_rectangle(
    30.0,
    490.0,
    1270.0,
    550.0,
    fill="#B1B1B1",
    outline="")

entry_image_2 = PhotoImage(file=relative_to_assets2("entry_1.png"))
entry_bg_2 = canvas.create_image(
    595.5,
    520.5,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=2
)
entry_2.place(
    x=38.0,
    y=500.0,
    width=1115.0,
    height=40.0
)

# code to display User Input
Qx=20.0
Ay=10.0
previousy=24.0
def generate_label(text,bgcolor,textcolor,x):
    global previousy, height

    label = tkinter.Label(content_frame, text=" ",wraplength=300, width=45, bg=f'{bgcolor}', fg=f'{textcolor}', anchor="e", relief='groove',borderwidth=2)
    label.pack()
    label.place(x=x, y=previousy)
    label.config(text=f"{text}")

    newy=label.winfo_reqheight()
    previousy=previousy + 10.0+newy

    height += 10.0 + newy

    content_frame.update_idletasks()
    content_frame.configure(height=height)
    scroll.config(scrollregion=scroll.bbox("all"))


def user_label():
    threading.Thread(target=user_text).start()

def user_text():
    speech = entry_2.get("1.0", "end-1c")
    entry_2.delete("1.0", tk.END)

    generate_label(speech.strip(), '#fccb06', 'Black', Qx)
    compare(speech)

button = tkinter.Button(window,text="Submit", command=user_label)
button.pack()
button.place(x=1215, y=505)

def start_listening():
    global stop_flag
    stop_flag = threading.Event()
    main_thread = threading.Thread(target=main)
    main_thread.daemon = True  # Allow the thread to exit when the main program exits
    main_thread.start()

button_image_2 = PhotoImage(file=relative_to_assets2("button_1.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=start_listening,
    relief="flat"
)
button_2.place(
    x=1171.0,
    y=500.0,
    width=32.0,
    height=32.0
)

window.resizable(False, False)


#Key Logger
def on_key_press(key):
    try:
        actions.append(('keyboard', 'press', key.char.lower()))
        print(actions)
    except AttributeError:
        actions.append(('keyboard', 'press', key))

def on_key_release(key):
    try:
        actions.append(('keyboard', 'release', key.char))
    except AttributeError:
        # This exception may occur for special keys like Shift or Alt
        actions.append(('keyboard', 'release', key))

def on_mouse_click(x, y, button, pressed):
    if pressed:
        x,y=mouse.position
        print(actions)
        actions.append(('mouse', 'click', (x,y, button)))


def playback():
    global playback_button,actions
    # Playback
    speak("Please select the recording you want me to play")
    logs = choose_playback_file('Saved-logs')
    if logs==None:
        messagebox.showinfo("gpt-5", "No files selected")
    else:
        print(logs)
        speak("starting the playback after five seconds")
        time.sleep(5)
        mouse_controller = MouseController()
        keyboard_controller = KeyboardController()

        for action_type, action, details in logs:
            if action_type == 'keyboard':
                if action == 'press':
                    keyboard_controller.press(details)
                elif action == 'release':
                    keyboard_controller.release(details)
            elif action_type == 'mouse':
                if action == 'click':
                    x, y, button = details
                    mouse_controller.position = (x, y)
                    time.sleep(2)
                    mouse_controller.click(button)
                    time.sleep(1)

        try:
            keyboard_listener.stop()
            mouse_listener.stop()
        except:
            pass

        messagebox.showinfo("gpt-5", "Playback Ended!")


# playback_button = tk.Button(window, text="start playback", command=playback)
keyboard_listener = KeyboardListener(on_press=on_key_press,on_release=on_key_release)
mouse_listener = MouseListener(on_click=on_mouse_click)
stop_button=None
recording_window=None

def start():
    global stop_button,recording_window
    keyboard_listener.start()
    mouse_listener.start()

    recording_window = Tk()

    recording_window.geometry("1312x602")  # window width and height
    recording_window.configure(bg="#0C257E")

    #specifying position for tkinter window to open up
    recording_window.geometry("100x70+10+10")
    #tkinter window will be on top even if other window is clicked
    recording_window.attributes("-topmost", True)

    # Pack the button widget onto the window
    stop_button = tk.Button(recording_window, text="Stop Recording", command=stop_listener)
    stop_button.pack()
    # playback_button.place(x=5,y=30)
    if not window.winfo_exists():
        stop_listener()

    print("Recording actions...")

    recording_window.mainloop()
    keyboard_listener.join()
    mouse_listener.join()

def stop_listener():
    global actions
    keyboard_listener.stop()
    mouse_listener.stop()
    time.sleep(1)
    actions.pop(-1)
    speak( "Give the name with which you would like to save the logs")

    file_path = filedialog.asksaveasfilename(title="Save Chat",initialdir="Saved-logs",confirmoverwrite=True,defaultextension='.pkl')
    log_file=os.path.basename(file_path)

    time.sleep(5)
    with open(f"Saved-logs/{log_file}", "wb") as f:
        pickle.dump(actions, f)

    stop_button.destroy()
    recording_window.destroy()
    speak(f"recording save as {log_file}")


#image Recognition
def generate_description():
    input_value = messagebox.askyesno("Records", "Do you want to give image from camera?")

    if input_value:

        speak("Starting your camera please wait")
        threading.Thread(target=object_from_video).start()

    else:
        threading.Thread(target=object_from_image).start()

def object_from_image():
    objects = []
    speak("please select the folder where you have you images you want to detect")
    path = browse_folder()
    if path:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
        image_files = []

        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                _, extension = os.path.splitext(filename)
                if extension.lower() in image_extensions:
                    image_files.append(os.path.join(path, filename))
        print(image_files)

        model = YOLO('yolov8n.pt')
        for image in image_files:
            results=model(f'{image}', show=False)
            names = model.names
            for r in results:
                for c in r.boxes.cls:
                    if names[int(c)] not in objects:
                        objects.append(names[int(c)])

        cv2.waitKey(0)
        print(objects)
        print('objects detected')
        speak("generating your description...!")

        respond(f"generate some description for all the objects in this list: {objects}",path)
    else:
        messagebox.showinfo("gpt-5", "No folder selected!")

def object_from_video():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    model = YOLO('yolov8n.pt')
    speak("show all the objects one by one. Press Q to stop the object detection")

    detected_objects = []
    while cap.isOpened():
        success, img = cap.read()
        results = model(img, show=True, stream=True)
        names = model.names

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # With opencv
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                for c in box.cls:
                    if (names[int(c)] not in detected_objects):
                        detected_objects.append(names[int(c)])
        print(detected_objects)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print('objects detected')
    speak("objeccts Detected! Please choose a folder where you want your description to be saved")
    path = browse_folder()
    speak("Generating description for you...!")
    respond(f"generate some description for all the objects in this list: {detected_objects}", path)


#image generator Code
def ProcessImage1(response):
    global image1_data
    print("processing image 1")

    image_url1 = json.loads(response.content.decode())['data'][0]['url']

    with open("image1.jpg", "wb") as file:
        image1_data = requests.get(image_url1)
        file.write(image1_data.content)

    print("image1 loaded")

def ProcessImage2(response):
    global image2_data
    print("Processing Image 2")
    image_url2 = json.loads(response.content.decode())['data'][1]['url']

    with open("image2.jpg", "wb") as file:
        image2_data = requests.get(image_url2)
        file.write(image2_data.content)
    print("image2 loaded")

def download_image1(image_prompt):
    filename = f"Generated Images/{image_prompt}.jpg"

    # Check if the file already exists
    if os.path.exists(filename):
        # Choose an alternative filename or skip the download
        # Example: Append a number to the filename
        base, extension = os.path.splitext(filename)
        index = 1
        while os.path.exists(f"{base}_{index}{extension}"):
            index += 1
        filename = f"{base}_{index}{extension}"

    with open(filename, "wb") as file:
        file.write(image1_data.content)


def download_image2(image_prompt):
    filename = f"Generated Images/{image_prompt}.jpg"

    # Check if the file already exists
    if os.path.exists(filename):
        # Choose an alternative filename or skip the download
        # Example: Append a number to the filename
        base, extension = os.path.splitext(filename)
        index = 1
        while os.path.exists(f"{base}_{index}{extension}"):
            index += 1
        filename = f"{base}_{index}{extension}"

    with open(filename, "wb") as file:
        file.write(image2_data.content)

def update_labels():
    global image_label_1,image_label_2

    image_width = 400
    image_height = 400
    try:
        image1 = Image.open("image1.jpg")
        image1 = image1.resize((image_width, image_height), Image.NEAREST)
        image1 = ImageTk.PhotoImage(image1)
        image_label_1.config(image=image1)
        image_label_1.image = image1

        image2 = Image.open("image2.jpg")
        image2 = image2.resize((image_width, image_height), Image.NEAREST)
        image2 = ImageTk.PhotoImage(image2)
        image_label_2.config(image=image2)
        image_label_2.image = image2

    except Exception as e:
        print(f"Error updating labels: {e}")


def generate_image(image_prompt):

    image_generator_URL = 'https://api.openai.com/v1/images/generations'

    payload={
        "prompt": image_prompt,
        "n": 2,
        "size": "1024x1024"
        }
    headers={
        "Content-Type":"application/json",
        "Authorization": f"Bearer YOUR_OPENAI_API_KEY"
        }

    print('generating your content... \nThis may take a while')
    set_status("Hold i am cooking up your image")
    response = requests.post(image_generator_URL,headers=headers,json=payload, stream=False)
    print(response)
    print(json.loads(response.content.decode()))


    try:
        image1=threading.Thread(target=ProcessImage1,args=(response,), daemon=True)
        image2=threading.Thread(target=ProcessImage2,args=(response,), daemon=True)

        image1.start()
        image2.start()
        image1.join()
        image2.join()
        if image1_data is not None and image2_data is not None:
            update_labels()

    except Exception as e:
        print(f"Error downloading image: {e}")


def create_image(image_prompt):
    global image_label_1,image_label_2
    if not os.path.exists("Generated Images"):
        os.mkdir("Generated Images")


    # Create the main window
    image_window = tk.Toplevel()
    image_window.title("Image and Button Example")
    image_window.geometry("1000x500")
    image_window.configure(bg="#000199")

    image_label_1 = tkinter.Label(image_window)
    image_label_1.place(x=80, y=10)

    image_label_2 = tkinter.Label(image_window)
    image_label_2.place(x=540, y=10)

    image_label_1 = tkinter.Label(image_window,text="Rendering your image please wait")
    image_label_1.place(x=90, y=10)

    image_label_2 = tkinter.Label(image_window,text="Rendering your image please wait")
    image_label_2.place(x=550, y=10)


    # Create the buttons
    save_button_1 = Button(image_window, text="Save Image", command=lambda: download_image1(image_prompt))
    save_button_1.place(x=250, y=430)

    refresh_button = Button(image_window, text="Recreate", command=lambda: threading.Thread(target=generate_image,args=(image_prompt,),daemon=True).start())
    refresh_button.place(x=490, y=450)

    save_button_2 = Button(image_window, text="Save Image", command=lambda: download_image2(image_prompt))
    save_button_2.place(x=700, y=430)

    #generate image
    threading.Thread(target=generate_image,args=(image_prompt,),daemon=True).start()

#music Player Code
def set_music_status(text):
    music_status.config(text=text)

# Search for music videos by song title
def play_song(music_name):
    global video_name

    pygame.mixer.init()

    api_key = "YOUR_YOUTUBE_API_KEY"
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=music_name,
        type="video",
        part="snippet",
        videoCategoryId=10,  # Music category ID
        maxResults=10
    )
    response = request.execute()
    set_music_status("Song Found!")
    print("Response generated")

    # Extract video IDs from search results
    video_ids = response["items"][0]['id']['videoId']
    video_name = response["items"][0]["snippet"]["title"]

    video_name=video_name.split("|")

    # Get the video URL from the user
    video_url = f"https://www.youtube.com/watch?v={video_ids}"

    # Create a Pytube object
    yt = YouTube(video_url)
    set_music_status(f"Loading {video_name[0]}")
    print(yt)
    video_stream = yt.streams.filter().first()

    print(video_stream)

    video_filename = "audio_stream.mp4"

    print(video_filename)
    # Construct the download path
    download_path = f"C:/Users/kdomg/PycharmProjects/gpt-5/{video_filename}"

    # Download the video stream
    video_stream.download(filename=video_filename)
    print("downloading...")

    # Load the downloaded video file
    video = mp.VideoFileClip(download_path)

    # Extract the audio from the video file
    audio = video.audio
    print(audio)

    try:
        # Write the audio to a separate file (optional)
        audio.write_audiofile("audio.mp3")

        # Load the audio file
        pygame.mixer.music.load("audio.mp3")

        # Play the audio file
        pygame.mixer.music.play()
        set_music_status(f"Playing:{video_name[0]}")

        # Wait for the audio to finish playing or if paused/stopped
        while (pygame.mixer.music.get_busy() or not exit_mixer):
            pygame.time.Clock().tick(10)

        # Stop pygame mixer
        pygame.mixer.quit()

        # Print a success message
        print("Audio extracted successfully!")
    except:
        messagebox.showinfo("gpt-5", "Make sure No other music is playing currently!")


# Function to pause the music
def pause_music(action):
    global exit_mixer

    if action=="pause":
        try:
            pygame.mixer.music.pause()
            set_music_status(f"Paused: {video_name[0]}")
        except Exception as e:
            print(e)

    if action=="play":
        try:
            pygame.mixer.music.unpause()
            set_music_status(f"Playing: {video_name[0]}")
        except Exception as e:
            print(e)

# Function to stop the music
def stop_music():
    global exit_mixer
    try:
        pygame.mixer.music.stop()
        exit_mixer=True
    except Exception as e:
        print(e)

def start_music(song_name):
    global music_status
    # Create the main window
    music_window = tk.Toplevel()
    music_window.title("Music Player")
    music_window.geometry("500x150")

    # Create a frame to organize widgets
    frame = tkinter.Frame(music_window)
    frame.pack(padx=10, pady=10)

    # Create and pack labels and entry in the frame
    entry_label = tkinter.Label(frame, text="Enter Song Name:")
    entry_label.grid(row=0, column=0, padx=5, pady=5)

    entry = tkinter.Entry(frame, width=30)
    entry.grid(row=0, column=1, padx=5, pady=5)

    music_status = tkinter.Label(frame, text="Ideal")
    music_status.grid(row=3, column=0, columnspan=4, pady=5)

    if song_name!="":
        threading.Thread(target=play_song, args=(song_name,), daemon=True).start()
        song_name=""

    # Create and pack the play button
    button_play = Button(frame, text="Play",
                         command=lambda: threading.Thread(target=play_song, args=(entry.get(),), daemon=True).start(),
                         bg="green", fg="white", font=("Helvetica", 12))
    button_play.grid(row=0, column=3, padx=5, pady=10)

    # Create and pack the pause button
    button_pause = Button(frame, text="Pause", command=lambda: pause_music("pause"), bg="yellow", fg="black",
                          font=("Helvetica", 12))
    button_pause.grid(row=2, column=0, padx=5, pady=10)

    # Create and pack the stop button
    button_stop = Button(frame, text="Stop", command=stop_music, bg="red", fg="white", font=("Helvetica", 12))
    button_stop.grid(row=2, column=1, padx=5, pady=10)

    # Create and pack the resume button
    button_resume = Button(frame, text="Resume", command=lambda: pause_music("play"), bg="blue", fg="white",
                           font=("Helvetica", 12))
    button_resume.grid(row=2, column=3, padx=5, pady=10)



def scrapper(url,path):

    r = requests.get(url)
    path=path+r'\data.txt'
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find all text elements in the parsed HTML
    text_elements = soup.find_all(string=True)

    # Combine and clean the text from these elements
    full_text = "\n".join(text_elements).strip()
    print(full_text)

    response,do,ai=gpt(f'analyze this website data:"{full_text}" \n\nreturn me full analysis when you are done analyzing','analyze')
    response = json.loads(response.content.decode())['choices'][0]['message']['content']

    speak("Enter your file name")

    file_path = filedialog.asksaveasfilename(title="analyzed data",initialdir="website-analysis",confirmoverwrite=True,defaultextension=".txt")
    file_name=os.path.basename(file_path)

    with open(f"website-analysis/{file_name}", "w") as f:
        f.write(response)
        f.close()
    speak(f'Analysis saved as {file_name}')

    print(f"Website has been analyzed and analysis is saved at Path: {file_path}")
    messagebox.showinfo("gpt-5", f"Website analyzed sucessfully")

    with open(path,"w", encoding='utf-8') as f:
        f.write(full_text)
        f.close()


#GPT Interaction
def command():
    r = recognize.Recognizer()
    with recognize.Microphone() as source:

        if speak_flag == 0 and gpt_in_use == 0: #do not update the status if gpt is generating content or speaking
            set_status("Listening...")
        print("Listening...")
        # r.pause_threshold = 2
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise before listening
        try:
            audio = r.listen(source)  # Add timeout to limit listening time

            if speak_flag == 0 and gpt_in_use == 0: #do not update the status if gpt is generating content or speaking
                set_status('Recognising...')

            query = r.recognize_google(audio, language="en-in")
            if speak_flag == 0 and gpt_in_use == 0:  #do not update the status if gpt is generating content or speaking
                set_status("Recognized!")

            generate_label(query,'red','white',Qx)
            return query

        except recognize.WaitTimeoutError:
            if speak_flag == 0 and gpt_in_use == 0:  #do not update the status if gpt is generating content or speaking
                set_status("No speech detected.")

        except recognize.UnknownValueError:
            if speak_flag == 0 and gpt_in_use == 0:  #do not update the status if gpt is generating content or speaking
                set_status("Sorry, I couldn't understand what you said.")
            time.sleep(1)

        except recognize.RequestError as e:
            print(e)
            messagebox.showinfo("Error","Please connect to internet")
            time.sleep(1)


def getinfo():
    f = open("User-data/info.txt", 'w')
    speak("please name me")
    ai_name= simpledialog.askstring("Input", "Name Your AI: ")
    if not(ai_name):
        ai_name="GPT-5"
    speak("What should i call you?")
    name = simpledialog.askstring("Input", "Enter your Name: ")
    if not(name):
        name="User"
    f.write(f"Name: {name}\nAiName: {ai_name}")
    f.close()


def wish():
    f = open("User-data/info.txt", 'r')
    name = f.readline()
    hour = int(datetime.datetime.now().hour)
    print(hour)
    if (hour > 0) and (hour <= 12):
        speak(f"Good morning {name[5:]}")
        print(name[5:])
    elif (hour >= 12) and (hour <= 18):
        speak(f"Good afternoon {name[5:]}")
    else:
        speak(f"Good evening {name[5:]}")


def save_chat(conversation):
    global chat_file

    print(conversation)
    speak("Input the name with which you would like to save the file")

    if not os.path.exists("Saved-Chats"):
        os.mkdir("Saved-Chats")

    file_path = filedialog.asksaveasfilename(title="Save Chat",initialdir="Saved-Chats",confirmoverwrite=True,defaultextension=".txt")
    file_name=os.path.basename(file_path)

    with open(f"Saved-Chats/{file_name}", "w") as f:
        f.write(conversation)
        f.close()
    speak(f'chats saved with name {file_name}')

def gpt(Query,do=None):
    # Using API Endpoint
    global gpt_in_use
    try:
        gpt_in_use=1
        f = open("User-data/info.txt", 'r')
        name = f.readline()[5:]
        ai_name = f.readline()[7:]
        global chat
        chat += f"{name}: {Query}\n{ai_name}:"
        Query = chat


        URL = 'https://api.openai.com/v1/chat/completions'

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{'role': 'system', 'content': Query}],
            "temperature": 1.0,
            "top_p": 1.0,
            "n": 1,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer YOUR_OPENAI_API_KEY"
        }

        if do=='analyze':
            set_status("Hang on! analysing the website Content")
            response = requests.post(URL, headers=headers, json=payload, stream=False)
            gpt_in_use=0

            return response, do, ai_name

        elif "generate some description" in Query:
            set_status('generating Description... \nThis may take a while')

        else:
            set_status('Thinking...')
        response = requests.post(URL, headers=headers, json=payload, stream=False)

        return response,do,ai_name
    except requests.exceptions.ConnectionError:
        messagebox.showinfo("Error","Please connect to the Internet")
        gpt_in_use = 0

    except Exception as e:
        print(e)
        gpt_in_use = 0
def respond(Query,objects=None):
    global wait_time,chat,gpt_in_use

    try:
        #get response from gpt
        response,do,ai_name=gpt(Query)
        # print(response)
        # response=json.loads(response.content.decode())

        response = json.loads(response.content.decode())['choices'][0]['message']['content']

        if "generate some description" in Query:
            print(objects)
            with open(f'{objects}/description.txt','w') as f:
                pass
            f=open(f'{objects}/description.txt','a')
            f.write(f'{response}\n')
            f.close()
            messagebox.showinfo("gpt-5", f"Description saved at {objects}")
            speak("Description saved!")
            gpt_in_use = 0

        else:
            chat += f'{response}\n'
            # print(f"{ai_name} says:\n{response}")
            print(chat)
            generate_label(response,'green','black',Ay)

            speak(response)
            gpt_in_use = 0

            return 'xyz',response
    except:
        speak("server is busy please try after 20 minutes")
        set_status("server is busy please try after 20 minutes")
        gpt_in_use=0

def update_ring(ring,stop_event):
    radius=130
    circle = canvas.create_oval(555-radius, 249-radius, 555+radius, 249+radius-5, outline="#000000", width=2)

    while not stop_event.is_set():
        width = random.randint(1, 25)
        radius=130+(width/2)

        ring.itemconfig(circle, width=width, outline="#4D4AC7")
        ring.coords(circle, 555- radius, 249 - radius, 555 + radius, 244 + radius)
        ring.update()
        time.sleep(0.1)  # Adjust the sleep time as needed
    canvas.delete(circle)

def speak(text):
    global speak_flag
    speak_flag=1
    threading.Thread(target=say,args=(text,)).start()

def say(text):
    global speak_flag
    #Threading to add Speaking effect
    stop_event = threading.Event()
    threading.Thread(target=update_ring,args=(canvas,stop_event)).start()

    set_status('Speaking....')
    winspeech.say(text)
    op_length = len(text)
    if op_length <= 50:
        wait_time = op_length / 9.5
        start_time = time.time()  # Get the start time

        while time.time() - start_time < wait_time:
            if speak_flag==0:
                break
    else:
        wait_time = op_length / 17
        start_time = time.time()  # Get the start time

        while time.time() - start_time < wait_time:
            if speak_flag == 0:
                break
    stop_event.set()  # Set the flag to stop the thread
    speak_flag=0
    set_status("IDEAL")

def wait_when_speaking(op_length):
    global speak_flag
    print(op_length)
    if op_length <= 50:
        wait_time = op_length / 9.5
        time.sleep(wait_time)

    else:
        wait_time = op_length / 17
        time.sleep(wait_time)
    start_time = time.time()  # Get the start time

    while time.time() - start_time < wait_time:
        if not stop_flag.is_set():
            speech = command()
            if speech:
                if "stop".lower() in speech.lower():
                    try:
                        winspeech.stop_talking()
                        speak_flag = 0
                        break
                    except:
                        pass

class Assistant(threading.Thread):
    def __init__(self,speech):
        self.speech=speech
        self.app_name=""
        threading.Thread.__init__(self)

    def open_app(self,application_name):
        AppOpener.open(application_name, match_closest=True)
        print(AppOpener.open('ls'))

    def open_website(self,site_name):
        if site_name in websites:
            wb.open(websites[site_name], new=1)
        else:
            print(f"Website '{site_name}' not found.")

    def run(self):
        # Split the string into words
        words = self.speech.lower()
        words=words.split()
        print(words)

        # Find the index of the specific word
        index = words.index("open")

        # Access the word after the specific word
        self.app_name= words[index + 1]

        self.open_app(self.app_name)
        self.open_website(self.app_name)


def main():
    # wishes to the user
    wish()

    while not stop_flag.is_set():
        # print(speak_flag,", ", gpt_in_use)

        if speak_flag == 0 and gpt_in_use == 0:  #do not Listen if gpt is generating content or speaking

            speech = command()
            compare(speech)

        if stop_flag.is_set():
            set_status("I've closed my ears")


def compare(speech):
    global speak_flag,gpt_in_use
    if speech:  # If there is some text in speech then proceed further

        if "my name is" in speech.lower():  # Updates the User's name
            name_arr = speech.split('my name is')[1]
            name = name_arr.split(" ")[1]
            print(f'\n\n{name}\n\n')
            respond(speech)

        elif "capital of india" in speech.lower():
            speak("Delhi is the capital of india")

        elif "save this conversation" in speech.lower():
            save_chat(chat)

        elif ("record my actions" in speech.lower()) or ("record my action".lower() in speech.lower()):
            speak("I am recording. please Perform Your clicks precisely")
            start()

        elif ("playback my actions" in speech.lower()) or("playback my action" in speech.lower()) or("repeat my action" in speech.lower())or("repeat my actions" in speech.lower()):
            playback()

        elif ("generate description of image" in speech.lower()) or ("detect some object" in speech.lower()) or ("detect object" in speech.lower()) or ("detect some objects" in speech.lower()) :
            generate_description()

        elif ("analyse a website" in speech.lower()) or ("analyse the website" in speech.lower()):
            speak("Yaa sure! please provide me the webiste URL")
            # Create a new temporary "parent"
            newWin = Tk()
            # But make it invisible
            newWin.withdraw()
            url = simpledialog.askstring("Input", "Enter the Url of website",parent=newWin)
            # Destroy the temporary "parent"
            newWin.destroy()
            time.sleep(1)
            if url:
                print("Hang on! analyzing the website contents")
                path = os.getcwd()
                threading.Thread(target=scrapper, args=(url,path,)).start()
            else:
                messagebox.showinfo("GPT-5","No URL Provided")

        elif ("stop listening" in speech.lower()) or ("do not listen" in speech.lower()) or ("turn off your ears" in speech.lower()) :
            speak("Turning off my ears")
            stop_flag.set()
            set_status("I've closed my ears")


        elif "generate image" in speech.lower():
            prompt=speech.split("image of")
            threading.Thread(target=create_image,args=(prompt[1],),daemon=True).start()


        elif "open" in speech.lower():
            assist=Assistant(speech)
            assist.start()


        elif "play" in speech.lower():
            music=speech.split("play")
            start_music(music)


        elif (("stop" in speech.lower()) or ("stop speaking" in speech.lower())):
            try:
                winspeech.stop_talking()
                speak_flag = 0
            except:
                pass

        elif 'exit' in speech.lower():
            speak("Goodbye! Have a great day!")
            time.sleep(2)
            window.destroy()
            exit()
        else:
            no_wait,response=respond(speech)
            if no_wait.lower()=='analyze'.lower():
                pass
            else:
                op_length = len(response)
                threading.Thread(target=wait_when_speaking,args=op_length)

                if speak_flag == 0 and gpt_in_use == 0:  #do not update the status if gpt is generating content or speaking
                    set_status("IDEAL")


if __name__ == "__main__":
    set_status('IDEAL')

    # Create the required directories if they do not exist
    if not os.path.exists("Saved-Chats"):
        os.mkdir("Saved-Chats")

    if not os.path.exists("Saved-logs"):
        os.mkdir("Saved-logs")

    if not os.path.exists("website-analysis"):
        os.mkdir("website-analysis")

    if not os.path.exists("User-data"):
        os.mkdir("User-data")


    try:
        open("User-data/info.txt", 'r').close
    except:
        open("User-data/info.txt", 'w').close

    # welcome the user by wish
    if not(open("User-data/info.txt", 'r').readline()[5:] != ''):
        # if no name is given to the system it asks for the info
        getinfo()

    stop_flag = threading.Event()
    # Create a thread to run the main() function
    main_thread = threading.Thread(target=main)
    main_thread.daemon = True  # Allow the thread to exit when the main program exits
    main_thread.start()

    # Start the Tkinter main loop in the main thread
    window.mainloop()
