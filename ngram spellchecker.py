# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#CHRISTOPHER M. CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

wd = "/home/cmchurch/Desktop/ngram-work/"
alphabet = 'abcdefghijklmnopqrstuvwxyzùàâûüæçéèêëïîôœABCDEFGHIJKLMNOPQRSTUVWXYZÙÀÂÛÜÆÇÉÈÊËÏÎÔŒ'
alpharegex = r"[" + re.escape(alphabet) + r"]\S+"
init="lexique"

# <codecell>

#adapted from PETER NORVIG SPELLCHECKER (http://norvig.com/spell-correct.html)

import re, collections, csv
from IPython.display import clear_output

def tokenize(text):
    return re.findall(alpharegex,text)

def readgrams(f):
    with open(wd + f,'r') as tsvin:
        tsvin = csv.reader (tsvin, delimiter="\t")
        model = collections.defaultdict(lambda: 1)
        for row in tsvin:
            model[row[0]]+=float(row[1])
        return model
    
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#NWORDS = train(tokenize(file(wd+'lexique.txt').read()))


if (init=='1grams'):
    NWORDS = readgrams('google-n-gram.txt')
elif (init=='lexique'):
    NWORDS = readgrams('lexique-with-freq.tsv')

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

cleaned_text = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕÏçÇ:\- ]', ' ', sample_text.lower().decode('utf8'))
cleaned_text = cleaned_text.replace(r'-\s','')
tokens = tokenize(cleaned_text)

# <codecell>

newtext=""

for token in tokens:
    newtext+=correct(token.encode('utf-8'))+ " "
print newtext

# <codecell>

alpharegex = r"[" + re.escape(alphabet) + r"]+"
def tokenize(text):
    return re.findall(alpharegex,text)

# <codecell>

print cleaned_text

# <codecell>

def strip_newlines(text):
    return text.replace(r'-\s','')

# <codecell>

print strip_newlines(sample_text)

# <codecell>


# <codecell>


