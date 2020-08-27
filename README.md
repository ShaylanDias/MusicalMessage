# MusicalMessage

This app provides a GUI which allows you to search for a song, then send the lyrics to a friend line-by-line over text.
Keep in mind that this will only work on a machine running OSX which is logged into Messages.

## Functionality

This a Flask API I have set up for retrieving song names and images. It then feeds that information to a local web scraper to get the lyrics.
These lyrics are then sent through the OSX Messages app to the desired Contact/Number using AppleScript. I have to credit https://github.com/adhorrig/azlyrics for providing the majority
of the web scraping code which I then modified to fit my needs.

## Setup:

1. Make sure you have a valid Python 3 install with pip package manager!
2. Install the dependencies of the script with `pip install -r requirements.txt`

## Running

`python3 main.py`