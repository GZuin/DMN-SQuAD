import json
import sys
import os
import nltk


def babify(dataset):
	subject = dataset[0]#['title']
	for sub in range(0,len(dataset)):
		subject=dataset[sub]
		for p in range(0,len(subject['paragraphs'])):
			paragraph = subject['paragraphs'][p]

			sentences = nltk.sent_tokenize(paragraph['context'])
			#print l
			#vet = nltk.sent_tokenize(l)
			paragraph['context']=sentences


			for q in range(0,len(paragraph['qas'])):
				for i in range(0,len(paragraph['qas'][q]['answers'])):
					qstart = paragraph['qas'][q]['answers'][i]['answer_start']
					basecounter=0
					for s in range(0,len(sentences)):
						if qstart >= basecounter and qstart<(basecounter+len(sentences[s])):
							paragraph['qas'][q]['answers'][i]['answer_start']=s+1
							break
						basecounter+=len(sentences[s])

			subject['paragraphs'][p]=paragraph
		dataset[sub]=subject
	#print dataset[0]['paragraphs'][0]['context']

def printdataset(dataset, output,mode='-l'):
	subject = dataset[0]#['title']
	globalcounter=0
	for sub in range(0,len(dataset)):
		subject=dataset[sub]
		for p in range(0,len(subject['paragraphs'])):
			paragraph = subject['paragraphs'][p]

			sentences = paragraph['context']
			counter=1			
			for s in sentences:
				#print s				
				output.write(str(globalcounter+counter)+' ')
				for char in s:	
					output.write(char.encode('utf8'))
				output.write('\n')
				counter+=1

			for q in range(0,len(paragraph['qas'])):
				output.write(str(globalcounter+counter)+' ')
				for char in paragraph['qas'][q]['question']:
					output.write(char.encode('utf8'))
				output.write('\t')
				for char in paragraph['qas'][q]['answers'][0]['text']:
					output.write(char.encode('utf8'))
				output.write(' \t'+str(paragraph['qas'][q]['answers'][0]['answer_start']+globalcounter)+'\n')
				counter+=1
			if mode=='-g':
				globalcounter+=counter
	output.close()


def printdataset_firsttext(dataset, output,mode='-g'):
	subject = dataset[0]#['title']
	globalcounter=0
	for sub in range(0,len(dataset)):
		subject=dataset[sub]
		for p in range(0,len(subject['paragraphs'])):
			paragraph = subject['paragraphs'][p]

			sentences = paragraph['context']
			counter=1			
			for s in sentences:
				#print s				
				output.write(str(globalcounter+counter)+' ')
				for char in s:	
					output.write(char.encode('utf8'))
				output.write('\n')
				counter+=1

			for q in range(0,len(paragraph['qas'])):
				paragraph['qas'][q]['answers'][0]['answer_start']+=globalcounter
			globalcounter+=counter

	for sub in range(0,len(dataset)):
		subject=dataset[sub]
		for p in range(0,len(subject['paragraphs'])):
			paragraph = subject['paragraphs'][p]
			counter=1			
			for q in range(0,len(paragraph['qas'])):
				output.write(str(globalcounter+counter)+' ')
				for char in paragraph['qas'][q]['question']:
					output.write(char.encode('utf8'))
				output.write('\t')
				for char in paragraph['qas'][q]['answers'][0]['text']:
					output.write(char.encode('utf8'))
				output.write(' \t'+str(paragraph['qas'][q]['answers'][0]['answer_start'])+'\n')
				counter+=1
			globalcounter+=counter

	output.close()



if __name__=="__main__":
	dataset_name = sys.argv[1]
	dataset = json.load(open(dataset_name))['data']
	babify(dataset)
	mode = sys.argv[2]
	if mode=='-g':
		printdataset_firsttext(dataset,open(dataset_name+'_long.babi.txt','w'),mode)
	else:
		printdataset(dataset,open(dataset_name+'.babi.txt','w'),mode)


