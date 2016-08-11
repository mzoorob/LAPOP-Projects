__author__ = 'zoorobmj'

# Description: Checks if questions in codebook are in text file questionnaires
# Input: List of question codes, surveys as text files in folder
# Output: CSV File with Question Codes as column 1 and "Si/no" for all subsequent columns

from gibberishclassifier import classify
import csv
import re
import os
import Queue


class QuestionsMatrix:

        def __init__(self, code_file):
            self.matrix = []
            csv_file = open(code_file)
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            self.clean_matrix(reader)

        def clean_matrix(self, reader):
            for row in reader:
                self.matrix.append(row)

        # This was the initial code but it flagged substrings (found b10 in vb10)
        # def check_questions(self, survey_file):
            # self.matrix[0].append("Is Question in: "+survey_file)
            # for item in self.matrix[1::]:
                # if item[0] in open(survey_file).read():
                    # item.append("Si")
                # elif item[0]+"." in open(survey_file).read():
                    # item.append("Si")
                # elif item[0].upper()+"." in open(survey_file).read():
                    # item.append("Si")
                # else:
                    # item.append("No")

        # This regex code finds exact matches
        def regex_check(self, survey_file):
            # creates a new column with file name as first cell
            self.matrix[0].append(survey_file[0:len(survey_file)-4])  # +" Y Sample")
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
            for line in lines:
                if classify(line) > 98:
                    lines.remove(line)
                # if len(line) < 5:
                    # print line
                    # lines.remove(line)
                # elif type(line[0]) == int:
                    # lines.remove(line)
                else:
                    file_data += line
            for item in self.matrix[1::]:
                item_count = 0
                regex = re.compile(r"\W"+item[0]+r"\W", re.I)
                if re.search(regex, file_data):
                    for index, line in enumerate(file_data.split("\n")):
                        if re.search(r"\b"+item[0]+r"\W", line, re.I):
                            this_elem = line.replace(",", "_").replace("\r", " ")
                            next_elem = file_data.split("\n")[(index + 1) % len(file_data.split("\n"))]
                            next_elem = next_elem.replace(",", "_").replace("\r", " ")
                            elements = this_elem
                            if classify(next_elem) < 50:
                                elements += " " + next_elem
                            start = 0
                            stop = 1
                            for m in regex.finditer(elements):
                                start = m.start()
                            if classify(elements) < 80:
                                # print elements+" "+str(classify(elements))
                                if item_count == 0:
                                    # item.append(elements[(start+len(item)):])
                                    item.append(elements[start:])
                                    item_count += 1
                                else:
                                    item[-1] += " " + elements[start:]
                else:
                    item.append("Not asked")

        def make_queue(self, survey_file):
            q = Queue.Queue()
            s = set()
            for item in self.matrix[1::]:
                s.add(item[0])
            word_string = ""
            for item in s:
                word_string += item+" "
            survey = open(survey_file).read()
            for word in survey.split(" "):
                if word.lower()[0:len(word)-1] in word_string:
                    q.put(word)
            return q

        # pre: none
        # post: Matrix has been saved to csv file
        # param: Output filename
        def save_matrix(self, filename):
            csv_file = open(filename, 'wb')
            writer = csv.writer(csv_file, delimiter=',', quotechar='|')
            writer.writerows(self.matrix)

if __name__ == '__main__':
    folder = "C:\Users\zoorobmj\PycharmProjects\Question_Matrix"   # my directory
    matrix = QuestionsMatrix("Honduras.csv")
    # creates list with all file names that are text files
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    # finds matches in all text files in folder
    for f in files:
        # os.remove(f)
        # matrix.regex_check(f)
        # matrix.del_empty_lines(f)
        matrix.get_questions(f)
        # q = matrix.make_queue(f)
        #  while not q.empty():
            # print q.get()
        print f+" is finished!"
    # saves completed matrix to new csv file
    matrix.save_matrix("HondurasCS.csv")
    print "end of program"