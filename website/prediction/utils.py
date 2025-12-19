import os
import pickle
import pandas as pd
from django.conf import settings

# Global variables to store the model and data
MODEL = None
PREDICTORS = None
FULL_DATA = None

def load_resources():
    """
    Loads the ML model and the dataset into memory.
    """
    global MODEL, PREDICTORS, FULL_DATA
    
    # helper to construct absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'ml_models', 'nba_model.pkl')
    data_path = os.path.join(base_dir, 'ml_models', 'NBA_games_compact.csv')

    if MODEL is None:
        try:
            with open(model_path, "rb") as f:
                # The notebook showed: rr, sfs, predictors = pickle.load(f)
                MODEL, _, PREDICTORS = pickle.load(f)
            print("NBA Model loaded successfully.")
        except FileNotFoundError:
            print(f"Error: Model file not found at {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")

    if FULL_DATA is None:
        try:
            # We use index_col=0 as seen in the notebook
            FULL_DATA = pd.read_csv(data_path, index_col=0)
            # Ensure sorting if necessary, notebook did 'df.sort_values("date")' but 'full' was just read
            # We'll assume the CSV is sufficiently prepared or we just need the latest rows
            print("NBA Data loaded successfully.")
        except FileNotFoundError:
            print(f"Error: Data file not found at {data_path}")
        except Exception as e:
            print(f"Error loading data: {e}")

def get_team_choices():
    """
    Returns a list of tuples (team_code, team_code) for the form choices.
    """
    if FULL_DATA is None:
        load_resources()
        
    if FULL_DATA is not None:
        # Assuming 'team_x' or 'team_y' contains the team codes
        # We need unique team codes. Use 'team_x' (home usually?) or 'team_y'
        teams = sorted(FULL_DATA["team_x"].unique())
        return [(t, t) for t in teams]
    return []

def predict_matchup(team_a, team_b):
    """
    Predicts the winner between team_a and team_b.
    Returns the predicted winner code.
    """
    if MODEL is None or FULL_DATA is None:
        load_resources()
        if MODEL is None or FULL_DATA is None:
            return "Model or Data not available"

    try:
        # Get latest rows for each team
        # We want the MOST RECENT stats for the team. 
        # Assuming the dataset is historical, we take .iloc[-1] after filtering
        t1 = FULL_DATA[FULL_DATA["team_x"] == team_a].iloc[-1]
        t2 = FULL_DATA[FULL_DATA["team_y"] == team_b].iloc[-1]
        
        # Determine predictors intersection if needed or just use what we loaded
        # The notebook passed 'predictors' to slice the dataframe
        
        # Compute difference: (t1 - t2)
        # Note: We must ensure we are selecting only the numeric columns that are in 'predictors'
        
        # Check if t1/t2 satisfy predictors
        # The notebook did: diff = (t1[predictors] - t2[predictors]).to_frame().T
        
        diff = (t1[PREDICTORS] - t2[PREDICTORS]).to_frame().T
        
        result = MODEL.predict(diff)[0]
        
        # notebook: winner = team_a if result == 1 else team_b
        winner = team_a if result == 1 else team_b
        return winner
    except Exception as e:
        print(f"Prediction error: {e}")
from datetime import datetime, timedelta
from nba_api.live.nba.endpoints import scoreboard

def get_todays_games():
    """
    Fetches today's games using the live endpoint.
    Returns a list of game dictionaries.
    """
    try:
        board = scoreboard.ScoreBoard()
        games = board.games.get_dict()
        return games
    except Exception as e:
        print(f"Error fetching today's games: {e}")
        return []

def get_week_schedule():
    """
    Fetches the schedule for the next 7 days.
    """
    # Note: For simplicity and speed in this demo, we might mock this or iterate 
    # using a valid endpoint. ScoreBoard is live only.
    # We will use the static schedule or iterate scoreboardv2 if needed.
    # Let's try to use a simple iteration for now if we can't find a bulk endpoint.
    
    # Actually, for a better user experience without too many API calls, 
    # let's just show tomorrow's games to start, or use a lightweight approach.
    
    # Using stats endpoint for future dates:
    from nba_api.stats.endpoints import scoreboardv2
    from nba_api.stats.static import teams

    nba_teams = teams.get_teams()
    team_map = {team['id']: team['abbreviation'] for team in nba_teams}
    
    upcoming_schedule = {}
    today = datetime.now()
    
    # Fetch next 5 days
    for i in range(1, 6): 
        date_obj = today + timedelta(days=i)
        date_str = date_obj.strftime("%Y-%m-%d") 
        
        try:
            board = scoreboardv2.ScoreboardV2(game_date=date_str)
            # transform to dict
            header = board.game_header.get_dict()
            headers = header['headers']
            data = header['data']
            
            games_list = []
            for row in data:
                game_dict = dict(zip(headers, row))
                # Add friendly names
                home_id = game_dict.get('HOME_TEAM_ID')
                visitor_id = game_dict.get('VISITOR_TEAM_ID')
                
                game_dict['home_team_name'] = team_map.get(home_id, 'UNK')
                game_dict['visitor_team_name'] = team_map.get(visitor_id, 'UNK')
                
                # Check for national TV
                # Key might be NATL_TV_BROADCASTER_ABBREVIATION
                
                games_list.append(game_dict)

            if games_list:
                upcoming_schedule[date_obj.strftime("%A, %b %d")] = games_list
        except Exception as e:
            print(f"Error fetching schedule for {date_str}: {e}")
            
    return upcoming_schedule
