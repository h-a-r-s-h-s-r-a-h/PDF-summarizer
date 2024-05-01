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
    return pdf_text

def open_pdf():
    win.filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])  
    if win.filename:
        summarized_text = summarize_pdf(win.filename)
        entry.delete(1.0, END)
        entry.insert(END, summarized_text)
        # Display the summarized text on the label
        summary_label.config(text=summarized_text)

def display_summary():
    summarized_text = entry.get(1.0, END)
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

def animate():
    # Your animation code here
    win.after(100, animate)  # Repeat the animation after 100 milliseconds

win = Tk()
win.geometry("750x400")
win.title("PDF Summarizer")

# Create a frame for the main content
content_frame = Frame(win)
content_frame.pack(pady=20)

# Create entry widget for text display
entry = Text(content_frame, width=60, height=15)
entry.pack(side=LEFT, padx=10)

# Create scrollbar for the entry widget
scrollbar = Scrollbar(content_frame, orient="vertical", command=entry.yview)
scrollbar.pack(side=RIGHT, fill="y")
entry.config(yscrollcommand=scrollbar.set)

# Create buttons and labels
button_frame = Frame(win)
button_frame.pack(pady=10)

open_button = ttk.Button(button_frame, text="Open PDF", width=20, command=open_pdf)
open_button.grid(row=0, column=0, padx=5)

summarize_button = ttk.Button(button_frame, text="Summarize", width=20, command=display_summary)
summarize_button.grid(row=0, column=1, padx=5)

play_button = ttk.Button(button_frame, text="Play Audio", width=20, command=play_audio)
play_button.grid(row=0, column=2, padx=5)

summary_label = Label(win, text="", wraplength=700)
summary_label.pack()

# Function to create animation
animate()

win.mainloop()
