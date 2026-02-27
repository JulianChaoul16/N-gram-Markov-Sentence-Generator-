"""
# Julian Chaoul
# 2/23/2026 
#
# Problem Statement - Create a program that generates sentences based on n-grams from a given text file.
#
# My algorithm uses a couple different steps and functions: 
# 1. Uses convert_to_list function, which takes in a list of filenames, reads the text from those files, and converts it into a list of sentences.
# 2. Uses arrange_frequency function, which creates a frequency dictionary of n-grams and a list of starting words for sentences.
# 3. Uses create_sentences function uses the frequency dictionary and starting words to generate new sentences based on the n-grams.
#      a. create_sentences uses the choose_next function which is used to randomly select the next word based on the frequency of the n-grams.
#      b. create_sentences also uses the make_proper function to format the generated sentences properly with punctuation.
#
# Example Usage:
#  PS C:\Users\JuJuC\OneDrive\Desktop\NLP\Ngram> python ngram.py 2 5 oceans.txt
This program belongs to Julian Chaoul
This program generates random sentences based on a 2-gram model.

Here are your generated sentences:
Today shipping routes carry the same time overfishing pollution and marine species.
Ocean acidification which can harm shell forming organisms and microscopic organisms and marine resources.
Beneath their surface forming a significant portion of years.
Ocean acidification which can harm shell forming a vast and regulating the blue whale.
The open ocean acidification which can harm shell forming organisms and habitat destruction threaten the long term stability of underwater mountains trenches and regulating the equator toward the world s climate but contains complex food webs driven by drifting phytoplankton that convert sunlight into energy through photosynthesis.

"""
import sys
import random


def convert_to_list(filenames: list) -> list:
    #Reads the text from the given files and converts it into a list of sentences.

    fulltext = []
    # Combines all the files into full text
    for files in filenames:
        with open(files, 'r', encoding = 'utf-8', errors = 'ignore') as file: 
            fulltext.append(file.read())
    full = " ".join(fulltext).lower() 
    
    tokens = []
    current = []
    #Tokenizes the full text into words and punctuation, separating sentences based on punctuation marks.
    for char in full:
        if char.isalnum() or char == "'":
            current.append(char)
        else:
            if current:
                tokens.append("".join(current))
                current = []
            
            if char in {'.', '!', '?'}: #treats . ? ! punctation as sentence enders
                tokens.append(char)

    if current:
        tokens.append("".join(current))

    # Seperates tokens into sentences 
    sentences = []
    current_sentence = []
    for token in tokens:
        current_sentence.append(token)
        if token in {'.', '!', '?'}:
            sentences.append(current_sentence)
            current_sentence = []

    return sentences 


def arrange_frequency(sentences: list, n: int) -> tuple:
    # Creates a frequency dictionary
    counts = {}
    start_words = []
    for sentence in sentences:
        #Ignore short sentences 
        if len(sentence) < n:
            continue
        
        ##Add all starting words to the list of starting words
        start_words.append(tuple(sentence[:n-1]))

        # Using sliding window of n
        for i in range(len(sentence) - n + 1):
            c = tuple(sentence[i:i+n-1])
            next_word = sentence[i+n-1]

            if c not in counts:
                counts[c] = {}
            counts[c][next_word] = counts[c].get(next_word, 0) + 1
    return counts, start_words



def choose_next(next_word: dict) -> str:
    #Randomly Select words from a dictionary of {word: frequency}
    total = sum(next_word.values())
    n = random.randint(1, total)

    #Marks every num 1 - total with a word, that is chosen based on frequenc.
    for c, freq in next_word.items():
            n -= freq
            if n <= 0:
                return c
    
    return random.choice(list(next_word.keys()))  # Fallback in case of an error


def make_proper(tokens):
    # Formats a sentence properly with punctuation
    output = []
    for t in tokens:
        if t in {'.', '!', '?'} and output:
            output[-1] = output[-1] + t
        else:
            output.append(t)
    return " ".join(output)


def create_sentences(frequency, start_words, n, m):
    # Our sentence generater 
    sentences = []
    max_attempts = m * 10 #To prevent infinite loops 
    attempts = 0  

    while len(sentences) < m and attempts < max_attempts:
        attempts += 1

        #Chooses random start 
        start = random.choice(start_words)
        sentence = list(start)

        for _ in range(50): #Limit sentence to 50 words 
            c = tuple(sentence[-(n-1):])    
            if c not in frequency:
                break

            next_word = choose_next(frequency[c])
            sentence.append(next_word)
            if next_word in {'.', '!', '?'}:
                sentences.append(make_proper(sentence))
                break

    return sentences

    
    

def main():

    if len(sys.argv) < 4:
        sys.exit(1)

    n = int(sys.argv[1])   # n-gram size
    m = int(sys.argv[2])   # number of words to generate
    filenames = sys.argv[3:]  

    # My header
    print("This program belongs to Julian Chaoul")
    print(f"This program generates random sentences based on a {n}-gram model.")
    print()


    sentences = convert_to_list(filenames)
    frequency, start_words = arrange_frequency(sentences, n)
    generated_sentences = create_sentences(frequency, start_words, n, m)
    print("Here are your generated sentences:")
    for sentence in generated_sentences:
        print(sentence)
    return 0



if __name__ == "__main__":
   raise SystemExit(main())



