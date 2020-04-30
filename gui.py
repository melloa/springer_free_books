from tkinter.ttk import Progressbar, Frame, Label, Entry, Checkbutton, Button
import tkinter as tk
import threading
import logging
import os

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky="nesw", padx=20, pady=20)
        self._create_widgets()
        self._selected_genre = set()
        self._helper = None
        self._books = []
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
        self.genres["height"] = 20
        self.genres["width"] = 30
        self.genres.grid(row=3, column=0, padx=(0, 10))

        self.books = tk.Listbox(self)
        self.books["height"] = 20
        self.books["width"] = 30
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
        db["command"] = self.start_download
        self._download_btn.set("Download")
        db.grid(row=7, column=0, columnspan=2, pady=10)
        LOG.info("All widgets created.")

    def set_output_folder(self, path):
        if self.output_path:
            self.output_path.insert(tk.END, path)

    def populate_genres(self, genres):
        self._genre_mapping = genres
        for genre in sorted(genres):
            self.genres.insert(tk.END, genre)
        LOG.info("Added {} genres".format(len(genres)))

    def start_download(self):
        titles = self.books.get(0, tk.END)
        if not titles:
            self._status_text.set("Please select a genre to continue")
            return

        self._is_started = not self._is_started
        self._toggle_state(not self._is_started)

        if self._is_started:
            books = self._books.copy()
            for book in books.iterrows():
                if book[1]["Book Title"] not in titles:
                    books = books.drop(index=book[0])

            LOG.info("Starting to download {} books".format(len(books)))
            self.bar["maximum"] = len(books)
            self._helper.STOP_FLAG = False
            self._download_thread = threading.Thread(
                daemon=True,
                target=self._helper.download_books,
                args=(books, self.output_path.get()),
                kwargs={
                    "pdf": self._pdf.get(),
                    "epub": self._epub.get(),
                    "verbose": True,
                    "label": self._status_text,
                    "progressbar": self._current_bar_value,
                },
            )
            self._download_thread.start()
            self._thread_check_in(self._download_thread)
        else:
            self._helper.STOP_FLAG = True

    def _thread_check_in(self, thread, period=100):
        if thread.isAlive():
            self.master.after(period, self._thread_check_in, thread, period)
        else:
            self._is_started = False
            self._toggle_state(True)

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
    LOG.info("Starting GUI application of the Springer ebook downloader")
    root = tk.Tk()
    root.title("Springer Ebook Downloader")
    root.resizable(0, 0)
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky="nesw")
    app = Application(master=frame)
    return app
