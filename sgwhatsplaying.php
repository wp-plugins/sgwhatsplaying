<?php
/*
Plugin Name: SG What's Playing
Plugin URI: http://www.moregruel.net/?page_id=73
Description: Display currently playing song in sidebar or posts
Author: Steve Greenland <steveg@moregruel.net>
Version: 1.1
Author URI: http://www.moregruel.net/
*/

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

/* Plugin constants */

define('SGWP_DB_VERSION', '1');


/* Create DB and options on install */

function sgwhatsplaying_install() {
	global $wpdb;

	$table_name = $wpdb->prefix . "sgwhatsplaying";

	if ($wpdb->get_var("SHOW TABLES LIKE '$table_name'") != $table_name) {
		$sql = "CREATE TABLE " . $table_name . " (
		id TINYINT,
	  	time TIMESTAMP,
	  	artist CHAR(30),
	  	title CHAR(30),
	  	album CHAR(30),
	  	state CHAR(10)
		);";

		if( file_exists( ABSPATH . 'wp-admin/includes/upgrade.php' ))
			require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
		else
			require_once(ABSPATH . 'wp-admin/upgrade-functions.php');

		dbDelta($sql);

		$coreid = 1;
		$insert = "INSERT INTO " . $table_name . "(id) " .
       		     "VALUES (" . $coreid. ")";

		$results = $wpdb->query( $insert );

      		add_option("sgwhatsplaying_db_version", SGWP_DB_VERSION);
      		add_option("sgwhatsplaying_password", "", "Update password");
	}

}

/* Update the DB with new info */

function sgwhatsplaying_update($myarg) {
	global $wpdb;
	if ($_POST['sgwhatsplaying'] == 'update') {
		$pwd = $_POST['password'];
		$rpwd = get_option("sgwhatsplaying_password");
		if ($pwd != $rpwd) {
			echo "FAIL";
			echo " bad password";
			die(0);
		}
		$table_name = $wpdb->prefix . "sgwhatsplaying";
		$artist = $_POST['artist'];
		$album = $_POST['album'];
		$title = $_POST['title'];
		$playstate = $_POST['state'];
		$sql = "UPDATE $table_name " .
			"SET artist = '" . $wpdb->escape($artist) . "', " .
			"album = '" . $wpdb->escape($album) . "', " .
			"title = '" . $wpdb->escape($title) . "', " .
			"state = '" . $wpdb->escape($playstate) . "' " .
			"WHERE id = 1";

		$results = $wpdb->query( $sql );
		if ($results == 1) {
			echo "OK";
		} else {
			echo "FAIL";
			$wpdb->print_error();
		}
		die(0);
	}
}

/* Option page */

function sgwhatsplaying_options() {
	if ('POST' == $_SERVER['REQUEST_METHOD']) {
		if (isset($_POST['sgwp_password'])) {
			update_option('sgwhatsplaying_password', $_POST['sgwp_password']);
		}
	}

	$sgwp_password = get_option('sgwhatsplaying_password');

	echo <<<END1
<div class="wrap">
	<h2>SG What's Playing Options</h2>

	<form action="" method="post" id="sgwhatsplaying-conf">
	<fieldset class="options">
	<ul><li>Password for sgwpupdate: <input type=text name="sgwp_password" value="$sgwp_password" size=16/>
	</li></ul></fieldset>
	<p class="submit">
		<input type="submit" name="Submit" value="Update Options " />
	</p>
	</form>
	</div>
END1;
}

function sgwhatsplaying_options_activate() {
	add_options_page("SG What's Playing Options", "SGWhatsPlaying", 8,
			"testoptions", "sgwhatsplaying_options");
}

/* The widget for the sidebar */

require_once('widget.php');

/* Okay, hook everything up into WP */
add_action('activate_sgwhatsplaying/sgwhatsplaying.php',
	 'sgwhatsplaying_install');
add_action('admin_menu', 'sgwhatsplaying_options_activate');
add_action('widgets_init', 'widget_SGWhatsPlaying_init');
add_action('init', 'sgwhatsplaying_update');

?>
