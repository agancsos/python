###############################################################################
## Name        : Chances                                                      #
## Author      : Abel Gancsos                                                 #
## Version     : v. 1.0.0                                                     #
## Description : Uses a large dataset to calculate chances of an event        #
###############################################################################
#!/bin/python
import random;
class Chances:
    heads = 0;
    tails = 0;
    max_flips = 5000;
    def __init__(self, flips=50):
        self.max_flips = flips;
        pass;
    def run(self):
        for flip_i in range(0, self.max_flips):
            result = random.randint(0,1);
            if(result == 0):
                self.heads += 1;
            else:
                self.tails += 1;
        return (self.heads / (self.tails + self.heads)) * 100;
    pass;

if __name__== "__main__":
    session = Chances();
    print("Your chances: {0:0.2f}%".format(session.run()));
    pass;