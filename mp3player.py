from tkinter import filedialog
import tkinter
import time
import pygame
import os
import mutagen

root = tkinter.Tk()
root.title('Music Player')
root.geometry("550x450")

pygame.mixer.init()

songs = []
current_song = ""
paused = False
looping = False
#button images
play_btn_img= tkinter.PhotoImage(file='Images/Play.png')
back_btn_img= tkinter.PhotoImage(file='Images/Back.png')
forward_btn_img= tkinter.PhotoImage(file='Images/Next.png')
pause_btn_img= tkinter.PhotoImage(file='Images/Pause.png')
loop_btn_img = tkinter.PhotoImage(file='Images/Loop.png')
no_loop_img = tkinter.PhotoImage(file='Images/No_Loop.png')
shuffle_btn_img = tkinter.PhotoImage(file='Images/Shuffle.png')

#grab song metadata(?) and time
def play_time():
    global status_bar,current_song,song_length
    
    current_time = pygame.mixer.music.get_pos()/1000
    converted_time = time.strftime('%H:%M:%S',time.gmtime(current_time))
    
    
    song = os.path.join(root.directory,current_song)
    
    song_mut = mutagen.File(song)
    
    song_length = song_mut.info.length
    
    converted_song_length = time.strftime('%H:%M:%S',time.gmtime(song_length))
    
    #configs
    status_bar.config(text=f'Time Elasped: {converted_time} of {converted_song_length}')
    print(f"Current Time: {int(current_time)} song length: {int(song_length)}")
    
    #go to next song automatically
    if int(current_time) >= int(song_length) and int(current_time) <=(int(song_length)+1):
        if looping == True:
            play_music()
        else:
            next_song()  
            
        print("wow")  
    #update time
    status_bar.after(1000,play_time)

Menubar = tkinter.Menu(root)
root.config(menu=Menubar)

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
    
    #play_txt.configure(text=f"Now Playing: {current_song.split('.')[0]}")
    play_time()
    
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
        songlist.selection_set(songs.index(current_song)+1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
       play_btn.configure(image = play_btn_img)

def prev_song():
    global current_song, paused
    try:
        songlist.selection_clear(0,END)
        songlist.selection_set(songs.index(current_song)-1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
       pass

def loopit():
    global looping
    looping = not looping
    
    #change image
    if looping == True:
        loop_btn.config(image=loop_btn_img)
    else:
        loop_btn.config(image=no_loop_img)

def shuffle():
    pass
    
#setting up Gui
organise_menu = tkinter.Menu(Menubar,tearoff=False)
organise_menu.add_command(label='Add Song', command=load_song)
organise_menu.add_command(label='Add Folder',command=load_music)
organise_menu.add_command(label='Remove Song (upcoming)')
Menubar.add_cascade(label='File',menu=organise_menu)

#listbox
songlist = tkinter.Listbox(root, bg="black", fg="white",width=80,height=15)
songlist.pack()

#where songs are displayed
control_frame = tkinter.Frame(root)
control_frame.pack()

#button gui
play_btn = tkinter.Button(control_frame,image=play_btn_img, borderwidth = 0,command = press_play)
back_btn = tkinter.Button(control_frame,image=back_btn_img, borderwidth = 0,command = prev_song)
forward_btn = tkinter.Button(control_frame,image=forward_btn_img, borderwidth = 0,command = next_song)
loop_btn = tkinter.Button(control_frame, image=no_loop_img, borderwidth=0, command = loopit)
shuffle_btn = tkinter.Button(control_frame, image = shuffle_btn_img, borderwidth=0, command = shuffle)

status_bar = tkinter.Label(root, text = '',bd = 1, relief = "groove", anchor = "e")
status_bar.pack(fill = "x", side = "bottom", ipady=2)

play_txt = tkinter.Label(control_frame, text = '', bd = 1,  anchor = "center", width = 5)

#setting up tkinter.Menu down below to look neat
play_txt.grid(row=0,column=1)

loop_btn.grid(row=1, column = 0, pady=5, padx = 40)
back_btn.grid(row=1,column=1,pady = 5, padx = 0)
play_btn.grid(row=1,column=2,pady = 5, padx = 50)
forward_btn.grid(row=1,column=3, pady = 5, padx=0)
shuffle_btn.grid(row=1, column = 4, pady=5, padx = 40)

root.mainloop()