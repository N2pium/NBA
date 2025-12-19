import pandas as pd
import os

base_dir = r"c:\Users\Schoo\OneDrive\Documents\NBA Website Project\website\prediction\ml_models"
input_path = os.path.join(base_dir, "NBA_games_merged.csv")
output_path = os.path.join(base_dir, "NBA_games_compact.csv")

print(f"Reading {input_path}...")
df = pd.read_csv(input_path, index_col=0)

indices_to_keep = set()

# For every team that appears in team_x, get the last row
if "team_x" in df.columns:
    teams_x = df["team_x"].unique()
    for team in teams_x:
        # Get index of the last occurrence
        last_idx = df[df["team_x"] == team].index[-1]
        indices_to_keep.add(last_idx)

# For every team that appears in team_y, get the last row
if "team_y" in df.columns:
    teams_y = df["team_y"].unique()
    for team in teams_y:
        last_idx = df[df["team_y"] == team].index[-1]
        indices_to_keep.add(last_idx)

compact_df = df.loc[list(indices_to_keep)].sort_index()

print(f"Original shape: {df.shape}")
print(f"Compact shape: {compact_df.shape}")

compact_df.to_csv(output_path)
print(f"Saved compact dataset to {output_path}")
