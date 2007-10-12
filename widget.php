<?php
/*  Copyright 2007  Steve Greenland  (email : steveg@moregruel.net)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/


/* The SG What's Playing widget for the sidebar */

function widget_SGWhatsPlaying_init() {

	if ( !function_exists('register_sidebar_widget') )
		return;

function widget_SGWhatsPlaying($args) {
	global $wpdb;

	// "$args is an array of strings that help widgets to conform to
	// the active theme: before_widget, before_title, after_widget,
	// and after_title are the array keys." - These are set up by the theme
	extract($args);

	// Get the current data
	$table_name = $wpdb->prefix . "sgwhatsplaying";
	$sql = "SELECT * FROM " . $table_name . " WHERE id=1 LIMIT 1";
	$songs = $wpdb->get_results($sql);
	$song = $songs[0];

	$timeago = time() - strtotime($song->time); /* Time since last update, in seconds */

	echo $before_widget . $before_title . "Now Playing";
	echo $after_title;
	echo "<ul><li>";
	if ($song->state == 'stop') {
		echo "Nothing's Playing...";
	} else {
		echo stripslashes($song->artist);
		echo " - ";
		echo stripslashes($song->title);
		if ($song->state == 'pause') {
			echo " (paused)";
		} elseif ($timeago > 30 * 60) {
			echo " (no recent updates)";
		}
	}
	echo "</li></ul>";

	echo $after_widget;
}

function widget_SGWhatsPlaying_control() {
	// No options.
	echo "<div>No widget options</div>";
}

	register_sidebar_widget(array("SG What's Playing", 'widgets'), 'widget_SGWhatsPlaying');
	register_widget_control(array("SG What's Playing", 'widgets'), 'widget_SGWhatsPlaying_control', 300, 200);

}
?>
