#!/usr/bin/python

"""Update SG What's Playing Plugin Wordpress blog

Config file has following sections

[sgwpupdate]
blog=URL
password=string
module=modname

[modname]
module_specific opttions.

for example:

[sgwpmpd]
mpdhost=hostname
mpdport=portnum

"""

import sys
import os
import time
from optparse import OptionParser
import ConfigParser

import logging, logging.handlers
import socket
import telnetlib

import urllib

from sgpyutil import daemon

def update_sgwhatsplaying(wpblogurl, wppassword,  wpdata):
    """wpdata is a dict with keys "artist", "title", "album", and "state"

    'state' should one of ("play", "pause", "stop")
    """
    logging.info("Updating %s with '%s', '%s', '%s', and '%s'",
                 wpblogurl,
                 wpdata['state'],
                 wpdata['artist'],
                 wpdata['title'],
                 wpdata['album'])
    params = wpdata.copy()
    params.update({'sgwhatsplaying':'update'})
    params.update({'password':wppassword})
    logging.debug("Parameters set as %s", params)
    params = urllib.urlencode(params)
    logging.debug("Parameters encoded as %s", params)
    try:
        f = urllib.urlopen(wpblogurl, params)
        logging.debug("url returned:\n %s", f.info())
        logging.debug(f.read().splitlines()[:30])
    except:
        logging.info("Server at %s unavailable", wpblogurl)
    return


def main(argv=None):
    # Option parsing
    parser = OptionParser(usage="usage: %prog [options] host version", version="0.1")
    parser.add_option("-d", "--debug", help="print program activity",
                      action="store_true", dest="debug", default=False)
    parser.add_option("-t", "--test", help="Show results of song lookup, but don't update blog",
                      action="store_true", dest="test", default=False)
    
    parser.add_option("-D", "--daemonize", help="Run as Unix daemon",
                      action="store_true", dest="daemon", default=False)

    parser.add_option("", "--title", help="Song title", action="store",
                      default="")
    parser.add_option("", "--album", help="Song title", action="store",
                      default="")
    parser.add_option("", "--artist", help="Song title", action="store",
                      default="")
    parser.add_option("", "--state", help="Song title", action="store",
                      default="")

    if argv is None:
        argv = sys.argv

    # Read command line options
    (options, args) = parser.parse_args()

    # Set up the console logger. We'll have two - one to the console,
    # one to a file, but we can't setup the file one until we've read
    # the config file
    
    logging.getLogger().setLevel(logging.NOTSET) # Handlers control log level
    conlog = logging.StreamHandler()
    conlog.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    if (options.debug):
        conlog.setLevel(logging.DEBUG)
    else:
        conlog.setLevel(logging.WARNING)
    logging.getLogger().addHandler(conlog)

    # Read config file
    cf = ConfigParser.ConfigParser()
    cfiles = cf.read(["/etc/sgwpupdate.conf", os.path.expanduser("~/.sgwpupdate.conf")])
    logging.debug("Read config files: %s", cfiles)

    # Convert config file to dict of dict.
    config = {}
    for s in cf.sections():
        config[s] = dict(cf.items(s))

    # Convenience configuration variables - one for the main, one for the
    # module
    cfmain = config['sgwpupdate']
    if 'module' in cfmain:
        cfmod = config[cfmain['module']]
    
    # make sure we have required info
    rk = ['blog', 'password'];
    for k in cfmain.keys():
        if k in rk:
            rk.remove(k)
    if rk:
        logging.error("Missing configuration values for:%s", " ".join(rk))
        return 2

    if 'logfile' in cfmain:
        filelog = logging.handlers.TimedRotatingFileHandler(
            filename = cfmain['logfile'],
            when="midnight", backupCount=2)
        filelog.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
        if options.debug:
            filelog.setLevel(logging.DEBUG)
        else:
            filelog.setLevel(logging.INFO)
            
        logging.getLogger().addHandler(filelog)
    
    songmodname =  cfmain['module']
    logging.debug("Loading song module %s", songmodname)
    songmod = __import__(songmodname)


    # Validate arguments.
    if options.daemon and options.title:
        logging.error("Option --daemon conflicts with --title")
        return 2


    # Okay, set for main loop 

    if options.daemon:
        daemon.daemonize(pidfile=cfmain.get('pidfile', None))
        logging.getLogger().removeHandler(conlog)

    wpdata_prev = {}
    wpdata = {}
    while 1:
        if options.title:
            wpdata['title'] = options.title
            wpdata['album'] = options.album
            wpdata['artist'] = options.artist
            wpdata['state'] = options.state
            dtime = -1
        else:
            (dtime, wpdata) = songmod.getsong(cfmod)
    
        if wpdata and wpdata != wpdata_prev: 
            if options.test:
                print "Artist: ", wpdata['artist']
                print "Title: ", wpdata['title']
                print "Album: ", wpdata['album']
                print "Player state: ", wpdata['state']
                logging.info("test: %(artist)s - %(title)s from %(album)s,"
                             " player is in %(state)s" % wpdata)
                return 0
            wpdata_prev = wpdata.copy()
            wpdata.update(dtime=dtime)
            logging.debug("wpdata: artist='%(artist)s', title='%(title)s',"
                          " album='%(album)s', "
                          " state='%(state)s', dtime=%(dtime)d" % wpdata)
                
            update_sgwhatsplaying(cfmain['blog'],
                                  cfmain['password'],
                                  wpdata)
        else:
            logging.debug("songmod.getsong() returned None for wpdata")
            
        if not options.daemon:
            return 0
        
        if (dtime > 0):
            time.sleep(dtime)
        else:
            time.sleep(60)

    return 0



if __name__ == "__main__":
    sys.exit(main())
