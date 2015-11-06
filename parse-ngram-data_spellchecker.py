#CHRISTOPHER M. CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

#KEEP ONLY 1GRAM and FREQUENCY
from os import walk
import csv
from IPython.display import clear_output

filepath = "E:/GoogleNGramData/one-gram-spellcheck/unziped/words-no-punc-num"

output=open(filepath+"/output.txt","w")
prev=""

for root,dir,files in walk(filepath):
    for f in files:
        with open(root + "/" + f,'r') as tsvin:
            tsvin = csv.reader (tsvin, delimiter="\t")
            for row in tsvin:
                ngram = row[0].split("_")[0]
                if (ngram != prev and prev!=""):
                    output.write(prev+"\t"+str(count)+"\n")
                    clear_output() #so i can see
                    print prev, "\t",count    #it working
                    count = 0
                prev = ngram
                count = count + int(row[2])
                
output.close()