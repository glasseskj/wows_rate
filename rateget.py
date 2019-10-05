import requests
import json
import os

player = []
shipname = []
battles = []
winrate = []
dmg = []
userteam = 1
fileexist = 3

 #check that file existor not
def readfile():#get info from replayfile
    global fileexist
    if os.path.isfile('setting.txt') == False:
        tempfile = open('setting.txt','w')
        tempfile.close()
    with open('setting.txt' , 'r') as replayfile:
        replaypath = replayfile.read()
        replayfile.close()
    if os.path.isfile(replaypath+'\\tempArenaInfo.json') == False:
        fileexist = 0
    else:
        fileexist = 1
    if fileexist == 1:
        with open(replaypath+'\\tempArenaInfo.json' , 'r') as Infoget:
            Info = json.load(Infoget)
            Infoget.close()
        for i in range(0,len(Info['vehicles']),+1):
            player.append(Info['vehicles'][i])

def datasearching():#using json from replayfile to get player static
    for i in range(0, len(player), +1):
        continueornot = True
        getdata = requests.get('https://api.worldofwarships.asia/wows/account/list/?application_id=326d59e631d3c0014d238810d0fce5d6&search={}'.format(player[i]['name']))
        temp = getdata.text
        find_id = json.loads(temp)
        if find_id['status'] == 'ok':
            account_id = str(find_id['data'][0]['account_id'])
            ship_id = str(player[i]['shipId'])
        if find_id['status'] != 'ok':
            continueornot = False
        url = 'https://api.worldofwarships.asia/wows/ships/stats/?'
        #ship_id = '4281284304'' can be a sample
        getdata = requests.get('{}application_id=326d59e631d3c0014d238810d0fce5d6&account_id={}&fields=pvp.battles&ship_id={}'.format(url,account_id,ship_id))
        temp = getdata.text
        find_battle = json.loads(temp)
        if continueornot == True:
            if find_battle['meta']['hidden'] == None and find_battle['status'] == 'ok':
                battles.append(find_battle['data'][account_id][0]['pvp']['battles'])
            else:
                battles.append(-1)
                continueornot = False
        if continueornot == True:
            getdata = requests.get('{}application_id=326d59e631d3c0014d238810d0fce5d6&account_id={}&fields=pvp.wins&ship_id={}'.format(url,account_id,ship_id))
            temp = getdata.text
            find_wins = json.loads(temp)
            wins = (find_wins['data'][account_id][0]['pvp']['wins'])
            if battles[i] == 0:
                winrate.append(0.0)
            else:
                winrate.append(round(float(wins) / float(battles[i]) * 100, 2))
        else:
            winrate.append(-1)
        getdata = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/ships/?application_id=326d59e631d3c0014d238810d0fce5d6&fields=name&ship_id={}'.format(ship_id))
        temp = getdata.text
        find_ships = json.loads(temp)
        shipname.append(find_ships['data'][ship_id]['name'])


teamA_name=''#for data classification
teamA_winrate=''
teamA_battles=''
teamA_ship=''

teamB_name=''
teamB_winrate=''
teamB_battles=''
teamB_ship=''

def dataprinting():
    global teamA_battles, teamA_name, teamA_winrate, teamA_ship, teamB_battles, teamB_name, teamB_winrate, teamB_ship
    for i in range(0, len(player), +1):
        if player[i]['relation'] == 0:
            player[i]['relation'] = 1
        if player[i]['relation'] == 1:
            w = player[i]['name'] + '\n'
            teamA_name = teamA_name + w#set data in a string
            w = str(winrate[i]) + '%\n'
            teamA_winrate = teamA_winrate + w
            w = str(battles[i]) + '\n'
            teamA_battles = teamA_battles + w
            w = shipname[i] + '\n'
            teamA_ship = teamA_ship + w
        if player[i]['relation'] == 2:
            w = player[i]['name'] + '\n'
            teamB_name = teamB_name + w  # set data in a string
            w = str(winrate[i]) + '%\n'
            teamB_winrate = teamB_winrate + w
            w = str(battles[i]) + '\n'
            teamB_battles = teamB_battles + w
            w = shipname[i] + '\n'
            teamB_ship = teamB_ship + w

def reset():
    global player, battles, winrate, dmg, userteam, fileexist, shipname
    global teamA_battles, teamA_name, teamA_winrate, teamA_ship, teamB_battles, teamB_name, teamB_winrate, teamB_ship
    shipname = []
    player = []
    battles = []
    winrate = []
    dmg = []
    userteam = 1
    fileexist = 3

    teamA_name = ''
    teamA_winrate = ''
    teamA_battles = ''
    teamA_ship = ''

    teamB_name = ''
    teamB_winrate = ''
    teamB_battles = ''
    teamB_ship = ''

from  Tkinter import *
from  ttk import *
import tkMessageBox

def show():
    global showWR, showID, showbattles, showShip
    global teamA_battles, teamA_name, teamA_winrate, teamB_battles, teamB_name, teamB_winrate
    dataprinting()
    showbattles.configure(text=teamA_battles + '\n\n\n' + teamB_battles)
    showWR.configure(text=teamA_winrate + '\n\n\n' + teamB_winrate)
    showID.configure(text=teamA_name + '\n\n\n' + teamB_name)
    showShip.configure(text=teamA_ship + '\n\n\n' + teamB_ship)
    win.update()
    #labelL.configure
win = Tk()
win.title('Rating')
win.geometry('700x500')
win.resizable(0, 0)

def clickSearch():
    reset()
    readfile()
    if fileexist == 0:
        wearning = 'Wrong path or not in battle'
        tkMessageBox.showerror(title='oops!', message=wearning)
    else:
        tkMessageBox.showinfo(title='Json found',message='Please wait until data update')
        datasearching()
        show()
search = Button(win, text="Search", command=clickSearch)
search.pack()

name = Label(win, text='Player ID')
name.place(x=20, y=30, anchor='nw')
battle = Label(win, text='Battle')
battle.place(x=350, y=30, anchor='nw')
wr = Label(win, text='WR')
wr.place(x=500, y=30, anchor='nw')
ship = Label(win,text='Ship')
ship.place(x=200, y=30, anchor='nw')

showID = Label(win, text='ID will be here')#showing string will be put in here
showID.place(x=20, y=80, anchor='nw')
showbattles = Label(win, text='Total battles')
showbattles.place(x=350, y=80, anchor='nw')
showWR = Label(win, text='Win Rate')
showWR.place(x=500, y=80,anchor='nw')
showShip = Label(win,text='Ships')
showShip.place(x=200,y=80)

win.mainloop()
#for i in range(0, len(player), +1):



