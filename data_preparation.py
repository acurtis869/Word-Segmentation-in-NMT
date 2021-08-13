# Import required packages
import random
import re
import string
import scipy.stats as ss
import numpy as np

## Define all the functions that are used to process the data

# Create function to load documents
# INPUT: directory of corpus
# OUTPUT: string containing the corpus
def load_doc(filename):
  # open the file as read only
  file = open(filename, mode=’rt’, encoding=’utf-8’)
  # read all text
  text = file.read()
  # close the file
  file.close()
  return text

# Then a function to split corpora into sentences
# INPUT: corpus in the form of a string
# OUTPUT: list of sentences (as strings)
def to_sentences(doc):
  return doc.strip().split(’\n’)

# Create function to clean data
# INPUT: list of raw sentences
# OUTPUT: list of cleaned sentences
def clean_lines(lines):
  # Create empty list to store cleaned lines
  cleaned = list()
  # Prepare regex for character filtering
  re_print = re.compile(’[^%s]’ % re.escape(string.printable))
  # Create translation table for removing punctuation unnecessary for grammar 
  table = str.maketrans(" ", " ", ’"#$%&\()*+./:;?!,.<=>@[\\]^_‘{|}~’)
  for line in lines:
    # Add spaces between necessary punctuation
    line = re.sub("-", " - ", line) 
    line = re.sub("’", " ’ ", line) 
    line = re.sub(" ", " ’ ", line) 
    # Tokenise on white space
    line = line.split()
    # Remove remaining punctuation from each token
    line = [word.translate(table) for word in line]
    # Convert words to lower case
    line = [word.lower() for word in line]
    # Store as string
    cleaned.append(’ ’.join(line))
  return cleaned

# Create a function to split data into training, validation and test sets
# INPUTS: English corpus (in list form); Foreign corpus (in list form); n_train
#    -- number of sentences in training corpus; n_val -- number of sentences in
#    validation corpus; n_test -- number of sentences in test corpus; seed --
#    random seed for reproducibility
# OUPUTS: English and foreign training, validation and test corpora (all in list
#    form)
def split_train_val_test(english, foreign, n_train, n_val, n_test, seed = 42):
  # First check both corpora have same amount of sentences
  if len(english) == len(foreign):
    n = len(english)
  else:
    sys.exit("Corpora not of same length")
  # Check required number of sentences does not exceed number available
  if (n_train + n_val + n_test > n):
    sys.exit("Number of sentences requested exceeds number available")
  # Set seed for reproducibility
  random.seed(seed)
  # Create random index
  index = random.sample(range(n), n)
  # Create empty lists to store new corpora
  english_train = []
  foreign_train = []
  # Add new sentences to corpora
  for i in range(n_train):
    english_train.append(english[index[i]])
    foreign_train.append(foreign[index[i]])
  # Repeat process above
  english_val = []
  foreign_val = []
  for i in range(n_train, n_train + n_val):
    english_val.append(english[index[i]])
    foreign_val.append(foreign[index[i]])
  # Repeat again
  english_test = []
  foreign_test = []
  for i in range(n_train + n_val, n_train + n_val + n_test):
    english_test.append(english[index[i]])
    foreign_test.append(foreign[index[i]])
  return english_train, foreign_train, english_val,
        foreign_val, english_test, foreign_test
                        
# Create a function to save sentences          
# INPUTS: corpus in list form; directory of where to save corpus
def save_sentences(sentences, filename):
  # Create a file to write into
  f = open(filename, "w")
  # Write in sentences
  for sent in sentences:
    f.write(sent + "\n")
  f.close()
                        
## Define the functions that are used to analyse the corpora
                        
# Create function that creates vector of unique vocabulary                       
# INPUT: corpus in list form
# OUTPUT: list of all unique words in corpus
def create_vocab(text):
  # Create empty list to store vocabulary
  vocab = []
  # Search for words and add to list if they are not already in it
  for line in text:
    line = line.split()
    for word in line:
     if word not in vocab:
       vocab.append(word)
  return vocab
                        
# Create function to calculate frequencies and ranks
# INPUTS: list of unique words in corpus; corpus in text form
# OUTPUTS: list of frequencies of each word and their respective ranks (1 being
#    the most frequent)
def zipf(vocab, text):
  n = len(vocab)
  # Create n-dim list to store frequencies
  freq = [0] * n
  # Find occurences of each word and add to respective frequency
  for line in text:
    line = line.split()
    for word in line:
      freq[vocab.index(word)] += 1
  # Calculate ranks
  rank = ss.rankdata(freq)
  # Adjust rank to correct format
  for i in range(n):
    rank[i] = len(rank) - rank[i] + 1
  return freq, rank
                        
# Create function to return the length of a vocabulary in a training set and the
#    frequency of the pth percentile word
# INPUTS: corpus in list form, percentile to output the frequency of
# OUTPUTS: size -- the number of unique words in the vocabulary; F_p -- the
#    frequency of the pth percentile word
def corpus_details(corpus, p = 0.5):
  vocab = create_vocab(corpus)
  frequency, rank = zipf(vocab, corpus)
  size = len(vocab)
  # Find where pth percentile value is
  index = np.where(rank == np.percentile(rank, p*100))[0][0]
  # Find frequency at that index
  F_p = frequency[index]
  print("Size of the vocab is: " + str(size))
  print("F_" + str(p) + " is: " + str(F_p))
  return size, F_p
                        
## Obtain datasets
                        
# Load in datasets:
# English
eng = load_doc('europarl-v7.fr-en.en')
eng_sentences = to_sentences(eng)
# French
fre = load_doc('europarl-v7.fr-en.fr')
fre_sentences = to_sentences(fre)
                        
# Clean datasets
eng_sentences = clean_lines(eng_sentences)
fre_sentences = clean_lines(fre_sentences)
                        
# Separate into train, validation and test for each training corpus size
for training_size in [25000, 50000, 100000, 200000, 400000, 800000]:
    eng_train, fre_train, eng_val, fre_val, eng_test, fre_test =
       split_train_val_test(eng_sentences, fre_sentences, training_size, 5000,
                            2000)
# These were then saved using save_sentences()

## Manual Splitter
                        
# Function for method 1 -- manual splitter based on known French morphology
# INPUT: French corpus in list form
# OUTPUT: Processed French corpus in list form
def french_morph(text):
  # Create empty list to store new lines
  out = []
  for line in text:
    # Add spaces around morphemes
    line = re.sub("ez ", " ez ", line)
    line = re.sub("ent ", " ent ", line)
    line = re.sub("ons ", " ons ", line)
    line = re.sub("ais ", " ais ", line)
    line = re.sub("ait ", " ait ", line)
    line = re.sub("i ons ", " ions ", line)
    line = re.sub("i ez ", " iez ", line)
    line = re.sub("ai ent ", " aient ", line)
    # Add edited line to output list
    out.append(line)
return out
                        
# This was then applied to all the french corpora produced above like so:
fre_train = to_sentences(load_doc('{French training Corpus}'))
save_sentences(french_morph(fre_train))
                        
## BPE Splitter
                        
# Install package with function to do this from Sennrich et al. (2016)
!pip install subword-nmt
                        
# Calculate how many splits are required
round(0.575 * len(create_vocab(fre_train))
      
# The splitting method then uses this number to create the splitting vocabulary
!subword-nmt learn-bpe -s {'num_operations'} < {'training_file'} > {'codes_file'}
      
# This was then applied to the three french corpora using the following line
subword-nmt apply-bpe -c {'codes_file'} < {'corpus_file'} > {'output_file'}
      
## Morfessor
      
# Install and import morfessor to use algorithm from Creutz and Lagus (2002)
!pip install morfessor
import morfessor
      
# Create function that trains Morfessor model and performs the segmentation on
#    the data
# INPUTS: the directory of the French training, validation and test corpora
# OUTPUTS: the processed training, validation and test corpora all in list form
def morfessor_splitter(train, val, test):
  # Import Morfessor training model
  io = morfessor.MorfessorIO()
  # Import training data in reable format
  train_data = list(io.read_corpus_file(train))
  # Define model, selecting the one proposed by Creutz and Lagus (2002)
  model = morfessor.BaselineModel()
  # Load training data into model
  model.load_data(train_data, count_modifier=lambda x: 1)
  # Train model in batch
  model.train_batch()
  # Create empty list to store all output corpora
  output_corpus = []
  # Process corpora using trained Morfessor model
  for corpus in [train, val, test]:
    lines = to_sentences(load_doc(corpus))
    out = []
    for line in lines:
      line = line.split()
      # Create empty string to add processed words to
      sentence = ’’
      # Add each processed word at a time
      for word in line:
        # Segment word
        split_word = str(model.viterbi_segment(word)[0])[2:-2]
        if split_word != word:
          # Remove commas Morfessor automatically adds around splits
          split_word = split_word.replace("’", "")
          split_word = split_word.replace(",", "")
        # Add processed word to the sentence
        sentence += split_word + " "
      out.append(sentence)
    output_corpus.append(out)
  return output_corpus[0], output_corpus[1], output_corpus[2]
      
# This was then applied to all the french corpora produced above like so:
fre_train, fre_val, fre_test = morfessor_splitter({'French training corpus'},
    {'French validation corpus'}, {'French test corpus'})
# These could then be saved using save_sentences()
