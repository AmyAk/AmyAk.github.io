import json

from pprint import pprint
import os

f=open('/home/wbql2828/PycharmProjects/Quereo_Human_evaluation/data/savedForm.json')
data = json.load(f)

for row in data:
    pprint(row['ID'])

if os.path.isfile('/home/wbql2828/PycharmProjects/Quereo_Human_evaluation/data/savedForm.json'):
    print("here")