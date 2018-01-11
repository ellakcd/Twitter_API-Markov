"""Generate Markov text from text files."""

from random import choice
from sys import argv
import twitter
import os

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    )

def open_and_read_file(file_paths):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    big_list_of_strings = []
    for ourfile in file_paths:
        big_list_of_strings.append(open(ourfile).read())
    document = " ".join(big_list_of_strings)

    return document



def make_chains(text_string, n):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """

    words = text_string.split()
    words.append(None)
    chains = {}
    # n = int(raw_input("How long would you like your n-gram to be? "))


    for word_index in range(0, len(words)-n):
        ngram = tuple(words[word_index:word_index + n])
        next_word = words[word_index + n]
    

        if ngram in chains:
            chains[ngram].append(next_word)
        else:
            chains[ngram] = [next_word]

    return chains


def make_text(chains):
    """Return text from chains."""

    while True: 
        key = choice(chains.keys())
        if key[0].capitalize() == key[0]:
            words = list(key)
            break

    character_count = 0
    for word in words: #words is list containing the first tuple worth of words
        character_count += len(word) + 1

    while character_count < 120:
        value_options = chains[key]
        next_word = choice(value_options)
        if next_word:
            words.append(next_word)
            key = key[1:] + (next_word,)
            character_count += len(next_word) + 1
        else: 
            key = choice(chains.keys())

    punctuation = [".", "!", "?", "!!!!!!!!!!!!!!!!!!!!!!!!!"]
    # weird_enders = ['(', ')', '[', ']']
    if words[-1][-1] == ",":
            words = words[:-1] + choice(punctuation)
    if words[-1].isalpha():
        words[-1] += choice(punctuation)
        # elif words[-1][-1] is in weird_enders:
        #     words[-1] += choice([punctuation])
    
    output = " ".join(words)
    # print output
    matching_punc_counts = {}
    for char in output:
        if char == '"':
            matching_punc_counts['"'] = matching_punc_counts.get('"', 0) + 1
        elif char == '(':
            matching_punc_counts['('] = matching_punc_counts.get('(', 0) + 1
        elif char == ')':
            matching_punc_counts[')'] = matching_punc_counts.get(')', 0) + 1        
    print matching_punc_counts
    if matching_punc_counts.get('"', 0) % 2 != 0:
        output += '"'
    if matching_punc_counts.get('(', 0) > matching_punc_counts.get(')', 0):
        output += ')'
    elif matching_punc_counts.get(')', 0) > matching_punc_counts.get('(', 0):
        output = '(' + output
    return output

def tweet(chains):
    """Return text from chains."""
    while True:
        status = api.PostUpdate(make_text(chains))
        print status.text 
        user_input = raw_input("Enter to tweet again [q to quit] >")
        if user_input == 'q':
            break

        

input_paths = argv[1:] 


input_text = open_and_read_file(input_paths)


chains = make_chains(input_text, 2)


random_text = make_text(chains)

actual_tweet = tweet(chains)

actual_tweet
