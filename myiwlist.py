#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import re
import subprocess


class Cell(object):
   def __init__(self,cell):
      self.cellnumber = cell['cellnumber']
      self.mac = cell['mac']
      self.frequency = cell['frequency']
      self.frequency_units = cell['frequency_units']
      try: self.channel = cell['channel']
      except KeyError: self.channel = ''
      self.signal_quality = cell['signal_quality']
      self.signal_total = cell['signal_total']
      self.signal_level_dBm = cell['signal_level_dBm']
      self.encryption = cell['encryption']
      self.essid = cell['essid']
      self.mode = cell['mode']
   def __str__(self):
      msg = 'Cell: %s    '%(self.cellnumber)
      msg += 'SSID: %s\n'%(self.essid)
      msg += 'Mode: %s\n'%(self.mode)
      msg += 'MAC: %s\n'%(self.mac)
      msg += 'Freq: %s %s\n'%(self.frequency, self.frequency_units)
      msg += 'Channel: %s\n'%(self.channel)
      msg += 'Signal: %s/%s (%s)\n'%(self.signal_quality, self.signal_total,
                                     self.signal_level_dBm)
      msg += 'Encryption: %s'%(self.encryption)
      return msg



cellNumberRe = re.compile(r"^Cell\s+(?P<cellnumber>.+)\s+-\s+Address:\s(?P<mac>.+)$")
regexps = [
    re.compile(r"^ESSID:\"(?P<essid>.*)\"$"),
    re.compile(r"^Protocol:(?P<protocol>.+)$"),
    re.compile(r"^Mode:(?P<mode>.+)$"),
    re.compile(r"^Frequency:(?P<frequency>[\d.]+) (?P<frequency_units>.+) \(Channel (?P<channel>\d+)\)$"),
    re.compile(r"^Frequency:(?P<frequency>[\d.]+) (?P<frequency_units>.+)$"),
    re.compile(r"^Encryption key:(?P<encryption>.+)$"),
    re.compile(r"^Quality=(?P<signal_quality>\d+)/(?P<signal_total>\d+)\s+Signal level=(?P<signal_level_dBm>.+) d.+$"),
    re.compile(r"^Signal level=(?P<signal_quality>\d+)/(?P<signal_total>\d+).*$")
]

# Detect encryption type
wpaRe = re.compile(r"IE:\ WPA\ Version\ 1$")
wpa2Re = re.compile(r"IE:\ IEEE\ 802\.11i/WPA2\ Version\ 1$")

# Runs the comnmand to scan the list of networks.
# Must run as super user.
# Does not specify a particular device, so will scan all network devices.
def scan(interface='wlan0'):
    cmd = ["sudo","iwlist", interface, "scan"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    points = proc.stdout.read().decode('utf-8')
    return points

# Parses the response from the command "iwlist scan"
def parse(content):
    cells = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        cellNumber = cellNumberRe.search(line)
        if cellNumber is not None:
            cells.append(cellNumber.groupdict())
            continue
        wpa = wpaRe.search(line)
        if wpa is not None :
            cells[-1].update({'encryption':'wpa'})
        wpa2 = wpa2Re.search(line)
        if wpa2 is not None :
            cells[-1].update({'encryption':'wpa2'}) 
        for expression in regexps:
            result = expression.search(line)
            if result is not None:
                if 'encryption' in result.groupdict() :
                    if result.groupdict()['encryption'] == 'on' :
                        cells[-1].update({'encryption': 'wep'})
                    else :
                        cells[-1].update({'encryption': 'off'})
                else :
                    cells[-1].update(result.groupdict())
                continue
    cells = [Cell(x) for x in cells]
    return cells
