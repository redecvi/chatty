from keras.models import load_model
import nltk
import json
import pickle
import numpy as np
import random

class Response:
    def __init__(self):
        self.model = load_model('files/chatty.h5')
        self.intents = json.load(open('files/intents.json'))
        self.words = pickle.load(open('files/words.pkl', 'rb'))
        self.classes = pickle.load(open('files/classes.pkl', 'rb'))
        self.lemmatizer = nltk.WordNetLemmatizer()

    def respond(self, msg):
        ints = self._predict_class(msg)
        res = self._get_response(ints)
        return res

    def _clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(w.lower()) for w in sentence_words]
        return sentence_words

    def _bow(self, sentence, words, show_details=True):
        """
        Return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

        Args:
            sentence: sentence to input
            words: vocabulary
            show_details (bool, optional): whether to show details. Defaults to True.
        """
        # tokenize the pattern
        sentence_words = self._clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return np.array(bag)
    
    def _predict_class(self, sentence):
        """
        filter out predictions below a threshold

        :param sentence: sentence to input
        :return: predicted class list
        """
        # filter out predictions below a threshold
        p = self._bow(sentence, self.words, show_details=False)
        res = self.model.predict(np.array([p]))[0]
        error_threshold = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>error_threshold]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def _get_response(self, ints):
        """
        Gets response

        :param ints: intents
        :param intents_json: intents file
        :return: result
        """
        tag = ints[0]['intent']
        list_of_intents = self.intents['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result