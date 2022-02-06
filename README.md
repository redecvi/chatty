# chatty
Chatty is a chatbot that gives very basic responses :)

It has the following structure:
chatty
├── chatty
│   ├── __init__.py
│   ├── gui.py
│   ├── response.py
│   └── train.py
├── files
│   ├── chatty.h5
│   ├── classes.pkl
│   ├── words.pkl
│   └── intents.json
├── README
├── requirements.txt
└── setup.py

The entry point is gui.py. It can be directly loaded. It will open the following window
![image](https://user-images.githubusercontent.com/61469992/152700202-55dedb37-e1f4-47bf-8051-79b732b8f712.png)

You can write in the textbox below and Chatty will respond.

The chatbot uses NLTK and Keras for the model and TKinter for the GUI.
