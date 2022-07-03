from pprint import pprint
import instagram_scraper
import csv
import os
from urllib.request import urlopen
from urllib.error import *
import time
import datetime
import re

header = ['shortcode','account','url','duration','title','published_datetime','comment','like','Thumbnail','video_play_count','video_view_count','category']

header2 = ['shortcode', 'id', 'text', 'created_at', 'username']

args = {"login_user": "xxxxxxxxx@gmail.com", "login_pass": "xxxxxxxxxxxx"}

timestr = time.strftime("%Y%m%d-%H%M%S")

#tahun-bulan-tanggal
waktu_ambil = datetime.datetime(2022, 5, 11).timestamp()  

alist_user = ['narasi.tv',
'narasinewsroom',
'wmnbynarasi',
'getstarted.narasi',
'matanajwa',
'namanyajuga.lyfe',
'klubbukunarasi',
'indonesiadigitaltribe',
'komunitasnarasi',
'narasi.ecosystem',
'najwashihab',
'andovidalopez',
'twk_id',
'jovialdalopez',
'bongkar.indonesia'
]

list_user = ['matanajwa']

insta_scraper = instagram_scraper.InstagramScraper(**args)
insta_scraper.authenticate_with_login()
print('berhasil login')

def data_comment(list_shortcode,directory):
    filename = 'comment.csv'
    with open(os.path.join(directory,filename), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header2)
        for shortcode in list_shortcode:
            try:
                print("Success comment scraping")
                for item in insta_scraper.query_comments_gen(shortcode):
                    writer.writerow([
                                    shortcode,
                                    item['id'],
                                    item['text'],
                                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['created_at'])),
                                    item['owner']['username']
                                ])
            except:
                print("Failed comment scraping")

def data_engagement(directory,filename,userAkun):
    activate = True
    with open(os.path.join(directory,filename), 'w', encoding='UTF8', newline='') as f:
        list_shortcode = []
        writer = csv.writer(f)
        writer.writerow(header)
        shared_data = insta_scraper.get_shared_data_userinfo(username=userAkun)
        print(userAkun)
        counter = 0
        for item in insta_scraper.query_media_gen(shared_data):
            x_match = re.search("(\|.*Musyawarah)",item['edge_media_to_caption']['edges'][0]['node']['text'])
            try:
                counter = counter + 1
                if item['taken_at_timestamp'] < waktu_ambil:
                    break

                if x_match.group().split()[1].lower() == 'musyawarah':
                    #print("Find")
                    list_shortcode.append(item['shortcode'])

                    if item['is_video']==False:
                        play_count = 0
                        view_count = 0
                        category = "Post"
                        url = 'https://www.instagram.com/p/' + item['shortcode'] + '/'

                    if item['is_video']==True and item['video_play_count']!=0:
                        play_count = item['video_play_count']
                        view_count = item['video_view_count']
                        category = "Reel"
                        url = 'https://www.instagram.com/reel/' + item['shortcode'] + '/'

                    if item['is_video']==True and item['video_play_count']==0:
                        play_count = 0
                        view_count = item['video_view_count']
                        category = "IgTV"
                        url = 'https://www.instagram.com/tv/' + item['shortcode'] + '/'

                    print('success :' + str(counter))
                    writer.writerow([
                        item['shortcode'],
                        userAkun,
                        url,
                        item['video_duration'],
                        item['edge_media_to_caption']['edges'][0]['node']['text'],
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['taken_at_timestamp'])),
                        item['edge_media_to_comment']['count'],
                        item['edge_media_preview_like']['count'],
                        item['thumbnail_src'],
                        play_count,
                        view_count,
                        category
                    ])
            except:
                pass

    return list_shortcode

def scrape_data_insta(list_user,is_feed,is_comment):
    for userAkun in list_user:
        list_shortcode = ["Cd9xg4oFW5X",
                          "Cd-bK5CFokr",
                          "Cd-2Er_lA0l",
                          "CeAQAOoFQcM",
                          "CeAnLTZF3T1",
                          "CeA9_DHl5aE",
                          "CeDkUnGl7GK",
                          "CeD1OlkBZsz",
                          "CeEAcOOljPX",
                          "CeFvnGIFujj",
                          "CeGI5vbheKm",
                          "CeGVqvZrpL7",
                          "CeIRx_uLfwo",
                          "CeIlp7CFWHP",
                          "CeLI7g-rS9j",
                          "CeLSiv6rTnA",
                          "CeLvvHalFNm",
                          "CeNbyMCMAWb",
                          "CeQcIxsBkAt",
                          "CeQp8TSlQ-r"]

        directory = os.path.join('./data',userAkun)
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = userAkun + '.csv'
        
        if is_feed:
            list_shortcode = data_engagement(directory,filename,userAkun)
        
        
        if is_comment:
            directory_comment = os.path.join(directory,'comment')
            if not os.path.exists(directory_comment):
                os.makedirs(directory_comment)
            
            data_comment(list_shortcode,directory)

if __name__ == "__main__":
    scrape_data_insta(list_user,is_feed=False,is_comment=True)
