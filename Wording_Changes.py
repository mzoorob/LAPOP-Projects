__author__ = 'Michael'

# description
# identifies wording differences between questions in a csv file


# these are from other files in this repository
from Survey_Checker import SurveyCheck
from QuestionMatrix import QuestionsMatrix
import re

# Static weight definitions
Core2014_column = 2  # (zero-indexed)



def compare_wordings(core2014, list2):
    difference = []
    try:
        for i, j in zip(core2014.split(" "), list2.split(" ")):
            if i != j:
                difference.append(i+" became "+j)
        if len(difference) < 1:
            difference.append("No difference")
    except:
        difference = ["No difference but maybe an error"]
    return '; '.join(difference)

if __name__ == '__main__':
    folder = "C:\Users\circlap\PycharmProjects\LAPOP"   # my directory

    matrix = QuestionsMatrix("Qclean.csv")
    Q_List = []
    wordings = SurveyCheck("2014Esp.csv")
    Core = []
    counter = 0
    for row in wordings:
        print row
        try:
            Core.append(row[2].strip())
            counter += 1
        except IndexError:
            print row
            print "error here"
            counter += 1
            continue
    print len(Core)

    # go through qs and compare with core or something
    col_idx = 1  # corresponds to what column (survey) we are in
    while col_idx < wordings.colcount:
        print "new column"
        row_idx = 0  # corresponds to what row (question) we are in
        matrix[0].append(wordings[row_idx][col_idx])
        row_idx += 1
        for item in matrix[1::]:
            while row_idx < wordings.rowcount:  # row in wordings[1:][col_idx]:
                try:
                    matrix[row_idx].append(compare_wordings(Core[row_idx], wordings[row_idx][col_idx]))
                    row_idx += 1
                except IndexError:
                    print "error"
                    row_idx += 1
                    continue
        col_idx += 1

    matrix.save_matrix("Differences_Espanol.csv")
    print "End of Program."
