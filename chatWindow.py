import tkinter as tk

class ChatWindow():
    def __init__(self, pubkey, name):

        root = tk.Tk()
        root.title("Chat with " + name)
        root.geometry("500x500")