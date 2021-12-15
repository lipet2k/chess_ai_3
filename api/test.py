import chess
import pandas as pd
import numpy as np

df = pd.read_excel("10_games.xlsx", "Sheet1")
row = df.iloc[1]
row = np.array(row.to_numpy())
row = row[1:]
print(row)


