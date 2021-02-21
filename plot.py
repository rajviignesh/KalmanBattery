import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df1 = pd.read_excel(r'Book1.xlsx',sheet_name=0)
SOCData = df1['SoC'].tolist()
OCVColumnname = "Ocv - T4"
OCVData = df1[OCVColumnname].tolist()
plt.plot(SOCData, OCVData)
plt.show()