import pandas as pd
import random
df_israel = pd.read_csv('df_israeli_players.csv')


def find_all_teammates(player):
    row = df_israel.loc[df_israel['name'] == player]
    team = list(row['2012'])[0]
    df = df_israel.loc[df_israel['2012'] == team]
    years = [i for i in range(2013,2023)]
    for year in years:
        row = df_israel.loc[df_israel['name'] == player]
        team = list(row[str(year)])[0]
        temp = df_israel.loc[df_israel[str(year)] == team]
        df = pd.merge(df, temp, on='name', how='outer')

    return df


def find_all_shared_teammates(player1, player2):
    merge1 = find_all_teammates(player1)
    merge2 = find_all_teammates(player2)
    return list(pd.merge(merge1, merge2, on='name')["name"].drop_duplicates())


def all_players():
    return list(df_israel["name"])


def get_random_pair(players_list):
    # Shuffle the players list to ensure random pairings
    k = 0

    random_players = random.sample(players_list, 2)

    # Iterate through pairs of players and check if they have less than 5 shared teammates
    while 4 > k or k > 12:

        shared = find_all_shared_teammates(random_players[0], random_players[1])
        k = len(shared)
        random_players = random.sample(players_list, 2)

    print(shared)
    return random_players


def main():

    player1 = 'Ofir Kriaf'
    player2 = 'Frantzdy Pierrot'
    players = all_players()

    # merged = get_random_pair(players)
    merged = find_all_shared_teammates(player1, player2)
    print(merged)


if __name__ == "__main__":
    main()

