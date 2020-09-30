from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
from pygame import mixer
from PIL import Image, ImageTk
import os
from mutagen.mp3 import MP3
import threading
import time
from ttkthemes import ThemedTk

SCRIPT_PATH = os.path.realpath(__file__)
MAIN_DIR = os.path.dirname(SCRIPT_PATH).replace("\\", "/") + "/"


class MusicPlayer():
    def __init__(self):
        self.musicFullPaths = {}
        self.musicFilename = {}
        self.muted = FALSE
        self.musicStatus = False
        self.volume = 1
        self.fileName = "s"
        self.statusText = ""
        self.mutedButton = False
        self.stoped = TRUE
        self.threadExit = TRUE
        self.musicIndex = 0
        super().__init__()
        # ITFT1  plastik
        self.windows = ThemedTk(theme="itft1")
        windows = self.windows
        windows.geometry('920x350')
        windows.resizable(0, 0)
        windows.title("Music Player")
        windows.iconbitmap(MAIN_DIR + "images/main.ico")
        # windows.configure(background="red")
        windows.grid_rowconfigure(0, weight=1)
        windows.grid_columnconfigure(0, weight=1)
        self.mainFrame = Frame(windows)
        self.mainFrame.pack(fill=BOTH)
        self.rightFrame = Frame(self.mainFrame)
        self.rightFrame.pack(side=RIGHT,  padx=10, pady=10)
        self.leftFrame = Frame(self.mainFrame)
        self.leftFrame.pack(padx=40, pady=10)
        self.topFrame = Frame(self.rightFrame)
        self.topFrame.pack(padx=10, pady=10)
        self.middleFrame = Frame(self.rightFrame)
        self.middleFrame.pack(padx=10, pady=10)
        # self.bottomFrame = Frame(self.mainFrame)
        # self.bottomFrame.pack(side=BOTTOM, fill=X)
        self.createIcon(windows)
        # მუდვილი ციკლი  ფლეირეის დახურვამდე
        windows.mainloop()

    def createIcon(self, windows):
        menubar = Menu(windows)
        windows.config(menu=menubar)

        subMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Import/Open", command=self.importFile)
        subMenu.add_command(label="Exit", command=self.exitWindows)
        subMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=subMenu)
        subMenu.add_command(label="About Us", command=self.messageBox)
        subMenu.add_command(label="Exit", command=self.exitWindows)

        playImage = PhotoImage(file=MAIN_DIR + "images//play.png")
        playButton = ttk.Button(
            self.middleFrame, image=playImage, command=self.playMusic)
        playButton.image = playImage
        playButton.grid(row=0, column=1, padx=10, pady=10)

        stopImage = PhotoImage(file=MAIN_DIR + "images/stop.png")
        stopButton = ttk.Button(
            self.middleFrame, image=stopImage, command=self.stopMusic)
        stopButton.image = stopImage
        stopButton.grid(row=0, column=2, padx=10, pady=10)

        pauseImage = PhotoImage(file=MAIN_DIR + "images/pause.png")
        pauseButton = ttk.Button(self.middleFrame, image=pauseImage,
                                 command=self.pauseMusic)
        pauseButton.image = pauseImage
        pauseButton.grid(row=0, column=3, padx=10, pady=10)

        resetImage = PhotoImage(file=MAIN_DIR + "images/reset.png")
        resetButton = ttk.Button(self.middleFrame, image=resetImage,
                                 command=self.resetMusic)
        resetButton.image = resetImage
        resetButton.grid(row=0, column=4, padx=10, pady=10)

        self.unmuteImage = PhotoImage(file=MAIN_DIR + "images/sound.png")
        self.mutedButton = ttk.Button(
            self.middleFrame, image=self.unmuteImage, command=self.muteMusic)
        self.mutedButton.image = self.unmuteImage
        self.mutedButton.grid(row=0, column=5, padx=10, pady=10)

        self.volumeControl = ttk.Scale(self.rightFrame, from_=0, to=100,
                                       orient=HORIZONTAL, command=self.setVolume)
        self.volumeControl.set(100)
        self.volumeControl.pack(padx=10, pady=10)

        self.statusText = ttk.Label(self.windows, text="Start", anchor=E)
        self.statusText.pack(side=BOTTOM)
        statusBar2 = ttk.Label(self.windows, text="Welcome! ©COPYRIGHT 2020",
                               relief=SUNKEN).pack(side=BOTTOM, fill=X)

        self.lb = ttk.Label(self.topFrame, text="--:--")
        self.lb.pack(pady=10, padx=10)
        self.lb2 = ttk.Label(self.topFrame, text="Time : --:--")
        self.lb2.pack(pady=10, padx=10)

        self.playListBox = Listbox(self.leftFrame)
        self.playListBox.pack(fill=X, expand=True, padx=10, pady=10)

        self.musicAddButton = ttk.Button(
            self.leftFrame, text="Add Track", command=self.importFile)
        self.musicAddButton.pack(side=LEFT, pady=10, padx=10)
        self.musicRemoveButton = ttk.Button(
            self.leftFrame, text="Remove Track", command=self.musicDeteleFromPlaylist)
        self.musicRemoveButton.pack(pady=10, padx=10)

        windows.wm_protocol("WM_DELETE_WINDOW", self.exitWindows)

    def exitWindows(self):
        print("closed")
        self.stopMusic()
        self.threadExit = FALSE
        self.windows.destroy()

    def playMusic(self):
        filePath = self.cursorSelection()
        mixer.init()
        if self.musicStatus and self.stoped:
            # print(self.stoped)
            mixer.music.play()
            self.stoped = FALSE
            self.threadExit = FALSE
            self.musicInfo()
            self.threadExit = TRUE
        try:
            paused
        except NameError as e:
            try:
                if filePath:
                    mixer.music.load(filePath)
                    self.statusText['text'] = f'Playing :{os.path.basename(self.fileName)}'
                    mixer.music.set_volume(self.volume)
                    mixer.music.play()
                    self.musicStatus = True
                    self.musicInfo()
            except Exception as e:
                # print(e)
                tkinter.messagebox.showwarning(
                    "Warrning : File Could't Found ! ", "Please import music file first and then try again.   ")
        else:
            self.unpauseMusic()
            self.threadExit = FALSE
            self.musicInfo()
            self.threadExit = TRUE

    def stopMusic(self):
        self.threadExit = FALSE
        try:
            mixer.music.stop()
            self.stoped = TRUE
            self.musicInfo()
        except Exception as e:
            pass
        self.statusText['text'] = "..."

    def pauseMusic(self):
        if self.musicStatus:
            self.threadExit = FALSE
            global paused
            paused = TRUE
            mixer.music.pause()
            self.statusText['text'] = "Paused "
            self.musicInfo()

    def unpauseMusic(self):
        if self.musicStatus:
            mixer.music.unpause()
            self.statusText['text'] = f'Playing :{os.path.basename(self.fileName)}'
            self.threadExit = FALSE
            self.musicInfo()
            self.threadExit = TRUE

    # def import_music(self):
    #     ttk.Label(self.windows, text="ss").grid(row=0, column=1)

    def setVolume(self, val):
        if self.musicStatus:
            self.volume = float(val)/100
            mixer.music.set_volume(self.volume)
        else:
            self.volume = float(val)/100

    def messageBox(self):
        # აქვს სხვადასხვა ტიპის შეტყობინება warrning, error, info...
        tkinter.messagebox.showinfo(
            "About Us", "this is 4th grade student project.")

    def importFile(self):
        self.fileName = tkinter.filedialog.askopenfilename(
            filetypes=[("Media files", "*.acc *.mp3 *.wav *.wma")])
        self.addPlaylist()
        # print(self.fileName)

    def resetMusic(self):
        if self.musicStatus:
            mixer.music.play()

    def muteMusic(self):
        if self.muted:
            self.mutedButton.image = self.unmuteImage
            self.mutedButton = ttk.Button(
                self.middleFrame, image=self.unmuteImage, command=self.muteMusic)
            self.mutedButton.grid(row=0, column=5, padx=10, pady=10)
            self.volumeControl.set(100)
            self.muted = FALSE
        else:
            muteImage = PhotoImage(file="E:/Music_Player/icon/no-sound.png")
            self.mutedButton.image = muteImage
            self.mutedButton = ttk.Button(
                self.middleFrame, image=muteImage, command=self.muteMusic)
            self.mutedButton.grid(row=0, column=5, padx=10, pady=10)
            self.volumeControl.set(0)
            self.muted = TRUE

    def musicInfo(self):
        musicPath = self.cursorSelection()
        if musicPath:
            song = MP3(musicPath)
            self.songLength = song.info.length
            min, sec = divmod(self.songLength, 60)
            min = round(min)
            sec = round(sec)
            # timeFomrat = '{}:{}'.format(
            #     str(round(min)).zfill(2), str(round(sec)).zfill(2))
            self.timeFomrat = '{:02d}:{:02d}'.format(round(min), round(sec))
            # print(timeFomrat)
            self.musicPlayTime = min * 60 + sec
            self.lb['text'] = f'Playing : {os.path.basename(musicPath)[:-4]}'
            self.lb2['text'] = "Time : " + self.timeFomrat
            self.th = threading.Thread(target=self.startCount,
                                       args=(min, sec, self.timeFomrat, self.lb2))
            self.th.start()

    def startCount(self, min, sec, times, label):
        while self.musicPlayTime > 0 and self.threadExit:
            min, sec = divmod(self.musicPlayTime, 60)
            timeFomrat = '{:02d}:{:02d}'.format(round(min), round(sec))
            self.musicPlayTime -= 1
            time.sleep(1)
            # self.lb2['text'] = "Time : " + timeFomrat + " / " + self.timeFomrat
            self.lb2['text'] = "Time : " + self.timeFomrat

    def addPlaylist(self):
        musicName = os.path.basename(self.fileName)[:-4]
        print(musicName, self.fileName)
        # self.importFile()
        if self.fileName != "":
            trackInPlaylist = False
            for name in enumerate(self.musicFilename):
                if name[1] == musicName:
                    trackInPlaylist = True

            if not trackInPlaylist:
                self.playListBox.insert(
                    self.musicIndex, musicName)
                self.musicFilename[f'{musicName}'] = self.musicIndex
                self.musicFullPaths[str(self.musicIndex)] = self.fileName
                self.musicIndex += 1
            else:
                tkinter.messagebox.showinfo(
                    "Already in playlist", "Track is Already in Playlist")

    def cursorSelection(self):
        if self.playListBox.curselection():
            musicName = self.playListBox.get(self.playListBox.curselection())
            id = 0
            id = self.playListBox.curselection()[0]
            for name, i in self.musicFilename.items():
                if name == musicName:
                    id = i

            musicPath = self.musicFullPaths[f'{id}']
            return musicPath
        else:
            tkinter.messagebox.showinfo(
                "Select Music", "Please Select Music !")
            return False

    def musicDeteleFromPlaylist(self):
        music = self.playListBox.get(self.playListBox.curselection())
        if self.playListBox.curselection():
            musicId = self.playListBox.curselection()[0]
            self.playListBox.delete(musicId)
            for i, path in self.musicFullPaths.items():
                if music == os.path.basename(path)[:-4]:
                    musicId = i
                    # print("---------------------", i)
            del self.musicFilename[os.path.basename(
                self.musicFullPaths[f'{musicId}'])[:-4]]
            del self.musicFullPaths[str(musicId)]


MusicPlayer()
