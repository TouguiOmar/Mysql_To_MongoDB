import mysql.connector, pymongo, datetime
from django.shortcuts import render
def index(request):
    #Get database name from index.html
    nom =request.POST.get('dbnom')

    #Connect to mysql using database name from input
    mydb = mysql.connector.connect(user='root', password='',
                                    host='127.0.0.1',
                                    database=nom)

    #Connect to mongodb
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mgodb = myclient["test1"]


    if(nom==None):
        return render(request,'index.html')
    else:
        mycursor = mydb.cursor()

        mycursor.execute("SHOW TABLES")
        data = mycursor.fetchall()
        mycursor=mydb.cursor(dictionary=True)
        for table in data:
            mycursor.execute("SELECT * From " +table[0])
            result = mycursor.fetchall()

            #Indiquer la collection de chaque table:
            mycol = mgodb[table[0]]
            col = mgodb['alt01']
            res = col.find()
            x = res[0]['image']
            print(x)

            with open('images/test.jpg', 'wb') as output:
               output.write(x)

            cursus = mydb.cursor(dictionary=True)

            cursus.execute("SHOW INDEX FROM "+table[0]+" WHERE Key_name ='PRIMARY'")

            look = cursus.fetchall()

            try:
                # eliminate data duplicate:
                mycol.create_index(look[0]['Column_name'], unique=True)
            except:
                pass
            for raw in result:
                 for key in raw:

                        #change type 'datetime' to String:
                      if (isinstance(raw[key], datetime.datetime) or isinstance(raw[key], datetime.date)):
                         raw[key] = raw[key].strftime('%Y-%m-%d %H:%M:%S')
                 try:
                    #Insert data:
                      mycol.insert_one(raw)
                 except:
                     pass

        return render(request,'success.html',{'nom':nom, 'data':data})
