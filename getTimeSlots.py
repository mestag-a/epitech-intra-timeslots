#!/bin/env python
## getTimeSlots.py for test in /home/mestag_a/Documents/Projets/EIP/TimeSlotsDefenses
## 
## Made by alexis mestag
## Login   <mestag_a@epitech.net>
## 
## Started on  Sun Jun  7 16:51:48 2015 alexis mestag
## Last update Thu Aug 13 19:00:05 2015 alexis mestag
##

import  datetime
import  getpass
import  json
import  requests
import  sys

usage   = 'usage: {} url'.format(sys.argv[0])

login_url = 'https://intra.epitech.eu/'

class   Slot:
    def __init__(self, jsonContent):
        self._date = datetime.datetime.strptime(jsonContent['date'], '%Y-%m-%d %H:%M:%S');
        self._available = jsonContent['id_team'] == None

    @property
    def date(self):
        return (self._date)
    @property
    def available(self):
        return (self._available)

    def __repr__(self):
        return ('Slot[date={}, available={}]'.format(self.date, self.available))
    def __str__(self):
        ret = '{:%H:%M}'.format(self.date)
        if (not self.available):
            # ret = u'\u0336' + u'\u0336'.join(ret)
            ret = u'\u0336'.join(ret) + u'\u0336'
        return (ret)

class   SlotsGroup:
    def __init__(self, jsonContent):
        self._title = jsonContent['title']
        self._slots = [Slot(jc) for jc in jsonContent['slots']]
        self._slots.sort(key=lambda s: s.date)
        self._date = self._slots[0].date

    @property
    def title(self):
        return (self._title)
    @property
    def date(self):
        return (self._date)
    @property
    def slots(self):
        return (self._slots)

    def __str__(self):
        return ('{:%Y-%m-%d}'.format(self.date))

def     dumpSlots(json_content):
    slotsGroups = json_content['slots']
    groups = [SlotsGroup(jc) for jc in slotsGroups]
    groups.sort(key=lambda sg: sg.date)
    toPrint = '\n'.join('{} => {}'.format(g, ', '.join(str(s) for s in g.slots)) for g in groups)
    print(toPrint)
    
def     main(toGet_url):
    ret = 1
    username = input('Username: ')
    password = getpass.getpass()
        
    params = {'format': 'json'}

    session = requests.Session()
    r = session.post(login_url, data={'login': username, 'password': password, 'remind': True})
    loginOk = r.status_code == 200
    print('Login:', 'OK' if loginOk else 'KO')

    if (loginOk):
        r = session.get(toGet_url, params=params)
        content = r.content.decode('utf-8').replace('// Epitech JSON webservice ...', '')
        json_content = json.loads(content)
        dumpSlots(json_content)
        ret = 0
    return (ret)

if (__name__ == '__main__'):
    if (len(sys.argv) < 2):
        print(usage, file=sys.stderr)
        exit(2)
    ret = main(sys.argv[1])
    exit(ret)
