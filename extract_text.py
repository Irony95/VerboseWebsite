import pdfminer
import os
from io import StringIO
import re
import pickle

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTText, LTAnno

#REQUIRED DEPENDENCIES
#pdfminer.six

###   MODIFY THE BELOW VARIABLES ACCORDINGLY   ###
#Specify output directory, otherwise leave blank to output to root   e.g C:/Users/duyua/Desktop/output/
Output_Dir = ""
Note_Name = ""
#Page range for the PDF(s) (inclusive)
minimum_page = 0
maximum_page = 999
############################################################


def extract_note(note_name):
    file_path = os.path.join('./sentPDFs', note_name)
    note_name = note_name.split(".")[0]

    if(os.path.isfile(os.getcwd() + "\\" + "\\pickle_notes\\" + note_name + "_pickle")):
        print(note_name + " already exists.")
        return

    note_text = Extract_PDF_text_filtered_algorithm(file_path, minimum_page, maximum_page)
    note_text = temp_Modify_note_text(note_text, note_name)
    Output(note_text, note_name)

def temp_Modify_note_text(note_text, note_name):
    note_text = re.split(r'\n', note_text)
    new_note_text = []
    for count, line in enumerate(note_text):
        if (re.fullmatch(r'[^A-Za-z.,]+', line) != None):
            line = ''
        line = re.sub(r'[^a-zA-Z0-9.\?\+:_%/\\,\(\)\'\- ]', '', line)
        line = re.sub(r'\(cid:[\d]+\)', '', line)
        line = re.sub(r'[\s]+', ' ', line)
        if (re.fullmatch(r'[\s]*', line) != None):
            continue

        else:
            test = re.finditer(r'\b[a-zA-Z]*\b\. \b[\w]*\b', line)
            test_iter = []
            iter_count = 0
            for iter in test:
                iter_count += 1
                test_iter.append(iter.group())

            if (test_iter == []):
                new_note_text.append(line)
                continue

            final_sentence = split_and_rejoin_sentences(test_iter, iter_count, line)
            for line in final_sentence:
                new_note_text.append(line)

    newer_note_text = []
    temp_hold = ""
    for count, line in enumerate(new_note_text):
        line = line.strip()
        if (not line.endswith(".")):
            temp_hold = temp_hold + line + " "
        else:
            newer_note_text.append(temp_hold + line)
            temp_hold = ""

    with open(os.getcwd() + "\\" + "\\pickle_notes\\" + note_name + "_pickle", "wb") as fp:  # Pickling
        pickle.dump(newer_note_text, fp)

    string = ""
    for line in newer_note_text:
        if (re.fullmatch(r'[\.\d]+', line) != None):
            continue
        string = string + line + "\n"
    return string

def split_and_rejoin_sentences(test_iter, iter_count, line):
    sentence_str = line
    matches = []
    for match in test_iter:
        match_split = re.split(r'\.', match)
        for split in match_split:
            matches.append(split)
    sentence_split = []
    for match in test_iter:
        split = re.split(match, sentence_str)
        sentence_split.append(split[0])
        sentence_str = split[-1]
        iter_count -= 1
        if (iter_count == 0):
            sentence_split.append(sentence_str)

    final_sentence = []
    sentence_index = 0
    for count, split in enumerate(matches):

        if (count % 2 != 0):
            final_sentence.append(" " + split + sentence_split[sentence_index])
        else:
            if (count == 0):
                final_sentence.append(sentence_split[0] + split + ".")
                sentence_index += 1
                continue
            final_sentence[sentence_index] = final_sentence[sentence_index] + split + "."
            sentence_index += 1
    return final_sentence




def Output(note_text, note_name):
    with open(os.getcwd() + "\\" + "noteTexts\\" + note_name + ".txt", "w", encoding="utf-8") as output:
        output.write(note_text)
    print("Note has been written to " + "./noteTexts/" + note_name + ".txt")

def Extract_PDF_text_filtered_algorithm(note_location, minimum_page, maximum_page):
    string_dict = {}
    string = ""
    output_string = StringIO()
    extracted = extract_pages(note_location)
    temp_extracted = extracted;
    for count, page_layout in enumerate(extract_pages(note_location)):
        if (count + 1 >= minimum_page and count + 1 <= maximum_page):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        if (isinstance(text_line, LTText)):
                            if (isinstance(text_line, LTAnno)):
                                continue
                            if (isinstance(text_line, LTChar)):
                                continue
                            for character in text_line:
                                if isinstance(character, LTChar):
                                    if (int(character.size) in string_dict):
                                        string_dict[int(character.size)] += 1
                                    else:
                                        string_dict[int(character.size)] = 0
    chosen_font_size = 0
    number_of_characters = 0
    for key in string_dict:
        if (string_dict[key] > number_of_characters):
            number_of_characters = string_dict[key]
            chosen_font_size = key
    print("A font size of " + str(chosen_font_size) + " was selected with a total of " + str(number_of_characters) + " characters.")
    for count, page_layout in enumerate(extract_pages(note_location)):
        if (count + 1 >= minimum_page and count + 1 <= maximum_page):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        if (isinstance(text_line, LTText)):
                            if (isinstance(text_line, LTAnno)):
                                continue
                            if (isinstance(text_line, LTChar)):
                                continue
                            for character in text_line:
                                if isinstance(character, LTChar):
                                    if(character.size < (chosen_font_size + 1) and  character.size >= chosen_font_size):
                                        string += (character.get_text())
                                        #"Italic" not in character.fontname
                                        #"Bold" not in character.fontname
                                else:
                                    string += " "
                            string += "\n"
    return string
