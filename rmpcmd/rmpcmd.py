###############################################################################
# Name       : rmpcmd                                                         #
# Author     : Abel Gancsos                                                   #
# Version    : v. 1.0.0                                                       #
# Description:                                                                #
###############################################################################
import sys;
import os;
import sqlite3;
import AMGData;
import urllib2;
import re;

"""
    This class helps import raw content about a professor, including feedback
    received from students and then searches for specific content.
"""
class RMPCMD:
    db_file = "";
    professor = "";
    school = "";
    api_base = "http://www.ratemyprofessors.com";
    search_base = api_base + "/search.jsp?query=";
    professor_page = "";
    department = "";
    session = None;
    verbose = False;
    no_update = False;
    pro_id = "";
    sch_id = "";
    dep_id = "";

    """
        This method initializes a new instance of the class.
    """
    def __init__(self,db,prof,sch,v,update,p,dep):
        self.db_file = db;
        self.professor = prof;
        self.verbose = v;
        self.professor_page = p;
        self.no_update = update
        self.school = sch;
        self.session = AMGData.AMGData(self.db_file);
        self.search_base += self.professor.replace(" ","+");
        self.search_base += ("+" + self.school.replace(" ","+"));
        if(self.verbose):
            print("".zfill(80).replace("0","="));
            print("# DB FILE  : {0}".format(self.db_file));
            print("# PROFESSOR: {0}".format(self.professor));
            print("# SCHOOL   : {0}".format(self.school));
            print("# API BASE : {0}".format(self.search_base));
            print("# PAGE     : {0}".format(self.professor_page));
            print("".zfill(80).replace("0","="));

    """
        This method creates the needed tables in the SQLite database.
    """
    def create_db(self):
        queries = list();
        queries.append("create table if not exists test (id integer primary key autoincrement,text_value character default '')");
        sql = "create table if not exists professors(id integer primary key autoincrement,first_name character default '',";
        sql += "last_name character default '',school integer default '1',department integer default '1',";
        sql += "last_updated_date timestamp default current_timestamp)";
        queries.append(sql);
        sql = "create table if not exists schools(id integer primary key autoincrement,school character default '',";
        sql += "city character default '',state character default '',last_updated_date timestamp default current_timestamp)";
        queries.append(sql);
        sql = "create table if not exists courses(id integer primary key autoincrement,course_number character default '',prof integer default '1',";
        sql += "course_name character default '',school integer default '1',last_updated_date timestamp default current_timestamp)";
        queries.append(sql);
        queries.append("create table if not exists department(id integer primary key autoincrement,department character default '')");
        sql = "create table if not exists feedback(id integer primary key autoincrement,overall character,comment character,";
        sql += "last_updated_date timestamp default current_timestamp,professor integer default '1',course integer default '1')";
        queries.append(sql);
        sql = "create table if not exists rmp_search_results(id integer primary key autoincrement,professor character default '',";
        sql += "school character default '', result_link character default '',last_updated_date timestamp default current_timestamp)";
        queries.append(sql);
        for query in queries:
            self.session.run_query(query);

    """
        This method imports the data from professor HTML page.
    """
    def import_professor_data(self):
        raw_html = urllib2.urlopen(self.professor_page).read();
        my_matches = re.findall(r"((\<strong\>)(.)+\</strong\>)",raw_html);
        if my_matches:
            row_index = 1;
            for my_match in my_matches:
                if(row_index % 3 == 0):
                    current_professor = my_match[0];
                    current_professor = current_professor.replace("<strong>","").replace("</strong>","");
                    if "of Specialization" not in current_professor and "Lecturer" not in current_professor and "  " not in current_professor:
                        if "Advisor" not in current_professor:
                            if(len(current_professor.split("/>")) > 1):
                                current_professor = current_professor.split("/>")[1];
                            name_comps = current_professor.split(" ");
                            if(len(name_comps) > 1):
                                self.session.run_query("insert into professors (first_name,last_name,department,school) values ('{0}','{1}','{2}','{3}')".format(
                                                   name_comps[0],name_comps[1],self.dep_id,self.sch_id));
                            print("##### {0}".format(current_professor));
                row_index += 1;

    """
        This method looks up the ID for a given record.
    """
    def lookup_id(self,table,key):
        if(table == "professors"):
            return self.session.query("select id from {0} where first_name||' '||last_name like '%{1}%'".format(table,key))[0][0];
        elif(table == "department"):
            return self.session.query("select id from {0} where department like '%{1}%'".format(table,key))[0][0];
        elif(table == "schools"):
            return self.session.query("select id from {0} where school like '%{1}%'".format(table,key))[0][0];

    """
        This method helps look up properties from the API page.
    """
    def prop_lookup(self,raw,search):
        my_matches2 = re.findall(r"prop2[^;]*;",raw,flags=re.DOTALL);
        if my_matches2:
            for my_match2 in my_matches2:
                current_match2 = my_match2;
                current_match2 = current_match2.replace("vmn_page_data =","");
                current_match2 = current_match2.replace(";","").replace("{","").replace("}","");
                props = tuple(current_match2.split(","));
                for prop in props:
                    if(prop.strip().split(":")[0].replace("\"","") == search):
                        return prop.strip().split(":")[1].replace("\"","");

    """
        This method imports the data from Rate My Professor(RMP).
    """
    def import_feedback_data(self):

        ## Search for professors through API
        reply = urllib2.urlopen(self.search_base);
        raw_response = reply.read();
        my_matches = re.findall(r"(/ShowRatings.jsp\?tid=(\d)+)",raw_response);
        
        ## Loop through matches
        if my_matches:
            for my_match in my_matches:
                current_match = my_match[0];
                current_match_value = current_match;
                current_match_value = current_match_value.strip();
                self.session.run_query("insert into rmp_search_results (professor,school,result_link) values ('{0}','{1}','{2}')".format(
                                      self.professor,self.school,current_match_value));
                ## Open comments page
                reply2 = urllib2.urlopen(self.api_base + current_match_value);
                raw_response2 = reply2.read();
                
                '''
                    Find professor and school data.
                '''
                ## School = 6, State = 5, Department = 3
                if(len(self.session.query("select * from schools where school = '{0}'".format(self.prop_lookup(raw_response2,"prop6")))) > 0):
                    self.session.run_query("update schools set state='{0}' where school='{1}'".format(self.prop_lookup(raw_response2,"prop5"),
                                           self.prop_lookup(raw_response2,"prop6")));
                else:
                    self.session.run_query("insert into schools (school,state) values ('{0}','{1}')".format(self.prop_lookup(raw_response2,"prop6"),
                                           self.prop_lookup(raw_response2,"prop5")));
                if(len(self.session.query("select * from department where department = '{0}'".format(self.prop_lookup(raw_response2,"prop3")))) == 0):
                    self.session.run_query("insert into department (department) values ('{0}')".format(self.prop_lookup(raw_response2,"prop3")));
                
                '''
                    Loop through comments
                    TODO:
                        * Filled in with tempated JSP
                '''

    """
        This method looks up feedback fro a given professor.
    """
    def search_content(self):
        results = list();
        '''
            Build query
        '''
        results = "select * from feedback join professors on feedback.professor = professors.id join courses on ";
        results += " courses.prof = professors.id join department on professors.department = department.id join schools on ";
        results += "schools.id = professors.school ";
        results += "where first_name||' '||last_name like '%" + self.professor + "%' and schools.school like '%" + self.school + "%'";
        rows = self.session.query(results);
        print("Results:");
        for result_row in rows:
            print("## {0}".format(",".join(str(column).strip() for column in result_row)));
    
    def run(self):
        session.create_db();
        self.pro_id = self.lookup_id("professors",self.professor);
        self.sch_id = self.lookup_id("schools",self.school);
        self.dep_id = self.lookup_id("department",self.department);
        if(self.no_update == True):
            self.import_professor_data();
            self.pro_id = self.lookup_id("professors",self.professor);
            self.sch_id = self.lookup_id("schools",self.school);
            self.dep_id = self.lookup_id("department",self.department);
            self.import_feedback_data();
        session.search_content();

if __name__ == "__main__":

    '''
        Globals
    '''
    scho = "Boston";
    pro = "George Ultrino";
    db = "";
    v = False;
    update = True;
    page = "http://www.bu.edu/csmet/fulltimefaculty/parttimefaculty/";
    dep = "Computer Science";

    ## Loop through the parameters to fill the global variables.    
    if(len(sys.argv) > 0):
        for arg_cursor in range(len(sys.argv)):
            if(sys.argv[arg_cursor] == "-f"):
                db = sys.argv[arg_cursor + 1];
            elif(sys.argv[arg_cursor] == "-p"):
                pro = sys.argv[arg_cursor + 1];
            elif(sys.argv[arg_cursor] == "-s"):
                scho = sys.argv[arg_cursor + 1];
            elif(sys.argv[arg_cursor] == "-v"):
                v = True;
            elif(sys.argv[arg_cursor] == "-u"):
                update = True;
            elif(sys.argv[arg_cursor] == "-a"):
                page = sys.argv[arg_cursor + 1];
            elif(sys.argv[arg_cursor] == "-d"):
                dep = sys.argv[arg_cursor + 1];
    if(db == ""):
        db = "./resources/db/rmp_cache.db";

    ## Fill database with content
    session = RMPCMD(db,pro,scho,v,update,page,dep);
    session.run();
