import os
path1 = os.getenv("USERPROFILE")
path2 = path1 + '\\Documents\\GitHub\\EH-Youtube\\'


#get all csv files in working directory
#https://stackoverflow.com/a/12280052/6030118
import glob
extension = 'csv'
os.chdir(path2)
files = glob.glob('*.{}'.format(extension))


import datetime
#https://stackoverflow.com/a/3682808/6030118
def unixToDate(x):
	y = os.path.getctime(x)
	z = datetime.datetime.fromtimestamp(y).strftime('%Y-%m-%d')
	return z


#a datetime object, need to convert it to string
#https://stackoverflow.com/a/3743240/6030118
today = str(datetime.datetime.now().date())


[os.remove(file) for file in files if unixToDate(file) != today]


if files == []: 
	import EH_Data_Clean_Up

#-----------------------------------------------------------------
#https://stackoverflow.com/questions/31758329/
#how to compare isodates



