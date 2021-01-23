from datetime import date
today = str(date.today())
eh_csv = 'Extra History Playlist'+ ' ' + today +".csv" #ZERO PUNCTUATION format

import csv
with open(eh_csv, newline='', encoding='UTF-8') as f:
    reader = csv.reader(f)
    data = list(reader)


import re
series_first = []
series_rest = []
singles_music_lies = []
all_episodes = []           #list of name of all episodes

#seperates all videos into 3 non-overlapping list: first episodes of a series,
#the other numbered episodes of the series, and singles/music/lies videos
for video in data:
    
    all_episodes.append(video[0])

    #need regex b/c normall string search of #1 also matched (Justinian &) Theodora #10 
    if len(re.findall('\\b1\\b', video[0])) == 1:
        series_first.append(video[0])
    elif '#' not in video[0]:
        singles_music_lies.append(video[0])
    else:
        series_rest.append(video[0])



#Dice's Coefficient
#got from here; John Rutledge's answer with NinjaMeTimbers modification
#https://stackoverflow.com/questions/653157/a-better-similarity-ranking-algorithm-for-variable-length-strings
#------------------------------------------------------------------------------------------
def get_bigrams(string):
    """
    Take a string and return a list of bigrams.
    """
    s = string.lower()
    return [s[i:i+2] for i in list(range(len(s) - 1))]

def string_similarity(str1, str2):
    """
    Perform bigram comparison between two strings
    and return a percentage match in decimal form.
    """
    pairs1 = get_bigrams(str1)
    pairs2 = get_bigrams(str2)
    union  = len(pairs1) + len(pairs2)
    hit_count = 0
    for x in pairs1:
        for y in pairs2:
            if x == y:
                hit_count += 1
                pairs2.remove(y)
                break
    return (2.0 * hit_count) / union
#-------------------------------------------------------------------------------------------


#only take couple words of the episode's names for comparison, b/c the first couple words are 99% of the 
#times the name of the series; can't make too short or words like 'the, of' etc will get matched (now or
#in future), or too long because will increase chance of superfluous match; does much better than w/o
#limitting to first few words
def first_three_words(name_string):
                                                       #eg ''.join vs ' '.join         
    first_three = ' '.join(name_string.split()[:5])  #-->'The Haitian Revolution' slightly worse
    #first_three = ''.join(name_string.split()[:5])  #--> 'TheHaitianRevolution', slightly better
    return first_three



#compared given episode with all first videos, and return a list of comparison scores
def compared_with_first(episode, series_name = series_first):

    episode_scores = []
    for i in series_name:
        x = first_three_words(episode)
        y = first_three_words(i)
        #comparison_score = round(string_similarity(episode, i),4)
        comparison_score = round(string_similarity(x,y),4)
        episode_scores.append((comparison_score, i))

    return episode_scores


matches = []

#go through video number 2,3,4 etc in a series, and compare them with the first episode
#of all series, then get a comparison score

for episode in series_rest:
    scores_list = compared_with_first(episode)
    similarity_score = 0
    most_likely_match = []

    #go thru list of comparison scores returned from compared_with_first,
    #then append the currentepisode/highest score/first episode to 
    #most_likely_match; repeat for all non-first episodes
    for score in scores_list:
        if score[0] > similarity_score:
            similarity_score = score[0]
            most_likely_match.clear()       #MIGHT HAVE BEEN THE CRUCIAL KEY 
            most_likely_match.append((episode,score)) 
    matches.append(most_likely_match)


final_match = []

for i in matches:
    final_match.append((i[0][0], i[0][1][1], i[0][1][0]))
    #just to get output in desired presentation



path = '/Users/Work/Desktop/'                   
with open('EH Sorting Episodes.csv', 'w', newline='',encoding='UTF-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for currentRow in final_match:
        csvwriter.writerow(currentRow)
        #print(currentRow)


