import nltk
from nltk.stem import WordNetLemmatizer
import json
import numpy as np
import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import random

# Download NLTK packages
nltk.download('punkt')
nltk.download('wordnet')

class Training():
    """
    Class to train the model
    """
    def __init__(self):
        print('Initializing training')
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?', '!']
        self.lemmatizer = WordNetLemmatizer()
        self.model = None
        self._load_intents()

    def _load_intents(self):
        """
        Loads the intents.json file in tho the 
        """
        intents = json.load(open('files/intents.json'))

        for intent in intents.get('intents'):
            for pattern in intent.get('patterns'):
                # tokenize each word
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)

                # add documents
                tag = intent.get('tag')
                self.documents.append((w, tag))

                # add classes to our class list
                if tag not in self.classes:
                    self.classes.append(tag)

        self.words = [self.lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))

        self.classes = sorted(list(set(self.classes)))
        
        # Save words and classes
        pickle.dump(self.words, open('files/words.pkl', 'wb'))
        pickle.dump(self.classes, open('files/classes.pkl', 'wb'))
    
    def train(self):
        train_x, train_y = self._prepare_training()
        self._train_model(train_x, train_y)
    
    def _prepare_training(self):
        """
        Performs pre-processing of data for training and creates train_x and train_y
        """
        print('Preparing training data')
        training = []
        output_empty = [0] * len(self.classes)

        for doc in self.documents:
            # initialize bag of words
            bag = []
            # list of tokenized words for the pattern
            pattern_words = doc[0]
            # lemmatize each word - create base word, in attempt to represent related words
            pattern_words = [self.lemmatizer.lemmatize(word.lower()) for word in pattern_words]
            # create bag of words array with 1, if word match found in current pattern
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            # output is a '0' for each tag and '1' for current tag (for each pattern)
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1

            training.append([bag, output_row])
        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training)
        # create train and test lists. X - patterns, Y - intents
        train_x = list(training[:,0])
        train_y = list(training[:,1])
        return train_x, train_y
    
    def _train_model(self, train_x, train_y, filename='chatty'):
        """
        Create model - 3 layers. First layer 128 neurons, second layer
        64 neurons and 3rd output layer contains number of neurons
        equal to number of intents to predict output intent with softmax

        :param train_x: list with the training data
        :param train_y: list with the training outcome
        :param filename: filename to save model as (will add .h5 extension)
        """
        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        # Compile model. Stochastic gradient descent with Nesterov
        # accelerated gradient gives good results for this model
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        #fitting and saving the model
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save(f'files/{filename}.h5', hist)
        self.model = model
        print('model created and saved')


if __name__ == '__main__':
    training = Training()
    training.train()