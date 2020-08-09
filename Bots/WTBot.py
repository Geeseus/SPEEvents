import praw
import calendar
from datetime import datetime, timedelta

def addpoints(userpoints, submission):
    score = submission.score
    points = 0
    if score >= 10:
        points = 1
    if score >= 50:
        points = 2
    if score >= 100:
        points = 3
    if score >= 250:
        points = 4
    if score >= 500:
        points = 5
    author = submission.author.name
    if points > 0:
        if author in userpoints:
            userpoints[author] += points
        else:
            userpoints[author] = points
        msg = 'Thank you for your submission! You received **' + str(points) + '** point(s) for this post. Your new total score is **' + str(userpoints[author]) + '**.\n\n[Subreddit Leaderboards](https://www.reddit.com/r/shitpostemblem/wiki/leaderboards)'
        submission.reply(msg)

def generatepts(userpoints, t1):
    f = open('pointsnew.txt', 'w')
    f.write(str(calendar.timegm(t1.utctimetuple())))
    for u, p in userpoints.items():
        f.write('\n' + u + ' ' + str(p))
    f.close()

def generatelbs(userpoints, wikipage):
    lbs = '#SPE Point Leaderboards'
    lbs += '\n\n| **User** | **Points** |\n|-|-|'
    for user, points in sorted(userpoints.items(), key = lambda item: item[1], reverse = True):
        lbs += '\n|u/' + user + '|' + str(points) + '|'
    wikipage.edit(lbs)

def generatecss(userpoints):
    none = []
    bronze = []
    silver = []
    gold = []
    plat = []
    for user, points in userpoints.items():
        tier = none
        if (points >= 20):
            tier = bronze
        if (points >= 40):
            tier = silver
        if (points >= 80):
            tier = gold
        if (points >= 200):
            tier = plat
        tier.append(user)
    f = open('genstyle.css', 'w')
    if (len(bronze) > 0):
        f.write('.author[href$="user/' + bronze[0] + '"] + .flair')
        for i in range(1, len(bronze)):
            f.write(', .author[href$="user/' + bronze[i] + '"] + .flair')
        f.write(' { border-width: 3px; border-style: solid; border-image: linear-gradient(#402000, #805020, #fff, #d0a060) 1; }\n')
        f.write('.comment .author[href$="user/' + bronze[0] + '"] + .flair')
        for i in range(1, len(bronze)):
            f.write(', .comment .author[href$="user/' + bronze[i] + '"] + .flair')
        f.write(' { border-width: 2px; }\n')
    if (len(silver) > 0):
        f.write('.author[href$="user/' + silver[0] + '"] + .flair')
        for i in range(1, len(silver)):
            f.write(', .author[href$="user/' + silver[i] + '"] + .flair')
        f.write(' { border-width: 3px; border-style: solid; border-image: linear-gradient(#404950, #b7c9d0, #fff, #506068) 1; }\n')
        f.write('.comment .author[href$="user/' + silver[0] + '"] + .flair')
        for i in range(1, len(silver)):
            f.write(', .comment .author[href$="user/' + silver[i] + '"] + .flair')
        f.write(' { border-width: 2px; }\n')
    if (len(gold) > 0):
        f.write('.author[href$="user/' + gold[0] + '"] + .flair')
        for i in range(1, len(gold)):
            f.write(', .author[href$="user/' + gold[i] + '"] + .flair')
        f.write(' { border-width: 3px; border-style: solid; border-image: linear-gradient(#c09040, #f0e080, #fff, #e09000) 1; }\n')
        f.write('.comment .author[href$="user/' + gold[0] + '"] + .flair')
        for i in range(1, len(gold)):
            f.write(', .comment .author[href$="user/' + gold[i] + '"] + .flair')
        f.write(' { border-width: 2px; }\n')
    if (len(plat) > 0):
        f.write('.author[href$="user/' + plat[0] + '"] + .flair')
        for i in range(1, len(plat)):
            f.write(', .author[href$="user/' + plat[i] + '"] + .flair')
        f.write(' { border-width: 3px; border-style: solid; border-image: border-image: linear-gradient(#203030, #50a0b0, #fff, #70d0a7, #006060) 1; }\n')
        f.write('.comment .author[href$="user/' + plat[0] + '"] + .flair')
        for i in range(1, len(plat)):
            f.write(', .comment .author[href$="user/' + plat[i] + '"] + .flair')
        f.write(' { border-width: 2px; }\n')
    f.close()

f = open('points.txt', 'r')
t0 = datetime.utcfromtimestamp(float(f.readline()))
t1 = datetime.utcnow() - timedelta(days=3)

fl = f.read().splitlines()
userpoints = {}
for line in fl:
    u,p = line.split(' ')
    userpoints[u] = int(p)
f.close()

reddit = praw.Reddit('sperankbot')

print('Read-only access: ' + str(reddit.read_only))

spe = reddit.subreddit('shitpostemblem')

print('Accessing ' + spe.display_name)

for submission in spe.new(limit=400):
    ts = datetime.utcfromtimestamp(submission.created_utc)
    if (t1 < ts):
        continue
    if (ts < t0):
        break
    
    title = submission.title.lower()
    if ('[wt]' in title):
        addpoints(userpoints, submission)

generatepts(userpoints, t1)
generatelbs(userpoints, spe.wiki['leaderboards'])
generatecss(userpoints)

input('Bot execution finished. Press ENTER to exit.')