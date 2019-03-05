import sys, gensim
import numpy as np
import re

# load pretrained word vector
models = [gensim.models.KeyedVectors.load_word2vec_format(arg, binary=arg.endswith(".bin")) for arg in sys.argv[1:]]
# str.endswith(suffix) : detect whether str end with suffix, if yes return ture
# sys.argv[1:]:there maybe several word2vec pretrained texts

def default_get(x, d):
    try:
        return d[x]
        #for example : model['love'] = wordvec of 'love'
    except KeyError:
        #KeyError : x doen't exist in the dict d
        return []

def get_mean(words, models):
    all_vectors = [default_get(word, model) for word, model in zip(words, models) if default_get(word, model) is not None]
    return [np.mean(x) for x in zip(*all_vectors)]

def zip_rep(words, vector):
    rep_vector = [vector for i in range(0, len(words))]
    #repeat vector
    return zip(words, rep_vector)

for i, line in enumerate(sys.stdin):
    #sys.stdin : input dictionary
    words = line.strip().split(" ")
    #line.strip() : delete " " at both sides of line
    if len(words) != len(models):
        sys.stderr.write("Number of models and words not matching at line " + str(i) + "! " + str(len(words)) + " " + str(len(models)) + "\n")
        continue
    s = [" ".join([word] + [str(x) for x in vector]) for word, vector in zip_rep(words, get_mean(words, models))]
    # s = ['word wordvector', 'word wordvector']
    lengths = [x.strip().split() for x in s]
    lengths_condition = [len(x) > 3 for x in lengths]
    # if source and target word both have counterpart wordvector
    if all(lengths_condition):
        print("\t".join(s))
    #output the line word \t wordvector \t word \t wordvector
