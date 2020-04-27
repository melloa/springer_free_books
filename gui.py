from tkinter.ttk import Progressbar, Frame, Label, Entry, Checkbutton, Button
import tkinter as tk
import threading
import os


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky="nesw", padx=20, pady=20)
        self._create_widgets()
        self._selected_genre = set()
        self._helper = None
        self._books = None
        self._is_started = False

    def _add_titles_to_listbox(self):
        books = []
        self.books.delete(0, tk.END)
        for genre in sorted(self._selected_genre):
            books.extend(self._helper.get_books_in_genres(self._books, genre))

        books.sort()
        self.books.insert(tk.END, *books)

    def _create_widgets(self):
        def _create_label(frame, text, coordinates):
            label = Label(frame, text=text, justify=tk.LEFT, anchor="w", width=20)
            label.grid(row=coordinates[0], column=coordinates[1])

        _create_label(self, "Output Folder:", (0, 0))
        self.output_path = Entry(self)
        self.output_path.insert(tk.END, os.getcwd())
        self.output_path.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        _create_label(self, "Available Genres:", (2, 0))
        _create_label(self, "Books to Download:", (2, 1))
        self.genres = tk.Listbox(self, selectmode="multiple")

        def on_genre_select(evt):
            indices = evt.widget.curselection()
            self._selected_genre.clear()
            for index in indices:
                value = evt.widget.get(index)
                self._selected_genre.add(value)
            self._add_titles_to_listbox()

        self.genres.bind("<<ListboxSelect>>", on_genre_select)
        self.genres.grid(row=3, column=0, padx=(0, 10))
        self.books = tk.Listbox(self)
        self.books.grid(row=3, column=1, padx=(10, 0))

        self._pdf = tk.IntVar(value=1)
        self.pdf = Checkbutton(self, text="PDF", variable=self._pdf)
        self.pdf.grid(row=4, column=0, pady=10)

        self._epub = tk.IntVar(value=1)
        self.epub = Checkbutton(self, text="EPUB", variable=self._epub)
        self.epub.grid(row=4, column=1, pady=10)

        self._status_text = tk.StringVar()
        self.status = Label(self, textvariable=self._status_text)
        self.status.grid(row=5, column=0, columnspan=2)
        self._current_bar_value = tk.IntVar(value=0)
        self.bar = Progressbar(self, variable=self._current_bar_value)

        self._download_btn = tk.StringVar()
        db = Button(self, textvariable=self._download_btn)
        db['command'] = self.start_download
        self._download_btn.set("Download")
        db.grid(row=7, column=0, columnspan=2, pady=10)

    def populate_genres(self, genres):
        self._genre_mapping = genres
        for genre in sorted(genres):
            self.genres.insert(tk.END, genre)

    def start_download(self):
        titles = self.books.get(0, tk.END)
        if not titles:
            self._status_text.set("Please select a genre to continue")
            return

        self._is_started = not self._is_started
        self._toggle_state(not self._is_started)

        if self._is_started:
            self.bar.maximum = len(titles)
            self._helper.STOP_FLAG = False
            self._helper.download_books(
                self._books,
                self.output_path.get(),
                selected_title=titles,
                pdf=True,
                epub=True,
                callback=self._update_progress
            )
        else:
            self._helper.STOP_FLAG = True
    
    def _update_progress(self, data, amount=1, **kwargs):
        new_value = self._current_bar_value.get() + amount 
        self._current_bar_value.set(new_value)
        return data

    def _toggle_state(self, enable):
        state = tk.NORMAL if enable else tk.DISABLED
        text = "Download" if enable else "Stop"
        status = "" if enable else "Starting downloader ..."
        self.output_path.config(state=state)
        self.genres.config(state=state)
        self.books.config(state=state)
        self.pdf.config(state=state)
        self.epub.config(state=state)
        self._download_btn.set(text)
        self._status_text.set(status)

        if enable:
            self.bar.grid_remove()
        else:
            self.bar.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")


def create():
    root = tk.Tk()
    root.title("Springer Ebook Downloader")
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky="nesw")
    app = Application(master=frame)
    return app
