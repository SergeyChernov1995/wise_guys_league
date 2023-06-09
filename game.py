# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------------
# Wise Guys League
# An implementation of the game show project coined by Sergey Chernov aka Gamer
# Copyright © 2023 Sergey Chernov aka Gamer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import time
from enum import Enum
import codecs
from random import randint
from random import choice
from random import randrange
from threading import Timer

class termi(Enum):
    default = 0
    random_pick = 1
    ready = 2
    pressed = 3
    after = 4
    noans = 5

class esh_stage(Enum):
    nachalo = 0
    priem = 1
    vse = 2
    no_priem = 3

stageII = esh_stage.nachalo
active = 0
player_term = [None, None]
_duel = termi.default
root = tk.Tk()
root.geometry("1024x768")
root.title("Лига Умников")
root.resizable(width=False, height=False)
duels = [[1, 2], [3, 4], [1, 3], [2, 4], [4, 1], [2, 3]]
log = codecs.open('log.txt', 'a', "utf_8_sig")
start_names = [[], []]
player = [[], []]
aux_list = [[], []]
labels_q = [[], []]
labels_m = [[], []]
kiek_klausimu_buvo_kvalifikacijoje = 0
index_term = 0
TermQ = []
buzzer = []
marj = [100, 0]
kto_nazhal = None
esh2_money = [2000, 2000, 3000, 3000, 4000, 4000, 5000, 5000]
esh2_numvar = [2,2,3,3,4,4,5,5]
esh1_money = [5000, 5000, 15000, 15000, 30000, 30000]
esh1_numvar = [4,4,5,5,6,6]
esh2_players = []
esh1_players = []
esh2_labels_n,  esh2_labels_m = [], []
esh1_labels_n, esh1_labels_m = [], []
termotvet = tkinter.StringVar()
final_q_ans = tkinter.StringVar()
final_1esh_q_ans = tkinter.StringVar()
Terminator_Question = None
runda_druga_drugi = 0
runda_druga_pierwszy = 0
que_num = 0
qterm = open('qbaset.txt', 'r')  # stage+1
for line in qterm:
    xi = {}
    HUH = line.rstrip("\n")
    xi["Q"] = HUH
    xi["A"] = list(map(str, qterm.readline().split()))
    test = []
    TermQ.append(xi)
qterm.close()

#q_stage2_2esh = open('questions_2esh.txt', 'r')
esh2base = []
vencer = []
testa = codecs.open("questions_2esh.txt", 'r', "utf_8_sig")
testb = testa.readlines()
testc = len(testb)
testd = 0
while True:
    testf = {}
    testf["round"] = int(testb[testd].rstrip('\n'))
    testd+=1
    testf["q"] = testb[testd].rstrip('\n')
    testf["v"] = []
    if (testf["round"]<=4):
        for testg in range(testf["round"]+1):
            testd+=1
            testf["v"].append(testb[testd].rstrip('\n'))
        testd+=1
        testf["c"] = int(testb[testd].rstrip('\n'))
    else:
        testf["v"] = None
        testd+=1
        testf["c"] = list(map(str, testb[testd].split(", ")))
        testf["c"][-1]=testf["c"][-1].rstrip("\n")
    esh2base.append(testf)
    testd+=1
    if (testd >= testc-1 ):
        break
testa.close()

#q_stage2_1esh = open('questions_1esh.txt', 'r')
esh1base = []
testa1 = codecs.open("questions_1esh.txt", 'r', "utf_8_sig")
testb = testa1.readlines()
testc = len(testb)
testd = 0
while True:
    testf = {}
    testf["round"] = int(testb[testd].rstrip('\n'))
    testd+=1
    testf["q"] = testb[testd].rstrip('\n')
    testf["v"] = []
    if (testf["round"]<=3):
        for testg in range(testf["round"]+3):
            testd+=1
            testf["v"].append(testb[testd].rstrip('\n'))
        testd+=1
        testf["c"] = int(testb[testd].rstrip('\n'))
    else:
        testf["v"] = None
        testd+=1
        testf["c"] = list(map(str, testb[testd].split(", ")))
        testf["c"][-1]=testf["c"][-1].rstrip("\n")
    esh1base.append(testf)
    testd+=1
    if (testd >= testc-1 ):
        break
testa1.close()


def clr():
    global buzzer, Terminator_Question
    for i in range(len(buzzer)):
        buzzer[i].place_forget()
    Terminator_Question.place_forget()


def accepted_in_terminator(*args):
    global _duel, kiek_klausimu_buvo_kvalifikacijoje
    global kto_nazhal
    if (not (kto_nazhal is None)):
        otvet = str(termotvet.get())
        log.write("Игрок даёт ответ " + otvet + '\n')
        no_spaces = otvet.replace(" ", "")
        no_sp_lower = no_spaces.lower()
        if (no_sp_lower == TermQ[index_term]["A"][0]):
            tk.messagebox.showinfo("Верно!", "Поздравляю, ответ правильный!")
            log.write("Это верный ответ" + '\n')
        elif (no_sp_lower in TermQ[index_term]["A"]):
            tk.messagebox.showinfo("Верно!", "Правильный ответ - " + TermQ[index_term]["A"][0])
            log.write("Это верный ответ (" + TermQ[index_term]["A"][0] + ')' + '\n')
        else:
            tk.messagebox.showinfo("Неверно!", "Ошибка! Правильный ответ - " + TermQ[index_term]["A"][0])
            log.write("Это неверный ответ. Правильный ответ - " + TermQ[index_term]["A"][0] + '\n')
        if ((kto_nazhal == 0) and (no_sp_lower in TermQ[index_term]["A"])) or (
                (kto_nazhal == 1) and not (no_sp_lower in TermQ[index_term]["A"])):
            winner = player_term[0]
        elif ((kto_nazhal == 1) and (no_sp_lower in TermQ[index_term]["A"])) or (
                (kto_nazhal == 0) and not (no_sp_lower in TermQ[index_term]["A"])):
            winner = player_term[1]
        # aux_list[player_term[winner] // 4][player_term[winner] % 4]['points'] +=3
        # labels_m[player_term[winner] // 4][player_term[winner] % 4]['text'] = aux_list[player_term[winner] // 4][player_term[winner] % 4]['points']
        aux_list[winner // 4][winner % 4]['points'] += 3
        labels_m[winner // 4][winner % 4]['text'] = \
        aux_list[winner // 4][winner % 4]['points']
        _duel = termi.default
        kto_nazhal = None
        kiek_klausimu_buvo_kvalifikacijoje+=1
        clr()
        show(kiek_klausimu_buvo_kvalifikacijoje)


def accepted9(*args):
    global active, stageII
    if (stageII!=esh_stage.vse):
        respuesta_para_la_ultima_pregunta = final_q_ans.get()
        log.write(esh2_players[active-1]['name']+"  даёт ответ " + respuesta_para_la_ultima_pregunta + '\n')
        no_spaces = respuesta_para_la_ultima_pregunta.replace(" ", "")
        no_sp_lower = no_spaces.lower()
        ghbdtn = []
        for i in range(len(esh2base[que_num]['c'])):
            ghbdtn.append(esh2base[que_num]['c'][i])
            ghbdtn[i]=ghbdtn[i].replace(' ', '')
            ghbdtn[i] = ghbdtn[i].lower()
        if (no_sp_lower in ghbdtn):
            uyy = esh2_players[active-1]['money']
            uyy += uyy*marj[1]//100
            esh2_players[active - 1]['money'] = uyy
        esh2_fillintheblank.config(state="disabled")
        #print(esh2_players[active-1]['money'])
        dummy_entry.focus_set()
        koi(2)

def accepted7(*args):
    global active, stageII
    if (stageII!=esh_stage.vse):
        respuesta_para_la_ultima_pregunta = final_1esh_q_ans.get()
        log.write(esh1_players[active-1]['name']+"  даёт ответ " + respuesta_para_la_ultima_pregunta + '\n')
        no_spaces = respuesta_para_la_ultima_pregunta.replace(" ", "")
        no_sp_lower = no_spaces.lower()
        ghbdtn = []
        for i in range(len(esh1base[que_num]['c'])):
            ghbdtn.append(esh1base[que_num]['c'][i])
            ghbdtn[i]=ghbdtn[i].replace(' ', '')
            ghbdtn[i] = ghbdtn[i].lower()
        if (no_sp_lower in ghbdtn):
            uyy = esh1_players[active-1]['money']
            uyy += uyy*marj[0]//100
            esh1_players[active - 1]['money'] = uyy
        esh1_fillintheblank.config(state="disabled")
        #print(esh1_players[active-1]['money'])
        dummy_entry.focus_set()
        koi(1)

def vyznachyty_peremozhcia(w):
    global vencer
    winner = max(w, key=lambda x: x['money'])
    #print(winner)
    # counter = len([i for i in orig if i['money']==winner['money']])
    kas_uzvareja = []
    for kk in range(len(w)):
        if w[kk]['money'] == winner['money']:
            kas_uzvareja.append(w[kk])
    #print(orig)
    # print(counter)
    if (len(kas_uzvareja) == 1):
        tk.messagebox.showinfo("Победитель эшелона - " + kas_uzvareja[0]['name'], 'Выигрыш: '+str(kas_uzvareja[0]['money']))
        log.write("Победитель эшелона - " + kas_uzvareja[0]['name']+'. Выигрыш: '+str(kas_uzvareja[0]['money'])+'\n')
    else:
        uiu = []
        for a in range(len(kas_uzvareja)):
            uiu.append(kas_uzvareja[a]['name'])
        ryadok = ', '.join(uiu)
        tk.messagebox.showinfo('У нас несколько победителей!', 'Победители эшелона - ' + ryadok+'\n. Каждый победитель получит по '+str(kas_uzvareja[0]['money']))
        log.write('Победители эшелона - ' + ryadok+'\n. Каждый победитель получит по '+str(kas_uzvareja[0]['money'])+'\n')


def stoptimer():
    root.after_cancel(root.time_is_up)

def expired():
    global _duel, kiek_klausimu_buvo_kvalifikacijoje
    root.after_cancel(root.time_is_up)
    log.write("Никто не дал ответа\n"+"Правильный ответ: "+TermQ[index_term]["A"][0]+'\n')
    _duel = termi.noans
    tk.messagebox.showinfo("Никто не дал ответа", "Правильный ответ: "+TermQ[index_term]["A"][0])
    for a in range(2):
        aux_list[player_term[a] // 4][player_term[a] % 4]['points'] +=1
        labels_m[player_term[a] // 4][player_term[a] % 4]['text'] = str(aux_list[player_term[a] // 4][player_term[a] % 4]['points'])
    kiek_klausimu_buvo_kvalifikacijoje+=1
    clr()
    show(kiek_klausimu_buvo_kvalifikacijoje)


def koi(www):
    #root.after_cancel(root.lop)
    global active, stageII, que_num
    if (stageII != esh_stage.vse):
        active += 1
        stageII = esh_stage.priem
        if (www == 2):
            if (active > len(esh2_players)):
                stageII = esh_stage.vse
                tk.messagebox.showinfo("Ждём", "Все игроки эшелона дали ответ")
                if (runda_druga_drugi<=len(esh2_money)):
                    answering[esh2base[que_num]['c']-1]['bg'] = "#80ff80"
                    log.write ("Правильный ответ - "+esh2base[que_num]['v'][esh2base[que_num]['c']-1]+'\n')
                    tk.messagebox.showinfo("Ответ", "Правильный ответ - " + esh2base[que_num]['v'][
                        esh2base[que_num]['c'] - 1] + '\n')
                    active = 0
                    for ki in range(len(esh2_players)):
                        esh2_labels_m[ki]['text'] = str(esh2_players[ki]['money'])
                    esh2base.pop(que_num)
                    next(2)
                else:
                    esh2_fillintheblank.place_forget()
                    dummy_entry.focus_set()
                    #answering[esh2base[que_num]['c']-1]['bg'] = "#80ff80"
                    log.write ("Правильный ответ - "+esh2base[que_num]['c'][0]+'\n')
                    tk.messagebox.showinfo("Ответ", "Правильный ответ - "+esh2base[que_num]['c'][0])
                    active = 0
                    for ki in range(len(esh2_players)):
                        esh2_labels_m[ki]['text'] = str(esh2_players[ki]['money'])
                    log.write("Итог второго эшелона: \n")
                    vyznachyty_peremozhcia(esh2_players)
                    for a in range(len(esh2_players)):
                        esh2_labels_n[a].place_forget()
                        esh2_labels_m[a].place_forget()
                    esh2base.pop(que_num)
                    for a in range(len(esh1_players)):
                        esh1_labels_n[a].place(relx=0.1, rely=0.04 + 0.07 * a)
                        esh1_labels_m[a].place(relx=0.18, rely=0.04 + 0.07 * a)
                    log.write("Первый эшелон: \n")
                    next(1)
            else:
                stageII = esh_stage.priem
                if (runda_druga_drugi<=len(esh2_money)):
                    for a in range(len(esh2base[que_num]['v'])):
                        answering[a]["state"] = "normal"
                        answering[a].place(relx=0.67, rely=0.02 + 0.07 * a)
                        #print(answering[a]['text'])
                    tk.messagebox.showinfo(esh2_players[active - 1]["name"], 'Дайте свой ответ')
                    # stageII = esh_stage.no_priem
                    # koi(www)
                else:
                    tk.messagebox.showinfo(esh2_players[active - 1]["name"], 'Дайте свой ответ')
                    final_q_ans.set("")
                    esh2_fillintheblank.config(state="normal")
        elif (www == 1):
            if (active > len(esh1_players)):
                stageII = esh_stage.vse
                tk.messagebox.showinfo("Ждём", "Все игроки эшелона дали ответ")
                if (runda_druga_pierwszy<=len(esh1_money)):
                    answering[esh1base[que_num]['c']-1]['bg'] = "#80ff80"
                    log.write ("Правильный ответ - "+esh1base[que_num]['v'][esh1base[que_num]['c']-1]+'\n')
                    tk.messagebox.showinfo("Ответ", "Правильный ответ - " + esh1base[que_num]['v'][
                        esh1base[que_num]['c'] - 1] + '\n')
                    active = 0
                    for ki in range(len(esh1_players)):
                        esh1_labels_m[ki]['text'] = str(esh1_players[ki]['money'])
                    esh1base.pop(que_num)
                    next(1)
                else:
                    esh1_fillintheblank.place_forget()
                    dummy_entry.focus_set()
                    #answering[esh1base[que_num]['c']-1]['bg'] = "#80ff80"
                    log.write ("Правильный ответ - "+esh1base[que_num]['c'][0]+'\n')
                    tk.messagebox.showinfo("Ответ", "Правильный ответ - "+esh1base[que_num]['c'][0])
                    active = 0
                    for ki in range(len(esh1_players)):
                        esh1_labels_m[ki]['text'] = str(esh1_players[ki]['money'])
                    log.write("Итог первого эшелона: \n")
                    vyznachyty_peremozhcia(esh1_players)
                    for a in range(len(esh1_players)):
                        esh1_labels_n[a].place_forget()
                        esh1_labels_m[a].place_forget()
                    esh1base.pop(que_num)
                    log.write("Игра окончена\n")
                    tk.messagebox.showinfo("Всё", "Игра окончена")
            else:
                stageII = esh_stage.priem
                if (runda_druga_pierwszy<=len(esh1_money)):
                    for a in range(len(esh1base[que_num]['v'])):
                        answering[a]["state"] = "normal"
                        answering[a].place(relx=0.67, rely=0.02 + 0.07 * a)
                        #print(answering[a]['text'])
                    tk.messagebox.showinfo(esh1_players[active - 1]["name"], 'Дайте свой ответ')
                    # stageII = esh_stage.no_priem
                    # koi(www)
                else:
                    tk.messagebox.showinfo(esh1_players[active - 1]["name"], 'Дайте свой ответ')
                    final_1esh_q_ans.set("")
                    esh1_fillintheblank.config(state="normal")





def term():
    global index_term, _duel, player_term
    index_term = randint(0, len(TermQ)-1)
    for w in range(2):
        z = tk.Label(text=aux_list[player_term[w]//4][player_term[w]%4]['name'])
        buzzer.append(z)
    for h in range(2):
        buzzer[h].place (relx = 0.4+0.3*h, rely = 0.59)
        buzzer[h]["bg"] = "#cccccc"
        buzzer[h]["text"] = aux_list[player_term[h]//4][player_term[h]%4]['name']
    log.write("Поединок: " + aux_list[player_term[0]//4][player_term[0]%4]['name']+' vs. '+aux_list[player_term[1]//4][player_term[1]%4]['name']+'\n')
    global Terminator_Question
    Terminator_Question = tk.Label(text=TermQ[index_term]["Q"], justify = tkinter.CENTER, wraplength=255)
    Terminator_Question.place(relx=0.36, rely=0.65)
    log.write("Вопрос: " + TermQ[index_term]["Q"] + '\n')
    _duel = termi.ready
    root.time_is_up = root.after(8000, expired)



def duel(i):
    global _duel, index_term, player_term
    #print(i)
    ord_fixture_in_group = (i-1) % len(duels)
    ord_group = (i-1) // len(duels)
    for c in range(4):
        for a in range(2):
            if (c+1 in duels[ord_fixture_in_group]) and (a == ord_group):
                labels_q[a][c]['bg'] = '#ccccff'
            else:
                labels_q[a][c]['bg'] = '#f0f0f0'
    #print(duels[ord_fixture_in_group])
    for a in range(2):
        player_term[a] = duels[ord_fixture_in_group][a]-1+ord_group*4
    tk.messagebox.showinfo("Поединок", aux_list[player_term[0]//4][player_term[0]%4]['name']+' и '+aux_list[player_term[1]//4][player_term[1]%4]['name']+', приготовиться!')
    term()


def choose(f):
    if (runda_druga_pierwszy == 0):
        log.write(esh2_players[active-1]['name']+' даёт ответ '+esh2base[que_num]['v'][f-1]+'\n')
        if (f==esh2base[que_num]['c']):
            esh2_players[active-1]['money'] += esh2_money[runda_druga_drugi-1]
            #print(esh2_players[active-1]['name']+': +'+str(esh2_money[runda_druga_drugi-1]))
        for a in range(len(esh2base[que_num]['v'])):
            answering[a]['state'] = "disabled"
        los = 2
        koi(los)
    else:
        log.write(esh1_players[active-1]['name']+' даёт ответ '+esh1base[que_num]['v'][f-1]+'\n')
        if (f==esh1base[que_num]['c']):
            esh1_players[active-1]['money'] += esh1_money[runda_druga_pierwszy-1]
            #print(esh1_players[active-1]['name']+': +'+str(esh1_money[runda_druga_pierwszy-1]))
        for a in range(len(esh1base[que_num]['v'])):
            answering[a]['state'] = "disabled"
        los = 1
        koi(los)



def rodyti_klausima(nr):
    global runda_druga_drugi, runda_druga_pierwszy, que_num, stageII, active
    #print('1')
    pole_qu.place(x=10, y=270)
    pole_qu['bg'] = '#8f8f8f'
    for j in range(6):
        answering[j].place_forget()
    if (nr == 2): #второй эшелон
        pole_qu['text'] = esh2base[que_num]['q']
        if (runda_druga_drugi <= len(esh2_money)):
            log.write("Вопрос "+str(runda_druga_drugi)+": "+str(esh2_money[runda_druga_drugi-1])+"\n"+esh2base[que_num]['q']+'\n')
            for a in range(len(esh2base[que_num]['v'])):
                #answering[a].place(x=115, y=380 + 32 * a)
                log.write(str(a + 1) + ". " + esh2base[que_num]["v"][a] + "\n")
                answering[a]['text'] = esh2base[que_num]["v"][a]
                answering[a]['state'] = "disabled"
                answering[a]['bg'] = '#00009f'
        elif (runda_druga_drugi == len(esh2_money)+1):
            log.write("Вопрос "+str(runda_druga_drugi)+": +"+str(marj[nr-1])+"%\n"+esh2base[que_num]['q']+'\n')
            esh2_fillintheblank.place(relx = 0.15, rely = 0.75)
            esh2_fillintheblank.config(state="disabled")
            pass #написать код, позволяющий ввести ответ с клавиатуры
    elif (nr == 1): #первый эшелон
        pole_qu['text'] = esh1base[que_num]['q']
        if (runda_druga_pierwszy <= len(esh1_money)):
            log.write("Вопрос "+str(runda_druga_pierwszy)+": "+str(esh1_money[runda_druga_pierwszy-1])+"\n"+esh1base[que_num]['q']+'\n')
            for a in range(len(esh1base[que_num]['v'])):
                #answering[a].place(x=115, y=380 + 32 * a)
                log.write(str(a + 1) + ". " + esh1base[que_num]["v"][a] + "\n")
                answering[a]['text'] = esh1base[que_num]["v"][a]
                answering[a]['state'] = "disabled"
                answering[a]['bg'] = '#00009f'
        elif (runda_druga_pierwszy == len(esh1_money)+1):
            log.write("Вопрос "+str(runda_druga_pierwszy)+": +"+str(marj[nr-1])+"%\n"+esh1base[que_num]['q']+'\n')
            esh1_fillintheblank.place(relx = 0.15, rely = 0.75)
            esh1_fillintheblank.config(state="disabled")
            pass #написать код, позволяющий ввести ответ с клавиатуры
    stageII = esh_stage.nachalo
    active = 0
    ppp = nr
    koi(nr)





def next(i):
    global runda_druga_drugi, runda_druga_pierwszy, que_num
    if (i == 2):
        runda_druga_drugi +=1
        if (len(esh2_money)>=runda_druga_drugi):
            while True:
                que_num = randint(0, len(esh2base)-1)
                if (esh2base[que_num]['round'] == ((runda_druga_drugi-1)//2)+1):
                    rodyti_klausima(2)
                    break
        elif (len(esh2_money)+1==runda_druga_drugi):
            while True:
                que_num = randint(0, len(esh2base)-1)
                if (esh2base[que_num]['round'] == ((runda_druga_drugi-1)//2)+1):
                    rodyti_klausima(2)
                    break
    elif (i == 1):
        runda_druga_pierwszy +=1
        if (len(esh1_money)>=runda_druga_pierwszy):
            while True:
                que_num = randint(0, len(esh1base)-1)
                if (esh1base[que_num]['round'] == ((runda_druga_pierwszy-1)//2)+1):
                    rodyti_klausima(1)
                    break
        elif (len(esh1_money)+1==runda_druga_pierwszy):
            while True:
                que_num = randint(0, len(esh1base)-1)
                if (esh1base[que_num]['round'] == ((runda_druga_pierwszy-1)//2)+1):
                    rodyti_klausima(1)
                    break








def osn_start():
    global qnum
    for a in range(2):
        for b in range(3):
            labels_q[a][b].place_forget()
            labels_m[a][b].place_forget()
    for a in range(2):
        esh2_players.append(aux_list[a][2])
        lp = tk.Label(text=esh2_players[a]['name'])
        esh2_labels_n.append(lp)
        lm = tk.Label(text=str(esh2_players[a]['money']))
        esh2_labels_m.append(lm)
    for a in range(2):
        for b in range(2):
            esh1_players.append(aux_list[a][b])
            lu = tk.Label(text=esh1_players[a*2+b]['name'])
            esh1_labels_n.append(lu)
            la = tk.Label(text=str(esh1_players[a*2+b]['money']))
            esh1_labels_m.append(la)
    log.write("Второй эшелон\n")
    for a in range(len(esh2_players)):
        esh2_labels_n[a].place(relx=0.1, rely = 0.05+0.08*a)
        esh2_labels_m[a].place(relx=0.18, rely = 0.05+0.08*a)
    #pole_qu.place(x=10, y=510)
    next(2)







def show(q):
    global kiek_klausimu_buvo_kvalifikacijoje, Terminator_Question, _A, _B
    root.after_cancel(root.start_qual)
    vvod.place_forget()
    termotvet.set("")
    if (q == 0):
        _A = tk.Label(text="Группа A")
        _A.place(relx=0.05, rely=0.05)
        _B = tk.Label(text="Группа B")
        _B.place(relx=0.55, rely=0.05)
        for a in range(2):
            for b in range(4):
                c = tk.Label(text = aux_list[a][b]['name'], bg="#f0f0f0")
                labels_q[a].append(c)
                d = tk.Label(text = str(aux_list[a][b]['points']), bg="#f0f0f0")
                labels_m[a].append(d)
                labels_q[a][b].place(relx=0.05+0.5*a, rely=0.15+0.06*b)
                labels_m[a][b].place(relx=0.2+0.5*a, rely=0.15+0.06*b)
                pass #Доделать
        kiek_klausimu_buvo_kvalifikacijoje += 1
        q += 1
        root.new_term = root.after(1500, lambda r=kiek_klausimu_buvo_kvalifikacijoje: show(r))
    elif (q<=12): #12
        kiek_klausimu_buvo_kvalifikacijoje = q
        TermQ.pop(index_term)
        duel(q)
        #show(kiek_klausimu_buvo_kvalifikacijoje)
        q += 1
    else:
        for a in range(2):
            aux_list[a].sort(key = lambda i:(i['points']), reverse=True)
            log.write("Результаты отборочного тура:")
            #print(aux_list[a])
        for a in range(2):
            for b in range(4):
                if (b == 0):
                    log.write("Группа "+chr(65+a)+':\n')
                log.write(str(b+1)+'. '+aux_list[a][b]['name']+'. '+str(aux_list[a][b]['points'])+'\n')
        for a in range(2):
            for b in range(4):
                labels_q[a][b]['text'] = aux_list[a][b]['name']
                labels_m[a][b]['text'] = str(aux_list[a][b]['points'])
                if (b in [0, 1]):
                    labels_q[a][b]['bg'] = '#ccffcc'
                    aux_list[a][b]['money'] = aux_list[a][b]['points'] * 2000
                    log.write(aux_list[a][b]['name']+' отправляется в первый эшелон, имея на счёте '+str(aux_list[a][b]['money'])+'\n')
                elif (b == 2):
                    labels_q[a][b]['bg'] = '#ffffcc'
                    aux_list[a][b]['money'] = aux_list[a][b]['points'] * 1000
                    log.write(aux_list[a][b]['name'] + ' отправляется во второй эшелон, имея на счёте ' + str(
                        aux_list[a][b]['money']) + '\n')
                else:
                    labels_q[a][b]['bg'] = '#7f7f7f'
                    log.write(aux_list[a][b]['name'] + ' выбывает из игры\n')
        tk.messagebox.showinfo("Отбор окончен", "Отборочный этап окончен")
        for a in range(2):
            labels_q[a][3].place_forget()
            labels_m[a][3].place_forget()
            labels_q[a].pop(3)
            aux_list[a].pop(3)
        marj[1] = (aux_list[0][2]['points']+aux_list[1][2]['points'])*4
        #print(marj[1])
        _A.place_forget()
        _B.place_forget()
        root.game_stage_II_start = root.after(4000, osn_start)
         #debug

                #
                # if (b == 0):
                #     log.write("Группа "+chr(65+a)+':\n')
                # log.write(str(b+1)+'. '+start_names[a][b].get()+'\n')
                # aux_dict = {}
                # aux_dict['name'] = start_names[a][b].get()
                # aux_dict['points'] = 0
                # aux_dict['money'] = 0
                # aux_list[a].append(aux_dict)
                # player[a][b].place_forget()

def onKeyPress(event):
    global kto_nazhal, _duel
    if not (_duel == termi.ready):
        pass
    elif not (event.char in set ('AaLlфФдД')):
        pass
    else:
        if (event.char in set('AaфФ')):
            buzzer[0]["bg"]="#ff0000"
            kto_nazhal = 0
        elif (event.char in set('LlдД')):
            buzzer[1]["bg"]="#ff0000"
            kto_nazhal = 1
        log.write('Кнопку нажимает '+aux_list[player_term[kto_nazhal]//4][player_term[kto_nazhal]%4]['name']+'\n')
        root.after_cancel(root.time_is_up)
        _duel = termi.pressed
        vvod.place(relx=0.5, rely = 0.88)
        vvod.focus_set()


def kwalif():
    global aux_list
    for a in range(8):
        if start_names[a//4][a%4].get()=="":
            tk.messagebox.showwarning("Имена", "По меньшей мере у одного из игроков пустое имя. Исправьте")
            break
    else:
        rich.place_forget()
        log.write("Игроки: "+'\n')
        #aux_list = []
        for a in range(2):
            for b in range(4):
                if (b == 0):
                    log.write("Группа "+chr(65+a)+':\n')
                log.write(str(b+1)+'. '+start_names[a][b].get()+'\n')
                aux_dict = {}
                aux_dict['name'] = start_names[a][b].get()
                aux_dict['points'] = 0
                aux_dict['money'] = 0
                aux_list[a].append(aux_dict)
                player[a][b].place_forget()
        root.start_qual = root.after(1500, lambda c=kiek_klausimu_buvo_kvalifikacijoje: show(c))


        #requires further work


def doSomething():
    if tk.messagebox.askyesno("Exit", "Do you want to quit the application?"):
        log.close()
        root.destroy()




for a in range(2):
    for b in range(4):
        dummy = tk.StringVar()
        dummy.set("Игрок "+str((a*4+b+1)))
        start_names[a].append(dummy)

for pl_field in range (8):
    nombre = ttk.Entry(root, textvariable = start_names[pl_field // 4][pl_field % 4])
    player[pl_field // 4].append(nombre)
    player[pl_field // 4][pl_field % 4].place(width=140, relx = 0.03+0.4*(pl_field//4), rely = 0.05+0.2*(pl_field % 4))

answering = []


for pp in range (6):
    v = tk.Button(root, width=27, height = 1, fg = "#ffffff", command = lambda kj=pp+1: choose(kj))
    answering.append(v)


pole_qu = tk.Label(root, width = 68, height=12, justify = tk.CENTER, wraplength=390, text="", bg="#8f8f8f", fg = "#ffffff", anchor = "n")
rich = tk.Button(root, text="Начать игру", command=kwalif, width = 14, height = 30)
rich.place(relx = 0.67, rely=0.05)
log.write('\n')
root.bind('<KeyPress>', onKeyPress)
vvod = tk.Entry(textvariable = termotvet)
vvod.bind("<Return>", accepted_in_terminator)
esh2_fillintheblank = tk.Entry(textvariable = final_q_ans)
esh2_fillintheblank.bind("<Return>", accepted9)
esh1_fillintheblank = tk.Entry(textvariable = final_1esh_q_ans)
esh1_fillintheblank.bind("<Return>", accepted7)
dummy_entry = tk.Entry()
root.protocol('WM_DELETE_WINDOW', doSomething)
root.mainloop()