import numpy as np
import argparse
import os
import json
from datetime import datetime


def prepare_source_data(filename):
    file_path = 'Source/{}'.format(filename)
    exists = os.path.isfile(file_path)
    if exists:
        with open(file_path, encoding='utf8') as infile:
            text = infile.read()
        return text.split(' ')
    else:
        raise Exception('File {} does not exist!'.format(filename))


def make_pairs(corpus, order):
    for i in range(order, len(corpus)-1):
        key = []
        for j in range(order, 0, -1):
            key.append(corpus[i - j])
        yield (' '.join(key), corpus[i])


def generate_markov_table(filename, order):
    try:
        corpus = prepare_source_data(filename)
    except Exception as exc:
        print(exc.args)

    pairs = make_pairs(corpus, order)
    word_dict = {}

    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    path = 'Table/{}_{}'.format(order, filename)
    with open(path, "w+", encoding='utf8') as outfile:
        outfile.write(json.dumps(word_dict))


def create_markov_text(word_dict, first_word, n_words, filename, order):
    chain = [first_word]
    two_behind, one_behind = first_word.split(' ')

    for i in range(n_words):
        next_value = np.random.choice(word_dict[two_behind + ' ' + one_behind])
        chain.append(next_value)
        two_behind, one_behind = one_behind, next_value

    now = datetime.now()
    date = now.strftime("%d_%m_%Y_%H_%M_%S")
    path = 'Output/{}_Order_{}_{}'.format(date, order, filename)
    with open(path, "w+", encoding='utf8') as outfile:
        outfile.write(' '.join(chain))


def markov_order_type(x):
    x = int(x)
    if x < 1 or x > 5:
        raise argparse.ArgumentTypeError("Order should be between 1 and 5!")
    return x


def main():
    parser = argparse.ArgumentParser(description='Create text based on Markov Chains')
    parser.add_argument("file", help="File containing learning model")
    parser.add_argument("order", help="Markov chain order <1, 5>", type=markov_order_type)
    parser.add_argument("n_words", help='Number of words in the output file', type=int)
    args = parser.parse_args()

    file_path = 'Table/{}_{}'.format(args.order, args.file)
    exists = os.path.isfile(file_path)
    if not exists:
        generate_markov_table(args.file, args.order)

    with open(file_path, "r", encoding='utf8') as infile:
        word_dict = json.loads(infile.read())

    first_word = np.random.choice(list(word_dict.keys())[:500])
    create_markov_text(word_dict, first_word, args.n_words, args.file, args.order)


if __name__ == "__main__":
    main()
