import tkinter as tk
from tkinter import filedialog

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("key.json")

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    try:
        username = texts[2].description.strip("\n")

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

    except IndexError:
        username = "unclassified"

def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(initialdir=os.path.abspath("."))

    detect_text(os.path.abspath(file_path))


if "__main__" == __name__:
    main()
