import tkinter as tk
import requests as rq
from PIL import Image, ImageTk
import get_lyrics
import autotext

lyrics = ""

session = rq.Session()

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("300x300")
        self.resizable(0, 0)
        self.title("Lyric Spamaroni")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageOne, PageTwo, StartPage, SearchPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        self.mainloop()

    def show_send_frame(self, lyrics, artist, title):
        frame = self.frames["PageTwo"]
        frame.set_lyrics(lyrics, artist, title)
        frame.tkraise()



    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def start_loop(self):
        self.window.mainloop()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bool = True
        load = Image.open("firstScreen.jpg")
        load = load.resize((300, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        pic = tk.Label(image=render, master=self)
        pic.img = render
        pic.place(x=0, y=0)
        pic.bind("<Button-1>", lambda x: controller.show_frame("SearchPage"))

    def callback(self, event):
        if self.bool:
            self.bool = False
        else:
            self.bool = True
        print("clicked at", event.x, event.y)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def set_lyrics(self, lyrics, artist, title):
        self.lyrics.set(lyrics)
        self.artist.set(artist)
        self.title.set(title)
        self.text.set("Enter an iPhone number to spam \"" + title + "\" by " + artist + " and press enter...")

    def __init__(self, parent, controller):
        self.lyrics = tk.StringVar()
        self.title = tk.StringVar()
        self.artist = tk.StringVar()
        self.text = tk.StringVar()
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Message(self, textvariable=self.text, width=230, justify=tk.CENTER)
        label.pack(side="top", fill="x")
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        # button.pack()
        self.number = tk.StringVar()

        self.entry = tk.Entry(master=self, textvariable=self.number, width=230, justify=tk.CENTER)
        # self.entry.bind('<Return>', self.sendSpam)
        self.entry.pack()
        button = tk.Button(self, text="Send!", command=self.sendSpam)
        button.pack()

        label = tk.Message(self, text="OR enter a name in your contacts (use number if not working)...", width=230, justify=tk.CENTER)
        label.pack()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        first_entry = tk.Entry(master=self, textvariable=self.first_name)
        last_entry = tk.Entry(master=self, textvariable=self.last_name)
        first_entry.pack()
        last_entry.pack()
        button = tk.Button(self, text="Send!",
                           command=self.sendToContact)
        button.pack()
        back = tk.Button(self, text="Choose Another Song",
                           command=self.backToSongChoice)
        back.pack()

    def backToSongChoice(self):
        self.controller.show_frame("SearchPage")

    def sendToContact(self):
        AutoText = autotext.AutoTextMac()
        print(self.first_name.get(), self.last_name.get())
        error = AutoText.message_by_name(self.lyrics.get(), self.first_name.get(), self.last_name.get(), delay=0.7)
        if (error != None):
            print("Errored! for name:", self.first_name.get(), self.last_name.get())

    def sendSpam(self):
        print(self.number.get())
        AutoText = autotext.AutoTextMac()
        AutoText.message_by_number(self.lyrics.get(), self.number.get(), delay=0.7)

class SearchPage(tk.Frame):

    def search(self, text):
        self.songs.clear()
        payload = {
            'method': 'track.search',
            'limit': 4,
            'track': self.query.get(),
            'format': 'json'
        }
        r = self.lastfm_get(payload, url = self.BASE_URL + '/search')
        print(r.status_code)
        print(r)
        js = r.json()
        results = js['results']['trackmatches']['track']
        count = 0

        for result in results:
            title = result['name']
            artist = result['artist']
            filename = str(count) + '.jpg'
            handler = self.downloadImage(title, artist, filename=filename)
            if handler == None:
                filename = "none.jpg"
            self.songs.append({'title': title,
                        'artist': artist,
                        'image': filename})

            self.addRow(title, artist, count, filename)
            count += 1
        temp = len(results)
        while temp < 4:
            self.addRow("No Results", "NA", temp, "none.jpg")
            temp += 1

    def addRow(self, title, artist, row, filename):
        load = Image.open(filename)
        load = load.resize((56, 56), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        pic = tk.Button(image=render, master=self.pictureFrame, command=lambda i=row: self.selectSong(i))
        pic.img = render
        pic.place(x=0, y=0)
        pic.grid(row=row, column=0)
        titleLabel = tk.Button(text=title, master=self.pictureFrame, padx=6, width=14, anchor=tk.W, justify=tk.LEFT,
                            borderwidth=0, command=lambda i=row: self.selectSong(i))
        titleLabel.grid(row=row, column=1)
        artistLabel = tk.Label(text=artist, master=self.pictureFrame, width=8, padx=6, anchor=tk.W, justify=tk.LEFT)
        artistLabel.grid(row=row, column=2)

    def selectSong(self, index):
        if len(self.songs) > index:
            song = self.songs[index]
            print(song)
            print((song['artist'], song['title']))
            lyrics = self.get_lyrics(song['artist'], song['title'])
            self.controller.show_frame("PageTwo")
            self.controller.show_send_frame(lyrics, song['artist'], song['title'])

    def downloadImage(self, title, artist, filename='image.jpg'):
        payload = {
            'method': 'track.getInfo',
            'track': title,
            'artist': artist,
            'format': 'json'
        }
        resp = self.lastfm_get(payload, self.BASE_URL + '/images').json()
        if 'album' in resp['track']:
            image_url = resp['track']['album']['image'][1]['#text']
            img_data = session.get(image_url).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)
            return handler
        else:
            return None

    def lastfm_get(self, payload, url):
        response = session.get(url, params=payload)
        return response

    def temp(self, text):
        self.controller.update_idletasks()
        self.search(text)

    def debug(self):
        print(self.query.get())

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.get_lyrics = get_lyrics.get_lyrics
        self.AutoTextMac = autotext.AutoTextMac

        self.BASE_URL = 'https://tiktokbikbok.herokuapp.com/api'
        self.songs = []
        masterFrame = tk.Frame(master=self)
        masterFrame.pack()
        self.frame = tk.Frame(master=masterFrame)
        self.frame.pack()
        self.var = tk.StringVar()
        self.query = tk.StringVar()
        self.query.trace("w", lambda name, index, mode, sv=self.query: self.debug())
        self.topLabel = tk.Label(text="Enter the song title", master=self.frame)
        self.topLabel.pack()
        self.entry = tk.Entry(master=self.frame, textvariable=self.query)
        self.entry.bind('<Return>', self.temp)
        self.entry.pack()

        self.frame2 = tk.Frame(master=self)

        self.pictureFrame = tk.Frame(master=self.frame, height=50, width=200)
        self.pictureFrame.pack()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


    def start_loop(self):
        self.window.mainloop()
