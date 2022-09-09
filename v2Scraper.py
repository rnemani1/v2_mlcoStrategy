from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import v2FirestoreManager
from datetime import datetime

def run(URL, letter):
    
    v2FirestoreManager.archive()
    v2FirestoreManager.league_count(URL, get_league(URL))

    if(letter == 'A'):
        t1Spread_span = '(//div[@role="button" and (span or *[name()="svg"])])[2]/span'
        t2Spread_span = '(//div[@role="button" and (span or *[name()="svg"])])[5]/span'
        t1mLine_span = '(//div[@role="button" and (span or *[name()="svg"])])[3]/span'
        t2mLine_span = '(//div[@role="button" and (span or *[name()="svg"])])[6]/span'
    else:
        t1Spread_span = '(//div[@role="button" and (span or *[name()="svg"])])[1]/span'
        t2Spread_span = '(//div[@role="button" and (span or *[name()="svg"])])[4]/span'
        t1mLine_span = '(//div[@role="button" and (span or *[name()="svg"])])[2]/span'
        t2mLine_span = '(//div[@role="button" and (span or *[name()="svg"])])[5]/span'
    
    driver = None
    dPath = '/Users/1nemani/Desktop/chromedriver'

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=dPath, options=options)

    try:
        driver.get(URL)
    except:
        time.sleep(1)
        driver.get(URL)

    t1Score_old = '00'
    t2Score_old = '00'
    t1Spread_old = '+0.0'
    t2Spread_old = '+0.0'
    t1mLine_old = '+000'
    t2mLine_old = '+000'

    while True:
         
        try:

            league = get_league(URL)

            #get spread
            try: 
                t1Spread = driver.find_element('xpath', t1Spread_span).text
                t2Spread = driver.find_element('xpath', t2Spread_span).text
            except NoSuchElementException:
                t1Spread = t1Spread_old
                t2Spread = t2Spread_old

            #get mLine
            try:    
                t1mLine = driver.find_element('xpath', t1mLine_span).text
                t2mLine = driver.find_element('xpath', t2mLine_span).text
            except NoSuchElementException:
                t1mLine = t1mLine_old
                t2mLine = t2mLine_old
            
            #trigger: new mLine
            if t1mLine_old != t1mLine or t2mLine_old != t2mLine:

                teams = get_teams_mLine(URL, t1mLine, t2mLine, t1Spread, t2Spread)

                v2FirestoreManager.out(league, teams[0], teams[1], teams[2], teams[3], teams[4], teams[5])

                t1mLine_old = t1mLine
                t2mLine_old = t2mLine
                
                now = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
                print(f'{now}: Money Line Update {t1mLine} {t2mLine}')

            #get score
            try:
                t1Score = driver.find_element('xpath', '(//div[starts-with(@aria-label, "current score")])[1]/span').text
                t2Score = driver.find_element('xpath', '(//div[starts-with(@aria-label, "current score")])[2]/span').text
            except NoSuchElementException:
                t1Score = t1Score_old
                t2Score = t2Score_old

            #trigger: new score
            if t1Score_old != t1Score or t2Score_old != t2Score:

                teams = get_teams_score(URL, t1Score, t2Score, t1mLine, t2mLine, t1Spread, t2Spread)

                #def in_(league, uTeam, fTeam, uScore, fScore, umLine, fmLine):
                v2FirestoreManager.in_(league, teams[0], teams[1], teams[2], teams[3], teams[4], teams[5], teams[6], teams[7])

                t1Score_old = t1Score
                t2Score_old = t2Score

                now = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
                print(f'{now}: Score Update {t1Score} {t2Score}')

            #trigger: new spread
            if t1Spread_old != t1Spread or t2Spread_old != t2Spread:

                teams = get_teams(URL, t1Spread, t2Spread)

                v2FirestoreManager.open(league, teams[0], teams[1], teams[2])

                t1Spread_old = t1Spread
                t2Spread_old = t2Spread

                now = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
                print(f'{now}: Spread Update {t1Spread} {t2Spread}')

        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass

def get_league(URL):
    return(URL.split("/", 10)[4])

def get_teams(URL, t1Spread, t2Spread):
    
    tUnformated = URL.split("/", 10)[-1]
    team1 = tUnformated.split("@", 3)[0]
    team2 = tUnformated.split("@", 3)[1]
    t1Unformated = team1.split("-", 30)
    t2Unformated = team2.split("-", 30)
    del(t2Unformated[-1])
    
    team2 = ""
    for i in t2Unformated:
        team2 += i + " "

    team1 = ""
    for j in t1Unformated:
        team1 += j + " "

    if '+' in t1Spread:
        uTeam = team1
        fTeam = team2
        fSpread = float(t2Spread[1:])
    else:
        uTeam = team2
        fTeam = team1
        fSpread = float(t1Spread[1:])

    teams = []

    teams.append(uTeam.strip(' '))
    teams.append(fTeam.strip(' '))
    teams.append(fSpread)

    return(teams)

def get_teams_spread(URL, t1Spread, t2Spread):
    
    tUnformated = URL.split("/", 10)[-1]
    team1 = tUnformated.split("@", 3)[0]
    team2 = tUnformated.split("@", 3)[1]
    t1Unformated = team1.split("-", 30)
    t2Unformated = team2.split("-", 30)
    del(t2Unformated[-1])
    
    team2 = ""
    for i in t2Unformated:
        team2 += i + " "

    team1 = ""
    for j in t1Unformated:
        team1 += j + " "

    if '+' in t1Spread:
        uTeam = team1
        fTeam = team2
        fSpread = float(t2Spread[1:])
    else:
        uTeam = team2
        fTeam = team1
        fSpread = float(t1Spread[1:])

    teams = []

    teams.append(uTeam.strip(' '))
    teams.append(fTeam.strip(' '))
    teams.append(fSpread)

    return(teams)

def get_teams_score(URL, t1Score, t2Score, t1mLine, t2mLine, t1Spread, t2Spread):
    
    teams_x = get_teams(URL, t1Spread, t2Spread)
    uTeam = teams_x[0]
    fTeam = teams_x[1]

    tUnformated = URL.split("/", 10)[-1]
    team1 = tUnformated.split("@", 3)[0]
    team2 = tUnformated.split("@", 3)[1]
    t1Unformated = team1.split("-", 30)
    t2Unformated = team2.split("-", 30)
    del(t2Unformated[-1])
    
    team2 = ""
    for i in t2Unformated:
        team2 += i + " "

    team1 = ""
    for j in t1Unformated:
        team1 += j + " "

    if(team1.strip(' ') == uTeam):
        uScore = t1Score
        fScore = t2Score
        umLine_odds = float(t1mLine[1:])
        fmLine_odds = float(t2mLine[1:])
        umLine_sign = (t1mLine[0])
        fmLine_sign = (t2mLine[0])

    else:
        uScore = t2Score
        fScore = t1Score
        umLine_odds = float(t2mLine[1:])
        fmLine_odds = float(t1mLine[1:])
        umLine_sign = (t2mLine[0])
        fmLine_sign = (t1mLine[0])
    
    teams = []
    
    teams.append(uTeam.strip(' ')) #[0]
    teams.append(fTeam.strip(' ')) #[1]
    teams.append(uScore) #[2]
    teams.append(fScore) #[3]
    teams.append(umLine_odds) #[4]
    teams.append(fmLine_odds) #[5]
    teams.append(umLine_sign) #[6]
    teams.append(fmLine_sign) #[7]

    #fmLine = float(t2mLine[1:])

    now = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    print(f'{now}: uTeam: {teams[0]} uScore: {teams[2]} umLine: {teams[6]}{teams[4]} fTeam: {teams[1]} fScore: {teams[3]} fmLine: {teams[7]}{teams[4]}')

    return(teams)

def get_teams_mLine(URL, t1mLine, t2mLine, t1Spread, t2Spread):
    
    teams_x = get_teams(URL, t1Spread, t2Spread)
    uTeam = teams_x[0]
    fTeam = teams_x[1]

    tUnformated = URL.split("/", 10)[-1]
    team1 = tUnformated.split("@", 3)[0]
    team2 = tUnformated.split("@", 3)[1]
    t1Unformated = team1.split("-", 30)
    t2Unformated = team2.split("-", 30)
    del(t2Unformated[-1])
    
    team2 = ""
    for i in t2Unformated:
        team2 += i + " "

    team1 = ""
    for j in t1Unformated:
        team1 += j + " "

    if(team1.strip(' ') == uTeam):
        uTeam = team1
        fTeam = team2
        fmLine_odds = float(t2mLine[1:])
        umLine_odds = float(t1mLine[1:])
        umLine_sign = (t1mLine[0])
        fmLine_sign = (t2mLine[0])
    else:
        uTeam = team2
        fTeam = team1
        fmLine_odds = float(t1mLine[1:])
        umLine_odds = float(t2mLine[1:])
        umLine_sign = (t2mLine[0])
        fmLine_sign = (t1mLine[0])

    teams = []

    teams.append(uTeam.strip(' '))
    teams.append(fTeam.strip(' '))
    teams.append(umLine_odds)
    teams.append(fmLine_odds)
    teams.append(umLine_sign)
    teams.append(fmLine_sign)

    now = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    print(f'{now}: uTeam: {teams[0]} umLine: {teams[4]}{teams[2]} fTeam: {teams[1]} fmLine: {teams[5]}{teams[3]}')

    return(teams)

