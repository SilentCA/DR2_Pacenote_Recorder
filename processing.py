import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline
import pathlib
import csv


# Load saved game data
npz_filename = input("Please input game log filename:")
npz_filename = pathlib.Path(npz_filename)
npz_file = np.load(npz_filename)
game_data = npz_file['samples']
run_time = game_data[0]
distance = game_data[2]
# Remove data when car is before starting line
# Reset run_time to zero when car start moving
idx = distance.nonzero()[0][0]
distance = distance[idx:]
run_time = run_time[idx:]
run_time = run_time - run_time[0]

spl = UnivariateSpline(run_time, distance)

# Load distance label
label_filename = npz_filename.with_stem(npz_filename.stem + '_alias').with_suffix('.csv')
distance_label = pd.read_csv(label_filename, sep='\t', names=['start','end','pacenote'])
# Align audio with run_time, audio start point is set after speech "five four three one go"
start_time = 6
distance_label['start'] = distance_label['start'] - start_time
pacenotes = distance_label
pacenotes['start'] = distance_label['start'].apply(spl)
pacenotes_filename = npz_filename.with_suffix('.pacenotes')
# pacenotes.to_csv(pacenotes_filename, sep=',', columns=['start','pacenote'], header=False, index=False, quoting=csv.QUOTE_NONE)
with open(pacenotes_filename,'w') as f:
    for i, line in pacenotes.iterrows():
        f.writelines(['{0},{1}\n'.format(line['start'],line['pacenote'])])
