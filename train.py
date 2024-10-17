import matplotlib.pyplot as plt
import os
import csv
import numpy as np

from plot_and_record import *


if __name__ == '__main__':
  # count how many examples of each label are in the dataset
  label_count = {label : 0 for label in LABELS}
  for file in os.listdir(DATA_DIR):
    file_path = os.path.join(DATA_DIR, file)
    if os.path.isfile(file_path):
      for label in LABELS:
        if label in file:
          label_count[label] += 1

  # plot each example
  num_rows = len(LABELS)
  num_columns = max(label_count.values())
  fig, ax = plt.subplots(num_rows, num_columns, sharex=True, sharey=True)

  index = 0
  for file in sorted(os.listdir(DATA_DIR)):
    file_path = os.path.join(DATA_DIR, file)
    if os.path.isfile(file_path):
      data = np.loadtxt(file_path, delimiter='\t')

      i = index // num_columns
      j = index % num_columns
      ax[i, j].plot(data)
      ax[i, j].set_title(file_path)
      index += 1
  
  plt.tight_layout()
  plt.show()
