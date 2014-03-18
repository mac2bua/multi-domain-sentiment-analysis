import os
import sys.argv

def makedir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)	


if __name__ == '__main__':


	numclusters = argv[1]

	files_data = open('doctopics.txt', 'r')

	#Lectura del archivo que devuelve mallet al clusterizar

	topics = {}
	for l in files_data.readlines()[1:]:
		fields = l.split()
		file_id = fields[0]
		file_name = fields[1].replace('file:','')
		topic_num = fields[2]
		topic_proportion = fields[3].replace('\n','')
		if not topics.has_key(topic_num):
			topics[topic_num] = []
		f = open(file_name, 'r')
		topics[topic_num].append((file_name, f.readlines(),topic_proportion))
		f.close()

	files_data.close()	
		

	#Creo los clusters en base a la informacion del archivo leido	

	path = '/home/cristian/Clusters/'
	makedir(path)

	num_topics = len(topics.keys())

	path_topics = path + 'Prueba_' + str(num_topics) + '_Topics/'
	makedir(path_topics)	

	for topic_num in topics.keys():
		path_actual_topic = path_topics + 'Topic-' + str(topic_num) +'/'
		makedir(path_actual_topic)
		for file_data in topics[topic_num]:
			file_path = file_data[0]
			file_tag = file_path.split('/')[-2]
			file_name = file_path.split('/')[-1]
			#print 'Tag:', file_tag, 'Name:', file_name
			path_actual_tag = path_actual_topic + file_tag + '/'
			makedir(path_actual_tag)
			of = open(path_actual_tag + file_name , 'w')
			of.writelines(file_data[1].encode('utf-8'))
			of.close()