#!/usr/bin/python

"""Unix Daemon creation and management

Functions to daemonize a python program, and tools to find and kill
that daemon later.

This is an abbreviated and modified version of a python daemon recipie
at http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/278731
posted by Chad Schroeder. Thanks, Chad.

His code was nicely commented, I stripped it out for compactness sake.
    
"""

import sys
import os

def maxfd(MAXFD=1024):
    """Attempt to retrieve maximum system fd.

    This is one of those nasty values that is system dependent, may be
    dynamic, and may not exist at all.

    """
    import resource		# Resource usage information.
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (maxfd == resource.RLIM_INFINITY):
        maxfd = MAXFD
  
    return maxfd
    

def daemonize(closefds=(0,1,2), pidfile=None, workdir="/", umask=0):
    """Daemonize the current process.

    - closefds - list of file descriptors to be closed.

    - pidfile - name of pidfile to be created.

    - workdir - working directory for daemon, usually "/".

    - umask - default umask for new files, usually 0
    
    """


    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if (pid != 0):
        os._exit(0)	# Exit parent of the first child.

    os.setsid()
    try:
        pid = os.fork()	# Fork a second child.
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if (pid != 0):
        # We might want to write the pid file here.
        if pidfile:
            os.umask(umask)
            f = open(pidfile, "w")
            f.write("%d\n" % (pid))
            f.close()
        os._exit(0)	# Exit parent of the second child.
    
    # This is our daemon process.
    if workdir:
        os.chdir(workdir)
    # Iterate through and close all file descriptors.
    for fd in closefds:
        try:
            os.close(fd)
        except OSError:	# ERROR, fd wasn't open to begin with (ignored)
            pass
            
    # Just close the stdio fds
    if (hasattr(os, "devnull")):
        REDIRECT_TO = os.devnull
    else:
        REDIRECT_TO = "/dev/null"
        
    os.open(REDIRECT_TO, os.O_RDWR)	# standard input (0)
    os.dup2(0, 1)			# standard output (1)
    os.dup2(0, 2)			# standard error (2)
    
    return(0)


from optparse import OptionParser

def main(argv=None):
    # Option parsing
    parser = OptionParser(usage="usage: daemon.py [options]", version="0.1")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      default=False,
                      help="print program activity")
    parser.add_option("-w", "--working-directory", dest="workdir", default=None,
                      help="Daemon working directory")
    parser.add_option("-u", "--umask", dest="umask", default=0022, type="int",
                      help="new umask")

    parser.add_option("-p", "--pidfile", dest="pidfile", default=None,
                      help="file in which to store PID")
    
    if argv is None:
        argv = sys.argv

    (options, args) = parser.parse_args()

    daemonize(workdir=options.workdir,
              umask=options.umask,
              pidfile=options.pidfile)

    return 0

if __name__ == "__main__":
    sys.exit(main())
