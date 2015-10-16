__author__ = 'Michael Zoorob'
 
# File name: Survey_Checker.py
# Author: Michael Zoorob
# VUnetid: zoorobmj
# Email: michael.j.zoorob@vanderbilt.edu
# Description: Read in a survey data in csv format and ensure equal range and type
 
import csv
import os
 
# Static weight definitions
# these values come from Stata
MISSING_VALUES = [".z", ".", ".c", ".a"]
country_column = 0
year_column = 1


class SurveyCheck:
    # Reads data from the provided .csv file and initializes an
    # internal 2d list to store the values.
    # Perform required pre-processing of raw data:
    # has attributes rowcount and colcount and method get_item
    def __init__(self, filename):
        self.mergefile = []
        csv_file = open(filename)
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        row_total, col_total = self.clean_up(reader)
        self.rowcount = row_total
        self.colcount = col_total

    def clean_up(self, reader):
        row_total = 0
        col_total = 0
        for row in reader:
            if row_total == 0:
                for val in row:
                    col_total += 1
            row_total += 1
            self.mergefile.append(row)
        return row_total, col_total

    def __getitem__(self, row_index):
        return self.mergefile[row_index]

    def get_dimensions(self):
        row_total = 0
        col_total = 0
        for row in self.mergefile:
            if row_total == 0:
                for row in self.mergefile:
                    row_total += 1
                if col_total > 0:
                    return row_total, col_total
            for var in row:
                if col_total == 0:
                    for var in row:
                        col_total += 1
            return row_total, col_total

    # produces dictionary with where keys, values change
    def category_changes(self, colindex, keyword=None):
        list_of_lengths = []
        list_of_names = []
        # go through the column
        for x in range(1, self.rowcount):
            if not keyword:
                keyword = self.mergefile[x][colindex]
                continue
            else:
                if keyword != self.mergefile[x][colindex]:
                    list_of_lengths.append(x)
                    list_of_names.append(keyword)
                    keyword = None
        combined = []
        for name, length in zip(list_of_names, list_of_lengths):
            combined.append([name, length])
        return combined

    def check_range(self, colindex, rowmax, rowmin=1, sample_min=None, sample_max=None):
        sample_list = []
        for x in range(rowmin, rowmax):
            if str(self.mergefile[x][colindex])[0] == ".":
                continue
            else:
                sample_list.append(self.mergefile[x][colindex][0])
        try:
            sample_min = min(sample_list)
            sample_max = max(sample_list)
        except:
            pass
        return sample_min, sample_max
        # for x in range(rowmin, rowmax):
        #     if str(self.mergefile[x][colindex])[0] == ".":
        #         continue
        #     else:
        #         p = process_value(self.mergefile[x][colindex])
        #         if not min:
        #             min = p
        #             max = p
        #             continue
        #         else:
        #             if p < min:
        #                 min = p
        #             if p > max:
        #                 max = p
        # return min, max

    def type_check(self):
        # type checks
        # prints type mismatches within columns to the console
        # returns list of column types
        col_types = []
        row_total, col_total = matrix.get_dimensions()
        for col in range(0, col_total):
            vartype = None
            # first row is variable names so I use row 1 not row 0
            for row in range(1, row_total):
                # ignore missing values; Stata output for missing value has form ".X"
                if matrix[row][col][0] == ".":
                    continue
                elif not vartype:
                    vartype = type(process_value(matrix[row][col]))
                else:
                    if type(process_value(matrix[row][col])) != vartype:
                        print "Type error in the " + str(matrix[0][col])+\
                              " column at row"+str(row)+"!"
                        print "here's the value: " +str(matrix[row][col])
            col_types.append(vartype)
        return col_types

    # pre: none
    # post: New data file has been saved to csv file
    # param: Output filename
    def save_new(self, filename):
        file = open(filename, 'w')
        writer = csv.writer(file, delimiter=',', quotechar='|')
        writer.writerows(self.mergefile)

def process_value(value):
    if not value:
        return value
    try:
        return int(value)
    except ValueError:
        try:
            value = value.strip()
        except AttributeError:
            return str(value)
    return value


# country_ranges is a list of lists
# each composite list is of form [country number, last row in array of that country]
# list is sorted ascending
def get_country(country_ranges, value):
    for country in country_ranges:
        if value <= country[1]:
            return country[0]
    return str(int(country_ranges[-1][0])+1)

def save_txt(list, file):
    f = open(file,"w")
    for line in list:
        f.write(line+"\n")
    f.close()


if __name__ == '__main__':
    folder = "C:\Users\circlap\PycharmProjects\LAPOP"   # my directory
    matrix = SurveyCheck("mergesample.csv")
    new_file = []
    types = matrix.type_check()
    for col, type in zip(matrix[0], types):
        line = "Column "+str(col)+": "+str(type)
        print line
        new_file.append(line)

    # ensure that country and year are in appropriate places
    country_changes = matrix.category_changes(country_column)
    year_changes = matrix.category_changes(year_column)

    current_min = "NA"
    for x in range(2, matrix.colcount):
            current_min, current_max = 0, 0
            previous = None
            range_change = False
            old_min, old_max = 0, 0
            for change in year_changes:
                if not previous:  # beginning of each column
                    previous = change[1]
                    current_min, current_max = matrix.check_range(x, rowmax=change[1])
                    if current_min:
                        old_min = current_min
                        old_max = current_max
                else:
                    current_min, current_max = matrix.check_range(x, rowmin=previous, rowmax=change[1])
                    if current_min:
                        if old_min:
                            if old_min != current_min:
                                range_change = True
                            elif old_max != current_max:
                                range_change = True
                            else:
                                range_change = False
                    if current_min:
                        old_min = current_min
                        old_max = current_max
                    previous = change[1]
                if range_change:
                    new_file.append("*****************************************")
                    new_file.append("This range differed from the range of the previous country year.")
                    new_file.append("All country years between these messages are suspect.")
                    new_file.append("*****************************************")
                    range_change = False
                if current_min:
                    new_file.append("The range for "+str(matrix[0][x])+" in country "+get_country(country_changes,change[1]) +\
                          ", year "+str(change[0])+" is "+str(current_min)+","+str(current_max))

    # creates list with all file names that are text files
    # files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    # for f in files:
        # os.remove(f)
        # matrix.regex_check(f)
        # matrix.del_empty_lines(f)
    # matrix.survey_check()
        # print f+" is finished!"
    # saves completed matrix to new csv file
    save_txt(new_file, "Audit_Output.txt")
    print "End of Program."

