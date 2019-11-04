from flask import Flask, jsonify
import json
import MySQLdb.cursors
import csv
from os.path import expanduser
import pandas as pd
from configobj import ConfigObj # install via pip3


app = Flask(__name__)

### 0. Logging information (TBD) # get configuration using bcelldb_init
config = (ConfigObj(expanduser('~/.my.cnf')))
def mysql_connect():
    return MySQLdb.connect(host=config['mysql_igdb']['host'],
                               user=config['mysql_igdb']['user'],
                               db=config['mysql_igdb']['database'])
db = mysql_connect()
cursor=db.cursor()

def get_config():
    """
    Look for config file in . and than ../
    Return ConfigObj dictionary.
    """
    # try to open config file in .
    try:
        config_file = open("config", "r")
    except IOError:
        # try from ../ directory
        try:
            config_file = open("../config", "r")
        except IOError:
            print("no config file found")

    return ConfigObj(config_file)

conf= get_config()
class Database:
    def query_call(self):
        reads= ("SELECT cell_id, tissue, v_call, NULL , j_call,c_call, junction_aa, repertoire_id_1, locus  FROM {}.repertoire_k " \
               "UNION ALL  " \
               "select cell_id, tissue, v_call, d_call , j_call,c_call, junction_aa, repertoire_id_1, locus from  {}.repertoire " \
               "UNION ALL  " \
               "SELECT cell_id, tissue, v_call, NULL , j_call,c_call, junction_aa, repertoire_id_1, locus  FROM {}.repertoire_l;").format(conf["database"],conf["database"],conf["database"])
        cursor.execute(reads)
        rows = cursor.fetchall()
        header = ["cell_id", "tissue", "v_call", "d_call", "j_call", "c_call", "junction_aa", "repertoire_id_1","locus"]
        fp = open('/tmp/file.csv', 'w')
        myFile = csv.writer(fp, delimiter=',')
        myFile.writerow(i for i in header)
        for j in rows:
            myFile.writerow(j)
        fp.close()
db = Database()
db.query_call()

def csv_json(filepath):
    df = pd.read_csv(filepath, dtype=str)
    df = df[pd.notnull(df['junction_aa'])]
    df[df.isnull()] = "NULL"
    with open('./repertoire_endpoint.json', 'w') as jsonfile:
        finalList = []
        grouped = df.groupby(['cell_id', 'tissue', 'repertoire_id_1'])
        for key, value in grouped:
            dictionary = {}
            j = grouped.get_group(key).reset_index(drop=True)
            for k in j.index:
                dictionary['cell_id'] = j.at[k, 'cell_id']
                dictionary['tissue'] = j.at[k, 'tissue']
                dictionary['repertoire_id'] = j.at[k, 'repertoire_id_1']
                dictList = []
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
        json.dump(finalList, jsonfile, indent=5)
        jsonfile.write('\n')
csv_json("/tmp/file.csv")

#calling app via flask
@app.route('/cell/', methods=['GET', 'POST'])
def repertoire():
    with open('./repertoire_endpoint.json', 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
    # We can then find the data for the requested date and send it back as json
    return jsonify(file_data)

if __name__ == '__main__':
    app.run(debug=True)