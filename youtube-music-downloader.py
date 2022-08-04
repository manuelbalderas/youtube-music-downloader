from urllib import request
from pytube import YouTube
import os
import re
import csv
destination = './music'


class Song:
    def __init__(self, song):
        self.artist = song[0]
        self.title = song[1]

    def get_html(self):
        search_query = self.artist.lower().replace(' ', '+') + '+' + \
            self.title.lower().replace(' ', '+')
        html = request.urlopen(
            'https://www.youtube.com/results?search_query=' + search_query)
        return html

    def get_url(self):
        video_ids = re.findall(
            r'watch\?v=(\S{11})', self.get_html().read().decode())
        url = 'https://www.youtube.com/watch?v=' + video_ids[0]
        return url

    def download(self):
        yt = YouTube(self.get_url())
        video = yt.streams.filter(only_audio=True).first()
        file = video.download(output_path=destination)
        file_name = os.path.join(
            destination, self.artist + ' - ' + self.title + '.mp3')
        os.rename(file, file_name)
        print(f'{self.artist} - {self.title} has been downloaded.')


def main():
    filename = 'music.csv'
    try:
        os.stat(destination)
    except:
        os.mkdir(destination)

    try:
        with open(filename) as f:
            reader = csv.reader(f)
            songs = list(reader)

        for i in range(len(songs)):
            s = Song(songs[i])
            s.download()

        print(f'{i+1} songs have been downloaded successfully.')

    except FileNotFoundError:
        print(f'''
        You should create a '{filename}' file with the songs you want to download as follow:
        
        song1_artist,song1_title
        song2_artist,song2_title
        .
        .
        .
        songN_artist,songN_title
        ''')

    except KeyboardInterrupt:
        print(
            f'The download has been interrupted. Only {i} songs have been downloaded successfully.')


if __name__ == '__main__':
    main()
