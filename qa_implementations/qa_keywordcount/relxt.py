import nltk
from nltk.sem import relextract
from nltk.tree import Tree

#
def extractSampleRels(sample):
	#with open('toyset', 'r') as f:
	#    sample = f.read().decode('utf-8')

	sentences = nltk.sent_tokenize(sample)
	tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

	entitiesMap = []

	for i, sent in enumerate(tagged_sentences):
		sent = nltk.ne_chunk(sent) # ne_chunk method expects one tagged sentence
		pairs = relextract.tree2semi_rel(sent)
		reldicts = relextract.semi_rel2reldict(pairs)
		for r in reldicts:
			entitiesMap.append((r['subjtext'],r['filler'],r['objtext']))

	return entitiesMap	



def extractEntities(sample):
	sentences = nltk.sent_tokenize(sample)
	#sentences = sample	
	tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	
	for sent in tagged_sentences:
		chunked=nltk.ne_chunk(sent,binary=True)

		prev = None
		continuous_chunk = []
		current_chunk = []
		for i in chunked:
			if type(i) == Tree:			
				continuous_chunk.append(" ".join([str(token)+'/'+str(pos) for token, pos in i.leaves()]))				
				#continuous_chunk.append(str(i.leaves()))
			else:
				continue
		return continuous_chunk


'''elif current_chunk:

				named_entity = " ".join(current_chunk)
				if named_entity not in continuous_chunk:
					continuous_chunk.append(named_entity)
					current_chunk = []'''
