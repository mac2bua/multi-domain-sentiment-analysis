
# class Corpus:

# 	def __init__(self, contents):
# 		self._contents = contents

# 	#def __init__(self, path):
# 	#	self._contents = contentsFrom(path)

# 	def contents(self):
# 		return self._contents

# 	#def contentsFrom(path):
		

# 	def split(self, training_portion):
# 		contents = self.contents()
# 		x = int(len(contents) * training_portion)
# 		trainset = Corpus(contents[0:x])
# 		testset = Corpus(contents[x:])
# 		return trainset, testset



# if __name__ == "__main__":

# 	contents = [("hola pedazo de boludo", "negative"), ("me encanta", "positive"),
# 		("esto es ser neutro", "neutral"), ("los odio", "negative"), ("es genial", "positive"), 
# 		("me da igual", "neutral"), ("una mierda", "negative"), ("y.. que te puedo decir?", "negative"),
# 		("los amo, son lo mas", "positive")]

# 	corpus = Corpus(contents)

# 	trainset, testset = corpus.split(0.7)

# 	print "Train:"
# 	for c in trainset.contents():
# 		print c

# 	print "\nTest:"
# 	for c in testset.contents():
# 		print c


import sys

def tag(path):
	return path.split('/')[-2].strip()

def result_tag(results):
	if results[0].strip().lower() == 'negative':
		negProp = results[1]
		posProp = results[3].replace('\n', '')
	else:
		posProp = results[1]
		negProp = results[3].replace('\n', '')

	if float(posProp) > float(negProp):
		#print 'res:', results, '\ntag: positive'
		return 'positive'
	else:
		#print 'res:', results, '\ntag: negative'
		return 'negative'

def update(metrics, actual_tag, result_tag):
	if actual_tag == 'positive':
		if result_tag == 'positive':
			metrics['tp'] += 1
		else:
			metrics['fn'] += 1
	elif actual_tag == 'negative':
		if result_tag == 'negative':
			metrics['tn'] += 1
		else:
			metrics['fp'] += 1
	else:
		print 'tag desconocido', actual_tag

def get_classifications(out_f, classifier, classifications_map):
	for l in out_f.readlines():
		split_l = l.split(column_separator)
		path = split_l[0].replace('file:','')
		actual_tag = tag(path).lower()
		if 'positive' == actual_tag or 'negative' == actual_tag:
			if (classifications_map.has_key(path)):
				classifications_map[path] = classifications_map[path].append((classifier, result_tag(split_l[1:]).lower(), actual_tag))
	return classifications_map

def get_files(out_f, files):
	for l in out_f.readlines():
		split_l = l.split(column_separator)
		path = split_l[0].replace('file:','')
		actual_tag = tag(path).lower()

		if 'positive' == actual_tag or 'negative' == actual_tag:	
			files.add(path)
		else:
			print 'Unkown tag [', actual_tag, ']' 
	return files


if __name__ == "__main__":

	classifiers = ['topic0', 'topic1', 'topic2', 'topic3', 'topic4', 'topic5', 'topic6',
				'topic7', 'topic8', 'topic9']


	column_separator = '\t'

	files = set([])

	for c in classifiers:
		out_f = open(c + '_classifier_test.txt', 'r')			
		files = get_files(out_f, files)

	print len(files)

	classifications_map = {} 
	for f in files:
		classifications_map[f] = []

	print len(classifications_map.keys())

	for c in classifiers:
		out_f = open(c + '_classifier_test.txt', 'r')
		classifications_map[c] = get_classifications(out_f, c, classifications_map)

	for path in classifications_map.keys():
		print "path:", path
		for res in classifications_map[path]:
			print res



