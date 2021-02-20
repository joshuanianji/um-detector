from __future__ import division
import sys
import os

__author__ = 'Emily Ahn and Elizabeth Hau'

''' *********************** analyze_text.py **************************
    This file contains methods that help analyze the transcriptions
    obtained from the audio files. Assuming we already have the 
    hypothesis file, we can read in the text file, process it to remove
    additional unwanted information in the file, and count filler words
    ******************************************************************
'''


def read_file(filename):
    ''' Takes in a file name and reads it in as a list of words
        Assuming the file is space delimited and is one continuous
        line of text
    '''
    with open(filename, 'r') as f:
        return f.read().split()


def preprocess_segments(segments):
    ''' Preprocesses the segments to remove numbers after words, <sil>, <s>, </s>,
        [NOISE] and return a new list with the cleaned up data
        i.e. new list returned will only contain the words spoken 
    '''
    new_list = []
    for word in segments:
        if not (word == '<sil>' or word == '<s>' or word == '</s>' or word == '[NOISE]'):
            if "(" in word:
                new_list.append(word.split("(")[0])
            else:
                new_list.append(word)
    return new_list


def filler_words(segments, filler='[SPEECH]'):
    ''' Takes in a list of the hypothesis segments and an optional parameter as 
        the filler word to search for and returns the % of the filler word's
        occurrence. The default filler word to search for is 'um' or 'uh', 
        represented as "[SPEECH]" in the hypothesis files. 
        This function assumes that the segments passed in is already cleaned up
        (only contains words spoken, no <s>, </s>, <sil>, or [NOISE])
    '''
    if not filler == '[SPEECH]':
        filler = filler.lower()

    num_filler = segments.count(filler)
    total_words = len(segments)
    print('total_words:', total_words)
    if filler == '[SPEECH]':
        filler = 'um or uh'  # for better printing in the results
    print('number of ', filler, 'said:', num_filler)
    percent = num_filler/total_words
    print('percent of filler words', percent)
    print('compared to TED standard frequency of filler words (0.005589%)...')
    # gold standard is hard coded into the program right now
    compare_to_standard(percent, 0.005589)
    return percent


def compare_to_standard(percent, standard):
    ''' This function takes in the percentage of the user's usage of filler
        words and compares it with the gold standard and prints out a 
        message informing the user their performance against the standard
    '''
    if percent < standard:
        print('GOOD JOB. You don\'t use many filler words.')
    else:
        print('Keep practicing! You still use too many filler words')


if __name__ == '__main__':
    DATADIR = sys.argv[1]  # directory to read the hypothesis files from
    # assumes the directory provided only contains text files of the hypotheses
    for f in os.listdir(DATADIR):
        if not f.startswith('.') and os.path.isfile(os.path.join(DATADIR, f)):
            print('file is:', f)
            filename = os.path.join(DATADIR, f)
            read = read_file(filename)  # original segments
            preprocessed = preprocess_segments(read)  # only spoken words
            print('\n*********** FILE: ', f, '****************')
            ums = filler_words(preprocessed)
            # likes = filler_words(preprocessed, 'like') #<-- inaccurate
            silences = filler_words(read, '<sil>')
            print('% of "um"s said ([\'SPEECH\'])', ums)
            # print '% of "like"s said', likes
            print('% of "<sil>"', silences)
