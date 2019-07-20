################################################################################
## Name          : iphone_backup                                               #
## Author        : Abel Gancsos                                                #
## Version       : v. 1.0.0                                                    #
## Description   :                                                             #  
################################################################################
#!/bin/python

class Backup:
	src_base_path = "/private/var/mobile/Library/";
	tar_base_path = "";
	items = [ "Notes", "CallHistory", "Voicemail", "AddressBook", "Mail" ];
	
	def __init__(self):
		pass;

	def backup(self):
		for item in self.items:
			print("Backing up (0)/(1)".format(self.src_base_path, item));
			pass;
		pass;
	pass;

if __name__ == "main":
	session = Backup();
	session.backup();
	pass;
