import sys
sys.path.append('./lyrics_pulling/') # adds the lyrics pulling modules to the path for import
sys.path.append('./texting/') # adds the texting modules to the path for import
import get_lyrics
import autotext

get_lyrics = get_lyrics.get_lyrics
AutoText = autotext.AutoTextMac()


lyrics = get_lyrics('Lil Mosey', 'Blueberry Faygo', dir='./', save=False)
AutoText.message_by_name(lyrics, 'David', 'McAllister', byline=True)