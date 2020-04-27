import tkinter as tk
import threading
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # self.master.configure(background='red')
        self.grid(row=0, column=0, sticky="nesw", padx=20, pady=20)
        self._create_widgets()
        self._selected_genre = set()
        self._helper = None
        self._books = None
        # self.grid_columnconfigure(0,weight=1)
        # self.grid_rowconfigure(1,weight=1)

    def _add_titles_to_listbox(self):
        books = []
        self.download.delete(0,tk.END)
        for genre in sorted(self._selected_genre):
            books.extend(self._helper.get_books_in_genres(self._books, genre))

        books.sort()
        self.download.insert(tk.END, *books)
        
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
        self.genres = tk.Listbox(self, selectmode='multiple')

        def on_genre_select(evt):
            indices = evt.widget.curselection()
            self._selected_genre.clear()
            for index in indices:
                value = evt.widget.get(index)
                self._selected_genre.add(value)
            self._add_titles_to_listbox()

        self.genres.bind('<<ListboxSelect>>', on_genre_select)
        self.genres.grid(row=3, column=0, padx=(0, 10))
        self.download = tk.Listbox(self)
        self.download.grid(row=3, column=1, padx=(10, 0))

        self.pdf = tk.Checkbutton(self, text="PDF")
        self.pdf.select()
        self.pdf.grid(row=4, column=0, pady=10)

        self.epub = tk.Checkbutton(self, text="EPUB")
        self.epub.select()
        self.epub.grid(row=4, column=1, pady=10)

        self.download_button = tk.Button(self, text="Download", command=self.start_download)
        self.download_button.grid(row=5, column=0, columnspan=2, pady=10)

    def populate_genres(self, genres):
        self._genre_mapping = genres
        for genre in sorted(genres):
            self.genres.insert(tk.END, genre)

    def start_download(self):
        titles = self.download.get(0, tk.END)
        if not titles:
            return
        self._helper.download_books(
            self._books,
            self.output_path.get(),
            selected_title=titles,
            pdf=True,
            epub=True,
        )


def create():
    root = tk.Tk()
    root.title("Springer Ebook Downloader")
    app = Application(master=root)
    return app
