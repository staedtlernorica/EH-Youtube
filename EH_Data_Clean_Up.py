from datetime import date
today = str(date.today())
eh_csv = 'EH Playlist ' + today +".csv" 

#https://stackoverflow.com/a/11196588/6030118
import os
path1 = os.getenv("USERPROFILE")
path2 = path1 + '\\Documents\\GitHub\\EH-Youtube\\'



#check if csv already exists
#https://stackoverflow.com/a/82852/6030118
from pathlib import Path
my_file = Path(path2 + eh_csv)
if my_file.is_file() ==  False:
	import EH_Playlist_Scraper


import csv
with open(path2 + eh_csv, newline='', encoding='UTF-8') as f:
	reader = csv.reader(f)
	data = list(reader)


#unicode normalize all episode title, to handle Simon Bolivar
from unicodedata import normalize
for i in data:
	i[0] = normalize('NFKC', i[0])
	#print(i)


import re
series_first = []
series_all = []
singles_music_lies = []

#seperates videos into 3 non-overlapping categories: first episodes of a series,
#the other numbered episodes of the series, and singles/music/lies videos
for video in data:

	if '#' in video[0]:
		#b/c normal string search of #1 also matched (Justinian &) Theodora #10 
		if (len(re.findall('\\b1\\b', video[0])) == 1) or ('oUtEJtBeCaQ' in video[7]):
			series_first.append(video[0])     
		series_all.append(video)
	else:
		singles_music_lies.append(video)


#oUtEJtBeCaQ

def compare_series_first(x):

	ep_in_words = x.split('-')[0].split()
	most_likely = ''
	current_highest = 0

	for i in series_first:              #run thru all first episodes

		word_match = 0      						#reset score for each episode
		for word in ep_in_words:        			#run thru all words in the episode at hand
			if word in i.split('-')[0].split():     #see if each word in ep_in_words are in splitted first episodes
				word_match = word_match + 1

		if word_match > current_highest:        #if current series first has most match
			current_highest = word_match        #adjust highest score
			most_likely = i                     #adjust highest episode

	return most_likely.split('-')[0]


#run through all serialized video (including #1), find most likely match in series_first    
final_match = []
for i in series_all:
	final_match.append([i[0], compare_series_first(i[0])])


#extend (over append) all remaining data (views, likes, comments etc)
#b/c append adds [obj1, obj2], while extend adds obj1, obj2 individually
#to final_match
for i in range(len(series_all)):
	final_match[i].extend(series_all[i][1:])

bad_series = ['D', 'The History of Non', 'WW1 Christmas Truce: Silent Night ']
good_series = ['D-Day', 'The History of Non-Euclidean Geometry',
					'WW1 Christmas Truce']
byz_id = ["oUtEJtBeCaQ","EO9DuuhNEoE","aN1imOXR4b4","RwXAGiIVsgQ",
			"I6vn6uRlPL8","6oHr-zd6Bew"]                    
#cosmetic fix for series name
for i in final_match:
	if i[1] in bad_series:
		index = bad_series.index(i[1])
		i[1] = good_series[index]	

	elif i[7] in byz_id:
		i[1] = "Justinian & Theodora"



#newline='' helps prevent line skipping when printing entry
#https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
#-------------------------------------------------------------------------------------
#encoding='UTF-8', or will run into UnicodeEncodeError, eg with EH episode
#♫ Admiral Yi: Drums of War - Sean and Dean Kiner - Extra History Music
#https://stackoverflow.com/questions/37490428/unicodeencodeerror-with-csv-writer
with open(path2 + 'EH Series Sorted ' + today + '.csv', 'w', newline='',encoding='UTF-8') as csvfile:
	csvwriter = csv.writer(csvfile)
	for currentRow in final_match:
		csvwriter.writerow(currentRow)
		#print(currentRow)

with open(path2 + 'EH Rest Sorted ' + today + '.csv', 'w', newline='',encoding='UTF-8') as csvfile:
	csvwriter = csv.writer(csvfile)
	for currentRow in singles_music_lies:
		csvwriter.writerow(currentRow)
		#print(currentRow)
