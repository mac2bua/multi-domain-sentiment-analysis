import sys

def drange(start, end, step):
	r = start
	while (r < end):
		yield r
		r += step

if __name__ == '__main__':

	CLASSIFIER_NAME = sys.argv[1]

	f = open(CLASSIFIER_NAME + '_classifier_test.txt', 'r')
	
	lines = f.readlines()

	for threshold in drange(0.05, 1.0, 0.05):
		tp = fp = tn = fn = 0
		for l in lines:
			l = l.replace('\n','')
			fields = l.split('\t')
			actual_tag = fields[0].split('/')[-2]
			if fields[1] == 'positivo':
				scorePositivo = float(fields[2])
			else:
				scorePositivo = float(fields[4])

			if actual_tag == 'positivo':
				if scorePositivo > threshold:
					tp += 1
				else:
					fn += 1
			else:
				if scorePositivo > threshold:
					fp += 1
				else:
					tn += 1

		recall = float(tp)/float(tp+fn)
		fpr = float(fp)/float(fp+tn)

		print recall, fpr