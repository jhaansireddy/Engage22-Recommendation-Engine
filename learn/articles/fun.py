
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from django.contrib.auth.models import User
from articles.models import UserDetails, Category, Articles


stop_words = set(stopwords.words('english'))
stop_words.add('also')
def give_keywords(my_text):
    r = Rake()
    ps = PorterStemmer()
    count = len(my_text.split(' '))
    r.extract_keywords_from_text(my_text)
    keywords = r.get_ranked_phrases()
    if count > 200:
        keywords= keywords[:int(count/10)]
    #print(keywords)
    con_string = ""
    stemmed =[]
    for i in keywords:
        l = i.split(' ')
        for j in l:
            w = ps.stem(j)
            if (w not in stemmed) and (w not in stop_words):
                stemmed.append(w)
                con_string= con_string+ " " + w

    return con_string

def similarity_count(text1,text2):
    count = 0
    t1 = text1.split(' ')
    t2 = text2.split(' ')
    for i in t1:
        for j in t2:
            if i==j:
                count = count + 1
                print(i)
    return count

# def compute_sim_users_init():
#     users = UserDetails.objects.all()
#     all_ids = users.values_list('id',flat = True)
#     superd = dict.fromkeys(all_ids,{})
#     v = ()
#     for x in users:
#         sim  = 0
#         v = v + (x.id)
#         for y in users.exclude(id = v):
#             sim = len(x.interests.all() & y.interests.all()) + len(x.likes.all() & y.likes.all())
#             superd[x.id][y.id] = sim
#             superd[y.id][x.id] = sim
#         ord =  dict(sorted(superd[x.id].items(),key= lambda item: item[1])) 
#         superd[x.id] = ord
#     return superd

def compute_sim_users(x):
    users = UserDetails.objects.all()
    superd = {}
    for y in users:
        sim  = 0
        sim = len(x.interests.all() & y.interests.all()) + len(x.likes.all() & y.likes.all())
        superd[y.id] = sim
    ord =  dict(sorted(superd.items(),key= lambda item: -item[1])) 
    return ord

def compute_sim_article(x):
    articles = Articles.objects.all().exclude(id=x.id)
    superd = {}
    for y in articles:
        sim  = 0
        sim = similarity_count(x.tags,y.tags)
        superd[y.id] = sim
    ord =  dict(sorted(superd.items(),key= lambda item: -item[1])) 
    return ord





