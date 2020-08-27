import azapi

api = azapi.AZlyrics()

def get_lyrics(artist, title, dir='./', save=False):
    """artist=name of artist, title=name of song, dir=directory to save (if saving), save=save the lyrics in a text file (boolean input)"""
    attempts = 0
    val = None
    title_lower = title.lower()
    if ' feat' in title_lower or '(feat' in title_lower:
        title = title[:title_lower.index('feat.')]
    elif ' ft' in title_lower or '(ft' in title_lower:
        title = title[:title_lower.index('ft')]
    elif ' featuring' in title_lower or '(featuring' in title_lower:
        title = title[:title_lower.index('featuring')]
    print(title + ' - ' + artist)
    data = api.search(title + ' - ' + artist)
    print(data)
    # Sometimes a network error will lead to the value being None. If this is the case, try again a few times.
    while val is None and attempts < 3:
        try:
            if data and type(data) is dict and len(data) > 0:
                print(data)
                url = data[0]['url']
                val = api.getLyrics(url=url, save=save, dir=dir, sleep=1)
            else:
                val = api.getLyrics(artist=artist, title=title, save=save, search=False, dir=dir, sleep=1)
        except Exception as e:
            print(e)
        attempts += 1
        print(val)
    return val