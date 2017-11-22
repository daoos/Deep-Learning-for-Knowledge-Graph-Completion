import sklearn as sk 
import scipy as sci 
import numpy as np 
import pandas as pd
import pickle

# Load in the pickle files containing the word encodings and the entity map
words = pickle.load(open('word_vectors.pkl','rb'))
key = pickle.load(open('entities_map.pkl','rb'))

# Load in the files containing the positive and negative triplets of (entity,predicate,entity)
pos = np.loadtxt('positiveTriplets.txt',delimiter=' ',dtype=str)
neg = np.loadtxt('negativeTriplets.txt',delimiter=' ',dtype=str)


# Make a list of the entities for looping over all of them later
entities = np.unique(pos[:,0])
predicates = np.unique(pos[:,1])

# A few helper functions for the main data converting tool
def encode_word(word):
    """
        Encodes a word if found in the word 
        encoding dictionary; otherwise returns
        an empty array.
    """
    if word in words.keys():
        return(words[word])
    max_len = max([words[x].shape[0] for x in words])
    return(np.empty(max_len))

def encode_entity(entity):
    """
        Builds an entity encoding by computing
        the average of all the word encodings.
        Ignores any words that don't have an 
        encoding in the words_vectors.txt file.
    """
    all_words = np.array([encode_word(x) for x in key[entity].split(' ') if x in words.keys()])
    if all_words.shape[0]==0:
        return(np.array([np.NaN]*300,dtype=float).transpose())
    return(all_words.mean(axis=0))


 # The build_rows function builds the appropriate rows of numerical data for a given entity. 
 # This is done by considering all triplets with this entity as the first object. Then it 
 # encodes all entities in this subset, including itself, and concatenates each encoding. 
 # Finally it looks as the predicate for each entity-entity pair and assigns 1,0, or -1 
 # depending on if the predicate is true, unknown, or false for that entity-entity pair. 
 # The result is a small dataframe of all the rows of this form where the first entity 
 # is the argument.

def build_rows(entity):
    """
        Builds a dataframe out of the triplets
        containing entity as the first object.
    """
    encoding = encode_entity(entity)
    temp_pos = pos[pos[:,0]==entity,:]
    temp_neg = neg[neg[:,0]==entity,:]
    pairs = []
    rows = []
    for each_obj in np.unique(temp_pos[:,2]):
        try:
            obj_encode = encode_entity(each_obj)
            
            if all(obj_encode != np.NaN):
                # Get the positive & negative triplet's objects
                temp2_pos = temp_pos[temp_pos[:,2]==each_obj,:]
                temp2_neg = temp_neg[temp_neg[:,2]==each_obj,:]

                # Build outputs from which predicates are in triplets
                pos_preds = np.array([x in np.unique(temp2_pos[:,1]) for x in predicates],dtype=int)
                neg_preds = np.array([x in np.unique(temp2_neg[:,1]) for x in predicates],dtype=int)
                preds = pos_preds - neg_preds

                # Update the data
                row = np.concatenate([encoding,obj_encode,preds])
                rows.append(row)
                pairs.append([entity,each_obj])
            else:
                print('Entity ' + obj_encode + ' has no encoding!')
        except:
            print("didn't work for "+ str(entity) + ", " + str(each_obj))
            return(np.NaN)

 
    rows = np.array(rows)
    pairs = np.array(pairs)
    if rows.shape[0] == 0:
        return(np.NaN)
    df = pd.concat([pd.DataFrame(pairs),pd.DataFrame(rows)],ignore_index=True,axis=1)
    col_names = ['EntityA','EntityB']+['a'+str(x) for x in range(300)]+['b'+str(x) for x in range(300)]+['p'+str(x) for x in range(5)]
    df.columns = col_names
    return(df)

entity = pos[1,0]
test = build_rows(entity)


# Running build_rows on all the entities to generate the main dataset
all_rows = pd.DataFrame([])
for entity in entities:
    df = build_rows(entity)
    if all(df != np.NaN):
        all_rows = pd.concat([all_rows,df])
    else:
        print ('Entity: '+entity+ ' failed!')

# Save the data to a file
all_rows.to_csv('EncodedData.csv',index=False)
