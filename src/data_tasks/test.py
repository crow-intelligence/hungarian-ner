doc_toks = ["Az","OTP", "Bank", "NYRT.", "és", "Valamilyen", "Kft."]
sentences = ["Az","OTP", "Bank", "NYRT",  ".", "és", "Valamilyen", "Kft", "."]
iobs = ['O', 'ORG', 'ORG', 'ORG', 'O', 'O', 'ORG', 'ORG', 'O']
new_tags = []

j = 0
k = 0
while j < len(sentences):
    if sentences[j] == doc_toks[k]:
        new_tags.append(iobs[j])
        j += 1
        k += 1
    else:
        new_tags.append(iobs[j])
        k += 1
        j += 2

for i in range(len(doc_toks)):
    print(doc_toks[i], new_tags[i])

