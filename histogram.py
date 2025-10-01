
import matplotlib.pyplot as plt

def showHistogram(data, title='-', bins=30, show = True):    
    fig = plt.figure(tight_layout=False)
    fig.canvas.manager.set_window_title(title)
    plt.hist(data, bins, edgecolor='black')
    if show: plt.show()
    