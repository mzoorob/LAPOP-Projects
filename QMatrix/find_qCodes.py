__author__ = 'zoorobmj'
import re
import csv
import os
from gibberishclassifier import classify
# from collections import OrderedDict
# import pandas as pd


def clean_list(q_list):
        for bad in ["TV.", "NR.", "UD.", "MUCHO.", "PAIS.", "INAP.", "IDNUM.", "PROV.", "ESTRATOSEC.", "MUNICIPIO.", "CLUSTER.", "UR.", "TAMANO.",
                    "IDIOMAQ.", "FECHA.", "INTERVIEW.", "ED.", "RESPONDENTS.", "ENTREVISTA.", "TODOS", "NS.", "DISTRITO.", "EXACTO.", "RESPONDE.",
                    "U.S.", "US.", "U.", "S.", "ENTREVISTADOS."]:
            try:
                q_list = [x for x in q_list if x != bad]
            except:
                pass
        return q_list

if __name__ == '__main__':
    folder = "C:\Users\zoorobmj\PycharmProjects\Question_Matrix"   # my directory
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    q_list = []
    file_data = ""
    for f in files:
        print f
        file_data = ""
        q_list = []
        with open(f, 'r') as file:
            for line in file:
                if classify(line) < 96:
                    file_data += line
        # get rid of brackets
        file_data = re.sub('\[','', file_data)
        file_data = re.sub('\]','', file_data)
        file_data = re.sub('\|','', file_data)
        file_data = re.sub('\_','', file_data)
        # delete lines beginning with copyright
        cr = re.compile(ur'(?m)^\xa9.*\n?', re.UNICODE)
        file_data = re.sub(ur'(?m)^\xa9.*\n?', '', file_data)
        # get rid of blank lines
        file_data = re.sub('\s+',' ', file_data)
        # print Qs
        # find all meeting this pattern
        # get unique values
        # return as csv
        q_codes = re.findall(r"[A-Z]+[A-Z0-9]*[.]", file_data)
        for q in q_codes:
            q_list.append(q)
        q_list = clean_list(q_list)
        # qs_final = list(OrderedDict.fromkeys(q_list))
        qs_final = []
        for q in q_list:
            if len(q)>2:
                qs_final.append(q)
        q_final = [["Questions", "Wording"]]
        idx = 1
        for q in qs_final[0:len(qs_final)-1]:
            code1 = q
            code2 = qs_final[idx]
            find_me = re.compile(re.escape(code1)+r".*?"+re.escape(code2), re.DOTALL)
            question1 = re.findall(find_me, file_data)[0].strip()
            question = ""
            question += question1
            ### audit some more
            q_codes2 = re.findall(r"[A-Z]+[A-Z0-9]*[.]", question)
            q_codes2 = clean_list(q_codes2)
            if len(q_codes2) > 1:
                q_end = q_codes2[1]
                m = re.match(r"(.*?)"+q_end, question)
                if m.group(1):
                    question = m.group(1)
                else:
                    question = question[0:len(m.group(0))]
            ###
            if len(question)<=len(code1):
                q_final.append([q, question1])
            else:
                q_final.append([q, question])
            idx += 1

        with open(f[0:-4]+".csv", 'wb') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(q_final)
            print f[0:-4]

    # files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    # files2 = []
    # files2.extend(files[1:])
    # files = files[0:len(files)-1]
    # idx = 1
    # df = pd.DataFrame()
    # for x, y in zip(files, files2):
    #     if idx == 1:
    #         df = pd.read_table(x)
    #         idx += 1
    #     df = df.merge(pd.read_table(y), how="outer")
    # df.to_csv("Concatenated_File.csv")