import calendar
from collections import OrderedDict
import random
import pandas as pd


#start date and dic of people for assignments
start=[2015,'07', 01]
People={'A':'R1', 'B':'R2', 'C':'R3', 'D':'R4'}



#create calendar object set start of week to sunday
C=calendar.TextCalendar(calendar.SUNDAY)

#ordered dic of months
MonthDic={'01':'January', '02':'February', '03':' March', '04':'April',
         '05':'May', '06':'June', '07':'July', '08':'August',
         '09':'September', '10':'October', '11':'November',
         '12':'December'}
MonthDic=OrderedDict(sorted(MonthDic.items(), key=lambda t:t[0]))
#extract the keys to use in the list system
MonthDicKeys=MonthDic.keys()

#reorder the calendar list to start from the start month for a one year period
E=True
for i in range(0,len(MonthDicKeys)):
   if MonthDicKeys[0]!=start[1] and E:
       P=MonthDicKeys.pop(0)
       MonthDicKeys.append(P)
   elif MonthDicKeys[0]==start[1]:
       E=False
#print MonthDicKeys

#Storage list: year, month, weeks of month list
UseList=[]
#create a control variable
control=start
for i in MonthDicKeys:
   UseList.append([control[0], i,C.monthdayscalendar(control[0], int(i))])
   if i=='12': control[0]=control[0]+1

#get the number of weeks (includes double count at end of month) in uselist
r=0
for i in UseList:
   for j in i[-1]:
       r+=1
#print r

#create the dataframe that will hold the final dataset used by pweave
df=pd.DataFrame(index=range(0, r),columns=['week', 'month', 'year', 'days', 'Assenments'])

#add to the dataframe the information in UseList
r=0
for i in UseList:
   for j in i[-1]:
       #can't add a list and atoms in the same assignment statement
       df.loc[r, 'days']=j
       df.loc[r, ['week', 'month', 'year']]=r, i[1], i[0]
       r+=1
#print df
#print ''

#add assignments for each week
#create a random list of people's assessments for the week
Assign=[People[i] for i in random.sample(People.keys(), 4)]
for index, row in df.iterrows():
   #print row['days']
   #if the week is a continuation from the last month don't change the assignments
   if 0==row['days'][0]:
       row['Assenments']=Assign
   else:
       Assign=[People[i] for i in random.sample(People.keys(), 4)]
       row['Assenments']=Assign

#print df

#and here we write are LaTeX print stuff to make the tables
#pweave is defaulting to Python 3 on my beast, oh joy
for i in MonthDicKeys:
   #month title and table begin statement
   print(r'\begin{center}')
   print(r'\Huge '+MonthDic[i])
   print(r'\end{center}')
   print(r'\begin{tabular}{||c|c|c|c|c|c|c|c||}')

   #print the table internals
   for index, row in df.loc[df['month']==i].iterrows():
       d=row['days']; d=[str(i) for i in d]
       a=row['Assenments']

       print(r'\DataDayAssignment{'+d[0]+'}{'+d[1]+'}{'+d[2]+'}{'+d[3]+'}{'+d[4]+'}{'+d[5]+'}{'+d[6]+'}')
       print(r'\ChoresCalendarWeek{'+a[0]+'}{'+a[1]+'}{'+a[2]+'}{'+a[3]+'}')

   print(r'\end{tabular}')
   print(r'\newpage')
   print()
   print()




