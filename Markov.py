import re
import string
import random

word_matrix = {}
# matrix format
# {word : {next_word: frequency, "Total Sum": total_words}}
#future work, maybe replace with database for scalability.
def build_matrix(file):
    with open(file, encoding="utf-8") as f:
        queue = []
        for line in f:
            #Create a list of words from the given sentence. Consider punctuation as "words."
            words = re.split('([{}])'.format(string.punctuation+" "), line)

            #remove the ' ' that keeps showing up for some reason. I dunno how to regex this out properly.
            #Maybe fix this dumb hack later.
            words = remove_items(words, ' ')
            words = remove_items(words, '\n')
            words = remove_items(words, '')
            for word in words:
                word = word.replace('\n', '')

                queue.append(word.lower())
            if len(queue) > 1:
                for i in range(len(queue) - 1):
                    current_word = queue[i]
                    next_word = queue[i + 1]

                    if current_word in word_matrix.keys():

                        if next_word in word_matrix[current_word].keys():
                            word_matrix[current_word][next_word] += 1
                            # In theory, there should never be a word with a space in it.


                        else:
                            word_matrix[current_word][next_word] = 1
                            #In theory, there should never be a word with a space in it.

                    else:
                        word_matrix[current_word] = {next_word: 1}
                last = queue[-1]
                queue = [last]


#quick hack from https://www.geeksforgeeks.org/python/remove-all-the-occurrences-of-an-element-from-a-list-in-python/
def remove_items(array, item):
    # remove the item for all its occurrences
    c = array.count(item)
    for i in range(c):
        array.remove(item)
    return array


#amount: How many "words" to generate
def babel(amount):
    words = list(word_matrix.keys())
    current_word = words[random.randint(0, len(words))]
    #current_word = "The"
    output = current_word
    for i in range(amount):
        if current_word in word_matrix.keys():
            # followups = list(word_matrix[current_word].keys())
            # #pick a random word from the list. Should make weighted in the future.
            # current_word = followups[random.randint(0, len(followups)-1)]
            current_word = get_followup_word(word_matrix[current_word])

        else:
            current_word = words[random.randint(0, len(words))]
       #Append the word to the output. This makes sure that punctuation looks correct,
       #because punctuation is a "word" in this.
        if current_word.isalnum():
            output += " "+ current_word
        else:
            output += current_word
    print(output)

def get_followup_word(followups):
    summation = sum(list(followups.values()))


    i = 0
    rng = random.randint(0, summation)

    followups_keys = list(followups.keys())
    for word in followups_keys:
        if i >= rng:
            return word
        else:
            i += followups[word]
    return followups_keys[-1]



#buildMatrix("input.txt")

build_matrix("pride and prejudice.txt")
build_matrix("bee movie script.txt")
build_matrix("Tragedies of sex.txt")

babel(30)
babel(30)
babel(30)




