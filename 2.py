import spacy
import numpy as np

nlp = spacy.load("en_core_web_md")

def find_similar_words(word):
    # get the vector representation of the input word
    word_vector = nlp.vocab[word].vector
    
    # find similar words based on cosine similarity
    similar_words = []
    for vocab_word in nlp.vocab:
        # skip words without vectors or stop words
        if not vocab_word.has_vector or vocab_word.is_stop:
            continue
        similarity = word_vector.dot(vocab_word.vector) / (np.linalg.norm(word_vector) * np.linalg.norm(vocab_word.vector))
        if similarity > 0.5:  # adjust this threshold to control how many similar words are returned
            similar_words.append(vocab_word.text)
    
    return similar_words

similar_words = find_similar_words("paracetamol")
print(similar_words)