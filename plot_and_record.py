import numpy as np
import pyqtgraph as pg
import serial


if __name__ == '__main__':
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

  # update all plots
  def update():
    global data

    # read as a byte array
    data_line = serial_port.readline()
    # convert to a string
    data_line = data_line.decode('utf-8')
    # remove trailing whitespace
    data_line = data_line.strip()
    print(data_line)
    # parse assuming a tab character delimiter
    data_line = data_line.split('\t')

    # if the line read from serial port is the correct format
    if len(data_line) == NUM_CHANNELS:
      for i in range(NUM_CHANNELS):
        # slide window by popping first sample...
        data[i, :-1] = data[i, 1:]
        # ...and appending new sample
        data[i, -1] = float(data_line[i])

        # update plot with new sample included
        plots[i].setData(data[i])

  # run update process every 1 ms
  timer = pg.QtCore.QTimer()
  timer.timeout.connect(update)
  timer.start(1)

  # start window
  pg.exec()
