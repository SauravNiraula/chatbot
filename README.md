# ChatBot

## Required Packages:
    1. NLTK

## for testing purpose please type "python test.py"

# code :

    from trainer import Main_trainer
    import process

### open dataset

    doc = process.open_file("path_to_your_dataset")

### process dataset

    questions, answers = process.process_txt(doc, ..*args)

### while training

    trainer = Main_trainer(questions, answers)
    trainer.train()
    trainer.save_model() # will save model to "model" in current directory


### testing model

    trainer = Main_trainer()
    model = trainer.load_model()

    answer = model.ask("question here")

    print(answer)