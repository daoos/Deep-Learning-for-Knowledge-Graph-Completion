# Deep-Learning-for-Knowledge-Graph-Completion

For this project, we took Deep Learning approaches to knowledge graph completion. Rather than using one of the standard knoweldge bases that many literary articles reference, we decided to apply our models on a subset of the Wikidata knowledge base. We built two models with differing architectures : the neural tensor network (NTN) and the multi layered perceptron (MLP). 

The NTN model builds word embeddings, and associated entity embeddings, during the training of the hidden layer weights. Below shows an example of the embeddings updating after each iteration. ![t-SNE of embeddings after each iteration](https://github.com/nickjoodi/Deep-Learning-for-Knowledge-Graph-Completion/raw/master/ntn/tsne.gif)
In this image we see how each of the embeddings is adjusted after each iteration. The *(x,y)* coordinates of each point is a reduction from the 300 dimensional embeddings to 2 dimensions following [t-SNE](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding) reduction scheme. The color of each embedding is the result of using k-means clustering on the final iteration; thus the .gif shows the convergence into these clusters. Trajectories for selected samples are also shown and illustrate the past 2 iterations for these entities. 


Below is a list of the contents of the repository. Please update when you commit.

###  data/ ~ Contains all the data we've built for this project. 
		EncodedData.csv:		The Main data, already encoded with entity embeddings, and 
						associated outputs. Of the form 
						[EntityA|EntityB|a0,a1,...,a299|b0,b1,...,b299|p0,p1,p2,p3,p4]
						where EntityA/B are the names of the entities, ai/bi are the 
						embeddings for these entities, and pi is the predicate for this
						entity-entity pair. Predicates follow {1: True, 0: Unknown, -1: False}.
		Build_Data.py:	  		The Python script used to generate EncodedData.csv
		Build_Data.ipynb: 		A Jupyter Notebook for the Build_Data.py script

###		data/raw/ ~ A directory containing the raw exported knowledge graph
		SparqlQuery.txt:		The query used to pull the data from WikiData
		wikiData.txt:			The result of the above query on WikiData
		wikiData.csv:			Same as wikiData.txt but in .csv format
		wikiData.py:			A python script used to generate much of processed/
		wikiData_Large.txt              A more realistic size data set to train the models. 10 times more
						data being pulled

### 	data/embeddings/ ~ A directory of word/entity embeddings and their scripts
		entity_embeddings.pkl:  	A dictionary of entity embeddings
		word_vectors.pkl:		A dictionary of word embeddings
		word_embeddings.py:		Script for generating word_vectors.pkl
		bad_entities.py:		A list of entities with no encoding 
		large_set/:                     A folder containing a more realistic size data set to train the models. 10 times more
						data being pulled

###		data/processed/ ~ A directory of processed versions of the data in raw/
		entities_map.pkl:		A dictionary that maps entity labels to their full names
		entities.txt:			A list of all the entities' full names
		positiveTriplets: 		The list of true statements for entity-entity pairs
		negativeTriplets:		A list of some false statements for entity-entity pairs
		predicates.txt: 		A list of the 5 predicates used for this project
		unique.txt: 			A list of the unique elements of vocab.txt
		vocab.txt: 			All words used throughout the entities.txt file
		large_set/:                     A folder containing a more realistic size data set to train the models. 10 times more
						data being pulled

### 	TeX/ ~ A directory containing the TeX for our report
		Project.TeX:  			The main TeX document. I have a standard pre-amble I've been building 
						over the years, so please excuse how huge it is. I have to say that a lot
		bib.bib:			The bibliography file. There are some examples already written if you need

### 	MLP/ ~ A directory containing the code for the MLP model
		MLP.ipynb:  			A Jupyter Notebook for building the MLP model (not functional yet)
		RunMLP.r:				Running MLP on R using RSNNS package
		MLP.rda:				The stored data (like .pkl) for runMLP. Not needed to use the script	

### 	ntn/ ~ A directory containing the code for the ntn model
		ntn.py:  			        A tensor flow 1.3 implementation of the neural tensor network over a 
							subset of the wikidata knowledge graph
		img/:				        Evaluation metrics of the ntn model - ROC curve, Max - Margin Loss with respect to
							the iteration, TSNE plots of the word vectors before and after training the model

### 	img/ ~ A directory containing a TSNE plot for the word embeddings pulled from a pretrained model using fastext
		We decided to use both random initialization and pretrained word embeddings due to a decent sized portion of words 
		contained in the entities missing from the model. Additionally, some entities in the Wikidata knowledge graph had no words 
		associated to them, just identifiers

