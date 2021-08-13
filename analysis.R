# Read in JSON files

library(rjson)

control_bleu_25k <- fromJSON(file = "~/25k/Control/control_bleu.json")
manual_bleu_25k <- fromJSON(file = "~/25k/Manual/manual_bleu.json")
bpe_bleu_25k <- fromJSON(file = "~/25k/BPE/bpe_bleu.json")
morfessor_bleu_25k <- fromJSON(file = "~/25k/Morfessor/morfessor_bleu.json")
control_bleu_50k <- fromJSON(file = "~/50k/Control/control_bleu.json")
manual_bleu_50k <- fromJSON(file = "~/50k/Manual/manual_bleu.json")
bpe_bleu_50k <- fromJSON(file = "~/50k/BPE/bpe_bleu.json")
morfessor_bleu_50k <- fromJSON(file = "~/50k/Morfessor/morfessor_bleu.json")
control_bleu_100k <- fromJSON(file = "~/100k/Control/control_bleu.json")
manual_bleu_100k <- fromJSON(file = "~/100k/Manual/manual_bleu.json")
bpe_bleu_100k <- fromJSON(file = "~/100k/BPE/bpe_bleu.json")
morfessor_bleu_100k <- fromJSON(file = "~/100k/Morfessor/morfessor_bleu.json")
control_bleu_200k <- fromJSON(file = "~/200k/Control/control_bleu.json")
manual_bleu_200k <- fromJSON(file = "~/200k/Manual/manual_bleu.json")
bpe_bleu_200k <- fromJSON(file = "~/200k/BPE/bpe_bleu.json")
morfessor_bleu_200k <- fromJSON(file = "~/200k/Morfessor/morfessor_bleu.json")
control_bleu_400k <- fromJSON(file = "~/400k/Control/control_bleu.json")
manual_bleu_400k <- fromJSON(file = "~/400k/Manual/manual_bleu.json")
bpe_bleu_400k <- fromJSON(file = "~/400k/BPE/bpe_bleu.json")
morfessor_bleu_400k <- fromJSON(file = "~/400k/Morfessor/morfessor_bleu.json")
control_bleu_800k <- fromJSON(file = "~/800k/Control/control_bleu.json")
manual_bleu_800k <- fromJSON(file = "~/800k/Manual/manual_bleu.json")
bpe_bleu_800k <- fromJSON(file = "~/800k/BPE/bpe_bleu.json")
morfessor_bleu_800k <- fromJSON(file = "~/800k/Morfessor/morfessor_bleu.json")

# Note: ‘~’ was replaced by the specific directory on my machine.

# Create function to calculate p-value
# INPUTS: H_0: base and new models are as good as each other
#        H_1: new model is better than base model
# base and new are both vectors that should have the same length
# OUPUT: p-value for above test
bootstrap_test <- function(base, new) {
  # Check vectors are correct length
  if (length(base) == length(new)) {
    n <- length(base)
  }
  else {
    errorCondition("vectors are of different lengths")
}
  # Return bootstrap p-value
  return(1 - sum(new > base) / n)
}

# Create database to store results
df = data.frame("Training Size" = rep(c(25000,
                                    50000,
                                    100000,
                                    200000,
                                    400000,
                                    800000), 4),
              "Segmentation" = c(rep("Baseline", 6), rep("Manual", 6),
                               rep("BPE", 6), rep("Morfessor", 6)),
              "Mean BLEU" = c(mean(control_bleu_25k), mean(control_bleu_50k),
                             mean(control_bleu_100k), mean(control_bleu_200k),
                             mean(control_bleu_400k), mean(control_bleu_800k),
                             mean(manual_bleu_25k), mean(manual_bleu_50k),
                             mean(manual_bleu_100k), mean(manual_bleu_200k),
                             mean(manual_bleu_400k), mean(manual_bleu_800k),
                             mean(bpe_bleu_25k), mean(bpe_bleu_50k),
                             mean(bpe_bleu_100k), mean(bpe_bleu_200k),
                             mean(bpe_bleu_400k), mean(bpe_bleu_800k),
                             mean(morfessor_bleu_25k), mean(morfessor_bleu_50k),
                             mean(morfessor_bleu_100k),
                                 mean(morfessor_bleu_200k),
                             mean(morfessor_bleu_400k),
                                 mean(morfessor_bleu_800k)),
              "BLEU Var" = c(var(control_bleu_25k), var(control_bleu_50k),
                            var(control_bleu_100k), var(control_bleu_200k),
                            var(control_bleu_400k), var(control_bleu_800k),
                            var(manual_bleu_25k), var(manual_bleu_50k),
                            var(manual_bleu_100k), var(manual_bleu_200k),
                            var(manual_bleu_400k), var(manual_bleu_800k),
                            var(bpe_bleu_25k), var(bpe_bleu_50k),
                            var(bpe_bleu_100k), var(bpe_bleu_200k),
                            var(bpe_bleu_400k), var(bpe_bleu_800k),
                            var(morfessor_bleu_25k), var(morfessor_bleu_50k),
                            var(morfessor_bleu_100k), var(morfessor_bleu_200k),
                            var(morfessor_bleu_400k), var(morfessor_bleu_800k)),
              "PVal" = c(rep(1, 6),
                        bootstrap_test(control_bleu_25k, manual_bleu_25k),
                        bootstrap_test(control_bleu_50k, manual_bleu_50k),
                        bootstrap_test(control_bleu_100k, manual_bleu_100k),
                        bootstrap_test(control_bleu_200k, manual_bleu_200k),
                        bootstrap_test(control_bleu_400k, manual_bleu_400k),
                        bootstrap_test(control_bleu_800k, manual_bleu_800k),
                        bootstrap_test(control_bleu_25k, bpe_bleu_25k),
                        bootstrap_test(control_bleu_50k, bpe_bleu_50k),
                        bootstrap_test(control_bleu_100k, bpe_bleu_100k),
                        bootstrap_test(control_bleu_200k, bpe_bleu_200k),
                        bootstrap_test(control_bleu_400k, bpe_bleu_400k),
                        bootstrap_test(control_bleu_800k, bpe_bleu_800k),
                        bootstrap_test(control_bleu_25k, morfessor_bleu_25k),
                        bootstrap_test(control_bleu_50k, morfessor_bleu_50k),
                        bootstrap_test(control_bleu_100k, morfessor_bleu_100k),
                        bootstrap_test(control_bleu_200k, morfessor_bleu_200k),
                        bootstrap_test(control_bleu_400k, morfessor_bleu_400k),
                        bootstrap_test(control_bleu_800k, morfessor_bleu_800k)),
              "Vocab Size" = c(24633, 32952, 43547, 57088, 74913, 98626,
                              23665, 31492, 41453, 54235, 71010, 93521,
                              13356, 17859, 23627, 31017, 40729, 53709,
                              6618, 8433, 10526, 13014, 16312, 19696),
              "Median Freq" = c(2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 9, 10,
                               11, 12, 13, 14, 9, 11, 14, 17, 20, 26))
                               
# Add a column for vocab reduction
df$PercentReduction <- 100 *
(rep(df$Vocab.Size[df$Segmentation == "Baseline"], 4) - df$Vocab.Size) / rep(df$Vocab.Size[df$Segmentation == "Baseline"], 4)

# This resulted in Table X (shown in Appendix B of dissertation)
# This table was analysed using figures 6 and 7 which were created with the
#    following code

# Import tidyverse to use ggplot
library(tidyverse)

# Figure 6
ggplot(df, aes(x = Training.Size, y = Mean.BLEU, col = Segmentation,
                      group = Segmentation)) + geom_point() + geom_line() +
  scale_x_continuous(breaks = c(25000, 50000, 100000, 200000, 400000, 800000),
                   labels = c("25k", "50k", "100k", "200k", "400k", "800k"),
                   trans = "log2") +
  xlab("Training Corpus Size (Sentences)") +
  ylab("Mean BLEU Score (%)") +
  labs(color = "Segmentation Method:") +
  theme(text = element_text(size=15), legend.position="bottom")
  
# Figure 7
ggplot(df, aes(x = Training.Size, y = Vocab.Size, col = Segmentation,
             group = Segmentation)) +
  geom_point() + geom_line() +
  scale_x_continuous(breaks = c(25000, 50000, 100000, 200000, 400000, 800000),
                   labels = c("25k", "50k", "100k", "200k", "400k", "800k"),
                   trans = "log2") +
  xlab("Training Corpus Size (Sentences)") +
  ylab("Vocabulary Size") +
  labs(color = "Segmentation Method:") +
  theme(text = element_text(size=15), legend.position="bottom") +
  geom_hline(yintercept=50000, linetype=’longdash’, col = ’black’)
  
# Figure 4
# Load in data
rank <- fromJSON(file = "Zipf/rank.json")
freq <- fromJSON(file = "Zipf/freq.json")

ggplot() + geom_point(aes(x = rank, y = freq)) + 
  scale_x_continuous(breaks = c(1, 10, 100, 1000, 10000, 100000),
                     labels = c("1", "10", "100", "1000", "10000", "100000"),
                     trans = "log10") +
  scale_y_continuous(breaks = c(1, 10, 100, 1000, 10000, 100000),
                     labels = c("1", "10", "100", "1000", "10000", "100000"),
                     trans = "log10") + 
  xlab("Rank") + ylab("Frequency") + 
  theme(text = element_text(size=15))
