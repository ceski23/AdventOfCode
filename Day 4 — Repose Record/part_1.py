import re
from operator import itemgetter

pattern = r'\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hour>\d{2}):(?P<minute>\d{2})\]\s(?P<text>.*)'
lines = open('input.txt').read().splitlines()
logs = [re.search(pattern, line).groupdict() for line in lines]
logs.sort(key=itemgetter('year', 'month', 'day', 'hour', 'minute'))

guards, tStart, currentId = {}, 0, None

for log in logs:
  match = re.search(r'Guard #(\d+)', log['text'])
  if match:
    currentId = match.group(1)
    if currentId not in guards: guards[currentId] = {}
  else:
    if 'falls asleep' in log['text']: tStart = int(log['minute'])
    elif 'wakes up' in log['text']:
      for i in range(tStart, int(log['minute'])):
        if i not in guards[currentId]: guards[currentId][i] = 0
        guards[currentId][i] += 1

guardId, minute, maxMinutes = None, None, 0
for gId, minutes in guards.items():
  minutesSum = sum(minutes.values())
  if minutesSum > maxMinutes:
    maxMinutes = minutesSum
    guardId = gId
    minute = max(minutes.items(), key=itemgetter(1))[0]

print(int(guardId) * minute)