# Unimelb-COMP90019-Project

## Based language and tools:  
Python, Javascript, Shell, and CouchDB.

## 0. Deployment  
Basic deployment shell script for NeCTAR cloud servers.

## 1. Data harvester  
Basic shell script for harvesting Melbourne tweets from 2017.8 to 2018.7.

## 2. Data partition and storage  
Split files from 1 and import into CouchDB.

## 3. Data analysis  
**3.1 Elementary analysis**	

	(You should have the files before running funcions!)

	Active users:
	Users who posted at least 300 and above tweets are regarded as active users.

	Three criteria:
    
	1. CR1. Coordinates
	Filter users who always posted tweets with the fixed coordinates and never moved.
	At least 10 tweets the user has.

	2. CR2. Followers/Followees
	Filter users whose number of followees is much bigger than followers.
	At least 300 followees and less than 100 followers. Followers/Followees < 0.1.
	
    3. CR3. Retweets/Tweets
	Filter users whose number of retweets is much greater than tweets.
	At least 300 retweets and less than 100 original tweets. Tweets/Retweets < 0.1.  
    	

**3.2 Deep analysis**  
Some deep analysis to filter normal users and bots.

## 4 Data visualisation  
Local host with Javascript to show the result. 

## Dataset:  
Exclude the big JSON file. 
