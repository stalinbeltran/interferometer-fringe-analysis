
import matplotlib.pyplot as plt

def showHistogram(data, title='-', bins=30, show = True, label = None, histtype='bar'):    
    fig = plt.figure(tight_layout=False)
    fig.canvas.manager.set_window_title(title)
    plt.hist(data, bins, label=label, histtype=histtype)
    plt.legend(label)
    if show: plt.show()
    