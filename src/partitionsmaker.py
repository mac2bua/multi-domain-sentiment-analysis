import random
import os
from os import listdir
from os.path import isfile, join

def makedir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)


def createCorpusFor(task, istrain, dataset):
	if istrain:
		t = 'trainset'
	else:
		t = 'testset'
	path = t + '/' + task
	makedir(path)
	for opinion_data in dataset:
		clase = opinion_data[task]
		makedir(path + '/' + clase)

		op_path = opinion_data['opinion']
		op = open(op_path, 'r')
		filename = op_path.split('/')[-1]
		f = open(path + '/' + clase + '/' + filename, 'w')
		for l in op.readlines():
			f.write(l)
		f.close()
		op.close()


if __name__ == '__main__':


	#leer las opiniones
	opiniones = {"Deportes" : {}, "Electro" : {}, "Juegos" : {}, "Peliculas" : {}, "Vehiculos" : {}, 
	"Hoteles" : {}, "Libros" : {}}

	for dominio in opiniones.keys():
		path = "/home/cristian/Escritorio/experimentos/mallet-2.0.7/data/corpus_original/" +  dominio + "Ciao/Negative"
		negativas = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
		path = "/home/cristian/Escritorio/experimentos/mallet-2.0.7/data/corpus_original/" +  dominio + "Ciao/Positive"
		positivas = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

		opiniones[dominio] = {'positivo' : positivas, 'negativo' : negativas}


	#crear una lista de elementos que contengan dominio, sentimiento y la opinion.
	listaOpiniones = []
	for dominio in opiniones.keys():
		for sentimiento in opiniones[dominio].keys():
			for opinion in opiniones[dominio][sentimiento]:
				listaOpiniones.append({'dominio': dominio, 'sentimiento': sentimiento, 'opinion': opinion})


	#seleccionar las opiniones de training y testing
	random.shuffle(listaOpiniones)
	n = len(listaOpiniones)
	splitIndex = int(n * 0.7)
	trainset = listaOpiniones[0:splitIndex] 
	testset = listaOpiniones[splitIndex:]

	#crear un corpus de entrenamiento que tenga solo positivo y negativo.

	createCorpusFor('sentimiento', True, trainset)

	#crear un corpus de entrenamiento con los dominios.
	
	createCorpusFor('dominio', True, trainset)

	#crear un corpus de entrenamiento por cada dominio.

	path = 'trainset/dominio_sentimiento'
	makedir(path)
	for opinion_data in trainset:
		dominio = opinion_data['dominio']
		sentimiento = opinion_data['sentimiento']
		makedir(path + '/' + dominio)

		op_path = opinion_data['opinion']
		op = open(op_path, 'r')
		filename = op_path.split('/')[-1]
		makedir(path + '/' + dominio + '/' + sentimiento)
		f = open(path + '/' + dominio + '/' + sentimiento + '/' + filename, 'w')
		for l in op.readlines():
			f.write(l)
		f.close()
		op.close()

	#crear un corpus de testing que solo tenga positivo y negativo

	createCorpusFor('sentimiento', False, testset)

	#crear un corpus de testing con los dominios.

	createCorpusFor('dominio', False, testset)

	#crear un corpus de testing por cada dominio

	path = 'testset/dominio_sentimiento'
	makedir(path)
	for opinion_data in testset:
		dominio = opinion_data['dominio']
		sentimiento = opinion_data['sentimiento']
		makedir(path + '/' + dominio)

		op_path = opinion_data['opinion']
		op = open(op_path, 'r')
		filename = op_path.split('/')[-1]
		makedir(path + '/' + dominio + '/' + sentimiento)
		f = open(path + '/' + dominio + '/' + sentimiento + '/' + filename, 'w')
		for l in op.readlines():
			f.write(l)
		f.close()
		op.close()
