import numpy as np
import pandas as pd


# Load saved game data
npz_file = np.load('./NZ, Hawkes Bay, Te Awanga Sprint Forward - 238.9s.npz')
game_data = npz_file['samples']
run_time = game_data[0]
distance = game_data[2]
# Remove data when car is before starting line
# Reset run_time to zero when car start moving
idx = distance.nonzero()[0]
distance = distance[idx:]
run_time = run_time[idx:]
run_time = run_time - run_time[0]

# Load distance label
distance_label = pd.read_csv('label.txt',sep='\t')
distance_label = distance_label[[0,2]]
