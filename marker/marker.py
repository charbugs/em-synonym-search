import requests
import spacy

nlp = spacy.load('de_core_news_sm')
vocab = nlp.vocab

def get_setup():
	return {
		'title': 'Synonyms Search',
		'description': "This marker highlights the search term and its synonyms. It works only for German texts.",
		'inputs': [{
			'id': 'word',
			'label': 'Search Term',
			'type': 'text'
		}],
		'supportedLanguages': 'German',
		'homepage': 'https://github.com/charbugs/em-synonym-search'
	}

def get_markup(markup_response):
	tokens = markup_response['tokens']
	word = markup_response['inputs']['word']

	if not word:
		return { 'error': 'You should give me a search term.'}

	lemmas = lemmatize(tokens);
	synonyms = get_synonyms(word)

	tokens_to_mark = []
	matching_types = set()

	for i, lemma in enumerate(lemmas):
		if lemma in synonyms:
			tokens_to_mark.append(i)
			matching_types.add(lemma)

	return { 
		'markup': [ { 'tokens': tokens_to_mark } ],
		'report': '<div><b>Found: </b>%s</div>' % 
			(', '.join(matching_types) if matching_types else 'nothing')
	}

def lemmatize(tokens):
	doc = spacy.tokens.Doc(vocab, tokens)
	return [t.lemma_ for t in doc]

def get_synonyms(word):
	synonyms = []
	data = requests.get(
		'https://www.openthesaurus.de/synonyme/search',
		params={ 'q': word, 'format': 'application/json' }
	).json()
	for synset in data['synsets']:
		for term in synset['terms']:
			synonyms.append(term['term'])
	return synonyms



