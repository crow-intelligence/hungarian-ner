import pandas as pd
import pickle

patterns = []
loci = []

with open('data/loc/countries.txt', 'r', encoding='iso-8859-1') as f:
    countries = f.read().split('\n')

for country in countries:
    if country not in loci:
        if len(country.split()) == 1:
            if country not in ',;.!%=/?+()':
                pattern = {"label": "GPE",
                           "pattern": country}
        else:
            pattern_list = []
            for e in country.split():
                ed = {"lower": e.lower()}
                pattern_list.append(ed)
            pattern = {"label": "GPE",
                       "pattern": pattern_list}
        patterns.append(pattern)
        loci.append(country)

with open('data/loc/hun_towns.txt', 'r', encoding='iso-8859-1') as f:
    hun_cities = f.read().split('\n')

for city in hun_cities:
    if city not in loci:
        if len(city.split()) == 1:
            if city not in ',;.!%=/?+()':
                pattern = {"label": "GPE",
                           "pattern": city}
        else:
            pattern_list = []
            for e in city.split():
                ed = {"lower": e.lower()}
                pattern_list.append(ed)
            pattern = {"label": "GPE",
                       "pattern": pattern_list}
        patterns.append(pattern)
        loci.append(city)

with open('data/loc/world_cities_500k.txt', 'r', encoding='iso-8859-1') as f:
    world_cities = f.read().split('\n')

for city in world_cities:
    if city not in loci:
        if len(city.split()) == 1:
            if city not in ',;.!%=/?+()':
                pattern = {"label": "GPE",
                           "pattern": city}
        else:
            pattern_list = []
            for e in city.split():
                ed = {"lower": e.lower()}
                pattern_list.append(ed)
            pattern = {"label": "GPE",
                       "pattern": pattern_list}
        patterns.append(pattern)
        loci.append(city)

df = pd.read_csv('data/loc/hungarian_geonames.tsv',
                 sep='\t',
                 encoding='utf-8')

for index, row in df.iterrows():
    locality_type = row['Type']
    location = row['Location']
    if location not in loci:
        if not pd.isnull(location) and not pd.isnull(locality_type):
            if locality_type == 'country' or locality_type == 'village'\
                    or locality_type == 'region' or locality_type == 'city'\
                or locality_type == 'town' or locality_type == 'national_capital':
                if len(location.split()) == 1:
                    if location not in ',;.!%=/?+()':
                        pattern = {"label": "GPE",
                                   "pattern": location}
                else:
                    pattern_list = []
                    for e in location.split():
                        ed = {"lower": e.lower()}
                        pattern_list.append(ed)
                    pattern = {"label": "GPE",
                               "pattern": pattern_list}
                patterns.append(pattern)
                loci.append(location)
            else:
                if len(location.split()) == 1:
                    if location not in ',;.!%=/?+()':
                        pattern = {"label": "GPE",
                                   "pattern": location}
                else:
                    pattern_list = []
                    for e in location.split():
                        ed = {"lower": e.lower()}
                        pattern_list.append(ed)
                    pattern = {"label": "GPE",
                               "pattern": pattern_list}
                patterns.append(pattern)
                loci.append(location)

with open('data/interim/locations.p', 'wb') as of:
    pickle.dump(patterns, of)

with open('data/interim/loci.p', 'wb') as of:
    pickle.dump(loci, of)
