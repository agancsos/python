###############################################################################
# Name      : glassdoor_search                                                #
# Author    : Abel Gancsos                                                    #
# Version   : 1.0.0.0                                                         #
###############################################################################
import os, sys, re, requests;

class GlassdoorHelper:
    operation=None;company=None;base_url=None;keyword_search=None;
    def __init__(self, params=dict()):
        self.operation = params["-o"] if "-o" in params.keys() else "ranking";
        self.company = params["-c"] if "-c" in params.keys() else r'Google';
        self.base_url = params["-b"] if "-b" in params.keys() else "";
        pass;
    def invoke(self):
        assert self.operation != "", "Operation cannot be empty...";
        assert self.company != "", "Company cannot be empty...";
        search_index = 0;
        comps = self.company.split(" ");
        search_index = 2 if len(comps) > 2 else 0;
        self.keyword_search = "-".join(self.company.split(" ")[:2])
        if (self.operation == "ranking"):
            if (self.base_url == ""):
                rsp = requests.post("https://www.glassdoor.com/Reviews/{0}-reviews-SRCH_KE.0,7.htm" \
                    .format(self.keyword_search), json={"sc.keyword": self.company}, headers={"User-Agent":"PostmanRuntime/7.26.8"});
                m = re.compile(r'Working-at[^"]+"'.format(self.company)).findall(str(rsp.content));
                company_id = None;
                for entry in m:
                    current = entry.split("\\")[0].replace('"', "").lower();
                    print(current);
                    if self.company.replace(" ", "-").lower() in current: company_id = entry.split("\\")[0].replace('"', ""); break;
                if company_id is not None:
                    rsp = requests.get("https://www.glassdoor.com/Overview/{0}".format(company_id), headers={"User-Agent":"PostmanRuntime/7.26.8"});
            else:
                rsp = requests.get(self.base_url, headers={"User-Agent":"PostmanRuntime/7.26.8"});
            if (rsp != None):
                #print(rsp.content);
                m = re.compile(r'"ratingValue"\s*:\s*"[^"]+"').findall(str(rsp.content));
                if (len(m) > 0):
                    comps = m[0].split(":");
                    print(comps[1].replace('"', "").strip());
                else:
                    print("Failed to find ranking...");
            else:
                print("Failed to find company...");
            pass;
        else:
            raise Exception("Operation not supported at this time...");
        pass;
    pass

if __name__ == "__main__":
    param = dict();
    for x in range(1, len(sys.argv[1:]), 2) : param[sys.argv[x]] = sys.argv[x + 1];
    session = GlassdoorHelper(param);
    session.invoke();
    pass;
