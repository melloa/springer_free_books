import tkinter as tk
import threading
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=20, pady=20)
        self._create_widgets()

    def _create_upper_labels(self):
        pass

    def _create_widgets(self):
        def _create_label(frame, text, coordinates):
            label = tk.Label(frame, text=text, justify=tk.LEFT, anchor="w", width=20)
            label.grid(row=coordinates[0], column=coordinates[1])

        _create_label(self, "Output Folder:", (0, 0))
        self.output_path = tk.Entry(self)
        self.output_path.insert(tk.END, os.getcwd())
        self.output_path.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        _create_label(self, "Available Genres:", (2, 0))
        _create_label(self, "Books to Download:", (2, 1))
        self.genres = tk.Listbox(self)
        self.genres.grid(row=3, column=0, padx=(0, 10))
        self.download = tk.Listbox(self)
        self.download.grid(row=3, column=1, padx=(10, 0))

        self.download_button = tk.Button(self)
        self.download_button["text"] = "Download"
        self.download_button["command"] = self.start_download
        self.download_button.grid(row=4, column=0, columnspan=2, pady=20)

    def populate_genres(self, genres):
        self._genre_mapping = genres
        for genre in sorted(genres):
            self.genres.insert(tk.END, genre)

    def start_download(self):
        print("hi there, everyone!")


def create():
    root = tk.Tk()
    root.title("Springer Ebook Downloader")
    app = Application(master=root)
    return app
