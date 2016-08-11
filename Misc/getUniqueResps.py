__author__ = 'zoorobmj'
import csv

## reads in a survey file csv with columns and rows.
## output: returns a spreadsheet with unique responses for each question.

def read_file(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
    return reader

if __name__ == '__main__':
    print "hello world"

    myfile = "NOLA_Responses.csv"

    survey = []
    with open(myfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            survey.append(row)

    output = [survey[0]]
    list_of_sets = []
    list_of_lengths = []
    for x in range(len(survey[0])):
        small_list = []
        for response in survey[1:]:
            small_list.append(response[x])
        small_set = set(small_list)
        helper = list(small_set)
        list_of_lengths.append(len(helper))
        list_of_sets.append(helper)

    output.append(list_of_sets)
    output.append(list_of_lengths)
    # output output as csv list of lists
    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(output)
