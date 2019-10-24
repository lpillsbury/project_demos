# !/usr/bin/env python3
# Copyright 2018 Leah Pillsbury leahp@bu.edu

# This program receives a list of possible words as input.
# Then the user enters in the command line the letters that can be used
# and the number of letters that should be used in the words.
# Note this program does not check for if the user gives bogus inputs

# Based on the number of letters that should be used, the word list
# should only be searched for words that are that length.

import string
import sys
import math
import itertools as it
import time

def PrintOutput(wordlist):
    " Print out all possible words, one per line, followed by a period"
    for item in wordlist:
        print(item)
    print('.')


def ncr(n, r):
    " Compute n choose r and return the result"
    numer = math.factorial(n)
    denom = math.factorial(r)*math.factorial(n-r)
    return numer/denom


def letter_method():
    " Only check the size words I want for the letters I have."
    # If there are a lot of number combinations, then look to see
    # if the words match the letters.
    # In the dictionary with the key that has the right number
    # of words all_words[N]
    # Loop through each word
    # Compare the letters in the word I'm going for to the letters I have.
    # If all the letters in the dictionary word are in my letter list,
    # then put the word in answer_words
    t0 = time.time()
    answer_words = []
    for word in all_words[N]:
        i = 0
        local_L = list(L)
        for letter in word:
            if letter in local_L:
                local_L.remove(letter)
                i = i+1
                continue
            else:
                break
        if i == N:
            answer_words.append(word)
    answer_words.sort()
    t1 = time.time()
    return answer_words


def anagram_method():
    # Create all possible combinations of the letters given the size
    t0 = time.time()
    all_combos = list(it.combinations(L, N))
    duplicate = []
    answer_words2 = []
    # Sort each combination alphabetically
    for combo in all_combos:
        combo = sorted(combo)
        duplicate.append(combo)

    # Make a list of only unique combinations
    # Sort combinations alphabetically
    final_combos = []
    for num in duplicate:
        if num not in final_combos:
            final_combos.append(sorted(num))

    # If a possible combination is also in anagram dictionary,
    # add it to a list of possible words.
    for combo in final_combos:
        combo = tuple(combo)
        if combo in anagram.keys():
            answer_words2.append(anagram[combo])
    flat_list = [item for sublist in answer_words2 for item in sublist]
    flat_list.sort()
    t1 = time.time()
    return flat_list


# First read in the word list to use.
filename = sys.argv[1]
f = open(filename, "r")

# Put all of the words into a dictionary by word length.
# According to Wikipedia, longest non-technical word in english is 28 letters.
# Make another dictionary of anagrams, don't worry about the length
# i.e. : AELP: [LEAP, PLEA]
# Why do I have to open and close the file each time?
# I tried to do it together and only got info into the first one

anagram = {}
for item in f:
    item = item.strip()
    # setdefault for a dictionary in python works like this:
    # if I haven't seen (in this case) the specific value for
    # tuple(sorted(set(item))) before, make a new entry with
    # in this case,
    # an empty list
    # and then in either case, append(item)
    # this is more compact than
    # x = tuple(sorted(set(item)))
    # if x not in anagram:
    #     anagram[x] = []
    # anagram[x].append(item)
    # basically,
    # anagram.setdefault(tuple(sorted(set(item))), []) is just a way of writing
    # anagram[tuple(sorted(set(item)))].append(item)
    # assuming that blah blah blah was already a key in anagram
    anagram.setdefault(tuple(sorted(list(item))), []).append(item)
# print(anagram)
f.close()

all_words = {i: [] for i in range(29)}
f = open(filename, "r")
for item in f:
    item = item.strip()
    len_name = len(item)
    all_words[len_name].append(item)
f.close()

while True:
    # Input the letters that can use to make words,
    # and number of letters for word.
    line = input()
    L, N = line.split()
    N = int(N)
    L = list(L)
    if(N == 0):
        quit()

    LchooseN = ncr(len(L), N)

    # based on testing various letter combinations,
    # the letter way becomes faster than the anagram way
    # when LchooseN is a bit under 1000 or greater.
    # It depends a bit on which letters you choose, but I
    # ran a few tests and it was consistent enough for these purposes.

    if LchooseN > 950:
        wordlist = letter_method()
    else:
        wordlist = anagram_method()
    PrintOutput(wordlist)
