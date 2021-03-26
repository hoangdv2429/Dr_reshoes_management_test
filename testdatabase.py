import psycopg2
conn = psycopg2.connect(database = 'test_1',user = 'postgres',password ='admin',host='localhost',port='5432') #ket noi vao database = conn
cur = conn.cursor() #con tro du lieu... lam viec o da


#truy van truc tiep :
cur.execute("select * from store.product")  #truy van 
data = cur.fetchall()
print(data)

#truy van co tham so:
s = 'CR'
cur.execute("select * from store.product where model = '%s'" % s)
data = cur.fetchall()
print(data)

#insert/updtae/delete:
cur.execute("insert into store.product values ('abc','2','AB','afdsa','90','1')")
conn.commit()
#test ddi r sang database xem ket qua
