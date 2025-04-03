from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
import sys
import pymysql
conf=SparkConf().setMaster('local[2]').setAppName('a')
sc=SparkContext(conf=conf)

ssc=StreamingContext(sc,5)  #响应时间
data=ssc.socketTextStream(sys.argv[1],int(sys.argv[2]))\
    .flatMap(lambda x:x.split(' '))\
    .map(lambda x:(x,1))\
    .reduceByKey(lambda x,y:x+y)
# data.pprint()#流数据要用pprint打印
#保存到文件里
data.saveAsTextFiles('file:///home/hadoop/output')
#保存到mysql里
def dbfunc(records):
    db=pymysql.connect(host='localhost',user='root',password='liujie',database='spark')
    cursor=db.cursor()
    def doinsert(p):
        sql="insert into wordcount(word,count) values('%s','%s')" % (str(p[0]),str(p[1]))
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    for item in records:
        doinsert(item)
def func(rdd):
    repartitionrdd=rdd.repartition(3)
    repartitionrdd.foreachPartition(dbfunc)
data.foreachRDD(func)
ssc.start()
ssc.awaitTermination()

ssc.stop()
sc.stop()