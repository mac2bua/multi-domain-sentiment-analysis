import sys

def tag(path):
	return path.split('/')[-2].strip()

def wtags(vector):
	weightedTags = {}
	for i in xrange(0, (len(vector)/2)):
		weightedTags[vector[2*i]] = float(vector[(2*i)+1].replace('\n', ''))
	return weightedTags

def perform_calculations(out_f):
	metrics = {}
	for l in out_f.readlines():
		split_l = l.split(column_separator)
		path = split_l[0].replace('file:','')
		actual_tag = tag(path).lower()
		weightedTags = wtags(split_l[1:])

		maxw = 'DeportesCiao'
		for t in weightedTags.keys():
			if weightedTags[t] > weightedTags[maxw]:
				maxw = t

		if not metrics.has_key(maxw):
			metrics[maxw] = []		
		
		metrics[maxw].append(path.split('/')[-1])

	return metrics		

def show_results(metrics):
	tp = metrics['tp']
	fp = metrics['fp']
	tn = metrics['tn']
	fn = metrics['fn']
	print 'Confusion Matrix'
	print ''
	print '\t --------------------------------'
	print '\t | Prediccion \t\t\t|'
	print '-----------------------------------------'
	print '|Real    | Positive\t|Negative\t|'
	print '-----------------------------------------'
	print '|Positive|', tp, '\t\t|', fn, '\t\t|'
	print '|Negative|', fp, '\t\t|', tn, '\t\t|'
	print '-----------------------------------------'
	print ''
	precision = float(tp)/float(tp+fp)
	recall =  float(tp)/float(tp+fn)
	f1 = (2.0*precision*recall)/(precision+recall)
	print 'Precision', precision   
	print 'Recall', recall
	print 'F1', f1
	print 'Accuracy', float(tp+tn)/float(tp+tn+fp+fn)

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

def resultsFrom(fileName, paths):
	out_f = open(fileName, 'r')
	metrics = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
	for l in out_f.readlines():
		split_l = l.split(column_separator)
		path = split_l[0].replace('file:','')
		if path.split('/')[-1] in paths:
			actual_tag = tag(path).lower()
			if 'positive' == actual_tag or 'negative' == actual_tag:	
				update(metrics, actual_tag, result_tag(split_l[1:]).lower())
			else:
				print 'Unkown tag [', actual_tag, ']' 
	return metrics		

	 	

if __name__ == '__main__':
	
	classifier_name = sys.argv[1]

	output_name = classifier_name + '_classifier_test.txt'

	column_separator = '\t'

	out_f = open(output_name, 'r')

	metrics = perform_calculations(out_f)

	tp = 0
	tn = 0
	fp = 0
	fn = 0

	for domain in metrics.keys():
		name = domain.replace('Ciao','').lower()
		classifier_data = resultsFrom(name + "_classifier_test.txt", metrics[domain])
		tp += classifier_data['tp']
		tn += classifier_data['tn']
		fp += classifier_data['fp']
		fn += classifier_data['fn']
		print domain, classifier_data, float(tp+tn)/float(tp+tn+fp+fn), float(tp)/float(tp+fp), float(tp)/float(tp+fn)

	print 'tp:', tp, 'tn:', tn, 'fp:', fp, 'fn:', fn

	print 'accuracy:', float(tp+tn)/float(tp+tn+fp+fn)

	print 'precision:', float(tp)/float(tp+fp)

	print 'recall:', float(tp)/float(tp+fn)