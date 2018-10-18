#######
# Hello! Thanks for reading my application.
# I do not have microsoft office installed on my home machine so did not feel comfortable submitting an Excel workbook.
# Instead, here's a small python script to complete the task.
# The output is a pdf file that you can find here: 
# And a notebook going through the code is here:
# Note that because the output is a PDF and there are 170 countries/regions, this script may take up to 2 minutes.
# Please feel free to contact me at pmcbr@sas.upenn.edu.
#######


import pandas as pd
from pandas.tseries.offsets import MonthEnd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# data source
source = 'https://www.treasury.gov/resource-center/data-chart-center/tic/Documents/slt1d_globl.csv'

# read in raw data
tic = pd.read_csv(source, skiprows=13, skipfooter=10, 
                  names = ('Country Name', 'Country Code', 'End of Month', 
                            'Total US Long-Term Securities', 'US Treasury', 
                            'US Agency Bonds', 'US Corporate and Other Bonds', 
                            'US Corporate Stocks'), 
                  engine='python', thousands=',', na_values = 'n.a.')


# add native date formatting
tic['End of Month'] = pd.to_datetime(tic['End of Month']) + MonthEnd(1)
tic.set_index(['Country Name', 'End of Month'], inplace = True)


def table_plots(country, df):
    """
    country is a string used to title the plots
    df should contain appropriate data
    returns matplotlib.pyplot figure for printing
    """
    fig, ax = plt.subplots(3,2, figsize = (18, 12))
    fig.suptitle(country, fontsize=20)
    for i, x in enumerate(ax.ravel()):

        if i == 0:
            x.table(cellText=list(zip(list(df.iloc[0,1:].index), list(df.iloc[0,1:].values))), 
                    colLabels=['', str(df.index[0])[:-12]],
                    loc='center')
            x.xaxis.set_visible(False) 
            x.yaxis.set_visible(False)
            x.set_title('Most Recent Data (millions USD)')
            continue
        x.grid(True)
        x.plot(df.iloc[:,i].dropna())
        x.set_title(df.iloc[:,i].name)

    return fig

# list of country names
countries = list(tic.index.levels[0])

# print to pdf
with PdfPages('tic_update.pdf') as pdf:
    for c in countries:

        fig = table_plots(c, tic.loc[c])
        pdf.savefig(fig)

        plt.close()


