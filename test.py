from trainer import Main_trainer
import process

document = process.open_file("dataset.txt")
questions, answers = process.process_txt(document)

trainer = Main_trainer(questions, answers)
trainer.train()
trainer.save_model()

# trainer = Main_trainer()
model = trainer.load_model()


while True:
    question = input("You > ")
    answer = model.ask(question)
    print("random > ", answer)