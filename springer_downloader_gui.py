import springer_downloader
import argparse

if __name__ == "__main__":
    args = argparse.Namespace(
        all=False,
        confirm_before_download=False,
        force=False,
        genre="",
        gui=True,
        list_books=None,
        list_genres=False,
        only_epub=None,
        only_pdf=None,
        output_folder="~/Downloads",
        title="",
        verbose=False,
    )
    springer_downloader.main(args)
