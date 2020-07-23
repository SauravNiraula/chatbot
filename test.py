from trainer import Main_trainer
import process

main_data = process.open_file("datasets/dataset.txt")
ai_data = process.open_file("datasets/ai.yml")
botprofile_data = process.open_file("datasets/botprofile.yml")
computers_data = process.open_file("datasets/computers.yml")
food_data = process.open_file("datasets/food.yml")
gossip_data = process.open_file("datasets/gossip.yml")
greetings_data = process.open_file("datasets/greetings.yml")
health_data = process.open_file("datasets/health.yml")
history_data = process.open_file("datasets/history.yml")
humor_data = process.open_file("datasets/humor.yml")
literature_data = process.open_file("datasets/literature.yml")
money_data = process.open_file("datasets/money.yml")
movies_data = process.open_file("datasets/movies.yml")
politics_data = process.open_file("datasets/politics.yml")
psychology_data = process.open_file("datasets/psychology.yml")
science_data = process.open_file("datasets/science.yml")
sports_data = process.open_file("datasets/sports.yml")
trivia_data = process.open_file("datasets/trivia.yml")
emotion_data = process.open_file("datasets/emotion.yml")

questions, answers = process.process_txt(main_data, ai_data, botprofile_data, computers_data, emotion_data, food_data, gossip_data, greetings_data, health_data, history_data, humor_data, literature_data, money_data, movies_data, politics_data, psychology_data, science_data, sports_data, trivia_data)

trainer = Main_trainer(questions, answers)
trainer.train()
# trainer.save_model()

# trainer = Main_trainer()
# model = trainer.load_model()


while True:
    question = input("You > ")
    answer = trainer.ask(question)
    print("random > ", answer)