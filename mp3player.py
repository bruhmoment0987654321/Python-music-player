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

def load_music():
    global current_song
    root.directory = filedialog.askdirectory()
    for song in os.listdir(root.directory):
        name,ext = os.path.splitext(song)
        if (ext == '.mp3') or (ext == '.wav') or (ext == '.ogg') :
            songs.append(song)
    
    for song in songs:
        songlist.insert("end",song)
    
    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]

def play_music():
    global current_song,tkinter
    pygame.mixer.music.load(os.path.join(root.directory,current_song))
    pygame.mixer.music.play()
    
    play_btn.configure(image = pause_btn_img)
    
    play_txt.delete(1.0,"end")
    play_txt.insert("end", "Now Playing: " + current_song)

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
    
    print("im just checking all that sut ")

def next_song():
    global current_song, paused
    try:
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

organise_menu = Menu(menubar,tearoff=False)
organise_menu.add_command(label='Open',command=load_music)
menubar.add_cascade(label='File',menu=organise_menu)


songlist = Listbox(root, bg="black", fg="white",width=100,height=15)
songlist.pack()

#button finctions
play_btn_img= PhotoImage(file='Play.png')
back_btn_img= PhotoImage(file='Back.png')
forward_btn_img= PhotoImage(file='Next.png')
pause_btn_img= PhotoImage(file='Pause.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame,image=play_btn_img, borderwidth = 0,command = press_play)
back_btn = Button(control_frame,image=back_btn_img, borderwidth = 0,command = prev_song)
forward_btn = Button(control_frame,image=forward_btn_img, borderwidth = 0,command = next_song)

play_txt = Text(control_frame, height = 1, width = 30)

play_txt.grid(row=0,column=1)

play_btn.grid(row=1,column=1,padx=7,pady=10)
back_btn.grid(row=1,column=0,padx=7,pady=10)
forward_btn.grid(row=1,column=2,padx=7,pady=10)
root.mainloop()