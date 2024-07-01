#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dateiname: projektarbeit_nltk.py

Funktion:
Extraktive Textzusammenfassung. 
Die Extraktsionsgröße kann über die Variable 'extrakt_percent' am Ende des 
Scripts mit Werten des Typs int() verändert werden.
Mit 'file_path =' im Direktaufruf am Ende des Skripts können Sie das Dateiverzeichnis ändern

Created on Wed Jun 26 14:21:53 2024

@author: Ulrich Semar

"""

# Bitte stellen Sie sicher, dass die folgenden NLTK-Ressourcen heruntergeladen wurden und zur Verfügung stehen. 
# Für eine Installation entfernen Sie das Kommentarzeichen '#' vor den drei Anweisungen
# Nach erfolgreicher Installation müssen diese drei Anweisungen wieder mit '#' auskommentiert werden

#--------------
# import nltk 
# nltk.download('punkt') 
# nltk.download('stopwords') 
#--------------

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string


class TextExtraktion:
    
    def __init__(self, file_path):
        
        '''
        Initiiert die Klasse TextExtraktion und folgende Methoden bei Aufruf
        
        read_text_file(), clean_and_tokenized(), normed_wordcount(), 
        word_freg -> import FreqDist, get_sentence_count()
        
        Parameters
        ----------
        file_path : TYPE 'str()'

        Returns
        -------
        None.

        '''
        # Paramterübergabe von file_path an self.file_path
        self.file_path = file_path
        
        # Aufruf der Methode 'read_text_file()' und Wertübergabe an 'self.text'
        self.text = self.read_text_file()
        
        # Aufruf der Methode clean_and_tokenized und Wertübergabe an self.filtered_words
        self.filtered_words = self.clean_and_tokenized(self.text)
        
        # Berechnet bei Initiierung die Häufigkeit/Frequenz der Worte und übergibt denr Wert an self.word_freg
        self.word_freq = FreqDist(self.filtered_words)
        
        # Aufruf der Methode normed_wordcount und Wertübergabe an self.normed_freq
        self.normed_freq = self.normed_wordcount()
        
        # Aufruf der Methode get_sentence_counts und Wertübergabe an self.sentence_counts zurück 
        self.sentence_counts = self.get_sentence_counts()
        
    
    def read_text_file(self):
        '''
        Liest die Textdatei aus self.file_path ein

        Returns
        -------
        text : TYPE 'str()'
            gibt den eingelesenen Text als String mit dem Namen 'text' zurück

        ''' 
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            return text    
    
    def clean_and_tokenized(self, text):
        '''
        Entfernt Satzzeichen, Stopwords und tokenisiert den Text
        
        Parameters
        ----------
        text : TYPE 'str()'
        
        Returns
        -------
        filtered_words : TYPE 'list[]'
        '''
        # Satzzeichen entfernen
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenisierung in Wörter
        words = word_tokenize(text.lower())
        
        # Sprache für stopwords festlegen
        stop_words = set(stopwords.words('english'))  
        
        # Stopwords entfernen
        filtered_words = [word for word in words if word not in stop_words]
        
        # Rückgabe des gereinigten und tokenisierten Textes
        return filtered_words
    

    def normed_wordcount(self):
        '''
        Normiert den Wordcount im Verhältnis zum größten Wert der gezählten Worte
        
        Returns
        -------
        normed_freq : TYPE 'dict{}'
        
        max_count >> Summe der häufigsten Worte 
        '''
        # Summe der häufigsten Worte ist max_count -> Aufruf beim Initiieren in word_freq
        max_count = max(self.word_freq.values())
        
        # Normieren des Word Counts
        normed_freq = {word: count / max_count for word, count in self.word_freq.items()}
        
        # Gebe den Normwert der Wortverteilung zurück
        return normed_freq

    def get_sentence_counts(self):
        '''
        Berechnet für jeden Satz im Text den Word Count

        Returns
        -------
        sentence_counts : TYPE dict{}
        '''
        # Tokenisierung der Sätze
        sentences = sent_tokenize(self.text)
        
        # Erzeuge Dictionary 
        sentence_counts = {}
        
        # Für jeden Satz in sentences berechne den Word Count
        for sentence in sentences:
            words = self.clean_and_tokenized(sentence)
            sentence_count = sum(self.word_freq.get(word, 0) for word in words)
            sentence_counts[sentence] = sentence_count 
            
        # Gibt den Wert in sentence_counts zurück    
        return sentence_counts

    def build_text_summ(self, extrakt_percent):
        '''
        Bildet die Text-Extraktion mit dem Prozentwert der in extrakt_percent festgelegt wurde

        Parameters
        ----------
        extrakt_percent : TYPE 'int()'
        
        Returns
        ---------
        summary : TYPE 'str()'
        
        '''
        # Schreibt die Schlüssel des Dictionarys in die Liste sentences
        sentences = list(self.sentence_counts.keys())
        
        # Erzeugt eine sortierte Liste der sentence counts
        sorted_sentences = sorted(self.sentence_counts, key=self.sentence_counts.get, reverse=True)
        
        # Berechnet den gewünschten Prozentwert aus der sortierten Liste
        summary_length = max(1, int(len(sentences) * extrakt_percent / 100))
        
        # Extrahiert den gewünschten Prozentwert aus der sortierten Liste
        summarized_sentences = sorted_sentences[:summary_length]
        
        # Bildet den Textstring mit join
        summary = ' '.join(summarized_sentences)
        
        # Gibt den Text an das aufrufende Objekt zurück
        return summary
    
# Prüfen ob die Datei direkt oder als Modulimport aufgerufen wird.
# Bei import als Modul wird der Code nach if__name__ ... nicht ausgeführt
if __name__ == "__main__":
    
    # Pfad zur Textdatei
    file_path = 'data/trees.txt'
    
    # Prozentsatz der Zusammenfassung
    extrakt_percent = 20
    
    # Erzeugt das Objekt 'extrakt_obj' von der Klasse TextExtraktion mit Parameterübergabe 'file_path'
    extrakt_obj = TextExtraktion(file_path)
    
    # Aufruf der Methode 'build_text_summ' mit Prameterübergabe des Prozentsatzes
    extrakted_text = extrakt_obj.build_text_summ(extrakt_percent)
    
    # Ausgabe des Extrahierten Textes
    print(f"\nExtraktion von {extrakt_percent}% des Originaltextes:\n\n{extrakted_text}\n")
    
    
