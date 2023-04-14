import json
import os
from glob import glob
import shutil
import fileinput

TEMPLATE_FILE = 'include/dynamic_dag_json/template.py'

JSON_FOLDER = 'include/dynamic_dag_json/'

for filename in glob(JSON_FOLDER + '*.json'):

    print(filename)

    config = json.load(open(filename))

    new_dagfile = f"dags/get_price_{config['dag_id']}.py"
    
    shutil.copyfile(TEMPLATE_FILE, new_dagfile)

    for line in fileinput.input(new_dagfile, inplace=True):

        line = line.replace("DAG_ID_HOLDER", config['dag_id'])

        line = line.replace("SCHEDULE_INTERVAL_HOLDER", config['schedule_interval'])

        line = line.replace("INPUT_HOLDER", config['input'])

        print(line, end="")