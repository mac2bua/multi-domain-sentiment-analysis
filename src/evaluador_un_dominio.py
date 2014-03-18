import sys
from os import listdir
from os.path import isfile, join
	
def tag(path):
	return path.split('/')[-2].strip()

def result_tag(results):
	if results[0].strip().lower() == 'negativo':
		negProp = results[1]
		posProp = results[3].replace('\n', '')
	else:
		posProp = results[1]
		negProp = results[3].replace('\n', '')

	if float(posProp) > float(negProp):
		#print 'res:', results, '\ntag: positivo'
		return 'positivo'
	else:
		#print 'res:', results, '\ntag: negativo'
		return 'negativo'

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

def perform_calculations(out_f):
	metrics = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
	for l in out_f.readlines():
		split_l = l.split(column_separator)
		path = split_l[0].replace('file:','')
		actual_tag = tag(path).lower()
		if 'positivo' == actual_tag or 'negativo' == actual_tag:	
			update(metrics, actual_tag, result_tag(split_l[1:]).lower())
		else:
			print 'Unkown tag [', actual_tag, ']' 
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

def show_clean(name, metrics):
	tp = metrics['tp']
	fp = metrics['fp']
	tn = metrics['tn']
	fn = metrics['fn']
	precision = float(tp)/float(tp+fp)
	recall =  float(tp)/float(tp+fn)
	f1 = (2.0*precision*recall)/(precision+recall)
	accuracy = float(tp+tn)/float(tp+tn+fp+fn)
	print name + '\t' + str(precision) +'\t' + str(recall) + '\t' + str(f1) + '\t' + str(accuracy)



if __name__ == '__main__':

	path = '/home/cristian/Escritorio/experimentos/mallet-2.0.7/results/src/mismo_dominio/'
	
	file_names = [f for f in listdir(path) if isfile(join(path, f))]

	#classifier_name = sys.argv[1]
	for file_name in file_names:

		#print file_name
		
		column_separator = '\t'

		out_f = open('mismo_dominio/' + file_name, 'r')
		
		metrics = perform_calculations(out_f)

		classifier_name = file_name.replace('_classifier_test.txt', '')

		show_clean(classifier_name, metrics)

