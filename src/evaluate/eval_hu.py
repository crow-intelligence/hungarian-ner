import pickle
import spacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer

with open("data/interim/test.p", "rb") as f:
    test_corpus = pickle.load(f)


nlp = spacy.load("models")


def evaluate(ner_model, examples):
    scorer = Scorer()
    for input_, annot in examples:
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot["entities"])
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    return scorer.scores


results = evaluate(nlp, test_corpus)
