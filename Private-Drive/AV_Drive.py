import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import filedialog
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import FileIO
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
from CTkListbox import *
from CTkToolTip import *
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import mimetypes
import os, sys 


###  https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


def main():
    win=ctk.CTk()
    app=Drive(win)
    win.mainloop()

class Drive(ctk.CTkTabview):
    def __init__(self, root):
        self.root = root
        self.root.after(0, lambda:root.state('zoomed'))
        self.root.title("Private Drive")
        self.root.minsize(1200,780)
        self.credentials_file = resource_path("data\\credentials.json")

            # Create credentials object from the JSON file
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file,scopes=['https://www.googleapis.com/auth/drive']  )# Scopes required for Drive API

    # Create a Drive service using the credentials
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

############################################################### MAIN GUI #################################################################################################################################################################################################
    
        self.mainfm = ctk.CTkFrame(self.root, fg_color='#eefbff')
        self.mainfm.pack(expand=True, fill=tk.BOTH)

        self.img = ctk.CTkImage(Image.open(resource_path('image\\AVs.png')), size=(350,150))
        self.imglbl = ctk.CTkLabel(self.mainfm, image=self.img, text='')
        self.textlbl = ctk.CTkLabel(self.mainfm, text='Drive', font=('Times New Roman',62), bg_color='#eefbff', fg_color='#eefbff', text_color='black')
        self.imglbl.place(relx=0.05,rely=0.13, anchor='center')
        self.textlbl.place(relx=0.13,rely=0.12, anchor='center')

        ctk.CTkButton(self.mainfm, corner_radius=20, text='+ New', height=80, bg_color='#eefbff', fg_color='white', hover_color='#e4e4e4', font=('Arial',28), text_color='black', command=self.folder1).place(relx=0.07, rely=0.24, anchor='center')
      
######################################################### TAB VIEW #####################################################################################
      
        
        self.tableframe = ctk.CTkFrame(self.mainfm, corner_radius=20, fg_color='white', bg_color='#eefbff', border_width=2)
        self.tableframe.place(relx=0.6, rely=0.5, anchor='center')

        self.tabview = ctk.CTkTabview(self.tableframe, corner_radius=20, fg_color='white', bg_color='#eefbff', border_width=0, segmented_button_selected_color='#b6e6e9', segmented_button_unselected_color='white', segmented_button_fg_color='white', segmented_button_selected_hover_color='#eaeaea', segmented_button_unselected_hover_color='#eaeaea')
        self.tabview._segmented_button.configure(font=('times new roman', 24, 'bold'), text_color='black', corner_radius=50)
        # place(relx=0.6, rely=0.5, anchor='center')
        self.tabview.add('≡')
        self.tabview.add('📁')
        self.tabview.pack(fill=BOTH, expand=True)
        self.tabview._segmented_button.grid(row=1, column=0,sticky="E")

        self.up_frame = ctk.CTkFrame(self.tabview.tab('≡'), height=150, fg_color='white', border_width=0)
        self.up_frame.pack(fill = BOTH)

        self.mydrive = ctk.CTkLabel(self.up_frame, text='My Drive', text_color='black', font=('Arial',30), bg_color='white', fg_color='white', corner_radius=100, width=0)
        self.mydrive.place(relx=0.07, rely=0.5, anchor='center')

        self.up_btn = ctk.CTkButton(self.up_frame, corner_radius=20, text='↑ upload folder', width=0, bg_color='white', fg_color='#eefbff', hover_color='white', border_color='#eefbff', border_width=4, font=('Arial',22, 'bold'), text_color='black', command=self.upload_folder)
        self.up_btn.place(relx=0.78, rely=0.8, anchor='center')
        CTkToolTip(self.up_btn, delay=0, message='Upload file')
     
        
################################################### TREEVIEW FOLDER LIST #########################################################################################################################

    
        self.table = ctk.CTkFrame(self.tabview.tab('≡'), bg_color='white', border_width=0)
        self.table.pack(padx=5, pady=5)
        # place(relx=0.5, rely=0.58, anchor=CENTER)

        self.scroll_y = ctk.CTkScrollbar(self.table, orientation=VERTICAL, fg_color='white', bg_color='white')

        self.style = ttk.Style(self.tabview.tab('≡'))
            # set ttk theme to "clam" which support the fieldbackground option
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", background="white", foreground="black", font=('Arial', 18, 'bold'))
        self.style.configure("Treeview", font=('Arial', 16),  rowheight=40)


        self.treeview = ttk.Treeview(self.table, columns=('name', 'type', 'id'), height=14, cursor='hand2')

        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.scroll_y.configure(command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scroll_y.set)

        self.treeview.heading('name', text='Name', anchor='w')
        self.treeview.heading('type', text='Type', anchor='w')
        self.treeview.heading('id', text='id')

        self.treeview['show'] = 'headings'

        self.treeview.column('name', width=600)
        self.treeview.column('type', width=700)
        self.treeview.column('id', width=1)
        
        # Fetch and display root folders
        self.treeview.pack(expand=True, fill=tk.BOTH)
        self.treeview.bind("<Double-1>", self.get_cursor)
        self.treeview.bind("<Return>", self.get_cursor)
        self.treeview.bind("<ButtonRelease-1>", self.get_name)
        self.display_folder_contents("root")

        self.create_widgets()

    def listb(self):
        self.labelfram = ctk.CTkFrame(self.mainfm, corner_radius=25, fg_color='white', bg_color='white', border_width=2)
        self.labelfram.place(relx=0.85, rely=0.9, anchor='center')

        self.listbox = CTkListbox(self.labelfram, width=350, height=150, corner_radius=25, bg_color='white', fg_color='white', text_color='black', font=('Arial',18,'bold'), border_width=2)
        self.listbox.pack(fill=BOTH, expand=True)

        self.crossbtn = ctk.CTkButton(self.listbox, text='╳', font=('times new roman',18,'bold'), text_color='black', width=0, bg_color='white', fg_color='white', hover_color='#e4e4e4', command=self.cross)
        self.crossbtn.pack(padx=15, anchor='e')

        # place(relx=0.88, rely=0.74, anchor='center')

    def cross(self):
        self.labelfram.destroy()


    def btn_list(self, root):
        self.btn_label = tk.StringVar()
        self.btn_l = ctk.CTkLabel(self.up_frame, textvariable=self.btn_label, width=700, height=40, corner_radius=50, text_color='black', fg_color='#eefbff', bg_color='white', font=('Arial',20, 'bold'), anchor='w').place(relx=0.34, rely=0.8, anchor = 'center')
        
        self.new_flder = ctk.CTkButton(self.up_frame, corner_radius=20, text='+', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20, 'bold'), text_color='black', command=self.folder0)
        self.new_flder.place(relx=0.58, rely=0.8, anchor='center')
        CTkToolTip(self.new_flder, delay=0, message="New Folder")

        self.del_flder = ctk.CTkButton(self.up_frame, corner_radius=20, text='🗑', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20), text_color='black', command=self.delete_file)
        self.del_flder.place(relx=0.63, rely=0.8, anchor='center')
        CTkToolTip(self.del_flder, delay=0, message="Delete")
        
        
    def btn_file(self, root):
        self.file_label = tk.StringVar()
        ctk.CTkLabel(self.up_frame, textvariable=self.file_label, width=700, height=40, corner_radius=50, text_color='black', fg_color='#eefbff', bg_color='white', font=('Arial',20, 'bold'), anchor='w').place(relx=0.34, rely=0.8, anchor = 'center')
        
        self.down_file = ctk.CTkButton(self.up_frame, corner_radius=20, text='↓', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20, 'bold','underline'), text_color='black', command=self.download_fun)
        self.down_file.place(relx=0.58, rely=0.8, anchor='center')
        CTkToolTip(self.down_file, delay=0, message="Download")

        self.del_file = ctk.CTkButton(self.up_frame, corner_radius=20, text='🗑', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20), text_color='black', command=self.delete_file)
        self.del_file.place(relx=0.63, rely=0.8, anchor='center')
        CTkToolTip(self.del_file, delay=0, message="Delete")

#################################################### FOLDER LIST ######################################################################
 
    def display_folder_contents(self, folder_id):
        # Clear existing tree items
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        query = f"'1_Y4mZbK4DHHct9G3CatKsVL2IBD2Iepp' in parents"
        self.results = self.drive_service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
        self.folders = self.results.get('files', [])

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for folder in self.folders:
            self.name = folder['name']
            self.type = folder['mimeType']
            self.folder_id = folder['id']
            self.treeview.insert("", "end", values=(self.name, self.type, self.folder_id))

            self.refresh_btn = ctk.CTkButton(self.up_frame, corner_radius=20, text='↻ Refresh', width=0, bg_color='white', fg_color='#eefbff', hover_color='white', border_color='#eefbff', border_width=4, font=('Arial',22, 'bold'), text_color='black', command=lambda folder_id=folder_id: self.display_folder_contents(folder_id))
            self.refresh_btn.place(relx=0.94, rely=0.8, anchor='center')
            CTkToolTip(self.refresh_btn, delay=0, message='Refresh')

################################################################# ALL FUNCTION ################################################################################################################################################################################################################################

    def folder1(self):
        
        self.new_folder = ctk.CTkFrame(self.root, width=300, height=250, corner_radius=25, fg_color='white', bg_color='#eefbff')
        self.new_folder.place(relx=0.12, rely=0.34, anchor='center')

        ctk.CTkLabel(self.new_folder, text='New Folder', font=('Arial', 28), text_color='black').place(relx=0.4, rely=0.3, anchor='center')
        self.entry = tk.StringVar()
        ctk.CTkEntry(self.new_folder, textvariable=self.entry, width=250, bg_color='white', border_color='#3c428f', fg_color='white', border_width=2, font=('Arial',24), text_color='black').place(relx=0.5, rely=0.5, anchor='center')
        
        ctk.CTkButton(self.new_folder, text='Cancel', width=1, font=('Arial', 16), text_color='#3c428f', bg_color='white', fg_color='white', corner_radius=100, hover_color='#f0f0f0', command=self.clear).place(relx=0.48, rely=0.8, anchor='center')
        ctk.CTkButton(self.new_folder, text='Create', width=1, font=('Arial', 16), text_color='#3c428f', bg_color='white', fg_color='white', corner_radius=100, hover_color='#f0f0f0', command=self.create_folder).place(relx=0.75, rely=0.8, anchor='center')

    def clear(self):
        self.new_folder.destroy()

    def folder0(self):
        
        self.new_folder0 = ctk.CTkFrame(self.root, width=300, height=250, corner_radius=25, fg_color='white', bg_color='#eefbff')
        self.new_folder0.place(relx=0.12, rely=0.34, anchor='center')

        ctk.CTkLabel(self.new_folder0, text='New Folder', font=('Arial', 28), text_color='black').place(relx=0.4, rely=0.3, anchor='center')
        self.entry0 = tk.StringVar()
        ctk.CTkEntry(self.new_folder0, textvariable=self.entry0, width=250, bg_color='white', border_color='#3c428f', fg_color='white', border_width=2, font=('Arial',24), text_color='black').place(relx=0.5, rely=0.5, anchor='center')
        
        ctk.CTkButton(self.new_folder0, text='Cancel', width=1, font=('Arial', 16), text_color='#3c428f', bg_color='white', fg_color='white', corner_radius=100, hover_color='#f0f0f0', command=self.clear0).place(relx=0.48, rely=0.8, anchor='center')
        ctk.CTkButton(self.new_folder0, text='Create', width=1, font=('Arial', 16), text_color='#3c428f', bg_color='white', fg_color='white', corner_radius=100, hover_color='#f0f0f0', command=self.create_folder0).place(relx=0.75, rely=0.8, anchor='center')

    def clear0(self):
        self.new_folder0.destroy()

    def download_fun(self):
        self.listb()
        item = self.treeview.selection()
        folder_name = self.treeview.item(item, "values")[0]
        id = self.treeview.item(item, "values")[2]
        
        if not id:
            print("Please enter a valid Google Drive file ID.")
            return
        self.types = [('All Files','*.*'),("Text files", "*.txt"),('PNG','*.png'),('JPG','*.jpg'),('JPEG','jpeg'),('Python files','*.py *.pyw')] 
        # Choose a local file to save the downloaded file
        file_path = filedialog.asksaveasfilename(initialfile= folder_name ,filetypes= self.types, defaultextension=self.type)

        if not file_path:
            print("Download canceled.")
            return
        
        # Download the file
        request = self.drive_service.files().get_media(fileId=id)
        fh = FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
            self.listbox.insert(tk.END, f"\nDOWNLOADING\n\t{file_path.split('/')[-1]}\n\tDownload {int(status.progress() * 100)}%.\t👌")
        messagebox.showinfo('Download',f'{file_path.split("/")[-1]} download successfully')

        print(f"File downloaded to: {file_path}")

############################################### CREATE FOLDER TO GOOGLE DRIVE #########################################################
    def create_folder(self):
        # self.folder1
        self.folder = self.entry.get()
        if self.folder:
            # Prepare file metadata
            self.file_metadata = {'parents': ['1_Y4mZbK4DHHct9G3CatKsVL2IBD2Iepp'], 'name': self.folder, 'mimeType': 'application/vnd.google-apps.folder'}
    # Create Folder to Google Drive
            self.file = self.drive_service.files().create(body=self.file_metadata,  fields='id').execute()
            self.update = messagebox.showinfo('New Folder',f'{self.folder}, folder is created successfully.')
            if self.update:
                self.clear()
                self.refresh()
                self.display_folder_contents('root')
        elif self.folder == '' and folder_id=='':
            messagebox.showerror('New Folder','Please Enter the Folder Name')
        else:
            messagebox.showerror('New Folder','Please Enter the Folder Name')
####################################################################################################
    def create_folder0(self):
        item = self.treeview.selection()
        folder_id = self.treeview.item(item, "values")[2]
        self.folder = self.entry0.get()
        # self.folder1
        if self.folder and folder_id:
            try:
                self.file_metadata = {'parents': [folder_id], 'name': self.folder, 'mimeType': 'application/vnd.google-apps.folder'}
    # Create Folder to Google Drive
                self.file = self.drive_service.files().create(body=self.file_metadata,  fields='id').execute()
                messagebox.showinfo('New Folder',f'{self.folder}, folder is created successfully.')
                self.clear0()
                self.refresh()
                self.list_files('root')
            except: AttributeError
        elif self.folder == '' and folder_id=='':
            messagebox.showerror('New Folder','Please Enter the Folder Name')
        else:
            messagebox.showerror('New Folder','Please Enter the Folder Name')
 
######################################## UPLOAD FILE TO GOOGLE DRIVE API ############################################################

    def upload_to_google_drive(self, file):
        item = self.treeview.selection()
        self.ID = self.treeview.item(item, "values")[2]
        if self.ID:
            # Prepare file metadata
            self.file_metadata = {'parents': [self.ID], 'name': file.split("/")[-1]}
    # Upload the file to Google Drive
            self.media = MediaFileUpload(file)
            self.file = self.drive_service.files().create(body=self.file_metadata, media_body=self.media, fields='id').execute()
            self.list_files('root')
            messagebox.showinfo('Private Drive','File upload successful', parent=self.root)
        else:
            messagebox.showerror('Uploading','Please Select the folder', parent=self.root)

    def upload(self):
        self.listb()
        item = self.treeview.selection()
        self.ID = self.treeview.item(item, "values")[2]
        if self.ID:
            files = filedialog.askopenfilenames()
            if files:            
                for file in files:
                    self.listbox.insert(tk.END,f'\n\tUploading File\n\n\t{file.split("/")[-1]}\t✅')
    
                self.upload_to_google_drive(file)
        else:
            messagebox.showinfo('Uploading','Please Select the folder', parent=self.root)

       
######################################################## GET CELL VALUE OF TREEVIEW ##################################################

   
    def get_cursor(self, event):
        try:
            item = self.treeview.selection()
            folder_id = self.treeview.item(item, "values")[2]
            self.tree_fun()
        except: IndexError


    def get_name(self, event):
        self.btn_list('root')
        try:
            self.id_value = self.treeview.item(self.treeview.focus(), "values")
            folder_name = self.id_value[0]
            folder_type = self.id_value[1]
            if folder_type == 'application/vnd.google-apps.folder':
                self.btn_label.set('')
                self.btn_label.set(folder_name)
            elif folder_type != 'application/vnd.google-apps.folder':
                self.btn_file('root')
                self.file_label.set('')
                self.file_label.set(folder_name)
        except: IndexError
        
        
# Function to delete selected file
    def delete_file(self):
        self.listb()
        selected_item = self.treeview.selection()
        if selected_item:
            selected_name = self.treeview.item(selected_item, 'values')[0]
            selected_id = self.treeview.item(selected_item, 'values')[2]
            msg = messagebox.askyesno('Delete Items',f"Do you want to delete folder: {selected_name}!")
            if msg:
                self.drive_service.files().delete(fileId=selected_id).execute()
                self.refresh()
                self.display_folder_contents('root')  # Refresh the file list after deletion
                self.listbox.insert(tk.END, f'\nDELETE\n\n{selected_name} folder,\nDeleted Successfully\t✅')
                messagebox.showinfo('Folder Deletion',f'{selected_name} folder, Deleted Successfully')
        else:
            messagebox.showinfo('Folder Deletion','Please Choose the Folder')

###################################################### DOWNLOAD THE FUNCTION ##########################################################

    def tree_fun(self):

        self.tableframe0 = ctk.CTkFrame(self.tabview.tab('≡'), corner_radius=20, fg_color='white', bg_color='#eefbff')
        self.tableframe0.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.second_frame = ctk.CTkFrame(self.tableframe0, height=150, fg_color='white', bg_color='white')
        self.second_frame.pack(fill = BOTH)

        self.backbtn = ctk.CTkButton(self.second_frame, text='➜', text_color='black', font=('Arial',22), hover_color='#dddddd', bg_color='white', fg_color='white', corner_radius=50, width=0, command=self.exit)
        self.backbtn.place(relx=0.04, rely=0.15, anchor='center')
        CTkToolTip(self.backbtn, delay=0, message='Back')

        self.headname = ctk.CTkButton(self.second_frame, text='My Drive', text_color='black', font=('Arial',30), hover_color='#dddddd', bg_color='white', fg_color='white', corner_radius=100, width=0, command=self.exit)
        self.headname.place(relx=0.08, rely=0.5, anchor='center')

        self.upl_btn = ctk.CTkButton(self.second_frame, corner_radius=22, text='↑ Upload file', width=0, bg_color='white', fg_color='#eefbff', hover_color='white', border_color='#eefbff', border_width=4, font=('Arial',22, 'bold'), text_color='black', command=self.upload)
        self.upl_btn.place(relx=0.82, rely=0.8, anchor='center')
        CTkToolTip(self.upl_btn, delay=0, message='Upload file')
 
        self.new_flder = ctk.CTkButton(self.second_frame, corner_radius=22, text='+ New', width=0, bg_color='white', fg_color='#eefbff', hover_color='white', border_color='#eefbff', border_width=4, font=('Arial',22, 'bold'), text_color='black', command=self.folder0)
        self.new_flder.place(relx=0.95, rely=0.8, anchor='center')
        CTkToolTip(self.new_flder, delay=0, message="New Folder")

        self.file_list = ctk.CTkFrame(self.tableframe0, width=500, height=500, bg_color='white', fg_color='white')
        self.file_list.pack(fill = BOTH, expand=True)

        self.lbl1 = tk.StringVar()
        self.id_label = ctk.CTkLabel(self.file_list, textvariable=self.lbl1, fg_color='white', bg_color='white', text_color='white')
        self.id_label.place(relx=0.5, rely=0.99, anchor='center')

        self.table1 = ctk.CTkFrame(self.file_list, bg_color='white')
        self.table1.pack(padx=5, pady=5)

        self.scroll_y = ctk.CTkScrollbar(self.table1, orientation=VERTICAL, fg_color='white', bg_color='white')

        self.style = ttk.Style(self.tableframe0)
            # set ttk theme to "clam" which support the fieldbackground option
        self.style.theme_use("clam")
        self.style.configure("Tree.Heading", background="white", foreground="black", font=('Arial', 18, 'bold'))
        self.style.configure("Tree", font=('Arial', 16), rowheight=40)

        self.second_tree()

    def second_tree(self):

        self.tree = ttk.Treeview(self.table1, columns=('name', 'type', 'id'), height=14, cursor='hand2')

        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.scroll_y.configure(command=self.tree.yview)

        self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.tree.heading('name', text='Folder_Name', anchor='w')
        self.tree.heading('type', text='Folder_Type', anchor='w')
        self.tree.heading('id', text='Folder_id', anchor='e')

        self.tree['show'] = 'headings'

        self.tree.column('name', width=600)
        self.tree.column('type', width=700)
        self.tree.column('id', width=1, anchor='e')
        
        # Fetch and display root folders
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<ButtonRelease-1>", self.get_value)
        self.list_files('root')

    def fldr_list(self, root):
        self.fldr_label = tk.StringVar()
        self.fldr_l = ctk.CTkLabel(self.second_frame, textvariable=self.fldr_label, width=750, height=40, corner_radius=50, text_color='black', fg_color='#eefbff', bg_color='white', font=('Arial',20, 'bold'), anchor='w').place(relx=0.36, rely=0.8, anchor = 'center')
        
        self.del_flder0 = ctk.CTkButton(self.second_frame, corner_radius=20, text='🗑', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20), text_color='black', command=self.delete)
        self.del_flder0.place(relx=0.68, rely=0.8, anchor='center')
        CTkToolTip(self.del_flder0, delay=0, message="Delete")

      
    def btn_file0(self, root):
        self.file_label0 = tk.StringVar()
        ctk.CTkLabel(self.second_frame, textvariable=self.file_label0, width=750, height=40, corner_radius=50, text_color='black', fg_color='#eefbff', bg_color='white', font=('Arial',20, 'bold'), anchor='w').place(relx=0.36, rely=0.8, anchor = 'center')

        self.down_file0 = ctk.CTkButton(self.second_frame, corner_radius=20, text='↓', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20, 'bold','underline'), text_color='black', command=self.download_file0)
        self.down_file0.place(relx=0.62, rely=0.8, anchor='center')
        CTkToolTip(self.down_file0, delay=0, message="Download")

        self.del_file0 = ctk.CTkButton(self.second_frame, corner_radius=20, text='🗑', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20), text_color='black', command=self.delete)
        self.del_file0.place(relx=0.67, rely=0.8, anchor='center')
        CTkToolTip(self.del_file0, delay=0, message="Delete")


    def exit(self):
        self.tableframe0.destroy()


# Function to delete selected file
    def delete(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_name = self.tree.item(selected_item, 'values')[0]
            selected_id = self.tree.item(selected_item, 'values')[2]
            self.drive_service.files().delete(fileId=selected_id).execute()
            self.list_files('root')  # Refresh the file list after deletion
            messagebox.showinfo('Folder Deletion',f'{selected_name} folder, Deleted Successfully')
        else:
            messagebox.showinfo('Folder Deletion','Please Choose the Folder')



    def get_value(self,folder_id,event=''):
        self.fldr_list('root')
        try:
            self.id_value = self.tree.item(self.tree.focus(), "values")
            self.folder_name = self.id_value[0]
            self.folder_type = self.id_value[1]
            self.folder_id = self.id_value[2]
            print(self.folder_id)
            self.lbl1.set(self.folder_id)
            print(self.folder_type)
            if self.folder_type == 'application/vnd.google-apps.folder':
                self.fldr_label.set(self.folder_name)
            elif self.folder_type != 'application/vnd.google-apps.folder':
                self.btn_file0('root')
                self.file_label0.set(self.folder_name)
        except: IndexError
            

    def list_files(self, folder):
        item = self.treeview.selection()
        folder_id = self.treeview.item(item, "values")[2]
        
        # Clear existing tree items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Call the Drive API
        self.results = self.drive_service.files().list( q=f"'{folder_id}' in parents", fields="files(id, name, mimeType)").execute()
        self.files = self.results.get('files', [])

        for file in self.files:
            file_name = file['name']
            file_id = file['id']
            file_type = file['mimeType']

            # Insert the file information into the TreeView
            self.tree.insert('', 'end', text=file_name, values=(file_name, file_type, file_id))

    def download_file0(self):
        self.id_value = self.tree.item(self.tree.focus(), "values")
        file_name = self.id_value[0]
        file_id = self.id_value[2]


        if not file_id:
            print("Please enter a valid Google Drive file ID.")
            return
        self.types = [('All Files','*.*'),("Text files", "*.txt"),('PNG','*.png'),('JPG','*.jpg'),('JPEG','jpeg'),('Python files','*.py *.pyw')] 
        # Choose a local file to save the downloaded file
        file_path = filedialog.asksaveasfilename(initialfile = file_name,filetypes= self.types, defaultextension=self.types)

        if not file_path:
            print("Download canceled.")
            return
        
        # Download the file
        request = self.drive_service.files().get_media(fileId=file_id)
        fh = FileIO(file_path, 'wb') 
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
            messagebox.showinfo('Download',f'{file_path.split("/")[-1]} download successfully')

        print(f"File downloaded to: {file_path}")


  ############################################################### #########################################################################################################

    def create_widgets(self):

        # self.current_dir = os.getcwd()

        self.up_frame1 = ctk.CTkFrame(self.tabview.tab('📁'), height=150, fg_color='white', border_width=0)
        self.up_frame1.pack(fill = BOTH)

        self.mydrive = ctk.CTkLabel(self.up_frame1, text='My Drive', text_color='black', font=('Arial',30), bg_color='white', fg_color='white', corner_radius=100, width=0)
        self.mydrive.place(relx=0.07, rely=0.5, anchor='center')

        self.up_btn = ctk.CTkButton(self.up_frame1, corner_radius=20, text='↑ upload folder', width=0, bg_color='white', fg_color='#eefbff', hover_color='white', border_color='#eefbff', border_width=4, font=('Arial',22, 'bold'), text_color='black', command=self.upload_folder)
        self.up_btn.place(relx=0.78, rely=0.8, anchor='center')
        CTkToolTip(self.up_btn, delay=0, message='Upload file')

        self.refresh_btn1 = ctk.CTkButton(self.up_frame1, corner_radius=20, text='↻ Refresh', width=0, bg_color='white', fg_color='#eefbff', hover_color='white', border_color='#eefbff', border_width=4, font=('Arial',22, 'bold'), text_color='black', command=self.refresh)
        self.refresh_btn1.place(relx=0.94, rely=0.8, anchor='center')
        CTkToolTip(self.refresh_btn1, delay=0, message='Refresh')

        self.tabframe1 = ctk.CTkFrame(self.tabview.tab('📁'))
        self.tabframe1.pack(fill=BOTH, expand=True)

        self.folder_canvas = ctk.CTkCanvas(self.tabframe1, bg="white", width=1320, height=600)
        self.folder_canvas.pack(padx=5, pady=5)

        self.refresh()
 
    def btn_bar(self, root):
        self.file_label1 = tk.StringVar()
        ctk.CTkLabel(self.up_frame1, textvariable=self.file_label1, width=0, corner_radius=50, text_color='white', fg_color='white', bg_color='white').place(relx=0.99, rely=0.99, anchor = 'center')
        
        self.file_label2 = tk.StringVar()
        ctk.CTkLabel(self.up_frame1, textvariable=self.file_label2, width=700, height=40, corner_radius=50, text_color='black', fg_color='#eefbff', bg_color='white', font=('Arial',20, 'bold'), anchor='w').place(relx=0.34, rely=0.8, anchor = 'center')
        
        self.down_file2 = ctk.CTkButton(self.up_frame1, corner_radius=20, text='↓', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20, 'bold','underline'), text_color='black', command=self.download_selected_folder)
        self.down_file2.place(relx=0.58, rely=0.8, anchor='center')
        CTkToolTip(self.down_file2, delay=0, message="Download folder")

        self.del_file2 = ctk.CTkButton(self.up_frame1, corner_radius=20, text='🗑', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20), text_color='black', command=self.delete_selected_folder)
        self.del_file2.place(relx=0.63, rely=0.8, anchor='center')
        CTkToolTip(self.del_file2, delay=0, message="Delete")


    def refresh(self):
        self.folder_canvas.delete("all")
        folders = self.list_folders()
        x = 10
        y = 10
        icon_size = 80

        self.folder_buttons = []

        for folder in folders:
            folder_name = folder['name']
            folder_id = folder['id']
            thumbnail_link = folder.get('thumbnailLink')
            if thumbnail_link:
                thumbnail = self.get_thumbnail(thumbnail_link)
                image = ctk.CTkImage(thumbnail.resize((icon_size, icon_size)))
            else:
                image = ctk.CTkImage(Image.open(resource_path("image\\folder_icon.png")), size=(icon_size, icon_size))

            btn = ctk.CTkButton(self.folder_canvas, image=image, text=folder_name, fg_color='white', text_color='black', compound=tk.BOTTOM)
            # , command=lambda folder_id=folder_id, folder_name=folder_name: self.on_folder_select(folder_id, folder_name)
            btn.image = image
            self.folder_canvas.create_window(x, y, window=btn, anchor="nw")
            btn.bind("<ButtonRelease-1>", lambda event, folder_id=folder_id, folder_name=folder_name: self.on_folder_select(folder_id, folder_name))
            btn.bind("<Double-1>", lambda event, folder_id=folder_id, folder_name=folder_name: self.doubleclick(folder_id, folder_name))
            self.folder_buttons.append(btn)
            x += icon_size + 105
            if x > 1200:
                x = 10
                y += icon_size + 80

    def list_folders(self):
        """
        List folders from Google Drive.
        """
        query = f"'1_Y4mZbK4DHHct9G3CatKsVL2IBD2Iepp' in parents"
        results = self.drive_service.files().list(q=query, fields="nextPageToken, files(id, name, thumbnailLink)").execute()
        items = results.get('files', [])
        return items

    def on_folder_select(self, folder_id, folder_name):
        self.btn_bar('root')
        self.selected_folder_id = folder_id
        self.selected_folder_name = folder_name
        self.file_label1.set(self.selected_folder_id)
        self.file_label2.set(self.selected_folder_name)


    def download_selected_folder(self):
        if hasattr(self, 'selected_folder_id'):
            destination = filedialog.askdirectory(title="Select download directory")
            if destination:
                folder_name = self.get_folder_name(self.selected_folder_id)
                folder_path = os.path.join(destination, folder_name)
                os.makedirs(folder_path, exist_ok=True)

                query = f"'{self.selected_folder_id}' in parents"
                files = self.drive_service.files().list(q=query).execute().get('files', [])
                for file in files:
                    file_name = file['name']
                    file_id = file['id']
                    file_path = os.path.join(folder_path, file_name)
                    self.download_file(file_id, file_path)
                messagebox.showinfo("Success", f"{folder_name} folder downloaded successfully.")
        else:
            messagebox.showerror("Error", "Please select a folder first.")

    def download_file(self, file_id, file_path):
        """
        Download file from Google Drive.
        """
        request = self.drive_service.files().get_media(fileId=file_id)
        fh = open(file_path, 'wb')
        downloader = request.execute()
        fh.write(downloader)
        fh.close()

    def get_folder_name(self, folder_id):
        """
        Get folder name by ID.
        """
        folder = self.drive_service.files().get(fileId=folder_id).execute()
        return folder['name']


    def delete_selected_folder(self):
        if hasattr(self, 'selected_folder_id'):
            result = messagebox.askquestion("Delete Folder", "Are you sure you want to delete this folder?")
            if result == "yes":
                try:
                    folder_name = self.get_folder_name(self.selected_folder_id)
                    self.drive_service.files().delete(fileId=self.selected_folder_id).execute()
                    messagebox.showinfo("Success", f"{folder_name} folder deleted successfully.")
                    self.refresh()
                    self.display_folder_contents('root')
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Please select a folder first.")

    def get_thumbnail(self, thumbnail_link):
        response = self.drive_service.files().get_media(fileId=thumbnail_link).execute()
        return Image.open(BytesIO(response))


    def upload_folder(self):
        folder_path = filedialog.askdirectory(title="Select folder to upload")
        if folder_path:
            folder_name = os.path.basename(folder_path)
            folder_metadata = {
                'parents': ['1_Y4mZbK4DHHct9G3CatKsVL2IBD2Iepp'],
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.drive_service.files().create(body=folder_metadata, fields='id').execute()
            folder_id = folder.get('id')

            for root, dirs, files in os.walk(folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    self.upload_file(file_path, folder_id)
                    self.refresh()
                    self.display_folder_contents('root')

            messagebox.showinfo("Success", f"{folder_name} folder uploaded successfully.")

    def upload_file(self, file_path, folder_id):
        file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
        mime_type, _ = mimetypes.guess_type(file_path)
        media = MediaFileUpload(file_path, mimetype=mime_type)
        self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()


    def upload_to_google_drive0(self, file):
        self.id = self.file_label1.get()
        if self.id:
            # Prepare file metadata
            self.file_metadata = {'parents': [self.id], 'name': file.split("/")[-1]}
    # Upload the file to Google Drive
            self.media = MediaFileUpload(file)
            self.file = self.drive_service.files().create(body=self.file_metadata, media_body=self.media, fields='id').execute()
            self.refresh01()
            messagebox.showinfo('Private Drive','File upload successful', parent=self.root)
        else:
            messagebox.showerror('Uploading','Please Select the folder', parent=self.root)

    def upload0(self):
        self.listb()
        self.id = self.file_label1.get()
        if self.id:
            files = filedialog.askopenfilenames()
            if files:            
                for file in files:
                    self.listbox.insert(tk.END,f'\n\tUploading File\n\n\t{file.split("/")[-1]}\t✅')
    
                self.upload_to_google_drive0(file)
        else:
            messagebox.showinfo('Uploading','Please Select the folder', parent=self.root)


######################################################################################################################################################
##########################################################################################################################################
 

    def doubleclick(self, folder_id, folder_name):

        self.tab2frame = ctk.CTkFrame(self.tabview.tab('📁'), border_width=0, bg_color='white', fg_color='white')
        self.tab2frame.place(relx=0.5, rely=0.5, anchor='center') 

        self.up_frame2 = ctk.CTkFrame(self.tab2frame, height=150, fg_color='white', border_width=0)
        self.up_frame2.pack(fill = BOTH)

        self.backbtn0 = ctk.CTkButton(self.up_frame2, text='➜', text_color='black', font=('Arial',22), hover_color='#dddddd', bg_color='white', fg_color='white', corner_radius=50, width=0, command=self.exit01)
        self.backbtn0.place(relx=0.03, rely=0.15, anchor='center')
        CTkToolTip(self.backbtn0, delay=0, message='Back')


        self.mydrive = ctk.CTkLabel(self.up_frame2, text='My Drive', text_color='black', font=('Arial',30), bg_color='white', fg_color='white', corner_radius=100, width=0)
        self.mydrive.place(relx=0.07, rely=0.5, anchor='center')

        self.up_btn = ctk.CTkButton(self.up_frame2, corner_radius=20, text='↑ upload file', width=0, bg_color='white', fg_color='#eefbff', hover_color='white', border_color='#eefbff', border_width=4, font=('Arial',22, 'bold'), text_color='black', command=self.upload0)
        self.up_btn.place(relx=0.8, rely=0.8, anchor='center')
        CTkToolTip(self.up_btn, delay=0, message='Upload file')

        self.refresh_btn1 = ctk.CTkButton(self.up_frame2, corner_radius=20, text='↻ Refresh', width=0, bg_color='white', fg_color='#eefbff', hover_color='white', border_color='#eefbff', border_width=4, font=('Arial',22, 'bold'), text_color='black', command=self.refresh01)
        self.refresh_btn1.place(relx=0.94, rely=0.8, anchor='center')
        CTkToolTip(self.refresh_btn1, delay=0, message='Refresh')

        self.tabframe1 = ctk.CTkFrame(self.tab2frame, border_width=0, bg_color='white', fg_color='white')
        self.tabframe1.pack(fill=BOTH, expand=True)

        self.folder_canvas0 = ctk.CTkCanvas(self.tabframe1, bg="white", width=1320, height=600)
        self.folder_canvas0.pack(padx=5, pady=5)


    # def doubleclick(self, folder_id, folder_name):
        files = self.list_files_in_folder(folder_id)
        self.folder_canvas.delete("all")
        x = 20
        y = 20
        icon_size = 80

        self.folder_buttons = []
        
        for file in files:
            file_name = file['name']
            file_id = file['id']
            file_icon = self.get_file_icon(file_name)
            image = ctk.CTkImage(file_icon, size=(icon_size, icon_size))

            btn = ctk.CTkButton(self.folder_canvas0, width=100, height=100, fg_color='white', bg_color='white', font=('Times New Roman',12), text_color='black', image=image, text=file_name, compound=tk.BOTTOM)
            btn.image = image
            # btn.bind("<ButtonRelease-1>", self.on_click)
            self.folder_canvas0.create_window(x, y, window=btn, anchor="nw")
            btn.bind("<ButtonRelease-1>", lambda event, file_id=file_id, file_name=file_name: self.on_click(file_id, file_name))
            self.folder_buttons.append(btn)
            x += icon_size + 120
            if x>1150:
                x = 20
                y += icon_size + 40


    def exit01(self):
        self.tab2frame.destroy()
        self.refresh()
    
    def btn_bar01(self, root):
        self.file_label10 = tk.StringVar()
        ctk.CTkLabel(self.up_frame2, textvariable=self.file_label10, corner_radius=50, text_color='white', fg_color='white', bg_color='white').place(relx=0.99, rely=0.99, anchor = 'center')
        
        self.file_label0 = tk.StringVar()
        ctk.CTkLabel(self.up_frame2, textvariable=self.file_label0, width=700, height=40, corner_radius=50, text_color='black', fg_color='#eefbff', bg_color='white', font=('Arial',20, 'bold'), anchor='w').place(relx=0.34, rely=0.8, anchor = 'center')
        
        self.down_file01 = ctk.CTkButton(self.up_frame2, corner_radius=20, text='↓', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20, 'bold','underline'), text_color='black')
        self.down_file01.place(relx=0.58, rely=0.8, anchor='center')
        CTkToolTip(self.down_file01, delay=0, message="Download")

        self.del_file01 = ctk.CTkButton(self.up_frame2, corner_radius=20, text='🗑', width=0, bg_color='#eefbff', fg_color='#eefbff', hover_color='white', font=('Arial',20), text_color='black', command=self.delete_selected_folder0)
        self.del_file01.place(relx=0.63, rely=0.8, anchor='center')
        CTkToolTip(self.del_file01, delay=0, message="Delete")

    def on_click(self, file_id, file_name):
        self.btn_bar01('root')
        self.selected_file_id0 = file_id
        self.selected_file_name = file_name
        self.file_label10.set(self.selected_file_id0)
        self.file_label0.set(self.selected_file_name)

    def list_files_in_folder(self, folder_id):
        """
        List files in a specific folder from Google Drive.
        """
        query = f"'{folder_id}' in parents"
        results = self.drive_service.files().list(q=query).execute()
        items = results.get('files', [])
        return items

    def refresh01(self):
        self.folder_canvas.delete("all")
        files0 = self.refresh0()
        x = 20
        y = 20
        icon_size = 80

        self.folder_buttons = []
        
        for file in files0:
            file_name = file['name']
            file_id = file['id']
            file_icon = self.get_file_icon(file_name)
            image = ctk.CTkImage(file_icon, size=(icon_size, icon_size))

            btn = ctk.CTkButton(self.folder_canvas0, width=100, height=100, fg_color='white', bg_color='white', font=('Times New Roman',12), text_color='black', image=image, text=file_name, compound=tk.BOTTOM)
            btn.image = image
            self.folder_canvas0.create_window(x, y, window=btn, anchor="nw")
            self.folder_buttons.append(btn)
            x += icon_size + 120
            if x>1150:
                x = 20
                y += icon_size + 40


    def refresh0(self):
        Id = self.file_label1.get()
        query = f"'{Id}' in parents"
        results = self.drive_service.files().list(q=query).execute()
        items = results.get('files', [])
        return items


    def delete_selected_folder0(self):
        Id = self.file_label10.get()
        if Id:
            result = messagebox.askquestion("Delete Folder", "Are you sure you want to delete this folder?")
            if result == "yes":
                try:
                    self.drive_service.files().delete(fileId=Id).execute()
                    messagebox.showinfo("Success", "folder deleted successfully.")
                    self.refresh01()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Please select a folder first.")


    def get_file_icon(self, file_name):
        # Provide file icons based on file extensions
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension in ('.png', '.jpg', '.jpeg', '.gif'):
            return Image.open(resource_path("image\\image_icon.png"))
        elif file_extension in ('.pdf'):
            return Image.open(resource_path("image\\pdf_icon.png"))
        elif file_extension in ('.doc', '.docx'):
            return Image.open(resource_path("image\\word_icon.png"))
        elif file_extension in ('.xls', '.xlsx'):
            return Image.open(resource_path("image\\excel_icon.png"))
        elif file_extension in ('.ppt', '.pptx'):
            return Image.open(resource_path("image\\powerpoint_icon.png"))
        else:
            return Image.open(resource_path("image\\file_icon.png"))


if __name__ == '__main__':
    main()
