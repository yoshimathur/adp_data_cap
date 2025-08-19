import pandas as pd
import matplotlib.pyplot as plt

def average_utilization(col_name, usage):
    mean = usage[[col_name, 'UsageFrequency']].groupby(col_name).mean('UsageFrequency')
    plt.bar(mean.index, mean['UsageFrequency'])
    return mean