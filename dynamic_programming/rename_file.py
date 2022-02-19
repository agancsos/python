#!/usr/bin/env python3
###############################################################################
# Name        : int_problem_solving.py                                        #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description :                                                               #
###############################################################################
import os, sys;
from unittest import UnitTest;

## The most effecient way to solve this is via DP (dynamic programming).
## The reason we use DP here is because we need to find a specific substring from a larger random string.
## The LRS can have any number of any characters and we need to count the matches within the substring.
class RenameFile(UnitTest):
    def __init__(self, expected): UnitTest.__init__(self, expected);
    def on_invoke(self, args):
        new_name = args["newName"];
        old_name = args["oldName"];
        result = 0;
        n = len(new_name); m = len(old_name);  ## Not neccessarily needed, but makes the iterations cleaner.
        dp = [1 for i in range(m + 1)];        ## Initialize a cache using the haystack, in this case the old name.
                                               ## Note that '1' is used here since we know the characters exist in the substring.

        ## Iterate through the seed, in this case the new name
        for i in range(1, n + 1):
            dpp = [0 for _ in range(m + 1)];   ## Initialize a secondary stack for the current cursor
                                               ## Note that '1' is used here because we don't know if the characters match the substring.

            ## Iterate through the haystack in order to find the substring
            for j in range(i, m + 1):
                dpp[j] = dpp[j - 1];           ## Used the previous result as the base value.  Keep in mind that DP is all about remembering.
                if new_name[i - 1] == old_name[j - 1]: dpp[j] += dp[j - 1];    ## If we find a match, great!  Increment.
            dp = dpp;                          ## Update the DP cache with our findings
        result = max(dp);                      ## Extract the final result.  Some use index -1, but if you look at the table, it's just the last value.
        return result % 1000000007;            ## Typical when using large values.  HackerRank does this often.
    pass;
  
if __name__ == "__main__":
    test1 = RenameFile(27);
    print(test1.invoke({"newName":"abc", "oldName":"aaabbbccc"}));

    test1b = RenameFile(4);
    print(test1b.invoke({"newName":"ccc", "oldName":"cccc"}));

    test1c = RenameFile(339);
    print(test1c.invoke({"newName":"rrk", "oldName":"eispnddxtnfqalswxsmksfooiwxynamdjxnsmkiewkwdpzjpkibcbbmzbiwpmjczcehtczqjzlkgyvszpuuvetdfluuhxpeopuxmdylaysttenjmcedcumoeeicjtxkkvxcxjowrcvlttsqhwkbbmigtqlovjgviyzgcqjvpvotwucsetidicyhtcmajphxyyooeovuxvuploklpbovqdwdypbxgajuqwadgeedjkgurhsxdvylmyfjqlwzldrouylqobsgemwdoibqvcyedfvqopfhkqmhusxqacoogjxcoxbfzlwcxfvqaavfegkcirqqgdyhljmaqzqifuaoubukypavebvdujgsulahkprfpnzqaqgvfdxwtqflceilpmszizfwbonxplcyqittpkpbcfsesgfbiqnipolefrelphjthqrzsphbnumgrifmwiztfuhqibgaxdvysyvgxlspminykbyumepubrxuoavyovdbielzdobgqcjznjbexalkghywioxzbvxzfcshcozmefwcrvyibjdfqvqmhxdpccjodlgvkplrfdedpzoprfeechwszhvcdooejlchcwcektfrdmowhsueavbrawmihzsnfhrafbqeawdixznppfwieaivtmpqzqtsvnvwjmgvhuesssaxgmoywdgvwiouzuqdebijcqycftaftuwtgxavemciuqmxenprpmyzrexshnvtesstwhytmatxbuzxpstpygfxphpfckjdbfbximeeswyndfhomcnwjtfruvzwbhlzbvebyeucepgcdpmghcibfxg"}));
