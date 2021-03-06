#!/usr/bin/env python

import threading
import argparse
import sys
import os

import helper
import gui


def main(args):
    output_folder = os.path.expanduser(args.output_folder)
    books = helper.get_table(output_folder, force=args.force)
    if args.gui:
        app = gui.create()
        app.set_output_folder(output_folder)
        app.populate_genres(helper.get_genres(books))
        app._helper = helper
        app._books = books
        threading.Thread(app.mainloop()).start()
        return 0

    if args.list_genres:
        print("\nAvailable genre options:")
        genres = helper.get_genres(books)
        for key in sorted(genres):
            print("  '{}': {} books".format(key, genres[key]))
        print()
        return 0

    if args.list_books is not None:
        print("\nList of available books:")
        count = 0
        books = helper.get_books_in_genres(books, args.list_books)
        for book in sorted(books):
            count += 1
            print("  {}. {}".format(count, book))
        print()
        return 0

    if not args.genre and not args.title and not args.all:
        print("\nNo books selected to download!")
        print("  Please select books by title (--title) or genre (--genre)")
        print("  If you want to download everything use --all\n")
        return 1

    helper.download_books(
        books,
        args.output_folder,
        force=args.force,
        selected_genre=args.genre,
        selected_title=args.title,
        pdf=(not args.only_epub),
        epub=(not args.only_pdf),
        confirm_download=args.confirm_before_download,
        verbose=args.verbose,
    )

    print("\nFinish downloading.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder", help="Folder to put downloaded books in")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all available book (both PDFs and EPUBs)",
    )
    parser.add_argument("--only_pdf", help="Downloads only PDFs")
    parser.add_argument("--only_epub", help="Downloads only EPUBs")
    parser.add_argument(
        "--list_genres", action="store_true", help="Lists out available genres"
    )
    parser.add_argument(
        "--list_books",
        nargs="?",
        const="",
        help="Lists available books (add argument to show book by specified genre",
    )
    parser.add_argument(
        "--force", action="store_true", help="Force download even if file exists"
    )
    parser.add_argument(
        "--genre", default="", help="Downloads only books from certain genre"
    )
    parser.add_argument(
        "--title", default="", help="Downloads only books contain argument in title"
    )
    parser.add_argument("--gui", action="store_true", help="Enables gui mode")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enables verbose mode"
    )
    parser.add_argument(
        "--confirm_before_download",
        action="store_true",
        help="Prompts user whether to download for each book",
    )

    args = parser.parse_args()
    sys.exit(main(args))
