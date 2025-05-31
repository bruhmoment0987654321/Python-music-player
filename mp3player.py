from tkinter import filedialog
from tkinter import *
import pygame
import os

root = Tk()
root.title('Music Player')
root.geometry("450x350")

pygame.mixer.init()

songs = []
current_song = ""
paused = False

menubar = Menu(root)
root.config(menu=menubar)
#most functions 
def load_music():
    global current_song
    root.directory = filedialog.askdirectory()
    for song in os.listdir(root.directory):
        name,ext = os.path.splitext(song)
        match ext:
            case '.mp3':
               songs.append(song) 
            case '.wav':
               songs.append(song)
            case '.ogg':
               songs.append(song)
            case '.flac':
                songs.append(song)
    
    for song in songs:
        songlist.insert("end",song)
    
    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]

def load_song():
    global current_song
    song = filedialog.askopenfilename(initialdir='audio/', title = "Choose an audio file", filetypes = (("MP3","*.mp3"),("Waveform Audio", "*.wav"),("Ogg Vorbis", "*.ogg"),("Free Lossless Audio Codec","*.flac"),))
    song = song.split("/")[-1]
    songlist.insert("end",song)
def play_music():
    global current_song
    pygame.mixer.music.load(os.path.join(root.directory,current_song))
    pygame.mixer.music.play()
    
    play_btn.configure(image = pause_btn_img)
    
    play_txt.delete(1.0,"end")
    play_txt.insert("end", "Now Playing: " + current_song.split('.')[0])

    print(current_song)
    
def pause_music():
    global paused
    
    paused = not paused
    print("paused = " + str(paused))
    
def press_play():
    global paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        pause_music()
        play_btn.configure(image = play_btn_img)
    else:
        if not paused:
            play_music()
        else:
            pygame.mixer.music.unpause()
            pause_music()
            play_btn.configure(image = pause_btn_img)
    
    print("pressed play")

def next_song():
    global current_song, paused
    try:
        songlist.selection_clear(0,END)
        songlist.selection_clear(0,END)
        songlist.selection_set(songs.index(current_song)+1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
       pass

def prev_song():
    global current_song, paused
    try:
        songlist.selection_clear(0,END)
        songlist.selection_set(songs.index(current_song)-1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
       pass

#setting up Gui
organise_menu = Menu(menubar,tearoff=False)
organise_menu.add_command(label='Add Song', command=load_song)
organise_menu.add_command(label='Add Folder',command=load_music)
organise_menu.add_command(label='Remove Song (upcoming)')
menubar.add_cascade(label='File',menu=organise_menu)

#listbox
songlist = Listbox(root, bg="black", fg="white",width=100,height=15)
songlist.pack()

#button images
play_btn_img= PhotoImage(file='Play.png')
back_btn_img= PhotoImage(file='Back.png')
forward_btn_img= PhotoImage(file='Next.png')
pause_btn_img= PhotoImage(file='Pause.png')

#where songs are displayed
control_frame = Frame(root)
control_frame.pack()

#button gui
play_btn = Button(control_frame,image=play_btn_img, borderwidth = 0,command = press_play)
back_btn = Button(control_frame,image=back_btn_img, borderwidth = 0,command = prev_song)
forward_btn = Button(control_frame,image=forward_btn_img, borderwidth = 0,command = next_song)


play_txt = Text(control_frame, height = 1, width = 30)

#setting up menu down below to look neat
play_txt.grid(row=0,column=1)
play_btn.grid(row=1,column=1,padx=7,pady=10)
back_btn.grid(row=1,column=0,padx=7,pady=10)
forward_btn.grid(row=1,column=2,padx=7,pady=10)

root.mainloop()