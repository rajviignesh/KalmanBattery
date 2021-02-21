import pandas as pd
import numpy as np
import xlrd
import math

Temp = "T1"

df1 = pd.read_excel('filename.xlsx', sheetname=0)
currentData = df1['current'].tolist()
voltageData = df1['term'].tolist()

df = pd.read_excel('Book1.xlsx', sheetname=0)
SOCData = df['SoC'].tolist()
OCVColumnname = "Ocv - " + Temp
OCVData = df[OCVColumnname].tolist()
R0Columnname = "R0-" + Temp
R0Data = df[R0Columnname].tolist()
R1Columnname = "r1-" + Temp
R1Data = df[R1Columnname].tolist()
C1Columnname = "c1-" + Temp
C1Data = df[C1Columnname].tolist()
R2Columnname = "r2-" + Temp
R2Data = df[R2Columnname].tolist()
C2Columnname = "c2-" + Temp
C2Data = df[C2Columnname].tolist()

X = np.array([0.01,0,0],[0,0.001,0],[0,0,0.001])
x = np.array(SOCData[0],[0],[0])
m = np.array([10])


def R0Select(SoC):
    for it in range(1,len(SOCData)):
        if(SoC < SOCData[it]):
            return R0Data[it-1]
        if(SoC == SOCData[it]):
            return R0Data[it]

def R1Select(SoC):
    for it in range(1,len(SOCData)):
        if(SoC < SOCData[it]):
            return R1Data[it-1]
        if(SoC == SOCData[it]):
            return R1Data[it]

def C1Select(SoC):
    for it in range(1,len(SOCData)):
        if(SoC < SOCData[it]):
            return C1Data[it-1]
        if(SoC == SOCData[it]):
            return C1Data[it]

def R2Select(SoC):
    for it in range(1,len(SOCData)):
        if(SoC < SOCData[it]):
            return R2Data[it-1]
        if(SoC == SOCData[it]):
            return R2Data[it]

def C2Select(SoC):
    for it in range(1,len(SOCData)):
        if(SoC < SOCData[it]):
            return C2Data[it-1]
        if(SoC == SOCData[it]):
            return C2Data[it]

def dOCVSelect(SoC):
    if(SoC <= 0.1):
        return 3.200328/0.1
    elif(SoC <= 0.6):
        return 0.141717/0.05
    elif(SoC <= 0.99):
        return 0.798499/0.84
    else:
        return 0.074456/0.01

for i in range(len(currentData)):

    #Initialising Data
    R0 = R0Select(x[0][0])
    R1 = R1Select(x[0][0])
    C1 = C1Select(x[0][0])
    R2 = R2Select(x[0][0])
    C2 = C2Select(x[0][0])

    #Step 1 - State Matrix
    t1 = math.exp(-1 / R1 * C1)
    t2 = math.exp(-1 / R2 * C2)

    A = np.array([1,0,0],[0,t1,0],[0,0,t2])
    B = np.array([1 / Q],[1 - t1],[1 - t2]) #What is Q

    x_t = A.dot(x) + B.dot(currentData[i])

    #Step 2 - Error Matrix
    X_t = A @ X @ A.transpose() + B @ m @ B.transpose()

    #Step 3 - Output Matrix
    dOCV = dOCVSelect(x[0][0])

    C = np.array([dOCV, 0 , 0],[0, -R1, 0],[0, 0, -R2])
    D = 1

    V_t = C.dot(x) + currentData[i] * R0 + n #What is n

    #Step 4 - Output Error Matrix
    Y = C @ X_t @ C.transpose() + D @ n @ D.transpose()

    #Step 5 - Kalman Gain
    L =  X_t @ C.transpose() @ np.linalg.inv(Y)

    #Step 6 - State Update
    r = voltageData[i] - V_t
    x_cap = x_t + L * r  #x or x_t

    #Step 7 - Error Matrix Update
    X_cap = X_t - L @ Y @ L.transpose()

    #Step 8 - Update Variables
    x = x_cap
    X = X_cap

    

