# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#CHRISTOPHER M. CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

import re, collections, csv
from math import log

wd = "/home/cmchurch/Desktop/ngram-work/"
alphabet = 'abcdefghijklmnopqrstuvwxyzùàâûüæçéèêëïîôœABCDEFGHIJKLMNOPQRSTUVWXYZÙÀÂÛÜÆÇÉÈÊËÏÎÔŒ'
alpharegex = r"[" + re.escape(alphabet) + r"]\S+"
trained_data="google-n-gram.txt"
#trained_data="lexique-with-freq.tsv"

# <codecell>

#adapted from PETER NORVIG SPELLCHECKER (http://norvig.com/spell-correct.html)


def tokenize(text):
    return re.findall(alpharegex,text)

def readgrams(f):
    with open(wd + f,'r') as tsvin:
        tsvin = csv.reader (tsvin, delimiter="\t")
        model = collections.defaultdict(lambda: 1)
        for row in tsvin:
            #print row[0],row[1]
            model[row[0]]+=float(row[1])
        return model
    
NWORDS = readgrams(trained_data)

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def strip_newlines(text):
    return text.replace('\n',' ')

# <codecell>

#following code from http://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
#somehow combine this with unmatched candidates to see if they could be broken into two words?

#words = NWORDS #use the same trained data as above
data="lexique-with-freq.tsv" #changed it to use lexique data for splitter and ngrams data for spell corrector
words = readgrams(data)

wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""
    s=s.decode('utf8')
    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))

# <codecell>

sample_text= """TtxTE. — Avis de Pédîteur. — Aventures périlleuses d'un marin français dans la Nom
valwglinèg, u. Une Course de taiaresux à Mndrid. — Christophe Colomb,‘ sa vie et
ses dèmuveﬂem ..... gn bpumnau {and de la mer. -- Géographie du département de
rgiuﬂ- Le Tour Il! la ‘ferre en qunire-‘ringts récits. — Curiosités géographiques. —-
Chroiique. l . i l ' """

# <codecell>

sample_text="""Ma vie, à partir de cette époque,

fut celle de tous les marins. J'aimais -

le métier que j'avais choisi et, à. ‘l'âge
de 21 dans, je servais en _qu_a1ité. de lieu-
tenant sous les ordres de Philippe qui i,
plus âgé que moi, était devenu plecapi-
tainede IÎESpérancc. Nous avions con-y.
serve -l'un pour l'autre notre amitié»
d'enfance que, pendant tout ce temps,

un seul nuage était venutroubler : je a  

m'étais faitrecevoirfranc-maçjonepAne
gleterre, et lorsque, longtempsaprès,

je Fappris à Phil-ippe,il entra dïansﬁ-yner dansllalbaiede
une colère tellement violente q+üe_ﬁj_a_

crus de ma dignité de quitter son lrgord. 

Mais au bout de quelques jours mon

ami vint me chercher, et nous eûmes
bien vite oublié ce léger dilféremdÿt,"""

# <codecell>

sample_text="""ruina lerpouvoir usurpe de Tallxouns ou
‘Shogouns, ‘et releva l’autorite du Mikado.
.Chaque année, des l‘êtes viennent-rappeler
l’anniversaire de cette révolutionJLes re-
jou‘issances durent trois jours, comme—r
autlef‘ois chez nous pounles ‘Erois.__Glo-
rieuses. La’première journée est remplie
par les courses de chemuxplauseconde
par un ’feu d’artiﬁce’tiré en plein,soleîl,
avec gel-Les de ‘fumce muÏticoloreË‘Le-
troisiènﬁe‘jour qppantient aux. «Souinôs »
ou luueurs. * t “I"""

# <codecell>

cleaned_text = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚàèìòùÀÈÌÒÙâêîôÂÊÎÔãõÃÕÏçÇ:\-\' ]', ' ', sample_text.lower().decode('utf8'))
#cleaned_text = cleaned_text.replace(r'-\s','')
tokens = tokenize(cleaned_text)
print tokens

# <codecell>

newtext=""

for token in tokens:
    token=token.encode('utf8')
    best_candidate = correct(token)
    #print token + ", "+ best_candidate.decode('utf8')
    if (token==best_candidate):
        breakword=infer_spaces(best_candidate)
        if (len(breakword.split(' ')) < 4):
            best_candidate=breakword.encode('utf8')
    newtext+=best_candidate.decode('utf8')+" "
print newtext

# <codecell>

#string together problem tokens and see if there is a different way to slice the pie
#currently not working, lost track of the logical flow

problem_tokens = []
problem=0
newtext=""

for token in tokens:
    token = token.encode('utf8')
    best_candidate = correct(token)
    if token not in NWORDS:
        problem_tokens.append(token)
        problem_string = "".join(problem_tokens)
        best_candidate = correct(problem_string)
        if best_candidate in NWORDS:
            newtext+=best_candidate.decode('utf8')+" "
        else:
            breakword = infer_spaces(problem_string)
            if (len(breakword) > (len(token) *1.5 )):
                problem=1
            else:
                best_candidate = breakword
    elif (problem==1):
        #print problem_tokens
        problem_tokens = []
        problem=0
        newtext+=best_candidate.decode('utf8')+" "
    else:
        newtext+=best_candidate.decode('utf8')+" "
print newtext

# <codecell>

if "leadasdasd" in NWORDS:
    print 'yes'

# <codecell>

print breakword

# <codecell>

problem_tokens = ["a","b","c"]
print 

# <codecell>


