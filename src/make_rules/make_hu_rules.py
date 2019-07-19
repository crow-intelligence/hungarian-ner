import pickle

import spacy
from spacy.pipeline import EntityRuler
import hu_core_ud_lg

with open('data/interim/entities.p', 'rb') as f:
    patterns = pickle.load(f)

patterns = [e for e in patterns if len(e['pattern']) > 0]

nlp = hu_core_ud_lg.load()
ruler = EntityRuler(nlp)

ruler.add_patterns(patterns)
nlp.add_pipe(ruler)
ruler.to_disk("data/processed/patterns.jsonl")

# test it
doc = nlp('Magyarország miniszterelnöke Orbán Viktor nem határos az Amerikai Egyesült Államokkal.')
print([(ent.text, ent.label_) for ent in doc.ents])

doc = nlp('Gyurcsány Ferenc, Orbán Viktor és Antal József miniszterelnökök.')
print([(ent.text, ent.label_) for ent in doc.ents])

doc = nlp('Nagy port kavart Márki-Zay Péter hódmezővásárhelyi polgármester, független ellenzéki politikus egy múlt heti interjúja, amiben hosszasan beszélt arról, hogy szerinte elfogadható (sőt szükséges), ha a szülő testi fenyítést alkalmaz gyerekeivel szemben fegyelmezésként.')
print([(ent.text, ent.label_) for ent in doc.ents])
