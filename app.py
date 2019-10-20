from flask import Flask, url_for, render_template, request
#from flask_mysqldb import MySQL
#from flask_ngrok import run_with_ngrok
import random
import pyodbc

app = Flask(__name__)
#run_with_ngrok(app)

'''
app.config['MYSQL_HOST'] = 'deepdivedb.database.windows.net'
app.config['MYSQL_USER'] = 'deepdive'
app.config['MYSQL_PASSWORD'] = 'admin@123'
app.config['MYSQL_DB'] = 'deepdivedb'

server_name='deepdivedb.database.windows.net'
db_name='deepdivedb'
#mysql = MySQL(app)
connection = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
	"Server=server_name;"
	"Database=db_name;"
	"uid=deepdive;pwd=admin@123")# Creating Cursor  
#connection = pyodbc.connect('Driver={SQL Server};''Server=server_name;''Database=db_name;''Trusted_Connection=yes;')# Creating Cursor  
#cursor = mysql.connection.cursor()
'''
server = 'deepdivedb.database.windows.net'
database = 'deepdivedb'
username = 'deepdive'
password = 'admin@123'
driver= '{ODBC Driver 17 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles', methods=['GET','POST'])
def api_article():
	inputInfo = request.form['pId']
	print(inputInfo)
	return writetodb(textSummary(),randomInfo(),inputInfo)


def randomInfo():
    randstring =""
    for x in range(9):
        randstring = randstring + str(random.randint(1,101)) + ","
    randstring = randstring + str(random.randint(1,101))
    return randstring

def textSummary():
	return ("This is newsample text" + str(random.randint(1,101)))

def getDbData(articleid):
    cur = connection.cursor()
    #cur.execute("select pName from PatientInfo where pId=1",)
    sql_select_query = """select pName from PatientInfo where pId = %s"""
    cur.execute(sql_select_query, (articleid,))
    record = cur.fetchall()
    #for row in record:
    #print ("PName:",record[0][0])

    #select pName from PatientInfo where pId=(%d),(articleid);
    #mysql.connection.commit()
    cur.close()
    return record[0][0]

def writetodb(summary,yaxisdata,patientid):
	cursor = connection.cursor()
	# Prepare SQL query to INSERT a record into the database.
	#sql = "UPDATE patientInfo SET pSummary=(?) WHERE pId = 20",('this is sample text')
	try:
	   # Execute the SQL command
	   print("Executing the command")
	   #sql_select_query = """UPDATE PatientInfo SET pSummary=%s , pGraphaYaxis=%s WHERE pId = %s"""
	   cursor.execute("UPDATE patientInfo SET pSummary=(?), pGraphYaxis=(?) WHERE pId = (?)",(summary,yaxisdata,patientid))
	   #cursor.execute("UPDATE PatientInfo SET pSummary=(?) , pGraphaYaxis=(?) WHERE pId = 1",(summary,yaxisdata,patientid))
	   #cursor.execute(sql_select_query, (summary,yaxisdata,patientid))
	   #cursor.execute("UPDATE PatientInfo SET pSummary='lsdjflsjdfljsaldfjsadfljas' WHERE pId = 1")
	   # Commit your changes in the database
	   print("Commiting the database")
	   connection.commit()
	   #print("Closing the db connection")
	   #cursor.close()	   
	   return "SUCCESS"
	except:
	   # Rollback in case there is any error
	   print("Rolling back due to error")
	   connection.rollback()
	   #print("Closing the db connection")
	   #cursor.close()	   
	   return "FAILURE"





if __name__ == '__main__':
    app.run()






