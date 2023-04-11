import tkinter as tk
import asyncio
from rasa.core.agent import Agent

# initialize the Rasa agent
agent = Agent.load("models/20230409-224137-archaic-centroid.tar.gz")

# create the main window
root = tk.Tk()
root.title("Rasa Chatbot")

# create the input box
input_box = tk.Entry(root, width=50)
input_box.pack()

# define a function to handle the button click
async def handle_click():
    user_input = input_box.get()
    response = await agent.handle_text(user_input)
    # display the response in a text box
    response_box.insert(tk.END, f"\nUser: {user_input}")
    response_box.insert(tk.END, f"\nBot: {response[0]['text']}")

# create the button
button = tk.Button(root, text="Send", command=lambda: asyncio.run(handle_click()))
button.pack()

# create the text box to display the conversation
response_box = tk.Text(root, width=50, height=20)
response_box.pack()

# start the main event loop
root.mainloop()

