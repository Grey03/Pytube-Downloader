from pytube import YouTube, Playlist
from tkinter import messagebox
import customtkinter
import os
__location__ = str(os.path.dirname(__file__))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title= "YoutubeDownloader"
        self.resizable(False,False)

        self.headingText = customtkinter.CTkLabel(self, text="Download any Youtube video or Youtube Playlist", font=("Roboto", 16, "bold"))
        self.headingText.pack(padx=5, pady=5)

        self.urlEntry = customtkinter.CTkEntry(self, placeholder_text="http://www.youtube.com/", width=500)
        self.urlEntry.pack(padx=5, pady=5)

        self.getVideo = customtkinter.CTkCheckBox(self, text="Video", font=("Roboto", 14))
        self.getVideo.pack(padx=5, pady=5)

        self.downloadButton = customtkinter.CTkButton(self, text="Download", command= lambda: App.startDownload(self))
        self.downloadButton.pack(padx=5, pady=5)

        self.outputButton = customtkinter.CTkButton(self, text="Output", command= lambda: os.startfile(__location__+"/output/"))
        self.outputButton.pack(padx=5, pady=5)

    def startDownload(self):  
        self.downloadButton.configure(text="Downloading...", state="disabled")
        self.update()
        url = (self.urlEntry.get())
        if url.find("playlist") == -1:
            if self.getVideo.get() == 0:
                try:
                    App.downloadAudio(url)
                except Exception as inst:
                    messagebox.showerror("Error", f"{inst}")
                    self.downloadButton.configure(state="normal", text="Download")
                    return
            else:
                try:
                    App.downloadVideo(url)
                except Exception as inst:
                    messagebox.showerror("Error", f"{inst}")
                    self.downloadButton.configure(state="normal", text="Download")
                    return
            messagebox.showinfo("Completed!", "Finished Downloading Video!")
            self.downloadButton.configure(state="normal", text="Download")
        else:
            self.downloadPlaylist(url)
    def downloadVideo(url):
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        stream.download(output_path=__location__ + "/output/")
    def downloadAudio(url):
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path=__location__ + "/output/")
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    def downloadPlaylist(self, playlistURL):
        try:
            playlist = Playlist(playlistURL)
        except:
            messagebox.showerror("Playlist Error", "Playlist URL not found")
        if self.getVideo.get() == 0:
            for url in playlist.video_urls:
                try:
                    App.downloadAudio(url)
                except:
                    messagebox.showerror("Download Failed", "Could not download: " + url)      
        else:
            for url in playlist.video_urls:
                try:
                    App.downloadVideo(url)
                except:
                    messagebox.showerror("Download Failed", "Could not download: " + url)    
        messagebox.showinfo("Completed!", "Finished Downloading Video!")
        self.downloadButton.configure(state="normal", text="Download")

app = App()
app.mainloop()

