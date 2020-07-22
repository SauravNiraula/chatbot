import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer

nltk.download('punkt')
nltk.download('wordnet')

import pickle
import os

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
        self.tokenized_questions = None
        self.refined_questions = []
        self.question_vector = []
        self.mapping_dict = {}

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
                temp = list(set(temp))

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

        print("creating mapping list of questions finished")

    def convert_to_vector(self):
        print("converting to vector")

        for question in self.refined_questions:
            temp = []
            for word in question:
                temp.append(self.mapping_dict[word])
            
            self.question_vector.append(temp)

        print("converting to vector finished") 
        print("training process completed!")


    def train(self):
        self.tokenize()
        self.stem()
        self.create_word_mapping_dict()
        self.convert_to_vector()

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
        for word in refined_question:
            try:
                temp.append(self.mapping_dict[word])
            except:
                temp.append(-1)

        temp = list(set(temp))

        score_list = []
        
        for each in self.question_vector:
            similarity_value = 0
            dissimilarity_value = 0
            for i in each:
                if i in temp:
                    similarity_value += 1;
                else:
                    dissimilarity_value += 0.0001;

            score_list.append(similarity_value - dissimilarity_value)

        max_score = max(score_list)
        # print(score_list)

        index_of_max_score = score_list.index(max_score)

        return self.answers[index_of_max_score]



if __name__ == "__main__":
    
    # trainer = Main_trainer(["", "Hello", "hi", "Hello, how are you?", "are you fine?", "how you doing", "are you happy?"], ["sorry your question doesnot match any questions in my model!", "Hi", "Hello", "I'm fine", "yes", "Good", "I am happy aslong as you are :)"])
    # trainer.tokenize()
    # # print(trainer.tokenized_questions)
    # trainer.stem()
    # # print(trainer.refined_questions)
    # trainer.create_word_mapping_dict()
    
    # trainer.convert_to_vector()

    # trainer.save_model()
    trainer = Main_trainer()

    model = trainer.load_model()
    
    while True:
        answer = model.ask(input("randomuser > "))
        print(answer + "\n")