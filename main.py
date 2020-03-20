#! /usr/bin/python
# -*- coding:utf-8 -*-
import flask
from flask import Flask,request
from flask import render_template
import json
from pprint import pprint
import collections
import os,sys
app=Flask(__name__)


# import argparse
# parser=argparse.ArgumentParser()
# parser.add_argument("port")
# args=parser.parse_args()
port='5001'
evaluateurs={}
evaluateurs['5000']='Jocelyne'
evaluateurs['5001']='Jean-Yves'
evaluateurs['5002']='Inconnu-1'
evaluateurs['5003']='Inconnu-2'
evaluateurs['5004']='Inconnu-3'
evaluateurs['5005']='Inconnu-4'
evaluateurs['5006']='Inconnu-5'
evaluateurs['5007']='Inconnu-6'
evaluateurs['5008']='Inconnu-7'
evaluateurs['5009']='Inconnu-8'
evaluateurs['5010']='Inconnu-9'

# evaluateurs_en={}
evaluateurs['5011']='inconnu-en1'
evaluateurs['5012']='inconnu-en2'
evaluateurs['5013']='inconnu-en3'
evaluateurs['5014']='inconnu-en4'
evaluateurs['5015']='inconnu-en5'
evaluateurs['5016']='inconnu-en6'
evaluateurs['5017']='inconnu-en7'
evaluateurs['5018']='inconnu-en8'
evaluateurs['5019']='inconnu-en9'
evaluateurs['5020']='inconnu-en10'


######## FR
save_form = []
save_form_nb = []
res_quereo_fr = collections.OrderedDict()
# chaine="Résultat d'évaluation de "+ evaluateurs[args.port]+ " sur le corpus QUEREO_FR "
chaine="Résultat d'évaluation de "+ evaluateurs[port]+ " sur le corpus QUEREO_FR "

res_quereo_fr["comment"] = chaine
res_quereo_fr["data"] = []
questions = []
fileToOpen = 'data/Quereo_FR_UD55/AnswersToEvaluate_SecondRound.json'
with open(fileToOpen, encoding='utf-8') as f:
    data = json.load(f)
for row in data['data']:
    q_object = collections.OrderedDict()
    q_object["ID"] = data['data'][row]["ID"]
    q_object["QUESTION"] = data['data'][row]["QUESTION"]
    q_object["SHORT_ANSWER"] = data['data'][row]["SHORT_ANSWER"]
    q_object["GENERATED_ANSWER"] = data['data'][row]["GENERATED_ANSWER"]
    q_object["MISSING_WORD"] = data['data'][row]["MISSING_WORD"]
    q_object["Need_LM_Assessing"] = data['data'][row]["Need_LM_Assessing"]
    q_object["CONFIGURATION_FILES"] = data['data'][row]["CONFIGURATION_FILE"]
    q_object["EVALUATION"] = "évaluer"
    q_object["ERROR"] = "évaluer"
    q_object["COMMENT"] = ""
    questions.append(q_object)


############## EN

save_form_en = []
save_form_nb_en=[]
questions_en=[]
res_quereo_en=collections.OrderedDict()
# chaine_en="Résultat d'évaluation de "+evaluateurs[args.port]+"  sur le corpus QUEREO_EN"
chaine_en="Résultat d'évaluation de "+evaluateurs[port]+"  sur le corpus QUEREO_EN"

res_quereo_en["comment"]=chaine_en
res_quereo_en["data"]=[]
fileToOpen_en='data/Quereo_ENG/AnswersToEvaluate_SecondRound.json'
with open(fileToOpen_en, encoding='utf-8') as f_en:
    data = json.load(f_en)
for row in data['data']:
    q_object = collections.OrderedDict()
    q_object["ID"] = data['data'][row]["ID"]
    q_object["QUESTION"] = data['data'][row]["QUESTION"]
    q_object["SHORT_ANSWER"] = data['data'][row]["SHORT_ANSWER"]
    q_object["GENERATED_ANSWER"] = data['data'][row]["GENERATED_ANSWER"]
    q_object["MISSING_WORD"] = data['data'][row]["MISSING_WORD"]
    q_object["Need_LM_Assessing"] = data['data'][row]["Need_LM_Assessing"]
    q_object["CONFIGURATION_FILES"] = data['data'][row]["CONFIGURATION_FILE"]
    q_object["EVALUATION"] = "évaluer"
    q_object["ERROR"] = "évaluer"
    q_object["COMMENT"] = ""
    questions_en.append(q_object)


@app.route('/')
def index():
    # return "Hello world !"
    return render_template('index.html')

@app.route('/quereo_fr.html',methods=['POST','GET'])
def quereo_fr():
    # if save_form:
    #     return render_template('quereo_fr.html', len=len(questions), content=save_form)
    # else:
    #     return render_template('quereo_fr.html', len=len(questions), content=questions)
    nb_reponse=request.args.get('nbr')
    flag=request.args.get('flag')
    if request.args.get('flag') == "save":
        # msg="here"
        # return render_template('test.html',msg=msg)
        save_form.clear()
        save_form_nb.clear()
        for i in range(0, len(questions)):
            q_object = collections.OrderedDict()
            q_object["ID"] = questions[i]["ID"]
            q_object["QUESTION"] = questions[i]["QUESTION"]
            q_object["SHORT_ANSWER"] = questions[i]["SHORT_ANSWER"]
            q_object["GENERATED_ANSWER"] = questions[i]["GENERATED_ANSWER"]
            q_object["MISSING_WORD"] = questions[i]["MISSING_WORD"]
            q_object["Need_LM_Assessing"] = questions[i]["Need_LM_Assessing"]
            q_object["CONFIGURATION_FILES"] = questions[i]["CONFIGURATION_FILES"]
            q_object["EVALUATION"] = request.form['eval' + str(i)]
            q_object["ERROR"] = request.form.getlist('erreur' + str(i))
            q_object["COMMENT"] = request.form['comment' + str(i)]
            save_form.append(q_object)
        # datafile = open('data/savedForm_'+evaluateurs[args.port]+'.json', 'w', encoding='utf-8')
        datafile = open('data/savedForm_'+evaluateurs[port]+'.json', 'w', encoding='utf-8')

        save_form_nb.append((nb_reponse,save_form))
        datafile.write(json.dumps(save_form_nb, sort_keys=False, ensure_ascii=False, indent=4))
        return render_template('quereo_fr.html', len=len(save_form), content=save_form, nbrep=nb_reponse, flag=flag)
    else:
        if save_form:
            return render_template('quereo_fr.html', len=len(questions), content=save_form, nbrep=save_form_nb[0][0],flag='recover')
        # elif os.path.isfile('data/savedForm_'+evaluateurs[args.port]+'.json'):
        elif os.path.isfile('data/savedForm_' + evaluateurs[port] + '.json'):
            # sfile = open('data/savedForm_'+evaluateurs[args.port]+'.json', encoding='utf-8')
            sfile = open('data/savedForm_' + evaluateurs[port] + '.json', encoding='utf-8')
            sfile_data = json.load(sfile)
            return render_template('quereo_fr.html', len=len(questions), content=sfile_data[0][1], nbrep=sfile_data[0][0],flag='recover')
        else:
            return render_template('quereo_fr.html', len=len(questions), content=questions)


@app.route('/quereo_en.html', methods=['POST','GET'])
def quereo_en():
    # return render_template('quereo_en.html', len=len(questions_en), content=questions_en)
    nb_reponse = request.args.get('nbr')
    flag = request.args.get('flag')
    if request.args.get('flag') == "save":
        # msg="here"
        # return render_template('test.html',msg=msg)
        save_form_en.clear()
        save_form_nb_en.clear()
        for i in range(0, len(questions_en)):
            q_object = collections.OrderedDict()
            q_object["ID"] = questions_en[i]["ID"]
            q_object["QUESTION"] = questions_en[i]["QUESTION"]
            q_object["SHORT_ANSWER"] = questions_en[i]["SHORT_ANSWER"]
            q_object["GENERATED_ANSWER"] = questions_en[i]["GENERATED_ANSWER"]
            q_object["MISSING_WORD"] = questions_en[i]["MISSING_WORD"]
            q_object["Need_LM_Assessing"] = questions_en[i]["Need_LM_Assessing"]
            q_object["CONFIGURATION_FILES"] = questions_en[i]["CONFIGURATION_FILES"]
            q_object["EVALUATION"] = request.form['eval' + str(i)]
            q_object["ERROR"] = request.form.getlist('erreur' + str(i))
            q_object["COMMENT"] = request.form['comment' + str(i)]
            save_form_en.append(q_object)
        datafile = open('data/savedFormEN_' + evaluateurs[
            args.port] + '.json', 'w', encoding='utf-8')
        save_form_nb_en.append((nb_reponse, save_form_en))
        datafile.write(json.dumps(save_form_nb_en, sort_keys=False, ensure_ascii=False, indent=4))
        return render_template('quereo_en.html', len=len(save_form_en), content=save_form_en, nbrep=nb_reponse, flag=flag)
    else:
        if save_form_en:
            return render_template('quereo_en.html', len=len(questions_en), content=save_form_en, nbrep=save_form_nb_en[0][0],
                                   flag='recover')
        # elif os.path.isfile('data/savedFormEN_' + evaluateurs[args.port] + '.json'):
        elif os.path.isfile('data/savedFormEN_' + evaluateurs[port] + '.json'):
            # sfileen = open('data/savedFormEN_' + evaluateurs[args.port] + '.json', encoding='utf-8')
            sfileen = open('data/savedFormEN_' + evaluateurs[port] + '.json', encoding='utf-8')
            sfile_data_en = json.load(sfileen)
            return render_template('quereo_en.html', len=len(questions_en), content=sfile_data_en[0][1],
                                   nbrep=sfile_data_en[0][0], flag='recover')
        else:
            return render_template('quereo_en.html', len=len(questions_en), content=questions_en)


@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/documentation.html')
def documentation():
    return render_template('documentation.html')

@app.route('/generation_corpus.html')
def generation_corpus():
    return render_template('generation_corpus.html')


@app.route('/test.html')
def test():
    return render_template('test.html')

@app.route('/resultat_quereo_fr.html', methods=['POST'])
def resultat_quereo_fr():
    res_quereo_fr["data"].clear()
    for i in range(0,len(questions)):
        q_object = collections.OrderedDict()
        q_object["ID"] = questions[i]["ID"]
        q_object["QUESTION"] = questions[i]["QUESTION"]
        q_object["SHORT_ANSWER"] = questions[i]["SHORT_ANSWER"]
        q_object["GENERATED_ANSWER"] = questions[i]["GENERATED_ANSWER"]
        q_object["MISSING_WORD"] = questions[i]["MISSING_WORD"]
        q_object["Need_LM_Assessing"]=questions[i]["Need_LM_Assessing"]
        q_object["CONFIGURATION_FILES"]=questions[i]["CONFIGURATION_FILES"]
        q_object["EVALUATION"]=request.form['eval'+str(i)]
        q_object["ERROR"]=request.form.getlist('erreur' + str(i))
        q_object["COMMENT"]=request.form['comment'+str(i)]
        res_quereo_fr["data"].append(q_object)
    # fr_fname='data/Quereo_FR_UD55/Resultat_Quereo_FR_'+evaluateurs[args.port]+'.json'
    fr_fname = 'data/Quereo_FR_UD55/Resultat_Quereo_FR_' + evaluateurs[port] + '.json'
    datafile = open(fr_fname, 'w', encoding='utf-8')
    datafile.write(json.dumps(res_quereo_fr, sort_keys=False, ensure_ascii=False, indent=4))
    return render_template('resultat_quereo_fr.html')



@app.route('/Quereo_SaveRecover.html', methods=['POST','GET'])
def Quereo_SaveRecover():
    if request.args.get('flag')=="save":
        # msg="here"
        # return render_template('test.html',msg=msg)
        save_form.clear()
        for i in range(0, len(questions)):
            q_object = collections.OrderedDict()
            q_object["ID"] = questions[i]["ID"]
            q_object["QUESTION"] = questions[i]["QUESTION"]
            q_object["SHORT_ANSWER"] = questions[i]["SHORT_ANSWER"]
            q_object["GENERATED_ANSWER"] = questions[i]["GENERATED_ANSWER"]
            q_object["MISSING_WORD"] = questions[i]["MISSING_WORD"]
            q_object["Need_LM_Assessing"] = questions[i]["Need_LM_Assessing"]
            q_object["CONFIGURATION_FILES"] = questions[i]["CONFIGURATION_FILES"]
            q_object["EVALUATION"] = request.form['eval' + str(i)]
            q_object["ERROR"] = request.form['erreur' + str(i)]
            q_object["COMMENT"] = request.form['comment' + str(i)]
            save_form.append(q_object)
        datafile = open('data/savedForm.json', 'w', encoding='utf-8')
        datafile.write(json.dumps(save_form, sort_keys=False, ensure_ascii=False, indent=4))
        return render_template('quereo_fr.html', len=len(questions), content=save_form)
    else:
        # if save_form:
        #     return render_template('quereo_fr.html', len=len(questions), content=save_form)
        if os.path.isfile('data/savedForm.json'):
            sfile=open('data/savedForm.json', encoding='utf-8')
            sfile_data=json.load(sfile)
            return render_template('quereo_fr.html', len=len(questions), content=sfile_data)
        else:
            return render_template('quereo_fr.html', len=len(questions), content=questions)

        # return render_template('quereo_fr.html')




@app.route('/resultat_quereo_en.html', methods=['POST'])
def resultat_quereo_en():
    res_quereo_en["data"].clear()
    for i in range(0,len(questions_en)):
        q_object = collections.OrderedDict()
        q_object["ID"] = questions_en[i]["ID"]
        q_object["QUESTION"] = questions_en[i]["QUESTION"]
        q_object["SHORT_ANSWER"] = questions_en[i]["SHORT_ANSWER"]
        q_object["GENERATED_ANSWER"] = questions_en[i]["GENERATED_ANSWER"]
        q_object["MISSING_WORD"] = questions_en[i]["MISSING_WORD"]
        q_object["Need_LM_Assessing"]=questions_en[i]["Need_LM_Assessing"]
        q_object["CONFIGURATION_FILES"]=questions_en[i]["CONFIGURATION_FILES"]
        q_object["EVALUATION"]=request.form['eval'+str(i)]
        q_object["ERROR"]=request.form.getlist('erreur' + str(i))
        q_object["COMMENT"]=request.form['comment'+str(i)]
        res_quereo_en["data"].append(q_object)
    # en_fname='data/Quereo_ENG/Resultat_Quereo_EN_'+evaluateurs[args.port]+'.json'
    en_fname = 'data/Quereo_ENG/Resultat_Quereo_EN_' + evaluateurs[port] + '.json'
    datafile = open(en_fname, 'w', encoding='utf-8')
    datafile.write(json.dumps(res_quereo_en, sort_keys=False, ensure_ascii=False, indent=4))
    return render_template('resultat_quereo_en.html')


if __name__ == '__main__':

    # app.run(host="0.0.0.0",  port=args.port)
    app.run(host="0.0.0.0")
    # app.run(host="localhost", debug=True)