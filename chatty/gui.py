#Creating GUI with tkinter
from chatty.response import Response
from tkinter import Tk, Text, Scrollbar, Button, END, NORMAL, DISABLED, FALSE

class GUI:
    """
    GUI class that creates chat window with TKinter
    """
    def __init__(self):
        self.response = Response()
        self.base = None
        self.entry_box = None
        self.chat_log = None
        self.scrollbar = None
        self.send_button = None
        self._create_gui()
    
    def _create_gui(self):
        """
        Create the GUI
        """
        self.base = Tk()
        self.base.title("Chatty")
        self.base.geometry("400x500")
        self.base.resizable(width=FALSE, height=FALSE)

        #Create Chat window
        self.chat_log = Text(self.base, bd=0, bg="white", height="8", width="50", font="Arial",)

        self.chat_log.config(state=DISABLED)

        #Bind scrollbar to Chat window
        self.scrollbar = Scrollbar(self.base, command=self.chat_log.yview, cursor="heart")
        self.chat_log['yscrollcommand'] = self.scrollbar.set

        #Create Button to send message
        self.send_button = Button(self.base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                            bd=0, bg="grey18", activebackground="grey73",fg='black',
                            command= self.send)

        #Create the box to enter message
        self.entry_box = Text(self.base, bd=0, bg="white",width="29", height="5", font="Arial")


        #Place all components on the screen
        self.scrollbar.place(x=376,y=6, height=386)
        self.chat_log.place(x=6,y=6, height=386, width=370)
        self.entry_box.place(x=128, y=401, height=90, width=265)
        self.send_button.place(x=6, y=401, height=90)

    def send(self):
        """
        Define what happens when click on send
        """
        msg = self.entry_box.get("1.0",'end-1c').strip()
        self.entry_box.delete("0.0",END)

        if msg != '':
            self.chat_log.config(state=NORMAL)
            self.chat_log.insert(END, "You: " + msg + '\n\n')
            self.chat_log.config(foreground="#442265", font=("Verdana", 12 ))

            res = self.response.respond(msg)
            self.chat_log.insert(END, "Bot: " + res + '\n\n')

            self.chat_log.config(state=DISABLED)
            self.chat_log.yview(END)

if __name__ == '__main__':
    gui = GUI()
    gui.base.mainloop()