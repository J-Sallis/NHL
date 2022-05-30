import pandas as pd
import numpy as np
import requests

url = 'https://moneypuck.com/moneypuck/playerData/careers/gameByGame/all_teams.csv'
r = requests.get(url, allow_redirects=True)
open('all_teams.csv','wb').write(r.content)
NHL = pd.read_csv('all_teams.csv')
NHL['team'] = NHL['team'].replace(['T.B','N.J','L.A','S.J'],['TBL','NJD','LAK','SJS'])
NHL['name'] = NHL['name'].replace(['T.B','N.J','L.A','S.J'],['TBL','NJD','LAK','SJS'])
NHL['opposingTeam'] = NHL['opposingTeam'].replace(['T.B','N.J','L.A','S.J'],['TBL','NJD','LAK','SJS'])
NHL['playerTeam'] = NHL['playerTeam'].replace(['T.B','N.J','L.A','S.J'],['TBL','NJD','LAK','SJS'])
NHL['team'] = NHL['team'].astype('string')
NHL = NHL.drop(NHL[NHL['situation']!= 'all'].index)
NHL['gameDate'] = pd.to_datetime(NHL['gameDate'].astype(str), format='%Y%m%d')
NHL_game = NHL.groupby(['team','gameId'])[['goalsFor','goalsAgainst']].sum()
NHL_game['tie'] = np.where(NHL_game['goalsFor'] == NHL_game['goalsAgainst'], True, False)
NHL_game['points'] = np.where(NHL_game['goalsFor'] > NHL_game['goalsAgainst'], 1, 0) + np.where(NHL_game['tie'] == True, 0.75,0)
NHL_game = NHL_game.loc[:,'points']
NHL = pd.merge(NHL,NHL_game,on=['team','gameId'])
col = list(NHL.columns)
x = ['goalsAgainst','hitsAgainst','hitsFor','goalsFor','season','team','points']
NHL_violin = NHL.loc[:,['hitsFor','goalsFor','playoffGame']]
DB = NHL.loc[:,x].groupby(by=['season','team']).agg({'goalsAgainst':'sum','points':'mean','hitsAgainst':'sum','hitsFor':'sum','goalsFor':'sum'}).reset_index()
DB['Goal_pct'] = DB.goalsFor/(DB.goalsAgainst + DB.goalsFor)
DB['Hits_pct'] = DB.hitsFor/(DB.hitsAgainst + DB.hitsFor)
DB['season'] = pd.to_datetime(DB['season'],format='%Y').dt.year
DB = DB.set_index('season')

playoffs = NHL.groupby(['team','season','playoffGame']).agg({'goalsAgainst':'sum','points':'sum','hitsAgainst':'sum','hitsFor':'sum','goalsFor':'sum','gameId':'count'}).reset_index()
playoffs['Goals per game'] = (playoffs['goalsAgainst'] + playoffs['goalsFor'])/playoffs['gameId']
playoffs['Hits per game'] = (playoffs['hitsAgainst'] + playoffs['hitsFor'])/playoffs['gameId']

cup=[]
for name, group in playoffs.loc[playoffs['playoffGame']==1].groupby(['season']):
    cup.append(str(group[['team','points']].loc[group['points'].idxmax(),'team']))
cup
playoffs = playoffs.groupby(['season','playoffGame']).agg({'Goals per game':'mean','Hits per game':'mean'}).reset_index()
playoffs.season += 1
playoffs = playoffs.rename({'season':'Year'})
cup_df = pd.DataFrame({'Cup_winner':cup})
cup_df = pd.DataFrame(np.repeat(cup_df.values, 2, axis=0))
cup_df = playoffs.join(cup_df)
cup_df['Goals/game vs Reg Season'] = cup_df['Goals per game'].pct_change()
cup_df['Hits/game vs Reg Season'] = cup_df['Hits per game'].pct_change()
cup_df =  cup_df.loc[cup_df['playoffGame'] == 1]
cup_df = cup_df.rename(columns={0:'Cup winner','season':'Season'})
cup_df[['Goals per game','Hits per game']] = cup_df[['Goals per game','Hits per game']].round(2)
cup_df= cup_df[['Season','Cup winner','Goals per game','Goals/game vs Reg Season','Hits per game','Hits/game vs Reg Season']]
HM_NHL = NHL.groupby(['team','season','gameId']).agg({'points':'mean','takeawaysAgainst':'sum',
                                                      'giveawaysAgainst':'sum','takeawaysFor':'sum','giveawaysFor':'sum','hitsAgainst':'sum','hitsFor':'sum',
                                                      'faceOffsWonFor':'sum','faceOffsWonAgainst':'sum',
                                                      'reboundsFor':'sum','reboundsAgainst':'sum','shotsOnGoalFor':'sum','shotsOnGoalAgainst':'sum',
                                                     'shotsOnGoalAgainst':'sum','shotsOnGoalFor':'sum','penalityMinutesFor':'sum','penalityMinutesAgainst':'sum','dZoneGiveawaysAgainst':'sum',
                                                      'dZoneGiveawaysFor':'sum','highDangerShotsAgainst':'sum','highDangerShotsFor':'sum','shotAttemptsAgainst':'sum','shotAttemptsFor':'sum' 
                                                     })
HM_NHL['Takeaways_diff'] = HM_NHL['takeawaysFor'] - HM_NHL['takeawaysAgainst']
HM_NHL['Giveaways_diff'] = HM_NHL['giveawaysFor'] - HM_NHL['giveawaysAgainst']
HM_NHL['Hits_diff'] = HM_NHL['hitsFor'] - HM_NHL['hitsAgainst']
HM_NHL['Faceoff_diff'] = HM_NHL['faceOffsWonFor'] - HM_NHL['faceOffsWonAgainst']
HM_NHL['Rebound_diff'] = HM_NHL['reboundsFor'] - HM_NHL['reboundsAgainst']
HM_NHL['Shots_diff'] = HM_NHL['shotsOnGoalFor'] - HM_NHL['shotsOnGoalAgainst']
HM_NHL['Pentalty_diff'] = HM_NHL['penalityMinutesFor'] - HM_NHL['penalityMinutesAgainst']
HM_NHL['Dzone_giveaways_diff'] = HM_NHL['dZoneGiveawaysFor'] - HM_NHL['dZoneGiveawaysAgainst']
HM_NHL['highDangerShots_diff'] = HM_NHL['highDangerShotsFor'] - HM_NHL['highDangerShotsAgainst']
HM_NHL['ShotAttempt_diff'] = HM_NHL['shotAttemptsFor'] - HM_NHL['shotAttemptsAgainst']
HM_NHL = HM_NHL.drop(['takeawaysFor','takeawaysAgainst','giveawaysFor','giveawaysAgainst','hitsFor','hitsAgainst','faceOffsWonFor','faceOffsWonAgainst',
                      'reboundsAgainst','reboundsFor','shotsOnGoalFor','shotsOnGoalAgainst','penalityMinutesAgainst','penalityMinutesFor',
                      'dZoneGiveawaysAgainst','dZoneGiveawaysFor','highDangerShotsAgainst','highDangerShotsFor',
                      'shotAttemptsAgainst','shotAttemptsFor'
                     ],axis='columns')
HM_NHL = HM_NHL.reset_index()
NHL_violin['goalsFor'] = NHL_violin['goalsFor'].astype(int)
lst=[]
lst += ['season','team','points']
for i in NHL.columns:
    if 'rebound' in i:
        lst.append(i)

NHL_rebound = NHL[lst]
y = x + ['reboundsFor','reboundsAgainst','playoffGame','gameDate','gameId']
NHL_season = NHL[y]
NHL_season = NHL_season.set_index('gameDate')
DB.to_pickle('NHL_edit.pkl')
HM_NHL.to_pickle('heat_map.pkl')
playoffs.to_pickle('playoffs.pkl')
cup_df.to_pickle('playoffs_table.pkl')
NHL_violin.to_pickle('NHL_violin.pkl')
NHL_rebound.to_pickle('NHL_rebound.pkl')