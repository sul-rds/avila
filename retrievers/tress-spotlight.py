from bs4 import BeautifulSoup
import requests
import os
import unicodecsv as csv
import re

from urllib.parse import unquote

from random import randint
from time import sleep




captions = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"
}
csv_file = open("tress.csv", "ab")
writer = csv.writer(csv_file, encoding="utf-8")
writer.writerow(["filename", "unique_id", "caption", "date", "place", "genre", "permalink"])



for pageno in range(1,9):
	print(str(pageno))

	page = requests.get("https://exhibits.stanford.edu/tress/browse/all-exhibit-items??page=" + str(pageno) + "&per_page=96", headers=headers)
	soup = BeautifulSoup(page.content, "html.parser")
	#print(soup)
	results_div = soup.find("div", {"id":"documents"})
	result_array = soup.find_all("article")

	for result in result_array:
		print('-----------')
		
		try:
			photo_link = result.find("div", {"class":"document-thumbnail"})
			thumbnail =  photo_link.find("img")["src"]
			thumbnail = unquote(thumbnail)
			full_img = thumbnail.replace('100,100','2048,2048').replace('square','full')
			photo_info_array = thumbnail.split("/")
			photo_info_uniqueid = photo_info_array[5]
			photo_info_slug = photo_info_array[6]

			print(photo_info_uniqueid)
			print(photo_info_slug)

			save_filename = photo_info_slug + '.jpg'
			print("Testing to see if " + save_filename + " has been downloaded before...")
			if os.path.exists(r"images/" + save_filename):
		 		print(save_filename + " has already been downloaded")
			else:
		 		sleep(randint(1,4))
		 		print('Downloading ' + full_img)
		 		filetosave = requests.get(full_img) 
		 		with open('images/' + save_filename, 'wb') as savedfile:
		 			savedfile.write(filetosave.content)

			permalink =  "https://purl.stanford.edu/" + photo_info_uniqueid
			print("Now going to " + permalink)
			photopage = requests.get(permalink, headers=headers)
			photosoup = BeautifulSoup(photopage.content, "html.parser")
			#print(photosoup)
			caption = photosoup.find("h1", {"class": "py-2"}).text
			print("Caption: "+ caption)

			try:
				date_label = photosoup.find("th", string= re.compile('Date created'))
				date = date_label.find_next("td").text.strip()
			except:
				date = ''
			print("Date: " + date)

			try:
				place_label = photosoup.find("th", string= re.compile('Place'))
				place = place_label.find_next("td").text.strip()
			except:
				place = ''
			print("Place: " + place)
			
			try:
				genre_label = photosoup.find("th", string= re.compile('Genre'))
				genre = genre_label.find_next("td").text.strip()
			except:
				genre = ''
			print("Genre: " + genre)

### These are bafflingly only on the spotlight instance, not the purl page:

# 
# 			try:
# 				topic_label = photosoup.find("th", string= re.compile('Topic'))
# 				topic = topic_label.find_next("td").text.strip()
# 			except:
# 				topic = ''
# 			print("Topic: " + topic)
# 
# 			try:
# 				physdesc_label = photosoup.find("th", string= re.compile('Physical Description'))
# 				physdesc = physdesc_label.find_next("td").text.strip()
# 			except:
# 				physdesc = ''
# 			print("Physical description: " + physdesc)



			writer.writerow([save_filename, photo_info_slug, caption, date, place, genre, permalink])

		except:
			print("ERROR on image " + result.text)
			continue

		
csv_file.close()