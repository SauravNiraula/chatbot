import os


def open_file(path):
    doc = None
    if (os.path.exists(path)):
        doc = open(path, 'r')
    else:
        print("path doesn't exists!")

    return doc

def process_txt(*args):
    questions = []
    answers = []

    i = 0

    for doc in args:

        while True:
            line = doc.readline()

            if line != '':
                if i % 2 == 0:
                    questions.append(line)
                else:
                    answers.append(line)

                i += 1
                
            else:
                break
    
    return questions, answers

if __name__ == "__main__":

    main_doc = open_file("/datasets/dataset.txt")
    ai_doc = open_file("datasets/ai.yml")
    print(process_txt(main_doc, ai_doc))