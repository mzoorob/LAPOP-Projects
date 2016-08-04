__author__ = 'zoorobmj'
import re
import csv
import os


if __name__ == '__main__':
    folder = "C:\Users\zoorobmj\PycharmProjects\Question_Matrix"   # my directory
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    q_list = []
    for f in folder:
        Qs = open('CoreESP2016.txt', 'r').read()
        # print Qs
        # find all meeting this pattern
        # get unique values
        # return as csv
        q_codes = re.findall(r"[A-Z]+[A-Z0-9]*[.]", Qs)
        q_list.append(q_codes)

    with open("CoreESP2016.csv", 'wb') as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in q_list:
            if len(val)==2:
                print val
            else:
                writer.writerow([val])