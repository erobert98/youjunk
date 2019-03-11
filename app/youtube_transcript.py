import requests
from youtube_transcript_api import YouTubeTranscriptApi
from app.db_util import *


def pull_transcript(videoId):
	try:
		var = YouTubeTranscriptApi.get_transcript(videoId)
		# var = [{'text': '[Music]', 'start': 0.4, 'duration': 2.319}, {'text': 'Democrat Party suffers mass exodus after', 'start': 3.56, 'duration': 6.63}, {'text': 'music superstars major announcement', 'start': 6.54, 'duration': 6.349}, {'text': "that's gonna leave a mark the Democrat", 'start': 10.19, 'duration': 4.529}, {'text': 'Party is hemorrhaging voters as it', 'start': 12.889, 'duration': 3.961}, {'text': 'suffers from an exit of black voters and', 'start': 14.719, 'duration': 4.081}, {'text': 'an exit of those who say it has become a', 'start': 16.85, 'duration': 4.589}, {'text': 'violent socialist hate group the', 'start': 18.8, 'duration': 4.53}, {'text': 'walkaway campaign was already doing', 'start': 21.439, 'duration': 4.021}, {'text': 'damage to the dem party and now it has', 'start': 23.33, 'duration': 3.99}, {'text': 'to contend with blacks at the exit of', 'start': 25.46, 'duration': 4.8}, {'text': "black Americans President Trump's", 'start': 27.32, 'duration': 4.59}, {'text': 'support among blacks has gone up', 'start': 30.26, 'duration': 4.29}, {'text': 'considerably since he was elected the', 'start': 31.91, 'duration': 4.95}, {'text': 'HUD economy is surely helping as blacks', 'start': 34.55, 'duration': 4.5}, {'text': 'are enjoying historic job opportunities', 'start': 36.86, 'duration': 5.25}, {'text': "that even Obama didn't bring now Trump", 'start': 39.05, 'duration': 4.95}, {'text': 'Republicans are getting a big leg up', 'start': 42.11, 'duration': 4.44}, {'text': 'from rap superstar business mogul Kanye', 'start': 44.0, 'duration': 5.64}, {'text': 'West Kanye West has taken humongous', 'start': 46.55, 'duration': 4.8}, {'text': 'amounts of grief for supporting Donald', 'start': 49.64, 'duration': 3.84}, {'text': 'Trump more than you or I will ever take', 'start': 51.35, 'duration': 4.86}, {'text': 'and yet he persisted and now he has', 'start': 53.48, 'duration': 4.77}, {'text': 'created apparently by making t-shirts', 'start': 56.21, 'duration': 4.41}, {'text': 'that were distributed at a tipi USA', 'start': 58.25, 'duration': 4.35}, {'text': 'event this weekend by pundit Candace', 'start': 60.62, 'duration': 5.1}, {'text': "Owens they're pretty cool shirts too", 'start': 62.6, 'duration': 5.67}, {'text': 'there are three designs to check out the', 'start': 65.72, 'duration': 5.73}, {'text': 'one above and two more Niki Schwan Kanye', 'start': 68.27, 'duration': 5.129}, {'text': 'West designed these black suit t-shirts', 'start': 71.45, 'duration': 3.869}, {'text': "for real Candace aoe's new black suit", 'start': 73.399, 'duration': 4.17}, {'text': 'movement they were handed out real', 'start': 75.319, 'duration': 4.83}, {'text': 'Candace iya there is no group in America', 'start': 77.569, 'duration': 4.621}, {'text': 'that has been more lied to more abused', 'start': 80.149, 'duration': 3.81}, {'text': 'or more taken advantage of by the', 'start': 82.19, 'duration': 4.95}, {'text': 'Democrats than black people at long last', 'start': 83.959, 'duration': 5.22}, {'text': 'we can return the favor by ending their', 'start': 87.14, 'duration': 4.92}, {'text': 'stranglehold on our votes support the', 'start': 89.179, 'duration': 6.241}, {'text': 'ble XIT today patriots people will argue', 'start': 92.06, 'duration': 5.43}, {'text': "it's a matter of opinion that democrats", 'start': 95.42, 'duration': 4.02}, {'text': 'take the black vote for granted but it', 'start': 97.49, 'duration': 4.799}, {'text': 'isn t democrats think they have the', 'start': 99.44, 'duration': 5.28}, {'text': 'black vote in the bag if anything they', 'start': 102.289, 'duration': 4.291}, {'text': "think they're Oded and when they get an", 'start': 104.72, 'duration': 3.509}, {'text': 'inkling that black voters arrant', 'start': 106.58, 'duration': 3.33}, {'text': 'lockstep enough behind Democrat', 'start': 108.229, 'duration': 3.42}, {'text': 'candidates well they just use the', 'start': 109.91, 'duration': 3.54}, {'text': 'politics of fear to try and push', 'start': 111.649, 'duration': 4.411}, {'text': 'everyone back in line remember Joe', 'start': 113.45, 'duration': 6.11}, {'text': "Biden's change speech page six had more", 'start': 116.06, 'duration': 5.809}, {'text': 'Kanye West has designed t-shirts', 'start': 119.56, 'duration': 4.63}, {'text': 'encouraging black people to exit or', 'start': 121.869, 'duration': 5.081}, {'text': 'black sit the Democratic Party West', 'start': 124.19, 'duration': 4.95}, {'text': 'designs debuted Saturday at Turning', 'start': 126.95, 'duration': 4.17}, {'text': "Point USA's young black Leadership", 'start': 129.14, 'duration': 3.42}, {'text': 'Summit a meeting of young black', 'start': 131.12, 'duration': 4.32}, {'text': "conservatives in Washington West didn't", 'start': 132.56, 'duration': 4.56}, {'text': 'attend the conference but was there in', 'start': 135.44, 'duration': 2.159}, {'text': 'spirit', 'start': 137.12, 'duration': 2.82}, {'text': "according to teepee USA's communications", 'start': 137.599, 'duration': 4.371}, {'text': 'director Candace Owens', 'start': 139.94, 'duration': 3.83}, {'text': 'Bleck said as a renaissance and I am', 'start': 141.97, 'duration': 3.57}, {'text': 'blessed to say that this logo these', 'start': 143.77, 'duration': 3.54}, {'text': 'colors were created by my dear friend', 'start': 145.54, 'duration': 4.44}, {'text': 'and fellow superhero Kanye West said', 'start': 147.31, 'duration': 6.03}, {'text': 'Owens 29 she gushed that West has taken', 'start': 149.98, 'duration': 5.37}, {'text': 'one of the boldest steps in America to', 'start': 153.34, 'duration': 3.81}, {'text': 'open a conversation we have needed to', 'start': 155.35, 'duration': 4.23}, {'text': 'have the rapper and husband of Kim', 'start': 157.15, 'duration': 4.65}, {'text': 'Kardashian visited the president inside', 'start': 159.58, 'duration': 4.14}, {'text': 'the Oval Office earlier this month', 'start': 161.8, 'duration': 4.35}, {'text': 'his bromance with Trump began around', 'start': 163.72, 'duration': 4.59}, {'text': "April when he tweeted the mob can't make", 'start': 166.15, 'duration': 5.04}, {'text': 'me not love him the new shirts come in', 'start': 168.31, 'duration': 5.01}, {'text': 'traffic cone orange teal and a muted', 'start': 171.19, 'duration': 4.2}, {'text': 'lavender with designs that say blech sit', 'start': 173.32, 'duration': 4.68}, {'text': 'are we free the clothes were part of a', 'start': 175.39, 'duration': 4.71}, {'text': 'broader launch of black sitcom which', 'start': 178.0, 'duration': 3.81}, {'text': 'includes testimonials from black', 'start': 180.1, 'duration': 3.66}, {'text': 'Americans who have left the Democratic', 'start': 181.81, 'duration': 4.53}, {'text': 'Party Owens said there will be a black', 'start': 183.76, 'duration': 4.17}, {'text': 'suit tour to major cities including', 'start': 186.34, 'duration': 4.11}, {'text': 'Chicago and Philadelphia starting next', 'start': 187.93, 'duration': 5.49}, {'text': 'year the black suit movement will spend', 'start': 190.45, 'duration': 5.67}, {'text': '2019 holding rallies in every major city', 'start': 193.42, 'duration': 4.53}, {'text': 'in America that the Democrats have', 'start': 196.12, 'duration': 5.25}, {'text': 'destroyed she said Chuck Woolery I like', 'start': 197.95, 'duration': 5.67}, {'text': 'it exclusive Kanye West and Candace', 'start': 201.37, 'duration': 4.86}, {'text': 'Owens how Africa inspired the ble XIT', 'start': 203.62, 'duration': 6.0}, {'text': 'artwork mAb experience straight out of', 'start': 206.23, 'duration': 6.69}, {'text': "Chicago 73rd Jeffery I'm looking forward", 'start': 209.62, 'duration': 6.8}, {'text': 'to bringing it home ble XIT Chicago', 'start': 212.92, 'duration': 6.75}, {'text': 'Thank You real canned accountants JW', 'start': 216.42, 'duration': 5.8}, {'text': 'photograph fires tonight real candy CEO', 'start': 219.67, 'duration': 4.08}, {'text': 'announced her national movement of', 'start': 222.22, 'duration': 3.12}, {'text': 'minorities with hundreds of young', 'start': 223.75, 'duration': 3.3}, {'text': 'leaders from around the nation that have', 'start': 225.34, 'duration': 2.82}, {'text': 'awakened to the truth', 'start': 227.05, 'duration': 6.68}, {'text': "it's called ble XIT check it out at", 'start': 228.16, 'duration': 5.57}]
		L = len(var)
		# print(var[98]['text'])
		item = 0
		transcript = []
		while item < L:
			transcript.append(var[item]['text'])
			item += 1

		ptranscript = " ".join(transcript)
		# print(ptranscript)	
		return ptranscript
		
	except:
		transcript = "Not available"
		print(f"{videoId}s transcript is {transcript}")
		return transcript

def update_transcripts():
	list_videoids =[]
	V = Video.query.all()
	for v in V:
		if v.transcript is None:
			list_videoids.append(v.videoId)
	print(len(list_videoids))


	for video in list_videoids:
		vid = find_videoIDs(video)
		var = YouTubeTranscriptApi.get_transcript(video)
		L = len(var)
		item = 0
		transcript = []
		while item < L:
			transcript.append(var[item]['text'])
			item += 1

		ptranscript = " ".join(transcript)
		vid.transcript = ptranscript
		db.session.commit()
		