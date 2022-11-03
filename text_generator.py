from random import choice, choices
from nltk.tokenize import WhitespaceTokenizer
from collections import defaultdict, Counter


class TextGenerator:

    def __init__(self):
        self.file_path = input()
        self.tokens = self.tokens()
        self.ngrams = self.ngrams()

    def read_file(self):
        with open(self.file_path, encoding="utf-8") as corpus:
            text = corpus.read()
        return text

    def tokens(self):
        text = self.read_file()
        tokenizer = WhitespaceTokenizer()
        return tokenizer.tokenize(text)

    def ngrams(self):
        ngrams = defaultdict(Counter)
        for i in range(len(self.tokens) - 2):
            ngrams[" ".join(self.tokens[i:i + 2])].update((self.tokens[i + 2],))
        return ngrams

    def get_start(self):
        ngram_list = list(self.ngrams)
        starts = [pair for pair in ngram_list if pair.split()[0][0].isupper() and pair.split()[0][-1] not in "!?."]
        return choice(starts).split()

    def generate_sentence(self, n_words=5):
        sentence = []
        while True:
            if len(sentence) == 0:
                sentence = self.get_start()
            word_1 = " ".join(sentence[-2:])
            pairs = list(self.ngrams[word_1].keys())
            counts = list(self.ngrams[word_1].values())
            word_2 = choices(pairs, counts)
            sentence.append(*word_2)

            if word_2[0][-1] in ".!?":
                if len(sentence) < n_words:
                    sentence = []
                    continue
                return " ".join(sentence)


if __name__ == "__main__":
    text_gen = TextGenerator()
    for _ in range(10):
        print(text_gen.generate_sentence())
