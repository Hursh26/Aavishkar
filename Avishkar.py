
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

#Scrapper imports
from bs4 import BeautifulSoup
import pickle

#GUI imports
import tkinter
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import Tk, Canvas, Text, Button, PhotoImage, simpledialog,messagebox
import subprocess
import cvzone



#global variables
chat = ""
wait_time = 0
mouse=Controller()
actions = []

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
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
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
def status(current):
    canvas.after(0,
    lambda: canvas.itemconfig('status', text=current))

def set_status(current):
    SetStatus=threading.Thread(target=status, args=(current,))
    SetStatus.start()
    print("Status setted as",current)

#code to display options
def options():
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
        text='Saved scrappers',
        borderwidth=2,
        highlightthickness=2,
        command=lambda: open_File('Scrapped-data'),
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

def show_options():
    ShowOptions=threading.Thread(target=options)
    ShowOptions.start()

def close_options(canvas,button1,button2,button3,button4):
    copt=threading.Thread(target=destroy_options,args=(canvas,button1,button2,button3,button4))
    copt.start()

def destroy_options(canvas,button1,button2,button3,button4):
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
    OpenFile=threading.Thread(target=choose_file,args=(location,))
    OpenFile.start()

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

entry_image_2 = PhotoImage(
    file=relative_to_assets2("entry_1.png"))
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
    objects=[]
    input_value = messagebox.askyesno("Records", "Do you want to give image from camera?")

    if input_value:

        speak("Starting your camera please wait")
        object_by_video()

    else:
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

def object_by_video():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    model = YOLO('yolov8n.pt')
    speak("show all the objects one by one. Press Q to stop the object detection and generate description")

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


def scrapper(url,path):

    r = requests.get(url)
    path=path+r'\data.txt'
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find all text elements in the parsed HTML
    text_elements = soup.find_all(string=True)

    # Combine and clean the text from these elements
    full_text = "\n".join(text_elements).strip()
    print(full_text)

    response,do,ai=gpt(f'analyze this website data:"{full_text}" \n\nReply me "Done!" when you are done analyzing','analyze')
    response = json.loads(response.content.decode())['choices'][0]['message']['content']
    if response:
        print(response)
        speak("I've analyzed your website content!")
        messagebox.showinfo("gpt-5", f"Website analyzed sucessfully")

    with open(path,"w", encoding='utf-8') as f:
        f.write(full_text)
        f.close()


#GPT Interaction
def command():
    r = recognize.Recognizer()
    with recognize.Microphone() as source:

        set_status("Listening...")
        print("Listening...")
        # r.pause_threshold = 2
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise before listening
        try:
            audio = r.listen(source)  # Add timeout to limit listening time
            set_status('Recognising...')
            query = r.recognize_google(audio, language="en-in")
            set_status("Recognized!")
            generate_label(query,'red','white',Qx)
            return query

        except recognize.WaitTimeoutError:
            set_status("No speech detected.")
        except recognize.UnknownValueError:
            set_status("Sorry, I couldn't understand what you said.")
            time.sleep(1)
        except recognize.RequestError as e:
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
    if (hour == 0) and (hour <= 12):
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
    try:
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

        else:
            set_status('generating your content... \nThis may take a while')
        response = requests.post(URL, headers=headers, json=payload, stream=False)
        return response,do,ai_name
    except requests.exceptions.ConnectionError:
        messagebox.showinfo("Error","Please connect to the Internet")

def respond(Query,objects=None):
    global wait_time,chat

    #get response from gpt
    response,do,ai_name=gpt(Query)
    # print(response)
    # response=json.loads(response.content.decode())
    try:
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

        else:
            chat += f'{response}\n'
            # print(f"{ai_name} says:\n{response}")
            print(chat)
            generate_label(response,'green','black',Ay)
            speak(response)
            set_status('Speaking....')
            return 'xyz',response
    except:
        speak("server is busy please try after 20 minutes")


def speak(text):
    winspeech.say(text)

def update_ring(circle,ring, center_x, center_y):
    global wait_time
    end_time = time.time() + wait_time  # Update the ring for 2 seconds
    while time.time() < end_time:
        width = random.randint(1, 5)
        radius = random.randint(270, 300)

        ring.itemconfig(circle, width=width, outline="#5FFDFF")
        ring.coords(circle, center_x - radius, center_y - radius, center_x + radius, center_y + radius)
        ring.update()
        time.sleep(0.1)  # Adjust the sleep time as needed


def main():
    # wishes to the user
    wish()

    while not stop_flag.is_set():
        speech = command()
        compare(speech)
        if stop_flag.is_set():
            set_status("I've closed my ears")


def compare(speech):
    if speech:  # If there is some text in speech then proceed further

        if "my name is".lower() in speech.lower():  # Updates the User's name
            name_arr = speech.split('my name is')[1]
            name = name_arr.split(" ")[1]
            print(f'\n\n{name}\n\n')
            respond(speech)

        elif "save this conversation".lower() in speech.lower():
            save_chat(chat)

        elif ("record my actions".lower() in speech.lower()) or ("record my action".lower() in speech.lower()):
            speak("I am recording. please Perform Your clicks precisely")
            start()

        elif ("playback my actions" in speech.lower()) or("playback my action" in speech.lower()) or("repeat my action" in speech.lower())or("repeat my actions" in speech.lower()):
            playback()

        elif "generate description of image".lower() in speech.lower():
            generate_description()

        elif ("analyse a website".lower() in speech.lower()) or ("analyse the website".lower() in speech.lower()):
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
                scrapper(url,path)
            else:
                messagebox.showinfo("GPT-5","No URL Provided")

        elif ("stop listening".lower() in speech.lower()) or ("do not listen" in speech.lower()) or ("turn off your ears" in speech.lower()) :
            speak("Turning off my ears")
            stop_flag.set()

        elif 'exit'.lower() in speech.lower():
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
                print(op_length)
                if op_length <= 50:
                    wait_time = op_length / 9.5
                    time.sleep(wait_time)
                else:
                    wait_time = op_length / 17
                    time.sleep(wait_time)
                set_status("IDEAL")


if __name__ == "__main__":
    set_status('IDEAL')

    # Create the required directories if they do not exist
    if not os.path.exists("Saved-Chats"):
        os.mkdir("Saved-Chats")

    if not os.path.exists("Saved-logs"):
        os.mkdir("Saved-logs")

    if not os.path.exists("Scrapped-data"):
        os.mkdir("Scrapped-data")

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
