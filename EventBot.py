import json
import praw
from datetime import datetime, timedelta

def addpoints(submission, userpoints, teampoints = None, team = None):
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
        
        if (team != None):
            if team in teampoints:
                teampoints[team] += points
            else:
                teampoints[team] = points
            msg = 'Thank you for your submission! You earned **' + str(points) + '** point(s) for your team.\n\n[Current Events and Leaderboards](https://events.shitpostemblem.xyz)'
        else:
            msg = 'Thank you for your submission! You earned **' + str(points) + '** point(s).\n\n[Current Events and Leaderboards](https://events.shitpostemblem.xyz)'
        
        submission.reply(msg)

def generatewtannouncement(event, tPoststart, tPostend):
    a  = '# ' + event['title'] + '\n\n'
    a += 'New weekly themes!\n\n'
    a += event['descr'].replace('\n', '\n\n') + '\n\n'
    a += '**Posting Phase** (UTC): ' + str(tPoststart) + ' - ' + str(tPostend) + '\n\n'
    a += '**Tag**: ' + event['tag']
    return a

def generateslapfightannouncement(event, tPoststart, tPostend):
    a  = '# ' + event['title'] + '\n\n'
    a += 'A new slapfight event has started!\n\n'
    a += event['descr'].replace('\n', '\n\n') + '\n\n'
    a += '**Posting Phase** (UTC): ' + str(tPoststart) + ' - ' + str(tPostend) + '\n\n'
    a += '**Teams**: ' + ', '.join(map(lambda team: '[' + team['name'] + '](https://www.reddit.com/r/shitpostemblem/submit?title=%5B' + team['name'] + '%5D)', event['teams']))
    return a

def generateslapfightwinannouncement(event, teampoints):
    a  = '# ' + event['title'] + '\n\n'
    a += 'This slapfight event has ended. Congratulations to the winning team, **' + event['winner'] + '**! Final scores:\n\n'
    a += generateteamlbs(teampoints)
    return a

def generatecontestannouncement(event, tPoststart, tPostend, tVotestart, tVoteend):
    a  = '# ' + event['title'] + '\n\n'
    a += 'A new contest has started!\n\n'
    a += event['descr'].replace('\n', '\n\n') + '\n\n'
    a += '**Posting Phase** (UTC): ' + str(tPoststart) + ' - ' + str(tPostend) + '\n\n'
    a += '**Voting Phase** (UTC): ' + str(tVotestart) + ' - ' + str(tVoteend) + '\n\n'
    a += '**Tag**: ' + event['tag']
    return a

def generateteamlbs(teampoints):
    lbs = '| **Team** | **Points** |\n|-|-|'
    for team, points in sorted(teampoints.items(), key = lambda item: item[1], reverse = True):
        lbs += '\n|' + team.capitalize() + '|' + str(points) + '|'
    return lbs

with open('./data/events.json') as fevents:
    events = json.load(fevents)

userpoints = {}
with open('./data/users.json') as fusers:
    users = json.load(fusers)
    for user in users:
        userpoints[user['name']] = user['points']

reddit = praw.Reddit('sperankbot')
spe = reddit.subreddit('shitpostemblem')
print('Accessing ' + spe.display_name)

announcements = []
otherevents = []
tNow = datetime.utcnow()
TFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
for event in events:
    tPoststart = datetime.strptime(event['poststart'], TFORMAT)
    tPostend = datetime.strptime(event['postend'], TFORMAT)
    tVotestart = datetime.strptime(event['votestart'], TFORMAT)
    tVoteend = datetime.strptime(event['voteend'], TFORMAT)
    tLastupdate = datetime.strptime(event['lastupdate'], TFORMAT) if event['lastupdate'] != None else None

    if event['type'] == 'Weekly Themes':
        if event['stage'] == 0 and tNow > tPoststart:
            announcements.append(generatewtannouncement(event, tPoststart, tPostend))
            event['stage'] = 1
        
        if event['stage'] == 1:
            if tLastupdate == None:
                t0 = tPoststart
            else:
                t0 = max(tLastupdate - timedelta(days=3), tPoststart)
            
            if tNow > tVoteend:
                t1 = tPostend
                event['stage'] = 2
            else:
                t1 = min(tNow - timedelta(days=3), tPostend)

            for submission in spe.new(limit=400):
                ts = datetime.utcfromtimestamp(submission.created_utc)
                if (t1 < ts):
                    continue
                if (ts < t0):
                    break
                
                title = submission.title.lower()
                if (event['tag'].lower() in title):
                    addpoints(submission, userpoints)

            event['lastupdate'] = tNow.strftime(TFORMAT)

    elif event['type'] == 'Slapfight':
        if event['stage'] == 0 and tNow > tPoststart:
            announcements.append(generateslapfightannouncement(event, tPoststart, tPostend))
            event['stage'] = 1
        
        if event['stage'] == 1:
            if tLastupdate == None:
                t0 = tPoststart
            else:
                t0 = max(tLastupdate - timedelta(days=3), tPoststart)
            
            if tNow > tVoteend:
                t1 = tPostend
                event['stage'] = 2
            else:
                t1 = min(tNow - timedelta(days=3), tPostend)
            
            teampoints = {}
            teamnames = []
            for team in event['teams']:
                teampoints[team['name']] = team['points']
                teamnames.append(team['name'])

            for submission in spe.new(limit=400):
                ts = datetime.utcfromtimestamp(submission.created_utc)
                if (t1 < ts):
                    continue
                if (ts < t0):
                    break
                
                title = submission.title.lower()
                for tn in teamnames:
                    if ('[' + tn.lower() + ']' in title):
                        addpoints(submission, userpoints, teampoints, tn)
                        break
            
            jsonTPs = []
            for t, p in teampoints.items():
                jsonTPs.append({
                    'name': t,
                    'points': p
                })
            event['teams'] = jsonTPs

            if event['stage'] == 2:
                maxteam = None
                maxpoints = 0

                for t, p in teampoints.items():
                    if p > maxpoints:
                        maxteam = t
                        maxpoints = p
                event['winner'] = maxteam

                announcements.append(generateslapfightwinannouncement(event, teampoints))

            event['lastupdate'] = tNow.strftime(TFORMAT)

    elif event['type'] == 'Contest':
        if event['stage'] == 0 and tNow > tPoststart:
            announcements.append(generatecontestannouncement(event, tPoststart, tPostend, tVotestart, tVoteend))
            event['stage'] = 1
        
        if event['stage'] == 1:
            if tLastupdate == None or tLastupdate < tPoststart:
                t0 = tPoststart
            else:
                t0 = tLastupdate
            
            if tNow > tPostend:
                t1 = tPostend
                event['stage'] = 2
            else:
                t1 = tNow

            for submission in spe.new(limit=400):
                ts = datetime.utcfromtimestamp(submission.created_utc)
                if (t1 < ts):
                    continue
                if (ts < t0):
                    break
                
                title = submission.title.lower()
                if (event['tag'].lower() in title):
                    event['participants'].append({
                        'name': submission.author.name,
                        'submission': submission.permalink
                    })
            
            event['lastupdate'] = tNow.strftime(TFORMAT)
            # TODO: Create voting post if stage == 2
        
        if event['stage'] == 2:
            if tNow > tVoteend:
                event['stage'] = 3
                # TODO: Announce winner

if (len(announcements) > 0):
    msg = "Hello! I'm u/SPEBot and this is an automatically generated post."
    for a in announcements:
        msg += '\n\n' + a
    msg += '\n\n---\n\n[Current Events and Leaderboards](https://events.shitpostemblem.xyz)'
    title = 'Event Announcements (' + tNow.strftime('%b-%d-%Y') + ')'
    submission = spe.submit(title, msg)
    submission.mod.sticky()

with open('./data/events.json', 'w') as fevents:
    json.dump(events, fevents, indent=2)

jsonUPs = []
for u, p in userpoints.items():
    jsonUPs.append({
        'name': u,
        'points': p
    })
with open('./data/users.json', 'w') as fusers:
    json.dump(jsonUPs, fusers, indent=2)

# TODO: Commit new json files