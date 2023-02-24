# import the libraries to use
from tkinter import *
from tkinter import scrolledtext
import os
import openai
import pyttsx3

question_asked = ''
response_msg = ''

# Set your API key as an environment variable
os.environ["OPENAI_API_KEY"] = "Paste openai api key here"

# Initialize the OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]

# tkinter dialogue box initialization and settings
root = Tk()
root.resizable(False, False)
root.geometry("850x500")
root.title("ChatBot Using OpenAI")
root.configure(bg='brown')

###############################################################################
'''https://stackoverflow.com/questions/53178718/
tkinter-inserting-button-in-a-text-box-next-to-text-in-each-line-dynamically'''
################################################################################


# function to add a tab stop at the left edge of the textbox
def reset_tabs(event):
    # Add a tab stop at the left edge of the widget
    right_margin = event.width - 8
    if right_margin <= 0: return
    tabs = (right_margin, "left")
    event.widget.configure(tabs=tabs)


# insert button function
def callback(text):
    SpeakText(str(text).capitalize())


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 145)
    engine.say(command)
    engine.runAndWait()


# function to predict titles
def predict_outcome(prompt, model, max_tokens=150):
    response = openai.Completion.create(engine=model,
                                        prompt=prompt,
                                        max_tokens=max_tokens,
                                        n=1, stop=None,
                                        temperature=0)
    message = str(response.choices[0].text.strip())
    return message


# function to get user input
def take_input():
    global question_asked, response_msg
    # clear previous string
    response_msg = ''
    question_asked = ''
    # get the input text string
    question_asked = str(inputtxt.get()).capitalize()
    # detect when no user input
    if len(question_asked) <= 0:
        return

    # output the user input to the chat screen
    Output.insert(END, '>> ' + question_asked + '\n', "left")
    # clear the last user input
    inputtxt.delete(0, 'end')
    # call the openai response function
    response_msg = predict_outcome(prompt=question_asked, model="text-davinci-002")

    # display OpenAI response message
    item = '>> ' + response_msg
    Output.insert(END, item + "\t\n")
    button = Button(Output, text="Play audio format", padx=2, pady=2,
                    cursor="left_ptr",
                    bd=1, highlightthickness=0,
                    command=lambda text=item: callback(text), fg="white", bg="black", font=('Times', 12))
    Output.window_create("end-2c", window=button)
    # output a newline
    Output.insert(END, '\n', "left")
    # returns back
    return

######################################
# Tkinter interface window settings
######################################


# assign the first label
l1 = Label(text="OpenAI chatBot message screen:", fg="white", bg="grey", font=('Times', 14))
# create the output text box
Output = scrolledtext.ScrolledText(root, height=10,
                width=80,
                bg="light yellow", font=('Times', 12))
# assign the second label
l2 = Label(text="Enter your request here:", fg="white", bg="grey", font=('Times', 14))
# create the user text input box
inputtxt = Entry(root,
              width=50,
              bg="white", justify=CENTER, font=('Times', 12))
# create the button to send user entered text
Display = Button(root, height=1,
                 width=15,
                 text="Send Request",
                 command=lambda: take_input(), fg="white", bg="black", font=('Times', 14))
# configure the text justification
Output.tag_configure("right", justify="right")
Output.tag_configure("left", justify="left")

# organise widgets in blocks before placing them in the parent widget
l1.pack()
Output.pack(fill="both", expand=True)
Output.bind("<Configure>", reset_tabs)
l2.pack()
inputtxt.pack()
Display.pack()
# Bind the Enter Key to the window
root.bind('<Return>', lambda event=None: Display.invoke())
# start dialogue app
mainloop()