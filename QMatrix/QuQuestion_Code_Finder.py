__author__ = 'Michael Zoorob'

# Description: Checks if questions in codebook are in text file questionnaires
# Input: List of question codes, surveys as text files in folder
# Output: CSV File with Question Codes as column 1 and "Si/no" for all subsequent columns

import csv
import re
import os


class QuestionsMatrix:

    def __init__(self, code_file):
        self.matrix = []
        csv_file = open(code_file)
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        self.clean_matrix(reader)

    def clean_matrix(self, reader):
        for row in reader:
            self.matrix.append(row)

    # This regex code finds exact matches
    def regex_check(self, survey_file):
        # creates a new column with file name as first cell
        self.matrix[0].append(survey_file[0:len(survey_file)-4])
        survey = open(survey_file).read()
        for item in self.matrix[1::]:
            regex = re.compile(r"\W"+item[0]+r"\W", re.I)
            # Some surveys had special letters before each question code
            # regex1 = re.compile(r"\W"+"X"+item[0]+r"\W", re.I)
            # regex2 = re.compile(r"\W"+"B"+item[0]+r"\W", re.I)
            # regex3 = re.compile(r"\W"+"Y"+item[0]+r"\W", re.I)
            if re.search(regex, survey):
                item.append("Si")
            # Some surveys had special letters before each question code
            # elif re.search(regex1, survey):
                # item.append("Si")
            # elif re.search(regex2, survey):
                # item.append("Si")
            # elif re.search(regex3, survey):
                # item.append("Si")
            else:
                item.append("No")

    # pre: none
    # post: Matrix has been saved to csv file
    # param: Output filename
    def save_matrix(self, filename):
        csv_file = open(filename, 'wb')
        writer = csv.writer(csv_file, delimiter=',', quotechar='|')
        writer.writerows(self.matrix)

if __name__ == '__main__':
    folder = 'C:\Users\Michael\'s\PycharmProjects\LAPOP'   # my directory
    matrix = QuestionsMatrix("Questions.csv")
    # creates list with all file names that are text files
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    # finds matches in all text files in folder
    for f in files:
        matrix.regex_check(f)
        print f+" is finished!"
    # saves completed matrix to new csv file
    matrix.save_matrix("Question Matrix.csv")
    print "end of program"
