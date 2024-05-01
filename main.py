import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from gtts import gTTS
import os
import pygame
from tkinter import *
from tkinter import ttk, filedialog  # Import filedialog module

import fitz  # PyMuPDF

win = Tk()
win.geometry("750x400")

entry = Entry(win, width=40)
entry.focus_set()
entry.pack()


def summarize_text(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens) * 0.5)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary_text = ' '.join(final_summary)  # Join sentences to form a summarized text
    return summary_text


def summarize_pdf(file_path):
    pdf_text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            pdf_text += page.get_text()
    print(pdf_text)  # Print the extracted text
    # summarized_text = summarize_text(pdf_text)
    # return summarized_text
    return pdf_text


def open_pdf():
    win.filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])  # Store the selected filename
    if win.filename:
        summarized_text = summarize_pdf(win.filename)
        entry.delete(0, END)
        entry.insert(0, summarized_text)
        # Display the summarized text on the label
        summary_label.config(text=summarized_text)


def display_summary():
    summarized_text = entry.get()
    # Display the summarized text
    summary_label.config(text=summarized_text)
    # Generate Text to Speech
    language = 'en'
    myobj = gTTS(text=summarized_text, lang=language, slow=False)
    myobj.save("summary.mp3")



def play_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("summary.mp3")
    pygame.mixer.music.play()


ttk.Button(win, text="Open PDF", width=20, command=open_pdf).pack()
ttk.Button(win, text="Summarize", width=20, command=display_summary).pack()
ttk.Button(win, text="Play Audio", width=20, command=play_audio).pack()
summary_label = Label(win, text="", wraplength=700)
summary_label.pack()

win.mainloop()




#python -m spacy download en_core_web_sm
