import requests, json # for VexDB API

def profile(team, season):

    # Base info
    print("\nLoading: Retrieving core info")
    raw = requests.get(f'https://api.vexdb.io/v1/get_teams?team={team}') # API GET request
    data = raw.json() # Parse JSON
    result = data["result"]
    teamdata = result[0] # Focus on main info

    # Number of other teams in organisation
    print("Loading: Retrieving organisation info")
    raw = requests.get(f'https://api.vexdb.io/v1/get_teams?organisation={teamdata["organisation"]}&nodata=true') # Only provides number of teams in organisation
    data = raw.json()
    orgteamcount = int(data["size"])

    # Events attended
    print("Loading: Retrieving event info")
    raw = requests.get(f'https://api.vexdb.io/v1/get_events?team={team}&season={season}&nodata=true') # Provides events attended
    data = raw.json()
    eventcount = int(data["size"])

    # Matches played
    print("Loading: Retrieving match info")
    raw = requests.get(f'https://api.vexdb.io/v1/get_matches?team={team}&season={season}&nodata=true') # Provides matches played
    data = raw.json()
    matchcount = int(data["size"])

    # Event rankings (including wins)
    print("Loading: Retrieving ranking info")
    raw = requests.get(f'https://api.vexdb.io/v1/get_rankings?team={team}&season={season}') # Provides rankings from events
    data = raw.json()
    rankings = data["result"] # Focus on main info
    lasteventdata = rankings[0]
    lasteventccwm = lasteventdata["ccwm"]
    lasteventopr = lasteventdata["opr"]
    lasteventdpr = lasteventdata["dpr"]
    lasteventmax = lasteventdata["max_score"]
    lasteventwins = lasteventdata["wins"]
    ccwm = [] # Declare lists
    wins = []
    maxscores = []
    try:
        for i in range(50):
            event = rankings[i]
            ccwm.append(event["ccwm"])
            wins.append(event["wins"])
            maxscores.append(event["max_score"])
    except IndexError:
        pass
    seasonmaxscore = max(maxscores)
    totalwins = sum(wins)
    avgccwm = sum(ccwm) / len(ccwm)

    print(f'\nTeam {teamdata["number"]} - "{teamdata["team_name"]}"\n\nGrade: {teamdata["grade"]}\nOrganisation: {teamdata["organisation"]} ({orgteamcount} teams under this organisation)\nLocation: {teamdata["city"]}, {teamdata["region"]}, {teamdata["country"]}\n\nEvents Attended: {eventcount}\nMatches Played: {matchcount}\nTotal Wins: {totalwins}\n\nSeason Max Score: {seasonmaxscore}\nSeason Average CCWM: {avgccwm} (Calc. Contribution to Winning Margin)\n\nLast Event CCWM: {lasteventccwm} (Calc. Contribution to Winning Margin)\nLast Event OPR: {lasteventopr} (Offensive Power Rating)\nLast Event DPR: {lasteventdpr} (Defensive Power Rating)\nLast Event Max Score: {lasteventmax}\nLast Event Wins: {lasteventwins}')

def menu():
    menuselect = input("VRC Insights v0.0.1\n\n1. Profile\n2. Log\n3. Predict\n\nSelection: ")

    if int(menuselect) == 1:
        team = str(input("\nInput Team Number: "))
        season = input("Input Season Name: ")
        profile(team, season)

menu()
