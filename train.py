import matplotlib.pyplot as plt
import os
import csv
import numpy as np

from plot_and_record import *


if __name__ == '__main__':
  # load data and corresponding labels
  label_count = {label : 0 for label in LABELS}
  raw_data = []
  labels = []
  file_paths = []
  for file in sorted(os.listdir(DATA_DIR)):
    file_path = os.path.join(DATA_DIR, file)
    if os.path.isfile(file_path):
      # determine what this file is labeled as
      for l in LABELS:
        if l in file:
          label = l
          label_count[label] += 1
          break

      # load data from file
      data = np.loadtxt(file_path, delimiter='\t')

      # keep storage arrays parallel
      raw_data.append(data)
      labels.append(label)
      file_paths.append(file_path)

  # plot each example
  num_rows = len(LABELS)
  num_columns = max(label_count.values())
  fig, ax = plt.subplots(num_rows, num_columns, sharex=True, sharey=True)

  for i, target_label in enumerate(LABELS):
    j = 0
    for data, label, path in zip(raw_data, labels, file_paths):
      if label == target_label:
        ax[i, j].plot(data)
        ax[i, j].set_title(path)
        j += 1
  
  plt.tight_layout()
  plt.show()

  # extract features (4 statistics)
  features = []
  for data in raw_data:
    feature_vector = []
    num_channels = data.shape[1]
    for channel in range(num_channels):
      signal = data[:, channel]
      feature_vector += [
        np.min(signal),
        np.max(signal),
        np.mean(signal),
        np.std(signal)
      ]

    features.append(feature_vector)

  features = np.array(features)
