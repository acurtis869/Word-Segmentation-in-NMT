# Find length of vocab and median word frequency
corpus_details(fre_train)

# Install OpenNMT to remote machine
!pip install OpenNMT-tf[tensorflow]

# The following process was then followed for each set of corpora (25k to 800k
#    training sizes; baseline, manual, bpe, and morfessor)

# Build vocabularies
!onmt-build-vocab --size 50000 --save_vocab {'French vocab output file'} {'French
    training corpus'}
!onmt-build-vocab --size 50000 --save_vocab {'English vocab output file'} {'English training corpus'}

# Train model
!onmt-main --model_type Transformer --config {'YAML configuration file'}
    --auto_config train --with_eval
# Where the YAML configuration file takes the form:
# ---
# model_dir: run/
# data:
#   train_features_file: {French training corpus}
#   train_labels_file: {English training corpus}
#   eval_features_file: {French validation corpus}
#   eval_labels_file: {English validation corpus}
#   source_vocabulary: {French vocabulary file}
#   target_vocabulary: {English vocabulary file}
# eval:
#   save_eval_predictions: true
#   steps: 1000
#   early_stopping:
#     metric: perplexity
#     min_improvement: 0.5
#     steps: 3
# train:
#   save_checkpoints_steps: 1000
#   average_last_checkpoints: 3
# ---
                                                                          
# Translate the test set
!onmt-main --config {'YAML configuration file'} --auto_config infer
    --features_file {'French test corpus'} --predictions_file {'English predictions output file'}
                                                                          
# Create function to create bootstrap distribution of BLEU test scores
# INPUTS: n_samples -- number of bootstrap samples to be taken; prediction --
#    the predictions made from the translation model in list form; target -- the
#    reference test set in English in list form; sample_size -- the size of each
 #   individual bootstrap sample; seed -- random seed for reproducibility
# OUTPUT: list of n_samples bootstrapped BLEU scores
import sacrebleu
def bootstrap_test(n_samples, prediction, target, sample_size, seed = 42):
  # Create empty list to store BLEU scores
  bleu_vec = []
  # Set seed for reproducibility
  random.seed(seed)
  # Make a temporary folder to store sampled corpora
  !mkdir bootstrap
  for i in range(n_samples):
    # Sample sentences randomly from the reference and predictions files
    index = random.choices(range(len(target)), k = sample_size)
    target_sample = []
    prediction_sample = []
    for j in range(len(index)):
      target_sample.append(target[index[j]])
      prediction_sample.append(prediction[index[j]])
    # Save sentences in temporary folder created earlier
    save_clean_sentences(prediction_sample, "bootstrap/sys")
    save_clean_sentences(target_sample, "bootstrap/ref")
    # Load documents (this had to be done to ensure correct format for SacreBLEU)
    sys = load_doc("bootstrap/sys")
    ref = load_doc("bootstrap/ref")
    # Calculate BLEU score
    bleu = sacrebleu.corpus_bleu(sys, ref)
    # Add BLEU score to list created at the start
    bleu_vec.append(bleu.score)
  return bleu_vec
                                                                          
# Calculate bootstrap distribution using function above
preds = to_sentences(load_doc("{'English predictions file'}"))
tgt = to_sentences(load_doc("{;English test corpus'}"))
bootstrap_test(1000, preds, tgt, 2000)
                                                                          
# The resulting vector was then saved using JSON
