import json
import praw
from datetime import datetime, timedelta

with open('./data/dec2021.json') as fevents:
    events = json.load(fevents)

reddit = praw.Reddit('sperankbot')
spe = reddit.subreddit('shitpostemblem')
print('Accessing ' + spe.display_name)

tNow = datetime.utcnow()
TFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
event = events[0]
tLastupdate = datetime.strptime(event['lastupdate'], TFORMAT)

decDays = [None] * 26
for day in event['days']:
    decDays[day['day']] = day

cDay = tNow.day
print('Current day: ' + str(cDay))
if (cDay <= 25):
    decDay = decDays[cDay]

    if (decDay['megathread'] == ''):
        msg = "Hello! 🤖.\n\n"
        msg += '# SPEcember Day ' + str(cDay) + '\n\n'
        msg += 'Today\'s theme/topic: **' + decDay['theme'] + '**\n\n'
        msg += 'Description: ' + decDay['descr'] + '\n\n'
        msg += 'To participate, include the phrase **SPEcember Day ' + str(cDay) + '** in the title of your post (so it can be recognized/detected by the bot). You can check your progress/participation on https://www.reddit.com/r/shitpostemblem/wiki/specember_2021\n\n'
        msg += 'Please only contact/ping the mods (regarding bot/progression issues) if there are posts that are newer than yours and have been counted (aka the bot has been active after you created it) or it\'s been 24+ hours since you created your post.\n\n'
        msg += '\n\n---\n\n[General Info](https://www.reddit.com/r/shitpostemblem/comments/qjxufd/specember_2021_announcement_information_and/)\n\n[SPE Discord Server](http://discord.shitpostemblem.xyz)'
        title = 'SPEcember 2021 - Day ' + str(cDay) + ' (Megathread)'
        megathread = spe.submit(title, msg)
        megathread.mod.sticky()
        decDay['megathread'] = megathread.id

t0 = tLastupdate
t1 = tNow

for submission in spe.new(limit=100):
    ts = datetime.utcfromtimestamp(submission.created_utc)
    if (t1 < ts):
        continue
    if (ts < t0):
        break
    
    title = submission.title.lower().replace(']', ' ').replace(')', ' ').replace('-', ' ').replace(':', ' ').replace(',', ' ').replace('.', ' ').replace('specember 2021', 'specember')
    idx0 = title.find('specember day ')
    if (idx0 >= 0 and submission.author.name != 'SPEBot'):
        idx0 += 14
        idx1 = title.find(' ', idx0)
        if (idx1 < 0):
            idx1 = len(title)
        strday = title[idx0:idx1]
        if (strday.isnumeric()):
            pDay = int(strday)
            if (pDay > 0 and pDay <= 25):
                decDay = decDays[pDay]
                decDay['participants'].append({
                    'name': submission.author.name,
                    'submission': submission.permalink
                })
                
                if (decDay['megathread'] != ''):
                    megathread = reddit.submission(id=decDay['megathread'])
                    megathread.reply('[' + submission.title + '](' + submission.permalink + ') by u/' + submission.author.name)
            else:
                print('Not a valid day: ' + str(pDay))
        else:
            print('Not numeric: ' + strday)

event['lastupdate'] = tNow.strftime(TFORMAT)

with open('./data/dec2021.json', 'w') as fevents:
    json.dump(events, fevents, indent=2)

# TODO: Commit new json file

table = {}
for i in range(1, 26):
    for p in decDays[i]['participants']:
        author = p['name']
        if (not (author in table)):
            table[author] = [False] * 26
        table[author][i] = True

lbs = '#SPEcember 2021 Participation Table'
lbs += '\n\n| **User**'
for i in range(1, 26):
    lbs += ' | **' + str(i) + '**'
lbs += ' |\n|-|'
for i in range(1, 26):
    lbs += '-|'

for user, pcp in sorted(table.items(), key = lambda item: item[0].lower()):
    lbs += '\n|u/' + user
    for i in range(1, 26):
        lbs += '|' + ('\u2713' if pcp[i] else ' ')
    lbs += '|'

spe.wiki['specember_2021'].edit(lbs)