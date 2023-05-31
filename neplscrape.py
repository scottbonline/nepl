import bs4 as bs
import urllib.request
import pprint
source = urllib.request.urlopen('https://nepl.org/score-sheets#sheet_3860').read()
soup = bs.BeautifulSoup(source,'html.parser')
my_dict = {}
scoresheet = soup.find_all('div' , class_='scoresheet stripe')
for event in scoresheet:
    if event.find('h3').text:
        location = event.find('h3').text
        my_dict[location] = {}
    matches = event.find_all('table', class_='match')
    match_num = 0
    for match in matches:
        match_num += 1
        match_num_str = "round_" + str(match_num)
        my_dict[location][match_num_str] = {}
        game_details = []
        table_rows = match.find_all('tr')
        for tr in table_rows:
            th = tr.find('th')
            td = tr.find_all('td')
            if tr.find('th', {'colspan': "3"}):
                game_name = (th.text)
                my_dict[location][match_num_str][game_name] = {}
            if tr.find('th', class_='player_name'):
                player_name = tr.find('th', class_='player_name').text
                my_dict[location][match_num_str][game_name][player_name] = {}
            if tr.find('td', class_='machine_score'):
                machine_score = tr.find('td', class_='machine_score').text
                my_dict[location][match_num_str][game_name][player_name]["machine_score"] = machine_score
            if tr.find('td', class_='machine_points'):
                machine_points = tr.find('td', class_='machine_points').text
                my_dict[location][match_num_str][game_name][player_name]["machine_points"] = machine_points
#pprint.pp(my_dict)
print(my_dict["GameCraft Arcade - Week 1 - Group 2"]["round_2"]["Foo Fighters"]["Ryan Belisle"])
print(my_dict["GameCraft Arcade - Week 1 - Group 2"]["round_2"]["Foo Fighters"]["Ryan Belisle"]["machine_score"])
print(my_dict["GameCraft Arcade - Week 1 - Group 2"]["round_2"]["Foo Fighters"]["Ryan Belisle"]["machine_points"])
