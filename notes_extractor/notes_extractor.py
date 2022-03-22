#!/usr/bin/env python3
###############################################################################
# Name        : extract_notes.py                                              #
# Version     : v. 1.0.0.0                                                    #
# Author      : Abel Gancsos                                                  #
# Description : Helps extract data about Apple Notes.                         #
###############################################################################
import os, sys, sqlite3;

class INNote:
    identifier=None;name=None;
    def __init__(self, row=None):
        if row != None:
            self.identifier = row[0];
            self.name       = row[1];
    pass;
class NotesExtractor:
    notes_path=None;connection=None;cursor=None;
    def __init__(self, params=dict()):
        self.notes_path       = params["-p"] if "-p" in params.keys() else "{0}/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite".format(os.environ['HOME']);
        assert os.path.exists(self.notes_path), "Notes cache must exist...";
        self.connection = sqlite3.connect(self.notes_path);
        self.cursor     = self.connection.cursor();
    def ensure_close(self):
        self.connection.commit();
        self.connection.close();
    def search(self, keyword=""):
        notes  = list();
        self.cursor.execute("SELECT ZIDENTIFIER, ZTITLE1 FROM ZICCLOUDSYNCINGOBJECT WHERE ZTITLE1 LIKE '%{0}%'".format(keyword));
        rows = self.cursor.fetchall();
        for row in rows: notes.append(INNote(row));
        return notes;
    pass;

if __name__ == "__main__":
    params = dict();
    for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
    session = NotesExtractor(params);
    notes   = session.search(params["-n"] if "-n" in params.keys() else "");
    for note in notes: print("{1}\t\tnotes://showNote?identifier={0}".format(note.identifier, note.name));
    session.ensure_close();
