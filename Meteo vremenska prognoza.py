import tkinter as tk
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageTk
import time
from sense_emu import SenseHat
import sqlite3
 
 
 
def wheatherIcon(outside_wheather):
    wheather_icons = [ImageTk.PhotoImage(Image.open(r'wheather icons/sunny.gif').resize((120,100))),
                    ImageTk.PhotoImage(Image.open(r'wheather icons/wind.gif').resize((120,100))),
                    ImageTk.PhotoImage(Image.open(r'wheather icons/cloudy.gif').resize((120,100))),
                    ImageTk.PhotoImage(Image.open(r'wheather icons/rain.gif').resize((120,100))),
                    ImageTk.PhotoImage(Image.open(r'wheather icons/snow.gif').resize((120,100))),]
 
    curr_wheather_icon = wheather_icons[0]
    if "vedro" in outside_wheather:
        curr_wheather_icon = wheather_icons[0]
    elif "vjet" in outside_wheather or "lahor" in outside_wheather:
        curr_wheather_icon = wheather_icons[1]
    elif "oblačno" in outside_wheather:
        curr_wheather_icon = wheather_icons[2]
    elif "kiš" in outside_wheather:
        curr_wheather_icon = wheather_icons[3]
    elif "snije" in outside_wheather:
        curr_wheather_icon = wheather_icons[4]
 
    print(outside_wheather)
    return curr_wheather_icon
 
 
def page1(root,out_cond,curr_wheather_icon,in_cond):
    photo_button = ImageTk.PhotoImage(Image.open('button.gif'))
    image_list.append(photo_button)
    page = tk.Frame(root, height=600,width=400, bg="black")
    page.place(x=0,y=0)
    labels = [tk.Label(page,text="Dobrodošli,", fg="grey",bg="black",font="15"),
              tk.Label(page,text=f"Trenutna temperatura vani: {out_cond['temp']} °C", fg="grey",bg="black",font="Impact 15"),
              tk.Label(page,text=f"Trenutno vrijeme vani: {out_cond['wheather']}", fg="grey",bg="black",font="Impact 15"),
              tk.Label(page,image=curr_wheather_icon,bg="black"),
              tk.Label(page,text=f"Trenutna temperatura u kući: {in_cond['temp']} °C", fg="grey",bg="black",font="Impact 15"),
              ]
    labels[0].place(x=20,y=20)
    labels[1].place(x=20,y=50)
    labels[2].place(x=20,y=80)
    labels[3].place(x=130,y=120)
    labels[4].place(x=20,y=260)
 
    time_label = tk.Label(page,text="0:0:0",font="Helvetica 40 bold",fg="grey",bg="black")
    time_label.place(x=100,y=500)
 
    def update_clock():
        global now
        now = time.strftime("%H:%M:%S")
        time_label.configure(text=now)
        root.after(500,update_clock)
 
    update_clock()
    time_label.configure(text=now)
    b = tk.Button(page,image=photo_button,width=200,height=60,borderwidth=0,relief="sunken",bg="black",command=changepage)
    b.place(x=100,y=350)
 
    def sense():
        global in_cond
        in_cond = {
             "temp" : round(s.get_temperature(),2),
             "press" : round(s.get_pressure(),2),
             "humm" : round(s.get_humidity(),2), 
         }
        labels[4].configure(text=f"Trenutna temperatura u kući: {in_cond['temp']} °C")
        root.after(2000,sense)
 
    sense()
 
def page2(root,out_cond,curr_wheather_icon,in_cond):
 
 
    photo_button_back = ImageTk.PhotoImage(Image.open('previous-page-button.gif'))
    image_list.append(photo_button_back)
    photo_button_next = ImageTk.PhotoImage(Image.open('next-button.gif'))
    image_list.append(photo_button_next)
 
    page = tk.Frame(root, height=600,width=400, bg="black")
    page.place(x=0,y=0)
    labels = [
              tk.Label(page,text=f"Trenutna temperatura vani: {out_cond['temp']} °C", fg="grey",bg="black",font="Impact 15"),    #0
              tk.Label(page,text=f"Trenutno vrijeme vani: {out_cond['wheather']}", fg="grey",bg="black",font="Impact 15"),      #1
              tk.Label(page,image=curr_wheather_icon,bg="black"),                                                               #2
              tk.Label(page,text=f"Trenutni pritisak vani: {out_cond['press']} Pa", fg="grey",bg="black",font="Impact 15"),     #3
              tk.Label(page,text=f"Trenutna vlažnost vani: {out_cond['humm']} %", fg="grey",bg="black",font="Impact 15"),       #4
              tk.Label(page,text=f"Trenutna temperatura u kući: {in_cond['temp']} °C", fg="grey",bg="black",font="Impact 15"),  #5
              tk.Label(page,text=f"Trenutni pritisak u kući: {in_cond['press']} Pa", fg="grey",bg="black",font="Impact 15"),    #6
              tk.Label(page,text=f"Trenutna vlažnost u kući: {in_cond['humm']} %", fg="grey",bg="black",font="Impact 15"),      #7
              ]
    labels[0].place(x=20,y=20)
    labels[1].place(x=20,y=50)
    labels[2].place(x=130,y=120)
    labels[3].place(x=20,y=80)
    labels[4].place(x=20,y=260)
    labels[5].place(x=20,y=320)
    labels[6].place(x=20,y=350)
    labels[7].place(x=20,y=380)
 
    b_back = tk.Button(page,image=photo_button_back,width=200,height=60,borderwidth=0,relief="sunken",bg="black",command=changepage)
    b_back.place(x=0,y=450)
 
    b_back = tk.Button(page,image=photo_button_next,width=200,height=60,borderwidth=0,relief="sunken",bg="black",command=changepage)
    b_back.place(x=200,y=450)
 
    def sense():
        global in_cond
        in_cond = {
             "temp" : round(s.get_temperature(),2),
             "press" : round(s.get_pressure(),2),
             "humm" : round(s.get_humidity(),2), 
         }
        labels[5].configure(text=f"Trenutna temperatura u kući: {in_cond['temp']} °C")
        labels[6].configure(text=f"Trenutni pritisak u kući: {in_cond['press']} Pa")
        labels[7].configure(text=f"Trenutna vlažnost u kući: {in_cond['humm']} %")
 
        conn = sqlite3.connect("logger.db")
        cur = conn.cursor()
 
        cur.execute("CREATE TABLE IF NOT EXISTS log(time,temp,pressure,humidity)")
        cur.execute("INSERT INTO log VALUES (?,?,?,?)",(time.strftime("%H:%M:%S"),in_cond['temp'],in_cond['press'],in_cond['humm']))
        counter = 0
        conn.commit()
 
        root.after(2000,sense)
 
    sense()
 
 
 
 
def changepage():
    global pagenum, root
    for widget in root.winfo_children():
        widget.destroy()
    if pagenum == 1:
        page2(root,out_cond,curr_wheather_icon,in_cond)
        pagenum = 2
    else:
        page1(root,out_cond,curr_wheather_icon,in_cond)
        pagenum = 1
 
 
 
image_list = []
 
s = SenseHat()
 
root = tk.Tk()
 
ico = Image.open('Weather-icon.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
 
root.title("Meteo app")
root.configure(bg="black")
w_h = 600
w_w = 400
root.geometry(f"{w_w}x{w_h}")
 
url = "https://vrijeme.hr/hrvatska_n.xml"
xml_data = requests.get(url).content
soup = BeautifulSoup(xml_data, features="xml")
print(soup)
now = time.strftime("%H:%M:%S")
 
for grad in soup.find_all("Grad"):
    if grad.GradIme.text == "Rijeka":
        out_cond = {
            "temp" : grad.Temp.text,
            "press" : grad.Tlak.text,
            "humm" : grad.Vlaga.text,
            "wheather" : grad.Vrijeme.text, 
        }
    else:
        pass
 
 
in_cond = {
             "temp" : round(s.get_temperature(),2),
             "press" : round(s.get_pressure(),2),
             "humm" : round(s.get_humidity(),2), 
         }
 
curr_wheather_icon = wheatherIcon(out_cond["wheather"])
 
 
pagenum = 1
 
page1(root,out_cond,curr_wheather_icon,in_cond)
 
root.mainloop()