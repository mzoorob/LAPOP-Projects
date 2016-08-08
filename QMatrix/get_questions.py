__author__ = 'Michael Zoorob'

# Description: Checks if questions in codebook are in text file questionnaires
# Input: List of question codes as csv file, surveys as text files in folder
# Output: CSV File with Question Codes as column 1 and the text of questions in subsequent columns

from gibberishclassifier import classify
import csv
import re
import os

class QuestionsMatrix:

        def __init__(self, code_file):
            self.matrix = []
            csv_file = open(code_file)
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            self.clean_matrix(reader)
            # self.clean_matrix2(reader)

        def clean_matrix(self, reader):
            for row in reader:
                self.matrix.append(row)

        def clean_matrix2(self, reader):
            list_of_qs = []
            for row in reader:
                for item in row:
                    if len(item) > 1:
                        list_of_qs.append(item)
            self.matrix = list_of_qs

        # This regex code finds exact matches
        def regex_check(self, survey_file):
            # creates a new column with file name as first cell
            self.matrix[0].append(survey_file[0:len(survey_file)-4])
            survey = open(survey_file).read()
            for item in self.matrix[1::]:
                regex = re.compile(r"\W"+item[0]+r"\W", re.I)
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


        # This regex code finds exact matches
        def regex_check_column(self, survey_file):
            csv_file = open(survey_file)
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            a_list = []
            for row in reader:
                a_list.append(row)
            for item in self.matrix:
                for row in a_list:
                    n = 0
                    for code in row:
                        if item[0] == code:
                            print "si"
                            item.append("Si")
                            n=1
                    if n == 0:
                        item.append("No")


        def del_empty_lines(self, survey_file):
            with open(survey_file, 'r+') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        #rewind
                        f.write(line)

        def get_questions(self, survey_file):
            self.matrix[0].append(survey_file[0:len(survey_file)-4])
            lines = [i for i in open(survey_file) if i[:-1]]
            file_data = ""
            punc = ",.?"
            for line in lines:
                # if classify(line) > 100:
                    # lines.remove(line)
                # elif len(line) < 5:
                    # lines.remove(line)
                # elif type(line[0]) == int:
                    # lines.remove(line)
                # else:
                good_content = False
                for char in punc:
                    if char in line:
                        good_content = True
                if good_content:
                    file_data += line
            for item in self.matrix[1::]:
                item_count = 0
                regex = re.compile(r"\W"+item[0]+r"\W", re.I)
                if re.search(regex, file_data):
                    for index, line in enumerate(file_data.split("\n")):
                        if re.search(r"\b"+item[0]+r"\W", line.rstrip(), re.I):
                            this_elem = line.replace(",", "@").replace("\r", " ")
                            next_elem = file_data.split("\n")[(index + 1) % len(file_data.split("\n"))]
                            next_elem = next_elem.replace(",", "@").replace("\r", " ")
                            elements = this_elem
                            # looks like if end of question is on next line it's likely flagged gibberish
                            if classify(next_elem) > 40:
                                elements += " " + next_elem
                            start = 0
                            stop = 1
                            for m in regex.finditer(this_elem):
                                start = m.start()
                            if classify(elements) < 95:
                                if item_count == 0:
                                    # item.append(elements[(start+len(item)):])
                                    item.append(elements[start:])
                                    item_count += 1
                                else:
                                    item[-1] += " " + elements[start:]
                else:
                    item.append("Not asked")

        # pre: none
        # post: Matrix has been saved to csv file
        # param: Output filename
        def save_matrix(self, filename):
            csv_file = open(filename, 'wb')
            writer = csv.writer(csv_file, delimiter=',', quotechar='|')
            writer.writerows(self.matrix)

if __name__ == '__main__':
    folder = "C:\Users\Michael\PycharmProjects\QuestionMatrix"   # my directory
    matrix = QuestionsMatrix("Question_list.csv")
    # creates list with all file names that are text files
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    # finds matches in all text files in folder
    for f in files:
        # os.remove(f)
        # matrix.regex_check(f)
        # matrix.del_lines(f)
        matrix.get_questions(f)
        print f+" is finished!"
    # saves completed matrix to new csv file
    matrix.save_matrix("CountryQs.csv")
    print "end of program"
