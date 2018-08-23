from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from bs4 import BeautifulSoup
import urllib
import matplotlib.pyplot as plt
import datetime
import json

with open("pokemon_ios.json","w") as fp:
    json.dump({},fp)


str_date="2016-07-21"
date_1 = datetime.datetime.strptime(str_date, "%Y-%m-%d")
end_date=datetime.datetime.strptime("2016-10-31", "%Y-%m-%d")
flag=0
size=[]
crat=[]
arat=[]
comdata={}
tmpdata={}
while date_1!=end_date:
    names=[]
    co = PlaintextCorpusReader("./data/"+str(date_1.year)+"-%02d-%02d/"%(date_1.month,date_1.day),".*\.html")
    for fileids in co.fileids():
        names.append(fileids)
    
    for i in names:
        if "ios" in i:
            url='data/'+str(date_1.year)+'-%02d-%02d/' %(date_1.month,date_1.day)+str(i)
            print url
            r = urllib.urlopen(url).read()
            soup = BeautifulSoup(r,"lxml")
            hr=i.split("_")[0]
            mi=i.split("_")[1]
            date_str=str(date_1.year)+"_%02d_%02d_%02d_%02d"%(date_1.month,date_1.day,int(hr),int(mi))
            desc=soup.find("p",{"itemprop":"description"}).get_text()
            #print "Description:\n"+desc
            
            ver = soup.find("span",{"itemprop":"softwareVersion"}).get_text()
            #print "Version:"+ver

            siz = soup.find_all("span",{"class":"label"})
            #print "Size:"+siz[3].next_sibling.split()[0]
            size.append([date_1.date(),int(siz[3].next_sibling.split()[0])])

            rat = soup.find_all("span",{"class":"rating-count"})
            if flag==0:
                curr=rat[0].get_text()
                allt=rat[1].get_text()
                flag=1
            if(len(rat)<2):
                allt=rat[0].get_text()
            else:
                curr=rat[0].get_text()
                allt=rat[1].get_text()
            #print "Current ratings:"+curr.split()[0]
            #print "All ratings:"+allt.split()[0]
            crat.append([date_1.date(),int(curr.split()[0])])
            arat.append([date_1.date(),int(allt.split()[0])])
            #print "\n\n\n"
            tmpdata={"total_rating":allt,
                     "total_rating_current_version":curr,
                     "file_size":siz[3].next_sibling,
                     "version":ver,
                     "Description":desc}
            with open("pokemon_ios.json",'r') as fp:
                ndata=json.load(fp)
                ndata[date_str]=tmpdata
            with open("pokemon_ios.json",'w') as fp:
                fp.write(json.dumps(ndata))
            
            
         
        
    date_1 = date_1 + datetime.timedelta(days=1)

si1=[]
si2=[]
cr1=[]
cr2=[]
ar1=[]
ar2=[]

for si in size:
    si1.append(si[0])
    si2.append(si[1])

for cr in crat:
    cr1.append(cr[0])
    cr2.append(cr[1])

for ar in arat:
    ar1.append(ar[0])
    ar2.append(ar[1])

fig1=plt.figure(figsize=(10,10))
plt.scatter(si1,si2)
plt.ylabel("size")
plt.xlabel("date")
plt.title("Size")
plt.grid(True)
fig1.savefig("IOS_Size.png")
plt.show()

fig2=plt.figure(figsize=(10,10))
plt.scatter(cr1,cr2)
plt.ylabel("Current Rating")
plt.xlabel("date")
plt.title("Current Rating")
plt.grid(True)
fig2.savefig("IOS_Current_Rating.png")
plt.show()

fig3=plt.figure(figsize=(10,10))
plt.scatter(ar1,ar2)        
plt.ylabel("All Raating")
plt.xlabel("date")
plt.title("All Rating")
plt.grid(True)
fig3.savefig("IOS_All_Rating.png")
plt.show()

