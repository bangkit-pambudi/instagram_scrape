from pprint import pprint
import instagram_scraper
import csv
import os
from urllib.request import urlopen
from urllib.error import *
import time
import datetime

header = ['shortcode','account','url','duration','title','published_datetime','comment','like','Thumbnail','video_play_count','video_view_count']

args = {"login_user": "", "login_pass": ""}

#tahun-bulan-tanggal
waktu_ambil = datetime.datetime(2022, 5, 1).timestamp()  

list_user = ['narasi.tv',
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

#list_user = ['getstarted.narasi']

insta_scraper = instagram_scraper.InstagramScraper(**args)
insta_scraper.authenticate_with_login()
print('berhasil login')

for userAkun in list_user:
    with open(os.path.join(userAkun + '.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        shared_data = insta_scraper.get_shared_data_userinfo(username=userAkun)
        print(userAkun)

        counter = 0
        for item in insta_scraper.query_media_gen(shared_data):
            if item['is_video']==True and item['video_play_count']!=0:
                try:
                    html = urlopen('https://www.instagram.com/reel/' + item['shortcode'] + '/')
                    print('sukses :' + str(counter))
                    writer.writerow([
                        item['shortcode'],
                        userAkun,
                        'https://www.instagram.com/reel/' + item['shortcode'] + '/',
                        item['video_duration'],
                        item['edge_media_to_caption']['edges'][0]['node']['text'],
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['taken_at_timestamp'])),
                        item['edge_media_to_comment']['count'],
                        item['edge_media_preview_like']['count'],
                        item['thumbnail_src'],
                        item['video_play_count'],
                        item['video_view_count']
                    ])
                except HTTPError as e:
                    print("HTTP error", e)
                except URLError as e:
                    print("Opps ! Page not found!", e)
            counter = counter + 1
            if item['taken_at_timestamp'] < waktu_ambil:
                break
