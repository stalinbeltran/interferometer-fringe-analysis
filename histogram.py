
import matplotlib.pyplot as plt

def showHistogram(data, title='-', bins=30):    
    fig = plt.figure(tight_layout=False)
    fig.canvas.manager.set_window_title(title)
    plt.hist(data, bins, color='skyblue', edgecolor='black')
    plt.show()
    