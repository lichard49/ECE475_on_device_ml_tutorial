# number of labels to record for
LABELS = [
  'wave',
  'punch'
]

# directory to record to
DATA_DIR = './data/'


if __name__ == '__main__':
  import numpy as np
  import pyqtgraph as pg
  from pyqtgraph.Qt import QtWidgets
  import serial
  import time


  # find port name using `ls /dev/tty*`
  SERIAL_PORT_NAME = '/dev/tty.usbserial-01C738BF'
  # match baud rate in firmware
  SERIAL_PORT_BAUD_RATE = 115200
  # number of axes to plot
  NUM_CHANNELS = 3
  # number of samples to plot per axes
  PLOT_WIDTH = 300

  # set up serial port and data structure
  serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUD_RATE)
  data = np.zeros((NUM_CHANNELS, PLOT_WIDTH))

  # set up plotting window
  window = pg.GraphicsLayoutWidget(show=True)
  window.setWindowTitle('Plot and Record')
  plots = [
    window.addPlot(row=(i + 1), col=1).plot(data[i])
    for i in range(NUM_CHANNELS)
  ]

  # set up callback for handling record button clicks
  is_recording = False
  current_recording_file = None

  def onButtonClicked(label):
    global is_recording, current_recording_file

    # toggle recording state
    is_recording = not is_recording

    if is_recording:
      # update background to reflect recording state
      window.setBackground('red')

      # set up file writing
      # include timestamp so data does not accidentally get overwritten
      recording_file_name =  label + '_' + str(time.time()) + '.txt'
      recording_file_path = DATA_DIR + recording_file_name
      current_recording_file = open(recording_file_path, 'w')
    else:
      window.setBackground('black')
      current_recording_file.close()

  # set up buttons that start recording when clicked
  button_row = window.addLayout(row=4, col=1)

  for i in range(len(LABELS)):
    label = LABELS[i]
    button = QtWidgets.QPushButton(label)
    button_callback = lambda _, label=label: onButtonClicked(label)
    button.clicked.connect(button_callback)

    proxy = QtWidgets.QGraphicsProxyWidget()
    proxy.setWidget(button)
    button_row.addItem(proxy)

  # update all plots
  def update():
    global data

    # read as a byte array
    data_line = serial_port.readline()
    # convert to a string
    data_line = data_line.decode('utf-8')
    # remove trailing whitespace
    parsed_data_line = data_line.strip()
    # print(parsed_data_line)
    # parse assuming a tab character delimiter
    parsed_data_line = parsed_data_line.split('\t')

    # if the line read from serial port is the correct format
    if len(parsed_data_line) == NUM_CHANNELS:
      if is_recording and current_recording_file is not None:
        # write to file when recording
        current_recording_file.write(data_line)

      for i in range(NUM_CHANNELS):
        # slide window by popping first sample...
        data[i, :-1] = data[i, 1:]
        # ...and appending new sample
        data[i, -1] = float(parsed_data_line[i])

        # update plot with new sample included
        plots[i].setData(data[i])

  # run update process every 1 ms
  timer = pg.QtCore.QTimer()
  timer.timeout.connect(update)
  timer.start(1)

  # start window
  pg.exec()
