import os
import numpy as np
#import scipy as sp
import matplotlib.pyplot as plt

A=[]  
time=[] #Running time, string
record=[]
Efield=[] #Electric field list
temp_time=[] #Temp time list, string
temp_record=[]
temp_Efield=[] #temp Electric field list
fList=[] #List of analysed Files

def fileList(): #Keeping only the needed files
    clist = os.listdir()
    x=0
    while x<len(clist): 
        if clist[x][0]!="T" and clist[x][3]!="6":
            clist.pop(x)
            x=0
        else:
            x=x+1
    return(clist)
   

def openFile(fl): #Creating List of Time and Ez
    for fnum in fl:
        A = open(fnum, "r") #entire file in A
        ln=0
        for x in A:
            if ln>3: #Dropping titles, remaining values
                #line = A.readline()
                text = x.split(",")
                time.append(text[0])
                record.append(int(text[1]))
                Efield.append(float(text[2]))
            else:
                ln=ln+1  
        
    print('Full list:')
    #print(Efield)
    print(len(Efield))

 
def graph(t,e): #Plotting Ez(time)
    #Remove the date from the time string
    timeT=[]
    timeT = t
    time = [s[11:] for s in timeT]
    #####################################
    plt.plot(time, np.abs(Efield), 'r--')
    plt.xlabel('time')
    plt.ylabel('Potential Gradiant [V/m]')
    x = [0, len(time)/8, len(time)/4, len(time)*3/8, len(time)/2, len(time)*5/8, len(time)*0.75, len(time)*7/8, len(time)]
    y = [time[0],time[int(len(time)/8-1)],time[int(len(time)/4-1)],time[int(len(time)*3/8-1)],time[int(len(time)/2-1)],time[int(len(time)*5/8-1)],time[int(len(time)*0.75-1)],time[int(len(time)*7/8-1)],time[int(len(time)-1)]]
    plt.xticks(x, y , rotation=90)
    #plt.arrow(59, 225, 0, 200, head_width=0.5, head_length=0.5, color='black')
    plt.show() 
    
def Average(Elst): # average of a list
    return sum(np.abs(Elst)) / len(Elst)  
          
def main():
    fList = fileList()
    openFile(fList)
    graph(time,Efield)
    print("Average PG value =", round(Average(Efield), 2))
    print("Max PG value =", round(max(np.abs(Efield)), 1))
main()
