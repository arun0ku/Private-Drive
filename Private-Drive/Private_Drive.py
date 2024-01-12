from tkinter import *
import customtkinter as ctk
from tkinter import filedialog
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image, ImageTk
from tkinter import messagebox
import webbrowser
import os

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
# ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

url = 'https://drive.google.com/drive/folders/1_Y4mZbK4DHHct9G3CatKsVL2IBD2Iepp?usp=drive_link'

def upload_to_google_drive(file_path):
    # Path to your credentials.json file
    credentials_file = 'credentials.json'

    # Create credentials object from the JSON file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file,
        scopes=['https://www.googleapis.com/auth/drive']  # Scopes required for Drive API
    )

    # Create a Drive service using the credentials
    drive_service = build('drive', 'v3', credentials=credentials)

    # Prepare file metadata
    file_metadata = {'parents': ['1_Y4mZbK4DHHct9G3CatKsVL2IBD2Iepp']}

    # Upload the file to Google Drive
    media = MediaFileUpload(file_path)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    messagebox.showinfo('Private Drive','File Upload Successfully ', parent=root)
    print('File uploaded. File ID:', file.get('id'))

def select_file_and_upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        upload_to_google_drive(file_path)

def callback():
    webbrowser.open_new(url)
   

# Tkinter window setup
root = ctk.CTk()
root.title("Upload File to Google Drive")
root.minsize(500,550)
root.geometry('600x650')
# root.resizable(500,600)

img = ctk.CTkImage(Image.open('images/pattern.jpg'), size=(1550,850))
imglbl = ctk.CTkLabel(root, image=img)
imglbl.pack(fill=BOTH, expand=TRUE)

mainframe = ctk.CTkFrame(imglbl, width=1300, height=700, fg_color='#00B2EE', corner_radius=100, bg_color='white')
mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)

lbl = ctk.CTkLabel(mainframe, text='--- PRIVATE DRIVE ---', font=('Century Gothic',72,'bold'), text_color='white').place(relx=0.23, rely=0.1)

img = ctk.CTkImage(Image.open('images/upload2.png'),size=(80,80))
uploadbtn = ctk.CTkButton(mainframe, image=img, corner_radius=50, hover_color='white', fg_color='transparent', text_color='black', border_width=2, border_color='white', text="Select File and Upload.......", font=('Century Gothic',24,'bold'), command=select_file_and_upload).place(relx=0.35, rely=0.4)

img2 = ctk.CTkImage(Image.open('images/download2.png'),size=(80,80))
downloadbtn = ctk.CTkButton(mainframe, image=img2, corner_radius=50, hover_color='white', fg_color='transparent', text_color='black', border_width=2, border_color='white', text="Select File and download..", font=('Century Gothic',24,'bold'), command=callback).place(relx=0.35, rely=0.6)


root.mainloop()
