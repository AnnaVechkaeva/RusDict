import codecs, json
from os.path import join, dirname
import sqlite3 as sqlite
from flask import Flask, redirect, url_for, escape, request, render_template
app = Flask(__name__)

def names():
    s = join(dirname(__file__))
    return(s)
    
    
@app.route('/')
def index():
    return render_template('search.html')

@app.route('/dict', methods=['GET', 'POST'])
def dictionary(name=None):
    if request.method == 'POST':
        word = request.form['word']
        word1 = request.form['word_m']
        word = word.upper()
        word1 = word1.upper()
        year1 = request.form['year_1']
        year1_1 = request.form['year_1_1']
        year1_2 = request.form['year_1_2']
        year2 = request.form['year_2']
        year2_1 = request.form['year_2_1']
        year2_2 = request.form['year_2_2']
        cent1 = request.form.getlist('cent_1')
        cent2 = request.form.getlist('cent_2')
        word_te = request.form['word_te']
        value_part_of_speech = request.form.getlist('part_of_speech')
        value_tran = request.form.getlist('tran')
        value_language = request.form.getlist('language')
        value_genre = request.form.getlist('genre')
        connection = sqlite.connect(names()+'/RusDict.db')
        cursor = connection.cursor()
        sql=""
        count = 0
        if word != '':
            if count == 1:
                sql += ' AND'
            if count == 0:
                sql += ' WHERE'
                count = 1
            sql = sql + " (Word1 IS '"+word+"' OR Word2 IS '"+word+"')"
        if word1 != '':
            if count > 0:
                sql += ' AND'
            else:
                sql += ' WHERE'
                count = 2
            sql = sql + " (Word1 LIKE '"+word1+"' OR Word2 LIKE '"+word1+"')"
        if value_part_of_speech != []:
            if count > 0:
                sql += " AND ("
            else:
                sql += " WHERE ("
            for i in value_part_of_speech:
                if count != 4:
                    sql += " Gram1 LIKE '%"+i+"%' OR Gram2 LIKE '%" + i + "%'"
                    count = 4
                else:
                    sql += " OR Gram1 LIKE '%"+i+"%' OR Gram2 LIKE '%" + i + "%'"
            sql += ')'
        
        if year1 != '':
            if count > 0:
                sql += " AND"
            if count == 0:
                sql += " WHERE"
            count = 5
            sql = sql + " date1 = "+year1+" AND date2 =" +year1
        
        if word_te != '':
            if count > 0:
                sql += " AND"
            if count == 0:
                sql += " WHERE"
            count = 6
            sql = sql + " example LIKE '%"+word_te+"%'"
        if value_tran != []:
            for i in value_tran:
                if count > 0 and count != 7:
                    sql += " AND"
                if count == 7:
                    sql += " OR"
                if count == 0:
                    sql += " WHERE"
                count = 7
                if i == "on":
                    sql += " Lang != ''"
                if i == "off":
                    sql += " Lang = ''"
        if value_language != []:
            for i in value_language:
                if count > 0 and count != 8:
                    sql += " AND"
                if count == 8:
                    sql += " OR"
                if count == 0:
                    sql += " WHERE"
                count = 8
                sql += " Lang LIKE '%" + i + "%'"
        
        if value_genre != []:
            arr1 = []
            for i in value_genre:
                if i == "biblia_apokrify":
                    arr1.append('Bib1')
                    arr1.append('Bib')
                elif i == "bogoslovie":
                    arr1.append("Bog1")
                    arr1.append("Bog")
                elif i == "agiografia":
                    arr1.append("Agiogr")
                    arr1.append("Agiogr1")
                elif i == "povesti_belletristika":
                    arr1.append('Pov')
                    arr1.append("Pov1")
                elif i == "gomiletika":
                    arr1.append("Gomilet")
                    arr1.append("Gom1")
                elif i == "liturgika":
                    arr1.append("Litur")
                    arr1.append("Litur1")
                elif i == "epistolografia":
                    arr1.append("Epi")
                    arr1.append("Epi1")
                elif i == "letopis":
                    arr1.append("Letop")
                elif i == "hronika_hronografia":
                    arr1.append("Letop")
                elif i == "dokumenty":
                    arr1.append("Docum")
                    arr1.append("Docum1")
            for j in arr1:
                if count > 0 and count != 9:
                    sql += " AND ("
                if count == 9:
                    sql += " OR"
                if count == 0:
                    sql += " WHERE ("
                count = 9
                sql += " " + j + " LIKE '%+%'"
            sql += ')'
        
        if year1_1 != '' and year1_2 != '':
            if count > 0:
                sql += " AND ("
            if count == 0:
                sql += " WHERE ("
            count = 10
            sql = sql + " (date1 <= "+year1_1+" AND date2 >=" +year1_1 +") OR (date1 <= "+year1_2+" AND date2 >=" +year1_2 +") OR (date1 >=" +year1_1+" AND date2 <= " +year1_2+")"
            sql += ')'
        if cent1 != []:
            for i in cent1:
                min_y = str(int(i)*100-100)
                max_y = str(int(i)*100)
                if count > 0 and count != 11:
                    sql += " AND ("
                if count == 11:
                    sql += " OR"
                if count == 0:
                    sql += " WHERE ("
                count = 11
                sql = sql + " date1 <= "+i+" AND date2 >=" +i+' OR (date1 >=' + min_y + " AND date2 <=" + max_y +')'
            sql += ')'
        if cent2 != []:
            for i in cent2:
                min_y = str(int(i)*100-100)
                max_y = str(int(i)*100)
                if count > 0 and count != 11:
                    sql += " AND ("
                if count == 11:
                    sql += " OR"
                if count == 0:
                    sql += " WHERE ("
                count = 11
                sql = sql + " date3 <= "+i+" AND date4 >=" +i +' OR (date3 >=' + min_y + " AND date4 <=" + max_y +')'
            sql += ')'
        if year2 != '':
            if count > 0:
                sql += " AND"
            if count == 0:
                sql += " WHERE"
            count = 12
            sql = sql + " date3 = "+year2+" AND date4 =" +year2
        if year2_1 != '' and year2_2 != '':
            if count > 0:
                sql += " AND ("
            if count == 0:
                sql += " WHERE ("
            count = 13
            sql = sql + " (date3 <= "+year2_1+" AND date4 >=" +year2_1 +") OR (date3 <= "+year2_2+" AND date4 >=" +year2_2 +") OR (date3 >=" +year2_1+" AND date4 <= " +year2_2+")"
            sql += ')'
        #sql = "SELECT * FROM Words JOIN Meanings ON Words.Id = Meanings.IDwords"+sql
        if value_tran == [] and year1 == '' and value_language == [] and value_genre == [] and word_te == '' and year1_1 == '' and year1_2 == '' and cent1 == [] and year2_1 == '' and year2_2 == '' and year2 == '' and cent2 == []:
            sql = "SELECT DISTINCT Words.Id, Words.Word1, Words.Gram1, Words.Word2, Words.Gram2, Words.Link, Words.Full FROM Words"+sql
        else:
            #sql = "SELECT DISTINCT Words.Id, Words.Word1, Words.Gram1, Words.Word2, Words.Gram2, Words.Link, Words.Full FROM (Words JOIN Meanings ON Meanings.IDword=Words.Id) JOIN Examples ON Meanings.Id = Examples.meaningID"+sql
            sql = "SELECT DISTINCT Words.Id, Words.Word1, Words.Gram1, Words.Word2, Words.Gram2, Words.Link, Words.Full FROM ((Words JOIN Meanings ON Meanings.IDword=Words.Id) JOIN Examples ON Meanings.Id = Examples.meaningID) JOIN Sources ON Sources.Id = Examples.source"+sql
        cursor.execute(sql)
        t = cursor.fetchall()
        arr = []
        for j in t:
            ar = []
            for d in j[:6]:
                ar.append(d)
            a = []
            for h in j[6].split('%'):
                a.append(h.split('&'))
            ar.append(a)    
            arr.append(ar)
        return render_template('result.html', name=name, arr = arr) 
    
    return render_template('search.html', name=name)

@app.route('/source', methods=['GET', 'POST'])
def source(name=None):
    if request.method == 'POST':
        connection = sqlite.connect('RusDict.db')
        cursor = connection.cursor()
        sql = "SELECT Id, F_Name, S_Name, Time1, Time2 FROM Sources"
        word = request.form['word']
        value_tran = request.form.getlist('tran')
        value_language = request.form.getlist('language')
        value_genre = request.form.getlist('genre')
        year = request.form['year']
        year1 = request.form['year1']
        count = 0
        if word != '':
            sql += " WHERE F_Name LIKE '%" + word + "%'"
            count = 1
        if value_tran != []:
            if count > 0:
                sql += " AND"
            else:
                sql += " WHERE"
            for i in value_tran:
                if count != 2:
                    if i == 'on':
                        sql += " lang != ''"
                    if i == 'off':
                        sql += " lang NOT LIKE '%_%'"
                    count = 2
                else:
                    if i == 'on':
                        sql += " AND lang != ''"
                    if i == 'off':
                        sql += " AND lang NOT LIKE '%_%'"
                    count = 2
        if value_language != []:
            if count > 0:
                sql += " AND"
            else:
                sql += " WHERE"
            for i in value_language:
                if count != 3:
                    sql += " example LIKE '%"+i+"%'"
                    count = 3
                else:
                    sql += " OR '%"+i+"%'"
        if value_genre != []:
            if count > 0:
                sql += " AND"
            else:
                sql += " WHERE"
            for i in value_genre:
                if count != 4:
                    if i != 'letopis':
                        sql = sql + ' ' + i + u" LIKE '%y%' OR " + i + "1 LIKE '%y%'" 
                        count = 4
                    else:
                        sql = sql + ' ' + i + u" LIKE '%y%'"
                else:
                    if i != 'letopis':
                        sql = sql + " OR " + i + u" LIKE '%y%' OR " + i + "1 LIKE '%y%'"
                    else:
                        sql = sql + " OR " + i + u" LIKE '%y%'"
        
        if year != '':
            if count > 0:
                sql += " AND"
            if count == 0:
                sql += " WHERE"
            sql = sql + " Time1 LIKE '%"+year+"%'"
        if year1 != '':
            if count > 0:
                sql += " AND"
            if count == 0:
                sql += " WHERE"
            sql = sql + " Time2 LIKE '%"+year1+"%'"
        cursor.execute(sql)
        t = cursor.fetchall()
        arr = []
        for i in t:
            arr.append([i[0], i[1]])
        return render_template('source_result.html', name=name, arr=arr) 
    return render_template('source.html', name=name)
@app.route('/link_part_of_speach', methods=['GET', 'POST'])
def link_part_of_speech(name=None):
    part_of_speech = request.form['part_of_speech']
    sql = "SELECT DISTINCT Id, Word1, Gram1, Word2, Gram2, Link, Full FROM Words WHERE Gram1 LIKE '%"+part_of_speech+"%' OR Gram2 LIKE '%"+part_of_speech+"%'"
    arr = []
    connection = sqlite.connect('RusDict.db')
    cursor = connection.cursor()
    cursor.execute(sql)
    t = cursor.fetchall()
    arr = []
    for j in t:
        ar = []
        for d in j[:6]:
            ar.append(d)
        a = []
        for h in j[6].split('%'):
            a.append(h.split('&'))
        ar.append(a)    
        arr.append(ar)
    return render_template('result.html', name=name, arr = arr) 

@app.route('/link_word', methods=['GET', 'POST'])
def link_word(name=None):
    word = request.form['word']
    word = word.upper()
    sql = "SELECT DISTINCT Id, Word1, Gram1, Word2, Gram2, Link, Full FROM Words WHERE Word1 LIKE '%"+word+"%' OR Word2 LIKE '%"+word+"%'"
    arr = []
    connection = sqlite.connect('RusDict.db')
    cursor = connection.cursor()
    cursor.execute(sql)
    t = cursor.fetchall()
    arr = []
    for j in t:
        ar = []
        for d in j[:6]:
            ar.append(d)
        a = []
        for h in j[6].split('%'):
            a.append(h.split('&'))
        ar.append(a)    
        arr.append(ar)
    return render_template('result.html', name=name, arr = arr) 


@app.route('/link_source', methods=['GET', 'POST'])
def link_source(name=None):
    source_id = request.form['source_id']
    sql = "SELECT * FROM Sources WHERE Id = "+source_id
    arr = []
    connection = sqlite.connect('RusDict.db')
    cursor = connection.cursor()
    cursor.execute(sql)
    t = cursor.fetchall()
    counter = 0
    for i in t:
        if i[5] == '' or i[5] is None or i[5] == '1' or i[5] == 1:
            a = []
            a.append(i)
            #a.append([1,2,3,4,5,6,7,8,9,0])
            arr.append(a)
            counter = 0
        else:
            arr[len(arr)-1].append(i)
            counter = 1
    return render_template('result.html', name=name, arr = arr)
@app.route('/link_w', methods=['GET', 'POST'])
def link_w(name=None):
    connection = sqlite.connect('RusDict.db')
    cursor = connection.cursor()
    word = request.form['word1']
    word = word.lower()
    value_tran = request.form.getlist('tran')
    value_language = request.form.getlist('language')
    value_genre = request.form.getlist('genre')
    year1 = request.form['year1']
    year1_1 = request.form['year1_1']
    year1_2 = request.form['year1_2']
    year2 = request.form['year2']
    year2_1 = request.form['year2_1']
    year2_2 = request.form['year2_2']
    cent1 = request.form.getlist('cent1')
    cent2 = request.form.getlist('cent2')
    sql = ""
    count = 0
    if word != '':
            if count == 1:
                sql += ' AND'
            if count == 0:
                sql += ' WHERE'
                count = 1
            sql = sql + " (Lower LIKE '%"+word+"%')"
    if value_tran != []:
        for i in value_tran:
            if count > 0 and count != 7:
                sql += " AND"
            if count == 7:
                sql += " OR"
            if count == 0:
                sql += " WHERE"
                count = 7
            if i == "on":
                sql += " Lang != ''"
            if i == "off":
                sql += " Lang = ''"
    if value_language != []:
        for i in value_language:
            if count > 0 and count != 8:
                sql += " AND"
            if count == 8:
                sql += " OR"
            if count == 0:
                sql += " WHERE"
                count = 8
            sql += " Lang LIKE '%" + i + "%'"
    if value_genre != []:
        arr1 = []
        for i in value_genre:
            if i == "biblia_apokrify":
                arr1.append('Bib1')
                arr1.append('Bib')
            elif i == "bogoslovie":
                arr1.append("Bog1")
                arr1.append("Bog")
            elif i == "agiografia":
                arr1.append("Agiogr")
                arr1.append("Agiogr1")
            elif i == "povesti_belletristika":
                arr1.append('Pov')
                arr1.append("Pov1")
            elif i == "gomiletika":
                arr1.append("Gomilet")
                arr1.append("Gom1")
            elif i == "liturgika":
                arr1.append("Litur")
                arr1.append("Litur1")
            elif i == "epistolografia":
                arr1.append("Epi")
                arr1.append("Epi1")
            elif i == "letopis":
                arr1.append("Letop")
            elif i == "hronika_hronografia":
                arr1.append("Letop")
            elif i == "dokumenty":
                arr1.append("Docum")
                arr1.append("Docum1")
        for j in arr1:
            if count > 0 and count != 9:
                sql += " AND"
            if count == 9:
                sql += " OR"
            if count == 0:
                sql += " WHERE"
                count = 9
            sql += " " + j + " LIKE '%+%'"
    if year1 != '':
        if count > 0:
            sql += " AND"
        if count == 0:
            sql += " WHERE"
        count = 5
        sql = sql + " Time1 = "+year1+" AND Time2 =" +year1
    if year1_1 != '' and year1_2 != '':
        if count > 0:
            sql += " AND"
        if count == 0:
            sql += " WHERE"
        count = 10
        sql = sql + " (Time1 <= "+year1_1+" AND Time2 >=" +year1_1 +") OR (Time1 <= "+year1_2+" AND Time2 >=" +year1_2 +") OR (Time1 >=" +year1_1+" AND Time2 <= " +year1_2+")"
        
    if cent1 != []:
        for i in cent1:
            min_y = str(int(i)*100-100)
            max_y = str(int(i)*100)
            if count > 0 and count != 11:
                sql += " AND ("
            if count == 11:
                sql += " OR"
            if count == 0:
                sql += " WHERE ("
            count = 11
            sql = sql + " Time1 <= "+i+" AND Time2 >=" +i+' OR (Time1 >=' + min_y + " AND Time2 <=" + max_y +')'
        sql += ')'
    if cent2 != []:
        for i in cent2:
            min_y = str(int(i)*100-100)
            max_y = str(int(i)*100)
            if count > 0 and count != 11:
                sql += " AND ("
            if count == 11:
                sql += " OR"
            if count == 0:
                sql += " WHERE ("
            count = 11
            sql = sql + " Time3 <= "+i+" AND Time4 >=" +i+' OR (Time3 >=' + min_y + " AND Time4 <=" + max_y +')'
        sql += ')'
    if year2 != '':
        if count > 0:
            sql += " AND"
        if count == 0:
            sql += " WHERE"
        count = 12
        sql = sql + " Time3 = "+year2+" AND Time4 =" +year2
    if year2_1 != '' and year2_2 != '':
        if count > 0:
            sql += " AND"
        if count == 0:
            sql += " WHERE"
        count = 13
    arr = []
    sql = "SELECT DISTINCT Name FROM Sources" +sql
    cursor.execute(sql)
    t = cursor.fetchall()
    return render_template('source_result.html', arr = t)

if __name__ == '__main__':
    app.run()

def roman2arabic(roman):
    digit = {"l":1,"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    arabic = 0
    for d in range(len(roman)):
        try:
            if digit[roman[d]]<digit[roman[d+1]]:
                arabic-=digit[roman[d]]
            else:
                arabic+=digit[roman[d]]
        except IndexError:
            arabic+=digit[roman[d]]
    return arabic
