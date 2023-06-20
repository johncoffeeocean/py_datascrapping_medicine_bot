from PyDictionary import PyDictionary

dictionary=PyDictionary()

input_word = "aspirin"
synonyms = dictionary.synonym(input_word)

print(f"Synonyms of {input_word}:")
for synonym in synonyms:
    print(synonym)