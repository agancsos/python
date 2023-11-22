#!/usr/bin/env python3
###############################################################################
# Name        : apple_link_to_note.py                                         #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description :                                                               #
###############################################################################
import os, sys, logging, sqlite3;
sys.path.append(os.path.dirname(__file__));
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	logger                     = logging.getLogger(__file__);
	note_name                  = params["-n"] if "-n" in params.keys() else "";
	notes_db_path              = "{0}/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite".format(os.environ["HOME"]);
	client                     = sqlite3.connect(notes_db_path);
	cursor                     = client.cursor();
	cursor.execute("select zidentifier, ztitle1, zfolder from ZICCLOUDSYNCINGOBJECT where ztitle1 is not null");
	notes                      = cursor.fetchall();
	for note in notes:
		if note_name == "" or note_name in note[1]:
			cursor2 = client.cursor();
			cursor2.execute("select ztitle2 from ZICCLOUDSYNCINGOBJECT where z_pk = '{0}'".format(note[2]));
			folder  = cursor2.fetchall()[0];
			logger.info("{0}/{1}: notes://showNote?identifier={1}".format(folder[0], note[1], note[0]));

