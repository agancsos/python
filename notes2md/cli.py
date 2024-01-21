#!/usr/bin/env python3
###############################################################################
# Name        : applie_notes_to_md.py                                         #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description :                                                               #
###############################################################################
import os, sys, logging;
sys.path.append(os.path.dirname(__file__));
from lib import migration_service;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	note_name                  = params["-n"] if "-n" in params.keys() else "";
	increase_sec_indents       = True if "--increase-indents" in params.keys() and int(params["--increase-indents"]) > 0 else False;
	dryrun                     = False if "--dry" in params.keys() and int(params["--dry"]) < 1 else True;
	remove_title               = True if "--remove-title" in params.keys() and int(params["--remove-title"]) > 0 else False;
	base_output                = params.get("-o", "");
	notes_db_path              = "{0}/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite".format(os.environ["HOME"]);
	session                    = migration_service.MigrationService(notes_db_path);
	session.migrate(note_name, dry=dryrun, increase_indents=increase_sec_indents, remove_title=remove_title, base_output=base_output);

