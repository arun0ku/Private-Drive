import customtkinter as ctk
import webbrowser

def main():
    win = ctk.CTk()
    clss = Main(win)
    win.mainloop()

class Main:
    def __init__(self, dr):
        self.dr = dr
        self.dr.minsize(500,400)
        self.dr.geometry('800x600')
        self.dr.title('Private Drive')

        self.url = 'https://drive.google.com/drive/folders/1_Y4mZbK4DHHct9G3CatKsVL2IBD2Iepp?usp=drive_link'

        self.upbtn = ctk.CTkButton(self.dr, text='UPLOAD_FILE', command=self.callback).pack(pady=20)
        self.downbtn = ctk.CTkButton(self.dr, text='DOWNLOAD_FILE' ).pack(pady=20)

    def callback(self):
        webbrowser.open_new(self.url)


if __name__ =='__main__':
    main()