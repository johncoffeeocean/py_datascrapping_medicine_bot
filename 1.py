
import spacy
from spacy.matcher import Matcher

# Load the pre-trained model
nlp = spacy.load("en_core_web_sm")

# Define the pattern for matching drug names
drug_pattern = [{"LOWER": {"IN": ["aspirin", "ibuprofen", "acetaminophen"]}}]

# Initialize the matcher with the drug pattern
matcher = Matcher(nlp.vocab)
matcher.add("DRUG",  [drug_pattern])

# Process the medical text data
doc = nlp("The patient was prescribed aspirin and ibuprofen for pain relief.")

# Use the matcher to find all drug matches in the text
matches = matcher(doc)

# Print the matched drug names
for match_id, start, end in matches:
    drug_name = doc[start:end].text
    print(drug_name)