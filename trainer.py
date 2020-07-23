import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer

nltk.download('punkt')
nltk.download('wordnet')

import tensorflow as tf

import pickle
import os
import random
import math
from collections import Counter

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

class Main_trainer:
    def __init__(self, questions=[], answers=[]):
        """
            > be sure you have nltk installed
            > question and answers should be list with same shape 
              if not it will be ignored
        
        """

        self.questions = questions
        self.answers = answers
        self.answer_vector = []
        self.tokenized_questions = None
        self.refined_questions = []
        self.question_vector = []
        self.mapping_dict = {}
        self.oned_list = []
        self.final_questions = []

        self.model = None

    def tokenize(self):
        print("tokenizing")

        self.tokenized_questions = [ nltk.word_tokenize(question) for question in self.questions ]

        print("tokeinzing finished")

    def stem(self):
        print("stemming and lemmatizing")

        for question in self.tokenized_questions:
            temp = []
            for word in question:
                if word.isalpha():
                    stemmed_word = stemmer.stem(word)
                    lemmatized_word = lemmatizer.lemmatize(stemmed_word, pos="a")
                    temp.append(lemmatized_word.lower())

            self.refined_questions.append(temp)

        print("stemming and lemmatizing finished")

    def create_word_mapping_dict(self):

        print("creating mapping list of questions")

        temp_list = []
        for question in self.refined_questions:
            temp = set(question)
            temp_list.extend(temp)

        temp_list = set(temp_list)
        
        for index, each in enumerate(temp_list):
            self.mapping_dict[each] = index
            self.oned_list.append(index)

        print("creating mapping list of questions finished")

    def convert_to_vector(self):
        print("converting to vector")

        for question in self.refined_questions:
            temp = []
            for word in question:
                temp.append(self.mapping_dict[word])
            
            self.question_vector.append(temp)

        print("converting to vector finished")


    def get_final_data(self):
        print("Getting final data")

        for each in self.question_vector:
            temp = []
            for i in self.oned_list:
                t = 0
                if i in each:
                    t = 1
                temp.append(t)

            self.final_questions.append(temp)

        self.answer_vector = [i for i in  range(len(self.question_vector))]

        print("Getting final data finished")

    

    def tensorflow_stuffs(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(50),
            tf.keras.layers.Dense(len(self.answer_vector))
        ])

        self.model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

        self.model.fit(self.final_questions, self.answer_vector, epochs=100)

        self.probability_model = tf.keras.Sequential([self.model, 
                                         tf.keras.layers.Softmax()])


    def train(self):
        print("training process started!")
        
        self.tokenize()
        self.stem()
        self.create_word_mapping_dict()
        self.convert_to_vector()
        self.get_final_data()
        self.tensorflow_stuffs()

        print("training process completed!")


    def save_model(self):
        with open("model", 'wb') as file:
            pickle.dump(self, file)

    def load_model(self):
        model = None
        if (os.path.exists("model")):
            with open("model", 'rb') as file:
                model = pickle.load(file)
        else:
            print("Model not found!")
        
        return model



    def ask(self, question):
        words = nltk.word_tokenize(question.lower())
        refined_question = [ lemmatizer.lemmatize(stemmer.stem(word)) for word in words ]
        temp = []
        final = []
        for word in refined_question:
            try:
                temp.append(self.mapping_dict[word])
            except:
                pass

        for i in self.oned_list:
            t = 0
            if i in temp:
                t = 1
            final.append(t)

        answer = self.probability_model.predict([final])

        answer = list(answer[0])

        max_answer = max(answer)

        temp = []

        for index, i in enumerate(answer):
            if i == max_answer:
                temp.append(index)

        index_max = random.choice(temp)

        return self.answers[index_max]


if __name__ == "__main__":
    
    trainer = Main_trainer(["", "Hello", "hi", "Hello, how are you?", "are you fine?", "how you doing", "are you happy?"], ["sorry your question doesnot match any questions in my model!", "Hi", "Hello", "I'm fine", "yes", "Good", "I am happy aslong as you are :)"])
    
    trainer.train()

    while True:
        answer = trainer.ask(input("You > "))
        print(answer)