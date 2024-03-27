# D I S C L A I M E R:
    # I have added  comments  for easier readability of the program
      # App developed by :
              # Manish Dhakal
              # Jaiman Shrestha
              # Prasanna Bhandari(Graphic Designer)
              # Safal Ghimire



from tkinter import *

import os
from tkinter import filedialog
import mysql.connector
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
global bgpic
success=None
global partnum
partnum=None
global filepath
import base64
import io
from io import BytesIO
filepath=None
global ip,ip_address
ip=None
ip_address="localhost"



#----------------------------------------------------------------------------#
#Create a class that add the info about the participant to the database


class Projectt:
    def __init__(self,Stall_Num,Pname,Pmembers,PImage):
        self.Stall_Num=Stall_Num
        self.Pname=Pname
        self.Pmembers=Pmembers
        self.PImage=PImage
    def addtodb(self):# adds to database
        try:  
            conn=mysql.connector.connect(host=open_ip(),user="root",password="swsc1234",database="projectdetails")
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS project_table(
                           
                        Stall_Number INTEGER ,
                        Project_Name TEXT, 
                        Project_Members TEXT,
                        Project_image BLOB,
                        Vote_Count INTEGER NOT NULL DEFAULT 0
                        )
                        ''')
            cursor.execute(" INSERT INTO project_table(Stall_Number,Project_Name,Project_Members,Project_image) VALUES (%s,%s,%s,%s)",
                        (self.Stall_Num,self.Pname,self.Pmembers,mysql.connector.Binary(self.PImage)))
            conn.commit()
        except mysql.connector.Error as err:
            return

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
      


#----------------------------------------------------------------------------#
#Delete Every Data From The Database
#----------------------------------------------------------------------------#
                

def deleteAll():
    result=messagebox.askyesno(title="Delete All Projects?",message="Are You Sure You Want To Delete All?",parent=dispwin)
    if result:
        conn=mysql.connector.connect(host=open_ip(),user="root",password="swsc1234",database="projectdetails")

        cursor=conn.cursor()
        delete=f"DELETE  FROM project_table"
        cursor.execute(delete)
        conn.commit()
        cursor.close()
        conn.close()

        dispdata()
    
    else:
        return


#----------------------------------------------------------------------------#
#Store The Ip In The Server_Ip.txt file
#----------------------------------------------------------------------------#

def store_data(file_name,data):

    if os.path.exists(file_name):
        
        with open(file_name,'w') as filee:
            filee.write(data)
    else:
        
        with open(file_name,'w') as filee:
            filee.write(data)

#----------------------------------------------------------------------------#
#View The Ip In The Server_Ip.txt file
#----------------------------------------------------------------------------#
            
def open_ip():
    global ip_address
    try:
        with open("Server_Ip.txt","r") as filee:
            ip_address=filee.read()
    except FileNotFoundError:
        ip_address="localhost"
    return ip_address

#----------------------------------------------------------------------------#
#Prompt the user to add a server Ip
#----------------------------------------------------------------------------#
        
        
def get_ip():
    global ip,current_ip
    ip=ip_entry.get()
    ip_entry.delete(0,len(ip))
    
    current_ip.destroy()
    store_data("Server_Ip.txt",ip)
    current_ip=Label(ipwin,text=f"Current IP : {ip}",font=("Helvetica",25),bg="#7393A7",fg="green")
    current_ip.place(x=30,y=300)


#----------------------------------------------------------------------------#
#Delete a desired data from the db
#----------------------------------------------------------------------------#



def deletefromdb(event,Pname): #Deletes From Database

    
    result=messagebox.askyesno(title="Delete Project?",message="Are You Sure You Want To Delete This Project?",parent=infowin)
    if result:
        conn=mysql.connector.connect(host=open_ip(),user="root",password="swsc1234",database="projectdetails")

        cursor=conn.cursor()
        delete=f"DELETE FROM project_table WHERE Project_Name= %s"
        cursor.execute(delete,(Pname,))
        conn.commit()
        cursor.close()
        conn.close()
        infowin.destroy()

        dispwin.destroy()
        dispdata()
    
    else:
        return

#----------------------------------------------------------------------------#
    #Converts Image BLOB to hexadecimal
#----------------------------------------------------------------------------#

def blob_to_hex(blob):  
    hex_representation = ''.join(format(byte, '02x') for byte in blob)
    return hex_representation

#----------------------------------------------------------------------------#
    #Convert  hexadecimal to resized image
#----------------------------------------------------------------------------#

def hex_to_resized_image(hex_string, new_size): 

    binary_data = bytes.fromhex(hex_string)
    byte_stream = io.BytesIO(binary_data)
    original_image = Image.open(byte_stream)
    resized_image = original_image.resize(new_size)
    return resized_image

#----------------------------------------------------------------------------#

def resize_image(img_path,width,height):
    org_image=Image.open(img_path)
    resized_image=org_image.resize((width,height))
    bgpic1=ImageTk.PhotoImage(resized_image)
    return bgpic1


#----------------------------------------------------------------------------#
#Creates new window for displaying individual data
#----------------------------------------------------------------------------#

def dispinfo(projname,details): 
    global infowin
    infowin=Toplevel(win)
    infowin.title(details[1])
    infowin.resizable(False,False)
    infowin.geometry("900x500")
    bgpic1=PhotoImage(file="projectdisp.png")
    canvas = Canvas(infowin, width=900, height=500)
    canvas.pack(fill="both", expand=True)
    bg_image = canvas.create_image(0, 0, anchor="nw", image=bgpic1)

    namelabel=Label(infowin,text=f"Stall No. {details[0]}\n\nProject Name:\n {details[1]}",font=("Times",15),fg="Black")
    namelabel.place(x=50,y=100)
    partnamearr=details[2].split(",")
    partnames=""
    for k in partnamearr:
        partnames=partnames+"\n"+k
    participants_label=Label(infowin,text=f"Participant Names : \n {partnames}",font=("Times",15),fg="black")
    participants_label.place(x=50,y=300)
    hexa=blob_to_hex(details[3])
    img=hex_to_resized_image(hexa,(500,350))
    tk_image=ImageTk.PhotoImage(img)
    canvas1 = Canvas(infowin,width=500,height=350,bg="Black")
    canv_image = canvas1.create_image(0, 0, anchor="nw", image=tk_image)
    canvas1.place(x=350,y=100)
    delete_label=Label(infowin,text="DELETE PROJECT",font=("Roboto",15,"underline"),fg="red")
    delete_label.bind("<Button-1>",lambda event,pname=details[1]:deletefromdb(event,pname))
    delete_label.place(x=700,y=470)
    
    infowin.mainloop()

#----------------------------------------------------------------------------#   
#Creates a window prompting the user to add IP address of the sever
#----------------------------------------------------------------------------# 
    
def add_ip():
    global ipwin,ip,ip_entry,current_ip
    ipwin=Toplevel(win)
    ipwin.title("Master Application - Add IP")
    ipwin.geometry("800x400")
    ipwin.configure(bg="#7393A7")
    ipwin.resizable(False,False)
    ip_label=Label(ipwin,text="Add Server IP : ",font=("CanterBold",30),bg="#7393A7")
    ip_label.place(x=20,y=100)
    ip_entry=Entry(ipwin,font=("Arial",25),bg="white",fg="black")
    ip_entry.bind("<Return>",lambda event=None:get_ip())
    ip_entry.place(x=400,y=100)
    submit_B=Button(ipwin,text="Submit",font=("Arial",15))
    submit_B.configure(command=get_ip)
    submit_B.pack(padx=20,pady=170)
    current_ip=Label(ipwin,text=f"Current IP : {ip}",font=("Helvetica",25),bg="#7393A7",fg="green")
    current_ip.place(x=30,y=300)



#----------------------------------------------------------------------------#
    #Retrieves The Info About Participants From The Database And Places It In the View Window
#----------------------------------------------------------------------------#
 
def creategrid(arg): 
    b=len(arg)
    def on_enter(event,label):
        label.config(bg="grey")

    def on_leave(event,label):
        label.config(bg="#B5C5D8")
    x_pos=18
    rows=30
    columns=100
    y_pos=100
    for k in range(0,b):
        project_label=Label(dispwin,text=f"{k+1}.  {arg[k][1]}",font=("ROBOTO",17),fg="black",width=16,anchor="w",bg="#B5C5D8")
        project_label.bind("<Button-1>",lambda name=arg[k][1],detail=arg[k]:dispinfo(name,detail))
        project_label.bind("<Enter>",lambda event,label=project_label:on_enter(event,label))
        project_label.bind("<Leave>",lambda event,label=project_label: on_leave(event,label))
        if (k%18)==0:
            y_pos=100

        try:
            project_label.place(x=30+300*(k//x_pos),y=y_pos+columns*(k//b))
        except ZeroDivisionError:
            project_label.place(x=30,y=100)
        finally:
            y_pos+=40



#----------------------------------------------------------------------------#
            #clears the added data on clicking submit button
#----------------------------------------------------------------------------#
            
def clear_all(): 
    for  k in range(0,len(entry_widgets)):
        entry_widgets[k].delete(0,len(entry_widgets[k].get()))
        entry_widgets[k].destroy()
        partlbls[k].destroy()
    entname.delete(0,len(entname.get()))
    partcount.delete(0,len(partcount.get()))
    id_entry.delete(0,len(id_entry.get()))


#----------------------------------------------------------------------------#
    #Retrieves The Data From The Input Fields After Clicking the submit button and creates an object of class Project
#----------------------------------------------------------------------------#
     
def submit(): #
    if partcount.get()==None: 
        messagebox.showwarning(title="Value Error",message="Fill Out All The Fields",parent=addwin)
    global success
    if success is not None: 
        success.destroy()
    pmembers=[] 
    Pname=entname.get() 
    stall_num=id_entry.get()
    if filepath is not None: 
        with open(filepath,'rb') as file:
            Pimage=file.read()
    else: 
        messagebox.showerror(title="Image File Error",message="Please Select An Image File",parent=addwin)
        return
    try:
        for k in entry_widgets: 
            pmembers.append(k.get())
    except NameError:
        return
    pmembers=",".join(map(str,pmembers))  
    ProjectN=Projectt(stall_num,Pname,pmembers,Pimage) 
    ProjectN.addtodb() 
    success=Label(addwin,text="Data Entry Successful",font=("Canterbold",35),fg="green",bg="#7393A7")
    success.place(x=800,y=700)
    clear_all()
    addwin.after(3000,lambda:success.destroy())


#----------------------------------------------------------------------------#
    #Creates An environment for entering participant names
#----------------------------------------------------------------------------#
      
def participant_names(): 

    global c,entry_widgets,partlbls
    try:
        partnum=int(partcount.get())
    except ValueError:
        messagebox.showwarning(title="Value Error", message="Please only input integers",parent=addwin)
    try:
        if partnum>15:
            messagebox.showwarning(title="Too Many Participants",message="Enter at max 15 participants",parent=addwin)
            return
    except UnboundLocalError:
        return

    c=450
    entry_widgets,partlbls=[],[]
    for k in range(1,partnum+1):
        pttext=f"Enter Participant No.{k} : "
        partlbl=Label(addwin,text=pttext,fg="black",font=("canterbold",30),bg="#7393A7")
        partlbl.place(x=240,y=c)
        partlbls.append(partlbl)
        partname=Entry(addwin,font=("Arial",15),bg="white",fg="black")
        partname.place(x=800,y=c)
        entry_widgets.append(partname)
        c+=50
    
#----------------------------------------------------------------------------#
        #Prompts the user to select an Image of The Participant
#----------------------------------------------------------------------------#

    
def openfile():
    global filepath

    filepath=filedialog.askopenfilename(initialdir='This PC',defaultextension=".png",title="Select An Image File",parent=addwin)
    filenamee=Label(addwin,text=filepath,font=("Arial",9,"underline"),fg="green",bg="#7393A7")
    filenamee.place(x=1200,y=320)


#----------------------------------------------------------------------------#
    #binds f11 to fullscreen
#----------------------------------------------------------------------------#
    
def toggle_fullscreen(wind,event=None): 
    state = not wind.attributes('-fullscreen')
    wind.attributes('-fullscreen', state)

#----------------------------------------------------------------------------#
    #Goes back to previous Window
#----------------------------------------------------------------------------#

def goback(window): 
    win.deiconify()
    window.destroy()
    
#----------------------------------------------------------------------------#
    #Places the back button
#----------------------------------------------------------------------------#

def placeback(window,color): #Places the back button
    backlabel=Label(window,text="← Back",fg="Black",font=("Arial",20,"underline"),cursor="Hand2",bg=color)
    backlabel.place(x=35,y=35)
    backlabel.bind("<Button-1>", lambda event=None: goback(window))

#----------------------------------------------------------------------------#
    #Creates  A new window for adding data
#----------------------------------------------------------------------------#

def adddata(): 

    global addwin,partcount,entname,id_entry
    addwin=Toplevel(win)
    addwin.title("Master Application - Add Data")
    addwin.geometry("1920x1080")
    bgpic=resize_image("Bg.png",addwin.winfo_screenwidth(),addwin.winfo_screenheight())
    canvas = Canvas(addwin, width=win.winfo_screenwidth(), height=win.winfo_screenheight())
    canvas.pack(fill="both", expand=True)
    bg_image1 = canvas.create_image(0, 0, anchor="nw", image=bgpic)

    placeback(addwin,"#7393A7")
    if win.attributes('-fullscreen'):
        toggle_fullscreen(addwin)
    addwin.bind("<F11>",lambda event:toggle_fullscreen(addwin,event))
    infolbl=Label(addwin,text="Enter The Project Details Below",font=("Azonix",20,"underline"),fg="Black",bg="#7393A7")
    infolbl.place(x=330,y=35)
    id_label=Label(addwin,text="Id. No: ",font=("CanterBold",35),bg="#7393A7")
    id_label.place(x=240,y=100)
    id_entry=Entry(addwin,font=("Arial",25),bg="white",fg="black")
    id_entry.place(x=800,y=100)
    namelbl=Label(addwin,text=" Name : ",font=("CanterBold",35),fg="Black",bg="#7393A7")
    namelbl.place(x=240,y=200)
    entname=Entry(addwin,font=("Arial",25),bg="white",text="Project Name",fg="black")
    entname.place(x=800,y=200)
    partlbl=Label(addwin,text="Organization (If Any) ",font=("CanterBold",35),fg="black",bg="#7393A7")
    partlbl.place(x=240,y=400)
    partcount=Entry(addwin,font=("Arial",25),bg="white",fg="black")
    partcount.place(x=800,y=400)
    partcount.bind("<Return>",lambda event:participant_names())
    imglbl=Label(addwin,text="Project Image : ",font=("CanterBold",35),fg="black",bg="#7393A7")
    imglbl.place(x=240,y=300)
    addimgbutton=Button(addwin,text="Select an image",command=openfile,font=("arial",14,"underline"),fg="Blue",padx=103)
    addimgbutton.place(x=800,y=300)
    submitbutton=Button(addwin,text="Submit",font=("CanterBold",34),command=submit,width=20,height=1)
    submitbutton.place(x=1100,y=750)
    addwin.mainloop()

#----------------------------------------------------------------------------#
    #creates a new window for displaying all entered data
#----------------------------------------------------------------------------#
    
def dispdata(): 
    global dispwin
    dispwin=Toplevel(win)
    dispwin.title("Master Application - View Data")
    dispwin.geometry("1920x1080")
    bgpic=resize_image("Viewdata_BG.png",dispwin.winfo_screenwidth(),dispwin.winfo_screenheight())
    canvas = Canvas(dispwin, width=dispwin.winfo_screenwidth(), height=dispwin.winfo_screenheight())
    
    canvas.pack(fill="both", expand=True)
    bg_image1 = canvas.create_image(0, 0, anchor="nw", image=bgpic)
    title1=Label(dispwin,text="List Of Projects",font=("CanterBold",35),fg="Black",bg="#7393A7")
    title1.place(x=600,y=10)
    delete_all=Label(dispwin,text="DELETE ALL",font=("Roboto",15,"underline"),fg="red",bg="#7393A7")
    delete_all.bind("<Button-1>",lambda event=None:deleteAll())
    delete_all.place(x=1000,y=30)
    placeback(dispwin,"#7393A7")
    if win.attributes('-fullscreen'):
        toggle_fullscreen(dispwin)
    dispwin.bind("<F11>",lambda event:toggle_fullscreen(dispwin,event))
    conn=mysql.connector.connect(host=open_ip(),user="root",password="swsc1234",database="projectdetails")
    cursor=conn.cursor()
    cursor.execute("SELECT * From project_table")
    alldata=list(cursor.fetchall())
    creategrid(alldata)
    dispwin.mainloop()

#----------------------------------------------------------------------------#
     # Initialize The Main Screen
#----------------------------------------------------------------------------#

def main(): 

    global win, canvas, bg_image,photo,fontss
    win = Tk()  
    win.title("DigiVote-Master Application")
    win.geometry("1920x1080")
    win.bind("<F11>",lambda event:toggle_fullscreen(win,event))
    win.attributes("-fullscreen",True)
    bgpic=resize_image("BGIMG.png",win.winfo_screenwidth(),win.winfo_screenheight())
    canvas = Canvas(win, width=win.winfo_screenwidth(), height=win.winfo_screenheight())
    canvas.pack(fill="both", expand=True)
    bg_image1 = canvas.create_image(0, 0, anchor="nw", image=bgpic)
    v_label=Label(text="        DigiVote  ",font=("CanterBold",80),fg="White",bd=0,highlightthickness=0)
    v_label.configure(bg="#794719")
    v_label.place(x=100,y=300)
    ms_label=Label(text="Master Application-Administrative Use Only",font=("CanterBold",50),fg="White")
    ms_label.configure(bg="#794719")
    ms_label.place(x=20,y=600)
    addip=Button(text=" Add IP  ",font=("Cantica",28,"bold"),padx=44,command=add_ip)
    addip.place(x=1100,y=400)

    view_data=Button(text="View Data",font=("Cantica",28,"bold"),padx=30,command=dispdata)
    view_data.place(x=1100,y=300)
    add_data=Button(text="Add Data",font=("Cantica",28,"bold"),padx=35,command=adddata)
    add_data.place(x=1100,y=500)

    win.mainloop()

#----------------------------------------------------------------------------#
    #Start The Application
#----------------------------------------------------------------------------#
    
if __name__=="__main__":
    main()
