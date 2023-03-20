import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def bar(imgpath,values1,values2):
    labels = ['pH', 'P', 'K', 'S']
    x = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, values1, width, label='Actual')
    rects2 = ax.bar(x, values2, width, label='Needed')

    ax.set_xlabel('Parameters')
    ax.set_ylabel('Values')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.savefig(imgpath, dpi=300, bbox_inches='tight')
    plt.close()