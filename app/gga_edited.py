import sys
import re
# from difflib import SequenceMatcher
# from newspaper import Article
# from sys import argv
# import textwrap
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.tokenize import word_tokenize, WordPunctTokenizer
from nltk.probability import FreqDist

# with open(argv[1], 'r', encoding='utf8') as myvideofile:
#   video = myvideofile.read()

# with open(argv[2], 'r', encoding ='utf8') as myarticlefile:
#   article = myarticlefile.read()

# Margin of error in decimal
n = 0.2

# Ratio threshold in decimal
q = 0.80

# Length of substrings
l = 4

word_length_threshold = 0

def do_comparison(article, video):
    niceVid = prepare_video(video)
    niceArt, p = prepare_article(article)
    freqtableV = analysis_of_video(niceVid, p)
    freqtableA = analysis_of_article(niceArt, p)
    match = analysis_of_both(freqtableV, freqtableA, p)
    if match > .7:
        print(f"Match with Frequency ratio : {match} ")
        return "full match"
    elif match < .7:
        # try:
        # print('hm')
        substring_match = substring_of_both(niceVid, niceArt)
        if substring_match > .7:
            print(f"Partial Substring match : {substring_match}")
            return "partial match"
        # except Exception as e:
        #     print(e)
        #     return 'something went wrong'
    else:
        return 'no match'
    # print(f" {substring_match} and {match}")
            

def prepare_video(video):
    alphanum_video = []    #initiliaze our list of words in video that are alphanumeric
    alphanum_video_unique = set()   #so many variables
    videolower = video.lower()   # lowers the video trnascript
    videowpt = WordPunctTokenizer().tokenize(videolower)  # tokenizes the lowered video transcript
    #print(f"{videowpt}")
    for word in videowpt:   # itereating through every word in the tokenzied video lower
        #print(f"{word}")
        if word.isalnum() == True and len(word) > word_length_threshold:    #   if word is alphanumeric and longer than X characters
            #print(f"{word}")
            alphanum_video.append(word)   #add valid words to list of alphanum_video
            alphanum_video_unique.add(word) # what does this do?
    #print(f"{alphanum_video}")
    video_word_count = len(alphanum_video)  # finds how many words are in list
    video_word_count_unique = len(alphanum_video_unique) # finds unique word count... do u really need two varibles for this?

    # Note: video_word_count is word count of video transcript without words containing non-alphunumeric characters
    print(f"{video_word_count_unique} unique words in video")

    return alphanum_video

def analysis_of_video(alphanum_video, p):

    fdistV = FreqDist()  #create freqdist of video
    for word in alphanum_video:
        condition = len(word)  #literally does nothing ?
        fdistV[word.lower()] += 1
    #print(fdistV.most_common(p))
    most_common_V = fdistV.most_common(p)  #creates array of top P words

    return most_common_V



def prepare_article(article):
    alphanum_article = []
    alphanum_article_unique = set()
    articlelower = article.lower().replace("\\n","")  #would replacing with a space be more accurate?
    articlewpt = WordPunctTokenizer().tokenize(articlelower) #tokenize
    #print(f"{articlewpt}")
    for word in articlewpt:
        #print(f"{word}")
        if word.isalnum() == True and len(word) > word_length_threshold:
            #print(f"{word}")
            alphanum_article.append(word)
            alphanum_article_unique.add(word)
    #print(f"{alphanum_article}")
    # article_word_count = len(alphanum_article)
    article_word_count_unique = len(alphanum_article_unique)
    # Note: article_word_count is word count of article transcript without words containing non-alphunumeric characters
    # print(f"{article_word_count_unique} words in article")

    p = article_word_count_unique

    return alphanum_article, p




def analysis_of_article(alphanum_article, p):   
    fdistA = FreqDist()  #create freqdist of article
    for word in alphanum_article:
        condition = len(word)  #literally does nothing
        fdistA[word.lower()] += 1
    #print(fdistA.most_common(p))
    most_common_A = fdistA.most_common(p)  #creates array of top P words

    return most_common_A

def analysis_of_both(most_common_A, most_common_V,p):

    words_in_common = []

    for pair in most_common_V:
        for pair2 in most_common_A:
            if pair[0] == pair2[0]:
                int1 = int(pair[1])
                int2 = int(pair2[1])
                if (int1 <= int2):
                    if (int1 / int2) >= (1 - n):
                        #print(f"{pair[0]}")
                        words_in_common.append(pair[0])
                elif (int2 < int1):
                    if (int2 / int1) > (1 - n):
                        #print(f"{pair[0]}")
                        words_in_common.append(pair[0])
    #print(f"{words_in_common}")
    number_WIC = len(words_in_common)
    #print (f"{number_WIC}")
    frequency_ratio = number_WIC / p
    return frequency_ratio


def substring_of_both(alphanum_video, alphanum_article):
    substring_in_video = []
    substring_in_article = []
    substring_in_common = []


    video_word_count = len(alphanum_video)  # finds how many words are in list
    item = 0
    while item < (video_word_count - (l-1)):
        substringv = alphanum_video[item:(item + l)]
        substring_in_video.append(substringv)
        item +=1
    # print(substring_in_video)
    # print('hello')
    item = 0
    article_word_count = len(alphanum_article)  # finds how many words are in list
    while item < (article_word_count - (l-1)):
        substringa = alphanum_article[item:(item + l)]
        substring_in_article.append(substringa)
        item +=1
    # print('hello2')
    # print(substring_in_article)
    # print('~~~~~~~~~~~~~~~~~~~~~~~`')
    # print(substring_in_video)
    # print(substring_in_article)
    if len(substring_in_article) or len(substring_in_video) == 0: 
        raise ValueError 
    for substring in substring_in_video:
        if substring in substring_in_article:
            substring_in_common.append(substring)

    if len(substring_in_video) < len(substring_in_article):
        string_ratio = (len(substring_in_common)/len(substring_in_video))

    else:
        # try:
        string_ratio = (len(substring_in_common)/len(substring_in_article))  #https://www.westernjournal.com/orders-30-countries-pile-minor-league-team-reveals-patriotic-logo/
        # except Exception as e:
        #     print(e)                                                                             
        #     string_ratio = (len(substring_in_common))/(len(substring_in_video)) #grace check this fix, sometimes get divide by zero
    print(f" DID IT WORK {string_ratio}")
    return int(string_ratio)



if __name__ == "__main__":
    main()