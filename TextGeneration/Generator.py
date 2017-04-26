from Vocab import Vocab
import sys

if __name__ == "__main__":
    input_file = sys.argv[1]
    vocab = Vocab(corpus=input_file)