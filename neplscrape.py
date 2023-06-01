import bs4 as bs
import urllib.request
import pprint
import sqlite3
from sqlite3 import Error


def get_nepl_data():
    source = urllib.request.urlopen('https://nepl.org/score-sheets#sheet_3860').read()
    soup = bs.BeautifulSoup(source,'html.parser')
    nepl_data = {}
    scoresheet = soup.find_all('div' , class_='scoresheet stripe')
    for event in scoresheet:
        if event.find('h3').text:
            location = event.find('h3').text
            nepl_data[location] = {}
        matches = event.find_all('table', class_='match')
        match_num = 0
        for match in matches:
            match_num += 1
            match_num_str = "round_" + str(match_num)
            nepl_data[location][match_num_str] = {}
            game_details = []
            table_rows = match.find_all('tr')
            for tr in table_rows:
                th = tr.find('th')
                td = tr.find_all('td')
                if tr.find('th', {'colspan': "3"}):
                    game_name = (th.text)
                    nepl_data[location][match_num_str][game_name] = {}
                if tr.find('th', class_='player_name'):
                    player_name = tr.find('th', class_='player_name').text
                    nepl_data[location][match_num_str][game_name][player_name] = {}
                if tr.find('td', class_='machine_score'):
                    machine_score = tr.find('td', class_='machine_score').text
                    nepl_data[location][match_num_str][game_name][player_name]["machine_score"] = machine_score
                if tr.find('td', class_='machine_points'):
                    machine_points = tr.find('td', class_='machine_points').text
                    nepl_data[location][match_num_str][game_name][player_name]["machine_points"] = machine_points

    return nepl_data

def dbconnect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_data(conn, row_data):
    sql = ''' INSERT INTO nepl(Location,Round,Game,Player,MachineScore,MachinePoints)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, row_data)
    conn.commit()
    return cur.lastrowid

if __name__=="__main__":
    
    # get nepl data
    nepl_data = get_nepl_data()
    
    # connect to db
    db_file = ("./nepl.db")
    sql_nepl_table = """ CREATE TABLE IF NOT EXISTS nepl (
                                        id integer PRIMARY KEY,
                                        Location text NOT NULL,
                                        Round integer,
                                        Game text,
                                        Player text,
                                        MachineScore integer,
                                        MachinePoints integer
                                    ); """
    conn = dbconnect(db_file)
    
    create_table(conn, sql_nepl_table)
    row_data = ("place", 1, "batman", "scott", "34,000", 3)
    add_data(conn, row_data)

    #sample = ('Western Mass Pinball Club - Week 5 - Group 21', {'round_1': {'Contact': {'Alexander Blaustein': {'machine_score': '193,860', 'machine_points': '7'}, 'Rick Rock': {'machine_score': '28,200', 'machine_points': '1'}, 'Connor Lafleur': {'machine_score': '104,240', 'machine_points': '4'}}}, 'round_2': {'Old Coney Island!': {'Alexander Blaustein': {'machine_score': '52,140', 'machine_points': '4'}, 'Rick Rock': {'machine_score': '131,080', 'machine_points': '7'}, 'Connor Lafleur': {'machine_score': '33,490', 'machine_points': '1'}}}, 'round_3': {'Grand Prix': {'Alexander Blaustein': {'machine_score': '382,850', 'machine_points': '7'}, 'Rick Rock': {'machine_score': '207,780', 'machine_points': '4'}, 'Connor Lafleur': {'machine_score': '129,950', 'machine_points': '1'}}}, 'round_4': {'Paragon': {'Alexander Blaustein': {'machine_score': '46,130', 'machine_points': '4'}, 'Rick Rock': {'machine_score': '52,280', 'machine_points': '7'}, 'Connor Lafleur': {'machine_score': '33,890', 'machine_points': '1'}}}})

    for location, v in nepl_data.items():
        print(location) # location
        for round, v_a in v.items():
            print(round) # round
            for player, v_b in v_a.items():
                print(player)
                for machine, v_c in v_b.items():
                    print(machine)
                    print(v_c["machine_score"])
                    print(v_c["machine_points"])
                    row_data = (location, round, player, machine, v_c["machine_score"], v_c["machine_points"] )
                    add_data(conn, row_data)

    
    #dbconnect
    
    # get nepl data
    
    #nepl_data = get_nepl_data()

    # how to query returned data
    #pprint.pp(nepl_data)
    #print(nepl_data["GameCraft Arcade - Week 1 - Group 2"]["round_2"]["Foo Fighters"]["Ryan Belisle"])
    #print(nepl_data["GameCraft Arcade - Week 1 - Group 2"]["round_2"]["Foo Fighters"]["Ryan Belisle"]["machine_score"])
    #print(nepl_data["GameCraft Arcade - Week 1 - Group 2"]["round_2"]["Foo Fighters"]["Ryan Belisle"]["machine_points"])