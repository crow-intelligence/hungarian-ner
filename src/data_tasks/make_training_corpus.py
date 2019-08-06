import pickle

from sacremoses import MosesDetokenizer
from spacy.gold import iob_to_biluo
from spacy.gold import offsets_from_biluo_tags

import hu_core_ud_lg

sentences = []
iobs = []

with open("data/corpora/hun_ner_corpus.txt", "r", encoding="iso-8859-2") as f:
    sent = []
    tags = []
    for l in f:
        l = l.strip().split("\t")
        if len(l) == 2:
            wd, tag = l[0], l[1]
            if tag == "0":
                tag = "O"
            sent.append(wd)
            tags.append(tag)
        else:
            if len(sent) > 0 and len(tags) > 0:
                sentences.append(sent)
                iobs.append(tags)
            sent = []
            tags = []

with open("data/corpora/HVGJavNEContext", "r", encoding="iso-8859-2") as f:
    sent = []
    tags = []
    for l in f:
        l = l.strip().split()
        if len(l) == 2:
            wd, tag = l[0], l[1]
            if tag == "0":
                tag = "O"
            sent.append(wd)
            tags.append(tag)
        else:
            if len(sent) > 0 and len(tags) > 0:
                sentences.append(sent)
                iobs.append(tags)
            sent = []
            tags = []

hunerwiki = [
    "data/corpora/huwiki.1.tsv",
    "data/corpora/huwiki.2.tsv",
    "data/corpora/huwiki.3.tsv",
    "data/corpora/huwiki.4.tsv",
]

for f in hunerwiki:
    with open(f, "r") as tf:
        sent = []
        tags = []
        for l in tf:
            l = l.strip().split("\t")
            wd, tag = l[0], l[-1]
            if len(l) == 2:
                wd, tag = l[0], l[1]
                if tag == "0":
                    tag = "O"
                sent.append(wd)
                tags.append(tag)
            else:
                sentences.append(sent)
                iobs.append(tags)
                sent = []
                tags = []
corpus = []
nlp = hu_core_ud_lg.load()
md = MosesDetokenizer(lang="hu")
for i in range(len(sentences)):
    detokenized_sent = md.detokenize(sentences[i])
    doc = nlp(detokenized_sent)
    doc_toks = [tok.text for tok in doc]
    if not (doc_toks == sentences[i]):
        # doc_toks rövidebb általában
        j = 0
        k = 0
        new_tags = []
        while j < len(sentences[i]):
            if sentences[i][j] == doc_toks[k]:
                new_tags.append(iobs[i][j])
                j += 1
                k += 1
            else:
                new_tags.append(iobs[i][j])
                k += 1
                j += 2
        tags = iob_to_biluo(new_tags)
    else:
        tags = iob_to_biluo(iobs[i])
    try:
        entities = offsets_from_biluo_tags(doc, tags)
        e = (detokenized_sent, entities)
        corpus.append(e)
    except Exception as err:
        print(err, detokenized_sent)
        continue

print(len(corpus))
corpus = [e for e in corpus if len(e[0]) > 0]
print(len(corpus))

with open("data/interim/corpus.p", "wb") as of:
    pickle.dump(corpus, of)
