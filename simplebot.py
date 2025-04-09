# WRITE YOUR CODE HERE
import tkinter.scrolledtext as tks #creates a scrollable text window

from datetime import datetime
from tkinter import *

from openai import OpenAI

# Initialize the OpenAI client with the API key
client = OpenAI()

# WRITE YOUR CODE HERE

# Generating response
def get_bot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


def create_and_insert_user_frame(user_input):
  userFrame = Frame(chatWindow, bg="#d0ffff")
  Label(
      userFrame,
      text=user_input,
      font=("Arial", 11),
      bg="#d0ffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
  Label(
      userFrame,
      text=datetime.now().strftime("%H:%M"),
      font=("Arial", 7),
      bg="#d0ffff"
  ).grid(row=1, column=0, sticky="w")

  chatWindow.insert('end', '\n ', 'tag-right')
  chatWindow.window_create('end', window=userFrame)


def create_and_insert_bot_frame(bot_response):
  botFrame = Frame(chatWindow, bg="#ffffd0")
  Label(
      botFrame,
      text=bot_response,
      font=("Arial", 11),
      bg="#ffffd0",
      wraplength=400,
      justify='left'
  ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
  Label(
      botFrame,
      text=datetime.now().strftime("%H:%M"),
      font=("Arial", 7),
      bg="#ffffd0"
  ).grid(row=1, column=0, sticky="w")

  chatWindow.insert('end', '\n ', 'tag-left')
  chatWindow.window_create('end', window=botFrame)
  chatWindow.insert(END, "\n\n" + "")


def send(event):
    chatWindow.config(state=NORMAL)

    user_input = userEntryBox.get("1.0",'end-2c')
    user_input_lc = user_input.lower()
    bot_response = get_bot_response(user_input_lc) 

    create_and_insert_user_frame(user_input)
    create_and_insert_bot_frame(bot_response)

    chatWindow.config(state=DISABLED)
    userEntryBox.delete("1.0","end")
    chatWindow.see('end')

# Create the main application window using Tk()
baseWindow = Tk()

# Set the title of the window
baseWindow.title("The Simple Bot")

# Set the size of the window
baseWindow.geometry("500x250")

# Create the chat window as a ScrolledText widget with "Arial" font
chatWindow = tks.ScrolledText(baseWindow, font="Arial")

# Configure tags for message alignment: 'tag-left' for bot messages, 'tag-right' for user messages
chatWindow.tag_configure('tag-left', justify='left')
chatWindow.tag_configure('tag-right', justify='right')

# Disable the chat window initially (it should not be editable by the user)
chatWindow.config(state=DISABLED)

# Create the send button, with specific font, text, and background color
# The 'command' option is commented out. Uncomment it and replace 'send' with your send function's name
sendButton = Button(
    baseWindow,
    font=("Verdana", 12, 'bold'),
    text="Send",
    bg="#fd94b4",
    activebackground="#ff467e",
    fg='#ffffff',
    command=send)
sendButton.bind("<Button-1>", send)
baseWindow.bind('<Return>', send)

# Create the user entry box where the user types their messages
userEntryBox = Text(baseWindow, bd=1, bg="white", width=38, font="Arial")

# Place the chat window, user entry box, and send button on the main window using specific coordinates and sizes
chatWindow.place(x=1, y=1, height=200, width=500)
userEntryBox.place(x=3, y=202, height=27)
sendButton.place(x=430, y=200)

# Start the main event loop to keep the application running and responsive
baseWindow.mainloop()    