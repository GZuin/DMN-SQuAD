import sys
import nltk
import os
import relxt as rt

whlist = ['What','what','When','when','Where','where','Which','whose','Whose','Whom','whom','which',
	  'How','how']##TODO: add how variants (how much, how long, etc)
	

#Tokenize sample text into sentences
def splittext(input_text):
	return nltk.sent_tokenize(input_text)


#Remove stopwords, leaving only meaningful words and add metadata to the query sentence
def cleartext(stopwords, input_line, isquery=0):
	# Add spaces between non aplhanumeric characters
	line=''	
	for w in input_line:
		if w.isalnum() or w=='\'':
			line+=w
		else:
			line+=' '+w+' '	
	
	if isquery:	
		queryentities = rt.extractSampleRels(line)
	line = line.split()		
	if isquestion: # findout which WH-word is being used, if any
		questionword=''		
		for word in line:
			if word in whlist:
				questionword=word	
	
	line = [x for x in line if x not in stopwords] #remove stopwords from sentence, leaving only menaingful words
	outline = ""		
	
	for word in line:
		outline+=word+' ' 
	
	if not isquery:
		return outline
	return (outline[0:-2],queryentities,questionword) #remove the '?' character

#Return the number of matches between the corpus and the query
def corpusmatches(corpus,query):
	matchesvet=[]	
	for s in range(0,len(corpus)):
		matchesvet.append(0)
		#print s
		for word_q in query.split():
			for word_s in corpus[s].split():
				if word_q==word_s:
					matchesvet[s]+=1
					break
	return matchesvet

#Return the passages wich have common keywords with the query 
def retrievesent(cmatches,corpus_ns,corpus_org,querysize): 
	minindex = querysize/2;
	candidates=[]	
	#select only pertinent sentences	
	for i in range(1,len(cmatches)):
		if cmatches[i]>=minindex:
			candidates.append((rt.extractSampleRels(corpus_org[i]),cmatches[i]))
	#sort for number of matches
	for i in range(0,len(candidates)-1):	
		for j in range(0,len(candidates)-i-1):
			if candidates[j+1][1] > candidates[j][1]:
				auxcandidate = candidates[j]
				candidates[j] = candidates[j+1]
				candidates[j+1] = auxcandidate

	return candidates

#Return the entities that have a relation with the ones in the query
def getawnsers(passages, query, queryEntities):
	awnsers=[]	
	for p in passages:
		for entities in p[0]:
			obj = entities[0]
			sbj = entities[2]
			if (obj in queryEntities) and (sbj not in queryEntities):
				if (sbj,obj) not in awnsers:
					awnsers.append((sbj,obj))
			if (sbj in queryEntities) and (obj not in queryEntities):
				if (obj,sbj) not in awnsers:
					awnsers.append((obj,sbj))
	return awnsers


if __name__ == '__main__':
	stopwords = open(sys.argv[2],'r').read()
	corpustext = open(sys.argv[1],'r').read()
	questiontext = str(open(sys.argv[3],'r').read())
	questiontext=questiontext[0].lower()+questiontext[1:]
	
	corpusvet = splittext(corpustext)
	corpusvet_nostop = []	
	for ci in corpusvet:
		corpusvet_nostop.append(cleartext(stopwords,ci))
	question = cleartext(stopwords,questiontext,1)
	
	cm = corpusmatches(corpusvet_nostop,question[0])
	
	candpassages = retrievesent(cm,corpusvet_nostop,corpusvet,len(str(question[0]).split())) 
	awnsers = getawnsers(candpassages,question,rt.extractEntities(questiontext))
	print awnsers
