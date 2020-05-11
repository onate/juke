# juke
mp3 playback flask app for raspberry pi

##Features
- Easily transfer music to the Pi from a PC. Music is stored on the device, so PC doesn't need to be on for listening. Just drag and drop a music folder to an icon on the desktop, and it transfers to the Pi.
- Ability to control playback from a phone, so again PC doesn't need to be on.
- Music is organized by artist and album. If I start playing the album, it should continue playing the whole album.
- The Pi music webservice starts up on boot, so I can just plug it in. Also, I can shut it down from my phone, to make it safe to unplug.

##Dependencies
On the Pi:
- Flask
- Python-VLC

Optional:
- HifiBerry DAC

On the PC:
- Mutagen
- PySFTP

##Setup
The files copy_folder.py and run_copy.bat should be copied to your PC. Create a short cut on your desktop to run_copy.bat, and set the start-up folder to the folder containing the file. Edit copy_folder.py to replace "password" with your Raspberry Pi password. Now you can just drag and drop a folder containing an album of MP3 files to the shortcut and it will clean up the names and FTP to your Pi (under the /home/pi/music folder). This assumes you have a tree structure like "Music/Artist/Album" on your PC. If not, you'll have to modify the script.

The juke folder should be copied to your Raspberry Pi. On my Pi, I just put it in my home folder (/home/pi/juke). Try running the app to make sure it works (can find all imports, etc), by typing "python3 juke.py" from the juke folder. Assuming it works, you should be able to browse to "http://raspberrypi.local:5000" from your PC (or phone) browser.

Now you want to configure it so the app will start up automatically on boot. Type "crontab -e" to open crontab. Add a new entry at the bottom "@reboot python3 /home/pi/juke/juke.py &". Save changes. That's it!