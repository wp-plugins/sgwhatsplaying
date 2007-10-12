=== SG What's Playing ===
Contributors: vmole
Tags: music, sidebar
Requires at least: 2.2.0
Tested up to: 2.3
Stable tag: trunk

Display currently playing song from MPD or other music players in a sidebar widget.

== Description ==

Yes, it's yet another "currently playing" plugin. What makes this one
better (or, at least, different)?

* Support for [MPD](http://www.musicpd.org/ "Music Player Daemon")

* Support for others is possible and possibly easy - see below.

* No file transfer -- WordPress is updated via HTTP POST.

* Updater should work on Linux/BSD, OSX, and Windows.

SG What's Playing (SGWP from now on) is comes in two components: the
WordPress plugin, and a [Python](http://www.python.org) program
(`sgwpupdate.py`) that reads data from the player and POSTs it to the
blog.

The `sgwpupdate.py` program can be run as a one-shot or, on Unix-like
systems, as a daemon. In one-shot mode, you can specify song details
rather than reading them from the player. Thus, if your player can
trigger a program on song or status change (e.g. Audacious, WinAMP (I
think!)), you can probably use `sgwpupdate.py` to update your
WordPress blog.

In daemon mode, `sgwpupdate.py` uses a player-specific module to
obtain the song meta-data from the player and then sends the data to
your WordPress blog. At present, the only included module is for MPD,
but writing modules for other players shouldn't be too difficult. See
the "Custom Player Modules" section below.

== Installation ==

= The WordPress plugin and widget. =

* Unpack the archive.

* Copy `sgwhatsplaying.php` and `widget.php` to a `sgwhatsplaying`
  directory in your WordPress plugins directory. Or just unpack the
  archive under your plugins directory - all the python stuff will be
  ignored.

* Activate the plugin.

* Goto Options->SGWhatsPlaying, and set the "password". Don't use a
  password you use for any real access - this is just key to keep
  random losers from screwing with your blog, and is not secure in any
  real way.

= The updater program =

* Unpack the archive on the machine with access to your music player.

* If you don't have Python installed, install it. 

* (OPTIONAL) Run `python setup.py install` to install the program and
  module into your regular Python site directories. But you can skip
  this: `sgwpupdate.py` will run fine out of any directory.

* Copy sgwpupdate.conf to your `$HOME/.sgwpupdate.conf`, or
  `/etc/sgwpupdate.conf`.

* Edit the configuration file to set `password` and `blog` in the
  `sgwpupdate` section, and (if using MPD) `mpdhost` and `mpdport` in
  the `sgwpmpd` section. See later in this document for complete
  configuration documentation.

* Run `sgwpupdate.py --debug` to test. If you're not using MPD, you can
  test with `sgwpupdate.py --debug --title 'Some Song Title' --artist 
  'Some Artist' --album 'Album Name' --state 'play'`.

* To start in daemon mode, run `sgwpupdate.py --daemon`.

* The file `sgwupdate.ini` is a Debian-compatible initrc file. Copy it
  to `/etc/init.d/sgwpupdate` and create the desired links in
  `/etc/rc?.d` to have sgwpupdate.py automatically start on system
  boot.

== Screenshots ==

Not yet.

== Configuration ==

Configuration is via file. On Unix-like systems (includding OSX?), the
file is read from `~/.sgwpupdate.conf` or `/etc/sgwpupdate.conf`. If
both exist, entries in the former override those in the latter. The
file format is the usual WIN.INI style, with sections denoted by
square brackets and items specified as `item = value`. Normally, the
file will have two sections: the standard `[sgwpupdate]` section and a
module specific section such as `[sgwpmpd]`.

The supported configuration items in `[sgwpupdate]` section are:

* `blog` - URL to WordPress blog, such as `http://www.example.net/wordpress`

* `password` - simple password to allow updates, must match option in
  plugin configuration.

* `module` - name of python module to do player specific update.

* `logfile` - full path to logfile (optional)

* `pidfile` - full path to name of file where PID will be written, if
  running in daemon mode. (optional)

The supported configuration items for the `[sgwpmpd]` module section are:

* `mpdhost` - name of host where MPD is running, eg `localhost` or
  `mpd.example.net`

* `mpdport` - TCP port number for MPD. Almost always 6600.

== Custom Player Modules ==

Write a Python module containing a function name `getsong` that takes
a single argument, which will be a dictionary of the config items from
the module-specific configuration section. The function should return
a tuple of (remainingtime, songdata). The `remainingtime` value sets
how long `sgwpupdate.py` will wait before checking again in daemon
mode. The dictionary `songdata` should contain the following keys:

* `artist` - song performer or writer.

* `title` - song title.

* `album` - album title for the song.

* `state` - current state of the player, should be one of 'play',
  'pause', or 'stop'.

Your best bet is probably to copy `sgwpmpd.py` and work from there.
