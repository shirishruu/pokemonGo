from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from bs4 import BeautifulSoup
import urllib
import re
import datetime
import json
import matplotlib.pyplot as plt
from matplotlib import dates
import numpy as np

with open("pokemon_android.json","w") as fp:
    json.dump({},fp)
str_date="2016-07-21"
date_1 = datetime.datetime.strptime(str_date, "%Y-%m-%d")
end_date=datetime.datetime.strptime("2016-10-31", "%Y-%m-%d")


size=[]
alrat=[]
five=[]
four=[]
three=[]
two=[]
one=[]
avrat=[]

while date_1!=end_date:
    names=[]
    co = PlaintextCorpusReader("./data/"+str(date_1.year)+"-%02d-%02d/"%(date_1.month,date_1.day),".*\.html")
    for fileids in co.fileids():
        names.append(fileids)
    
    for i in names:
        if "android" in i:
            url='data/'+str(date_1.year)+'-%02d-%02d/' %(date_1.month,date_1.day)+str(i)
            print url
            r = urllib.urlopen(url).read()
            soup = BeautifulSoup(r,"lxml")
            hr=i.split("_")[0]
            mi=i.split("_")[1]
            date_2=date_1.replace(hour=int(hr),minute=int(mi))
            date_str=str(date_1.year)+"_%02d_%02d_%02d_%02d"%(date_1.month,date_1.day,int(hr),int(mi))
            try:
                desc=soup.find("div",{"class":"show-more-content text-body"}).get_text()
            except:
                continue
            #print "Description:\n"+desc
            try:
                ver = soup.find("div",{"itemprop":"softwareVersion"}).get_text()
                #print "Version:"+ver
            except:
                continue                
            
            try:
                siz = soup.find("div",{"itemprop":"fileSize"}).get_text()
                #print "Size:"+str(re.findall('\d+', siz)[0])
                
                s=int(re.findall('\d+', siz)[0])
            except:
                continue            
            size.append([date_2,int(s)])
            try:
                arat = soup.find("div",{"class":"score"}).get_text()
                #print "Average ratings:"+arat
                avrat.append([date_2,float(arat)])
            except:
                continue
            try:
                rat = soup.find("span",{"class":"reviews-num"}).get_text()
                #print "All ratings:"+rat
                a=rat
                b=a.split(',')
                c=0
                for j in range(0,len(b)-1):
                    c+=int(b[j])*(10**len(b[j+1]))+int(b[j+1])
                alrat.append([date_2,int(c)])
            except:
                continue
            try:
                strat = soup.find_all("span",{"class":"bar-number"})
            #print "5:"+strat[0].get_text()
                a=strat[0].get_text()
                b=a.split(',')
                c=0
                for j in range(0,len(b)-1):
                    c+=int(b[j])*(10**len(b[j+1]))+int(b[j+1])
                five.append([date_2,int(c)])
            except:
                continue
            #print "4:"+strat[1].get_text()
            try:
                a=strat[1].get_text()
                b=a.split(',')
                c=0
                for j in range(0,len(b)-1):
                    c+=int(b[j])*(10**len(b[j+1]))+int(b[j+1])
                four.append([date_2,int(c)])
            except:
                continue
            try:
                #print "3:"+strat[2].get_text()
                a=strat[2].get_text()
                b=a.split(',')
                c=0
                for j in range(0,len(b)-1):
                    c+=int(b[j])*(10**len(b[j+1]))+int(b[j+1])
                three.append([date_2,int(c)])
            except:
                continue
            #print "2:"+strat[3].get_text()
            try:
                a=strat[3].get_text()
                b=a.split(',')
                c=0
                for j in range(0,len(b)-1):
                    c+=int(b[j])*(10**len(b[j+1]))+int(b[j+1])
                two.append([date_2,int(c)])
            except:
                continue
            try:
            #print "1:"+strat[4].get_text()    
                a=strat[4].get_text()
                b=a.split(',')
                c=0
                for j in range(0,len(b)-1):
                    c+=int(b[j])*(10**len(b[j+1]))+int(b[j+1])
                one.append([date_2,int(c)])
            except:
                continue
            
            #print "\n\n\n"
            try:
                tmpdata={"average_rating":arat,
                         "total_rating":rat,
                         "rating_1":strat[4].get_text(),
                         "rating_2":strat[3].get_text(),
                         "rating_3":strat[2].get_text(),
                         "rating_4":strat[1].get_text(),
                         "rating_5":strat[0].get_text(),
                         "file_size":siz,
                         "version":ver,
                         "description":desc}
                with open("pokemon_android.json",'r') as fp:
                    ndata=json.load(fp)
                    ndata[date_str]=tmpdata
                with open("pokemon_android.json",'w') as fp:
                    fp.write(json.dumps(ndata))
            except:
                continue
         
         
        
    date_1 = date_1 + datetime.timedelta(days=1)
hfmt = dates.DateFormatter('%y/%m/%d %H:%M')       
si1=[]
si2=[]
for i in size:
    si1.append(i[0])
    si2.append(i[1])
fig1=plt.figure(figsize=(10,10))
ax = fig1.add_subplot(111)
plt.scatter(si1,si2)
ax.xaxis.set_major_formatter(hfmt)
plt.xticks(rotation='vertical')
plt.ylabel("size")
plt.xlabel("date")
plt.title("Size")
plt.grid(True)
fig1.savefig("ANDROID_Size.png")
plt.show()

av1=[]
av2=[]
for i in avrat:
    av1.append(i[0])
    av2.append(i[1])
fig2=plt.figure(figsize=(10,10))
ax = fig2.add_subplot(111)
plt.scatter(av1,av2)
ax.xaxis.set_major_formatter(hfmt)
plt.xticks(rotation='vertical')
plt.ylabel("Average Rating")
plt.xlabel("date")
plt.title("Average Rating")
plt.grid(True)
fig2.savefig("ANDROID_Average_Rating.png")
plt.show()

al1=[]
al2=[]
for i in alrat:
    al1.append(i[0])
    al2.append(i[1])

fig3=plt.figure(figsize=(10,10))
ax = fig3.add_subplot(111)
plt.scatter(al1,al2)    
ax.xaxis.set_major_formatter(hfmt)    
plt.xticks(rotation='vertical')
plt.ylabel("All Rating")
plt.xlabel("date")
plt.title("All Rating")
plt.grid(True)
fig3.savefig("ANDROID_All_Rating.png")
plt.show()

fi1=[]
fi2=[]
for i in five:
    fi1.append(i[0])
    fi2.append(i[1])

fig4=plt.figure(figsize=(10,10))
ax = fig4.add_subplot(111)
plt.scatter(fi1,fi2)        
ax.xaxis.set_major_formatter(hfmt)
plt.xticks(rotation='vertical')
plt.ylabel("5 Rating")
plt.xlabel("date")
plt.title("5 Rating")
plt.grid(True)
fig4.savefig("ANDROID_5_Rating.png")
plt.show()

fo1=[]
fo2=[]
for i in four:
    fo1.append(i[0])
    fo2.append(i[1])

fig5=plt.figure(figsize=(10,10))
ax = fig5.add_subplot(111)
ax.xaxis.set_major_formatter(hfmt)
plt.xticks(rotation='vertical')
plt.scatter(fo1,fo2)        
plt.ylabel("4 Rating")
plt.xlabel("date")
plt.title("4 Rating")
plt.grid(True)
fig5.savefig("ANDROID_4_Rating.png")
plt.show()

th1=[]
th2=[]
for i in three:
    th1.append(i[0])
    th2.append(i[1])

fig6=plt.figure(figsize=(10,10))
ax = fig6.add_subplot(111)
plt.scatter(th1,th2)      
ax.xaxis.set_major_formatter(hfmt)  
plt.xticks(rotation='vertical')
plt.ylabel("3 Rating")
plt.xlabel("date")
plt.title("3 Rating")
plt.grid(True)
fig6.savefig("ANDROID_3_Rating.png")
plt.show()

tw1=[]
tw2=[]
for i in two:
    tw1.append(i[0])
    tw2.append(i[1])

fig7=plt.figure(figsize=(10,10))
ax = fig7.add_subplot(111)
plt.scatter(tw1,tw2)        
ax.xaxis.set_major_formatter(hfmt)
plt.xticks(rotation='vertical')
plt.ylabel("2 Rating")
plt.xlabel("date")
plt.title("2 Rating")
plt.grid(True)
fig7.savefig("ANDROID_2_Rating.png")
plt.show()

on1=[]
on2=[]
for i in one:
    on1.append(i[0])
    on2.append(i[1])


fig8=plt.figure(figsize=(10,10))
ax = fig8.add_subplot(111)
plt.scatter(on1,on2)        
ax.xaxis.set_major_formatter(hfmt)
plt.xticks(rotation='vertical')
plt.ylabel("1 Rating")
plt.xlabel("date")
plt.title("1 Rating")
plt.grid(True)
fig8.savefig("ANDROID_1_Rating.png")
plt.show()
        
