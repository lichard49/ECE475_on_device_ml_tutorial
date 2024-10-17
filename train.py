import matplotlib.pyplot as plt
import os
import csv
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
import emlearn

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
  labels = np.array(labels)

  # generate train/test split
  k_fold_split = StratifiedKFold(n_splits=2)
  train_index, test_index = k_fold_split.split(features, labels)
  # just look at the first fold
  train_index = train_index[0]
  test_index = test_index[0]
  train_features = features[train_index]
  train_labels = labels[train_index]
  test_features = features[test_index]
  test_labels = labels[test_index]

  # train model
  clf = RandomForestClassifier(random_state=0)
  clf.fit(train_features, train_labels)

  # evaluate model
  predict_labels = clf.predict(test_features)
  accuracy = accuracy_score(test_labels, predict_labels)
  ConfusionMatrixDisplay.from_predictions(test_labels, predict_labels)
  plt.title('Accuracy = ' + str(accuracy) + '%')
  plt.show()

  # train final model using all data
  final_clf = RandomForestClassifier(random_state=0)
  final_clf.fit(features, labels)

  # export final model
  ported_clf = emlearn.convert(final_clf, method='inline')
  ported_clf.save(file='./out/model.h', name='model')
