import sys
import os.path
import re
from glob import glob
from mutagen.easyid3 import EasyID3
import pysftp
import posixpath

filename_pat = re.compile('\\W+')

def escape_name(name):
    return filename_pat.sub("_", name)

def split_artist_album(folder_full):
    head, album = os.path.split(folder_full)
    head, artist = os.path.split(head)
    _, head = os.path.split(head)
    if head != "Music":
        raise RuntimeError("Invalid folder")        
    return escape_name(artist), escape_name(album)
    
def format_file_name(mp3_file):
    id3 = EasyID3(mp3_file)
    track_num = int(id3["tracknumber"][0].split("/")[0])
    track_name = id3["title"][0]
    return "{:02d}_{}.mp3".format(track_num, escape_name(track_name))

def main():
    folder_full = sys.argv[1]
    artist, album = split_artist_album(folder_full)
    mp3_files = glob(os.path.join(folder_full, "*.mp3"))
    if not mp3_files:
        raise RuntimeError("Folder is empty")    
    with pysftp.Connection("raspberrypi.local", username="pi", password="password") as con:
        rem_folder = posixpath.join("music", artist, album)
        print(rem_folder)
        con.makedirs(rem_folder)
        con.chdir(rem_folder)
        for mp3_file in mp3_files:
            rem_file = format_file_name(mp3_file)
            print(rem_file)
            con.put(mp3_file, rem_file)
            con.chmod(rem_file)
    print("Done")
    
if __name__ == "__main__":
    main()