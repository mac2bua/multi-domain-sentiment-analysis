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

		maxw = '0'
		for t in weightedTags.keys():
			#print "T:", t
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
	if actual_tag == 'positivo':
		if result_tag == 'positivo':
			metrics['tp'] += 1
		else:
			metrics['fn'] += 1
	elif actual_tag == 'negativo':
		if result_tag == 'negativo':
			metrics['tn'] += 1
		else:
			metrics['fp'] += 1
	else:
		print 'tag desconocido', actual_tag

def result_tag(results):
	if results[0].strip().lower() == 'negativo':
		negProp = results[1]
		posProp = results[3].replace('\n', '')
	else:
		posProp = results[1]
		negProp = results[3].replace('\n', '')

	if float(posProp) > float(negProp):
		#print 'res:', results, '\ntag: positive'
		return 'positivo'
	else:
		#print 'res:', results, '\ntag: negative'
		return 'negativo'

def resultsFrom(fileName, paths):
	out_f = open(fileName, 'r')
	metrics = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
	for l in out_f.readlines():
		split_l = l.split(column_separator)
		path = split_l[0].replace('file:','')
		if path.split('/')[-1] in paths:
			print l.replace('\n','')
			actual_tag = tag(path).lower()
			if 'positivo' == actual_tag or 'negativo' == actual_tag:	
				update(metrics, actual_tag, result_tag(split_l[1:]).lower())
			else:
				print 'Unkown tag [', actual_tag, ']' 
	return metrics		

	 	

if __name__ == '__main__':
	
	#nombre del clasificador por topicos: 5top.me, 5top.nb, 10top.me, etc.
	classifier_name = sys.argv[1]

	#que tipo de clasificadores usar para sentiment: me => maxent, nb => bayes
	ctype = sys.argv[2]

	#4 => 5Topics, 5 => 10Topics, 6 => 15Topics
	tsNumber = sys.argv[3]

	output_name = classifier_name + '_classifier_test.txt'

	column_separator = '\t'

	out_f = open(output_name, 'r')


	metrics = perform_calculations(out_f)

	tp = 0
	tn = 0
	fp = 0
	fn = 0

	for domain in metrics.keys():
		name = domain.lower()
		classifier_data = resultsFrom("ts" + str(tsNumber) + "." + name[-1] + ctype + "_classifier_test.txt", metrics[domain])
		partial_tp = classifier_data['tp']
		partial_tn = classifier_data['tn']
		partial_fp = classifier_data['fp']
		partial_fn = classifier_data['fn']
		tp += partial_tp
		tn += partial_tn
		fp += partial_fp
		fn += partial_fn
		if (partial_tp+partial_tn+partial_fp+partial_fn != 0):
			partial_acc = float(partial_tp+partial_tn)/float(partial_tp+partial_tn+partial_fp+partial_fn)
		else:
			partial_acc = 0.0
		if (partial_tp+partial_fp != 0):		
			partial_prec = float(partial_tp)/float(partial_tp+partial_fp)
		else:
			partial_prec = 0.0
		if (partial_tp+partial_fn != 0):		
			partial_rec = float(partial_tp)/float(partial_tp+partial_fn)
		else:		
			partial_rec = 0.0		
		#print domain, classifier_data, partial_prec, partial_rec, partial_acc 


	accuracy = float(tp+tn)/float(tp+tn+fp+fn)
	precision = float(tp)/float(tp+fp)
	recall = float(tp)/float(tp+fn)
	f1 = (2*precision*recall)/(precision+recall)

	#print classifier_name + '-' + ctype +'\t' + str(precision) +'\t' + str(recall) + '\t' + str(f1) + '\t' + str(accuracy)
	
