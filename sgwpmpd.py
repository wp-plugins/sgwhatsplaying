#!/usr/bin/python

"""SGWhatsPlaying module for MPD

"""

import sys
import logging
import socket
import telnetlib

def mpd_connect(host="localhost", port=6600):
    """Connect to MPD server
    """
    logging.debug("Connecting to MPD at %s:%d", host, port)
    try:
        tn = telnetlib.Telnet(host, port)
    except socket.error, inst:
        logging.error("connection to %s:%d failed: %s", host, port, inst)
        return None
    
    (mid, mo, f) = tn.expect(["^OK MPD .*"], 5)
    logging.debug("tnconnect returned: %s ", f)
    return tn


def rspdict(f):
    """Convert multiple lines returned from MPD into dictionary

    Assumed form is "key: value", other lines are ignored
    """
    resp=f.splitlines()
    result = {}
    for l in resp[:-1]:
        logging.debug("rspdict: %s", l)
        try:
            (k, v) = l.split(": ")
            result[k] = v
        except ValueError:
            pass # ignore bad splits.
    return result
    

def mpdstatus(mpd):
    mpd.write("status\r\n")
    (mid, mo, f) = mpd.expect(["OK"], 5)
    resp=f.splitlines()
    mpds = rspdict(f)
    return mpds

def mpdcurrent(mpd):
    mpd.write("currentsong\r\n")
    (mid, mo, f) = mpd.expect(["OK"], 5)
    mpdc = rspdict(f)
    return mpdc

def getsong(config):
    """Return (time_to_next, wpdata) tuple

    Parameters
    
    - `config` dict of values from modules config file section
    """
    mpd = mpd_connect(config['mpdhost'], int(config['mpdport']))
    if not mpd:
        logging.error("MPD unavailable")
        return None
    
    mpds = mpdstatus(mpd)
    mpdc = mpdcurrent(mpd)
    mpd.close()

    wpdata = {}
    wpdata['artist'] = mpdc.get('Artist', 'unknown')
    wpdata['title'] = mpdc.get('Title', 'unknown')
    wpdata['album'] = mpdc.get('Album', 'unknown')
    wpdata['state'] = mpds.get('state', 'unknown')
    if 'time' in mpds:
        (p, t) = mpds['time'].split(":")
        p = int(p)
        t = int(t)
        rt =  t - p + 1
    else:
        rt = 60
    return (rt, wpdata)


