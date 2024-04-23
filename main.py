from flask import Flask, render_template, request, redirect
import pyodbc

qa = Flask(__name__)

def connection():
    server = '143.47.101.114' #Your server name
    db = 'QA_Automation_Staging_DB'
    username = 'StagingAutomationDB_User' #Your login
    password = 'Asc$nd@s#113' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+db+';UID='+username+';PWD='+ password
    conn = pyodbc.connect(cstr)
    return conn

@qa.route("/")
def login():
    return render_template("Login.html")

@qa.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@qa.route("/dashboard.html")
def dashboardhtml():
    return render_template("dashboard.html")

@qa.route("/modules" ,methods = ['GET', 'POST'])
def module(): 

    if request.method == 'POST':
        name = str(request.form["module_input"])
        impacts = str(request.form["impacts_input"])
        print("this is name: " +name)
        conn = connection()
        cursor = conn.cursor()
        modules = []
        cursor.execute("SELECT * FROM dbo.qa_modules")
        for row in cursor.fetchall():
            modules.append({"code": row[0], "modulename": row[1], "impacts": row[2]})
        modules_count = len(modules)
        code = modules_count+1
        qry = "insert into qa_modules values('{code}','{modulename}','{impacts}')".format(code =code, modulename = name,impacts=impacts)
        cursor.execute(qry)
        conn.commit()
        conn.close()

    modules = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.qa_modules")
    for row in cursor.fetchall():
        modules.append({"code": row[0], "modulename": row[1], "impacts": row[2]})
    conn.close()

    # print(test_scenarios)

    return render_template("modules.html",modules = modules)


@qa.route("/testscenarios/<module>/<modulename>" ,methods = ['GET', 'POST'])
def testscenario(module,modulename):     
    module = module.split("=")
    module = module[1]

    modulename = modulename.split("=")
    modulename = modulename[1]

    testscenario = []
    conn = connection()
    cursor = conn.cursor()

    qry = "select * from dbo.qa_testscenarios where module="+module+""
    print(qry)

    cursor.execute(qry)
    for row in cursor.fetchall():
        testscenario.append({"code": row[0], "testscenario": row[2], "testscenario_description": row[3]})
    conn.close()

    return render_template("testscenarios.html",testscenarios = testscenario, modulename=modulename,modulecode=module)   


@qa.route("/testcase/<modulecode>/<testscenariocode>/<testscenario>" ,methods = ['GET', 'POST'])
def testcase(modulecode,testscenariocode,testscenario):

    modulecode = modulecode.split("=")
    modulecode = modulecode[1]

    testscenariocode = testscenariocode.split("=")
    testscenariocode = testscenariocode[1]

    testscenario = testscenario.split("=")
    testscenario = testscenario[1]


    testcases = []
    conn = connection()
    cursor = conn.cursor()
    qry = "select * from dbo.qa_testcases where code="+modulecode+" and testscenario="+testscenariocode
    print(qry)
    cursor.execute(qry)
    for row in cursor.fetchall():
        testcases.append( {"code": row[0], "testscenariocode": row[1], "testcase_id": row[2],"testcase_summary": row[3]})
    conn.close()
    print(testcase)





    TestRunname = []
    conn = connection()
    cursor = conn.cursor()
    qry = "select * from qa_testrun order by 1 desc"

    print(qry)
    cursor.execute(qry)
    tb = cursor.fetchall()
    first_row = tb[0]
    code = first_row[0]
    version = first_row[1]
    description = first_row[2]       
    conn.close()
    print(testcase)
    return  render_template("testcase.html",ScenarioName=testscenario,testcases=testcases,testrun=version)   
   

@qa.route("/testrun",methods = ['GET', 'POST'])
def TestRun():

    if request.method == 'POST':
        version = str(request.form["version"])
        description = str(request.form["description"])
        conn = connection()
        cursor = conn.cursor()
        testruns = []
        cursor.execute("select * from qa_testrun")
        for row in cursor.fetchall():
            testruns.append({"code": row[0], "version": row[1], "description": row[2]})
        testruns_count = len(testruns)

        code = testruns_count+1
        qry = "insert into qa_testrun values('{code}','{version}','{description}')".format(code =code, version = version,description=description)
        cursor.execute(qry)
        conn.commit()
        conn.close()

    conn = connection()
    cursor = conn.cursor()
    testruns = []
    cursor.execute("select * from qa_testrun order by 1 desc")
    for row in cursor.fetchall():
            testruns.append({"code": row[0], "version": row[1], "description": row[2]})
    
    


    return render_template("TestRun.html",testruns=testruns)

@qa.route("/addtestrun",methods = ['GET', 'POST'])
def add_test_run():

    return render_template("addtestrun.html")


@qa.route("/spangpt",methods = ['GET', 'POST'])
def spangpt():
    
    if request.method == 'POST':
        question = str(request.form["question"])

        answer =""

        if question=="what is your name":
            answer="Murali"
        
       
        return render_template("spangpt1.0.1.html",answer=answer)

    return render_template("spangpt1.0.1.html")
    
        

if(__name__ == "__main__"):
    qa.run(debug=True)    