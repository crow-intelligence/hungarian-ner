import itertools
import random
import pickle

import nltk


def get_entities(ner_tags):
    person_pattern = r"""KT: {<I-PER>+}"""
    location_patterns = r"""KT: {<I-LOC>+}"""
    organization_pattern = r"""KT: {<I-ORG>+}"""

    person_chunker = nltk.chunk.regexp.RegexpParser(person_pattern)
    person_chunks = nltk.chunk.tree2conlltags(person_chunker.parse(ner_tags))
    persons = [
        " ".join(word for word, tag, chunk in group)
        for key, group in itertools.groupby(person_chunks, lambda l: l[1] == "I-PER")
        if key
    ]

    location_chunker = nltk.chunk.regexp.RegexpParser(location_patterns)
    location_chunks = nltk.chunk.tree2conlltags(location_chunker.parse(ner_tags))
    locations = [
        " ".join(word for word, tag, chunk in group)
        for key, group in itertools.groupby(location_chunks, lambda l: l[1] == "I-LOC")
        if key
    ]

    organization_chunker = nltk.chunk.regexp.RegexpParser(organization_pattern)
    organization_chunks = nltk.chunk.tree2conlltags(
        organization_chunker.parse(ner_tags)
    )
    organizations = [
        " ".join(word for word, tag, chunk in group)
        for key, group in itertools.groupby(
            organization_chunks, lambda l: l[1] == "I-ORG"
        )
        if key
    ]
    return list(set(persons)), list(set(locations)), list(set(organizations))


with open("data/interim/locations.p", "rb") as f:
    patterns = pickle.load(f)

with open("data/interim/loci.p", "rb") as f:
    loci = pickle.load(f)

locs = []
orgs = []
pers = []

with open("data/corpora/hun_ner_corpus.txt", "r", encoding="iso-8859-1") as f:
    ner_tags = []
    for l in f:
        l = l.strip().split("\t")
        if len(l) == 2:
            if l[0] not in ",;.!%=/?+()":
                ner_tags.append((l[0], l[1]))
    p, l, o = get_entities(ner_tags)
    pers.extend(p)
    locs.extend(l)
    orgs.extend(o)

with open("data/corpora/HVGJavNEContext", "r", encoding="iso-8859-1") as f:
    ner_tags = []
    for l in f:
        if len(l.split()) == 2:
            l = l.strip().split()
            if l[0] not in ",;.!%=/?+()":
                ner_tags.append((l[0], l[1]))
    p, l, o = get_entities(ner_tags)
    pers.extend(p)
    locs.extend(l)
    orgs.extend(o)

hunerwiki = [
    "data/corpora/huwiki.1.tsv",
    "data/corpora/huwiki.2.tsv",
    "data/corpora/huwiki.3.tsv",
    "data/corpora/huwiki.4.tsv",
]

for f in hunerwiki:
    ner_tags = []
    with open(f, "r") as tf:
        for l in tf:
            l = l.strip().split("\t")
            if len(l) == 6:
                wd, tag = l[-2], l[-1]
                if wd not in ",;.!%=/?+()":
                    tag = tag.replace("B-", "I-")
                    ner_tags.append((wd, tag))

    p, l, o = get_entities(ner_tags)
    pers.extend(p)
    locs.extend(l)
    orgs.extend(o)

pers = list(set([e for e in pers if e not in loci]))
loci.extend(pers)
locs = list(set([e for e in locs if e not in loci]))
loci.extend(locs)
orgs = list(set([e for e in orgs if e not in loci]))
loci.extend(orgs)

print(len(pers), len(locs), len(orgs))

for person in pers:
    if len(person.split()) == 1:
        pattern = {"label": "PERSON", "pattern": person.title()}
    else:
        pattern_list = []
        for e in person.split():
            ed = {"lower": e.lower()}
            pattern_list.append(ed)
        pattern = {"label": "PERSON", "pattern": pattern_list}
    patterns.append(pattern)

for location in locs:
    if len(location.split()) == 1:
        pattern = {"label": "GPE", "pattern": location.title()}
    else:
        pattern_list = []
        for e in location.split():
            ed = {"lower": e.lower()}
            pattern_list.append(ed)
        pattern = {"label": "GPE", "pattern": pattern_list}
    patterns.append(pattern)

for organization in orgs:
    if len(organization.split()) == 1:
        pattern = {"label": "ORG", "pattern": organization.title()}
    else:
        pattern_list = []
        for e in organization.split():
            ed = {"lower": e.lower()}
            pattern_list.append(ed)
        pattern = {"label": "ORG", "pattern": pattern_list}
    patterns.append(pattern)

with open("data/interim/entities.p", "wb") as of:
    pickle.dump(patterns, of)

with open("data/interim/ents.p", "wb") as of:
    pickle.dump(loci, of)
