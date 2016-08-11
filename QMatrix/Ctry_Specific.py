__author__ = 'zoorobmj'


import csv
import os
import re

def read_csv(filename):
    data = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


# content is list of lists
def save_csv(content, f="output.csv"):
    with open(f, 'wb') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(content)

if __name__ == '__main__':
    folder = "C:\Users\zoorobmj\PycharmProjects\Question_Matrix"   # my directory
    file_list = [f for f in os.listdir(folder) if f.endswith('.csv')]

    ## get the core Qs
    core = read_csv("Core.csv")
    core_qs = []
    for row in core:
        core_qs.append(row[0])
    ## keep only country files in this list
    file_list.remove("Core.csv")

    for f in file_list:
        data = read_csv(f)
        merge_file = [data[0]]
        for row in data[1:]:
            regex = re.compile(row[0])
            if not [m.group(0) for l in core_qs for m in [regex.search(l)] if m]:
                merge_file.append(row)
        print f[0:-4]
        save_csv(merge_file, f=f[0:-4]+"_CountrySpecificQuestions.csv")