import spacy
from spacy.training import Example, offsets_to_biluo_tags

nlp = spacy.blank("uk")  # або 'en' для англійської

ner = nlp.add_pipe("ner")

labels = ["RANK_NAME", "PERSON", "POSITION"]
for label in labels:
    ner.add_label(label)

TRAIN_DATA = [
    # "Сержант" займає позиції з 0 по 7, "Іванов" з 8 по 14, "північному кордоні" з 25 по 44
    ("Сержант Іванов був помічений на північному опорніку.",
     {"entities": [(0, 7, "RANK_NAME"), (8, 14, "PERSON"), (32, 51, "POSITION")]}),
    # "Полковник" займає позиції з 0 по 9, "Петров" з 10 по 16, "підрозділу" з 24 по 34
    ("Отряд Ехо був помічений на позиції Альфа.",
     {"entities": [(0, 5, "RANK_NAME"), (6, 9, "PERSON"), (27, 40, "POSITION")]}),
]


def check_alignment(text, entities):
    try:
        biluo_tags = offsets_to_biluo_tags(nlp.make_doc(text), entities)
        print(f"Alignment successful for text: {text}")
        print(f"BILUO Tags: {biluo_tags}")
    except Exception as e:
        print(f"Alignment error in text: {text}")
        print(str(e))


def get_ner_model():
    # todo add cashing to not increase disk usage
    nlp = spacy.load('../classifier/trained_ner_model')

    return nlp


if __name__ == '__main__':
    for text, annotations in TRAIN_DATA:
        check_alignment(text, annotations['entities'])

    optimizer = nlp.begin_training()

    for i in range(20):
        losses = {}
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], losses=losses, drop=0.3)
        print(f"Епоха {i + 1}: втрати - {losses}")

    nlp.to_disk("trained_ner_model")

    print()
    print("Сержант Іванов був помічений на північному опорніку")
    doc = nlp("Сержант Іванов був помічений на північному опорніку.")
    print(doc.ents)
    for ent in doc.ents:
        print(ent.text, ent.label_)

    print("Вовчік висувається на поляну")
    doc = nlp("Вовчік висувається на поляну.")
    print(doc.ents)
    for ent in doc.ents:
        print(ent.text, ent.label_)

    print("Отряд Ехо був помічений на позиції Альфа")
    doc = nlp("Отряд Ехо був помічений на позиції Альфа.")
    print(doc.ents)
    for ent in doc.ents:
        print(ent.text, ent.label_)
