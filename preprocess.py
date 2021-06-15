from num2words import num2words
import spacy

nlp = spacy.load("en_core_web_md")

#preprocessing
def num_to_words(text):
	"""
	Return :- text which have all numbers or integers in the form of words
	Input :- string
	Output :- string
	"""
	# separer le texte en mots
	after_spliting = text.split()

	for index in range(len(after_spliting)):
		if after_spliting[index].isdigit():
			after_spliting[index] = num2words(after_spliting[index])

    # jogner la liste en une chaine de caracteres avec l'espace comme separateur
	numbers_to_words = ' '.join(after_spliting)
	return numbers_to_words

def wordvec(str):
    str = num_to_words(str)
    doc = nlp(str.lower())
    vec = doc.vector

    return vec