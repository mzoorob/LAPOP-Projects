__author__ = 'zoorobmj'

import csv
import os
# Python 2.7
# Merges Questionnaires


def read_csv(f):
    data = []
    with open(f, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


def clean_countries(file_list):
    countries = set()
    for f in file_list:
        countries.add(f[0:-9])
    bad_list = ["ChileV2", "ChileV1", "Uruguay 2006", "CoreES"]
    for item in bad_list:
        countries.remove(item)
    return sorted(list(countries))

# content is list of lists
def save_csv(content, f="output.csv"):
    with open(f, 'wb') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(content)


if __name__ == '__main__':
    folder = "C:\Users\zoorobmj\PycharmProjects\Question_Matrix"   # my directory
    file_list = [f for f in os.listdir(folder) if f.endswith('.csv')]
    merge_file = [["Question"]]
    idx = 2
    for f in file_list:
        merge_file[0].append(f[0:-4])
        # first questionnaire
        if idx == 2:
            data = read_csv(f)
            for row in data[1:]:
                merge_file.append(row)
        else:
            data = read_csv(f)
            for row in data[1:]:
                for item in merge_file:
                    if row[0] == item[0]:
                        ## asked before
                        item.append(row[1])
            ## append not asked for every item that's blank in this new column
            for item in merge_file[1:]:
                asked = False
                for row in data[1:]:
                    if row[0] == item[0]:
                        asked = True
                if not asked:
                    item.append("Not asked")
            for row in data[1:]:
                new = True
                for item in merge_file[1:]:
                    if row[0] == item[0]:
                        new = False
                if new:
                    new_q = [row[0]]
                    for x in range(idx-2):
                        new_q.append("Not asked")
                    new_q.append(row[1])
                    merge_file.append(new_q)
        idx += 1
        print f[0:-4]

    save_csv(merge_file, f="AllQuestionnairesWording.csv")
