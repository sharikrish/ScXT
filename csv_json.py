import csv
import json
import pandas as pd
from itertools import groupby


df = pd.read_csv('filter_test.csv', dtype=str)
#with open('./filter_test.csv', 'r') as df:
with open('./repertoire_endpoint.json', 'w') as jsonfile:

    finalList = []
    finalDict = []

    grouped =df.groupby(['cell_id', 'tissue', 'repertoire_id_1'])

    for key, value in grouped:
        dictionary = {}
        j = grouped.get_group(key).reset_index(drop=True)
        for k in j.index:
            anotherDict = {}
            dictionary['cell_id'] = j.at[k, 'cell_id']
            dictionary['tissue'] = j.at[k, 'tissue']
            dictionary['repertoire_id'] = j.at[k, 'repertoire_id_1']
            dictList = []
            anotherDict = {}
            for i in j.index:
                anotherDict = {}
                anotherDict['locus'] = j.at[i, 'locus']
                anotherDict['v_call'] = j.at[i, 'v_call']
                anotherDict['d_call'] = j.at[i, 'd_call']
                anotherDict['j_call'] = j.at[i, 'j_call']
                anotherDict['c_call'] = j.at[i, 'c_call']
                anotherDict['junction_aa'] = j.at[i, 'junction_aa']
                dictList.append(anotherDict)

        dictionary['Processed sequence with annotations'] = dictList

        finalList.append(dictionary)
    json.dump(finalList,jsonfile, indent=5)
    jsonfile.write('\n')

# def get_nested_rec(key, grp):
#     rec = {}
#     rec['cell_id'] = key[0]
#     rec['tissue'] = key[1]
#     # rec['v_call'] = key[2]
#     # rec['d_call'] = key[3]
#     # rec['j_call'] = key[4]
#     # rec['c_call'] = key[5]
#     #rec['junction_aa'] = key[6]
#
#     for locus_pa in ['locus']:
#         print(locus_pa)
#         for field in ['v_call','d_call','c_call', 'junction_aa']:
#             rec[locus_pa] = list(grp[field].unique())
#     return rec
#
# records = []
# for key, grp in df.groupby(['cell_id','tissue']):
#     rec = get_nested_rec(key, grp)
#     #print(key, grp)
#     records.append(rec)
#
# records = dict(data = records)
# #print(records)
# #print(json.dumps(records, indent=4))
#



#
#
#
# fields = ("repertoire_id_1", "cell_id", "tissue", "v_call", "d_call", "j_call", "c_call", "junction_aa")
# with open('./repertoire_endpoint.csv', 'r') as csvfile:
#     with open('./repertoire_endpoint.json', 'w') as jsonfile:
#         next(csvfile)
#         reader = csv.DictReader(csvfile, fields)
#         final_data = {}
#         for row in reader:
#             final_data[row["repertoire_id_1"]]={
#                 "cell_id": row["type"],
#                 "locus": row["locus"],
#                 "name":row["name"],
#                 "VDJ_id":row["VDJ_id"]
#             }
#             json.dump(final_data, jsonfile)
#             jsonfile.write('\n')