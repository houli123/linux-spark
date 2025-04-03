#all 
from pyspark import SparkConf,SparkContext  
conf=SparkConf().setMaster("local").setAppName("a")
from pyspark.sql import SparkSession,Row
from pyspark.sql.types import *
sc=SparkContext(conf=conf)
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()
#rdd
ls=['hello world']
rdd3=sc.parallelize(ls)  #并行化
rdd3.foreach(print) 
 rdd1=sc.textFile("file:///home/hadoop/word.txt") #用本地的方式
rdd2=sc.textFile("hdfs://192.168.134.19:9000/test/word.txt") #用hdfs的方式
rdd1.cache()  #持久化操作。等价于rdd1.persist（MEMORY_ONLY)只存在内存
rdd1.keys().foreach(print)  #generate a new rdd with rdd's keys()
rdd1.values().foreach(print)
rdd1.sortByKey().foreach(print)  #sort by first and second
rdd2=rdd1.sortBy(lambda x:x[0],ascending=False)  # sort by x[?]
rdd3=rdd1.mapValues(lambda x:x+10)
ls=[("hadoop",6),("spark",2),("hadoop",4),("spark",6)]
rdd1=sc.parallelize(ls).map(lambda x:(x[0],(x[1],1)))
#reduceByKey=only transform rdd's key
rdd2=rdd1.reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1]))
rdd3=rdd2.map(lambda x:(x[0],x[1][0]/x[1][1]))
print(rdd1.count(),rdd1.collect(),rdd1.first(),rdd1.take(3),rdd1.reduce(lambda x,y:x+y))
rdd1=sc.textFile("file:///home/hadoop/rdd/file*.txt")
rdd1.repartition(1) #partition again to 1 part.or use "collect" to collect two files
#accumulator
a=sc.accumulator(0)  #initialize
rdd2=rdd1.map(lambda x:a.add(x))  #惰性
rdd2.count()  #需要任意一个转换操作
print(a.value)
---------------------------------------------------------------------------------------
#dataframe
df1=spark.read.json('file:///home/hadoop/people.json')
df1.show()
df2=spark.read.csv('file:///home/hadoop/people.txt',header=True)#,sep=' '
# df1.createOrReplaceTempView("students")
#用sql查询，属于schema
# df2=spark.sql("select * from students")
df1.printSchema()
df1.select(df1['name'],df1.age+10).show()
df1.filter(df1.age>29).show()
df1.groupBy("age").count().show()
df2=df1.sort(df1.age.desc())
df2.show()
---------------------------------------------------------------------------------------
#rdd_to_dataframe
#转换成row型，为了转dataframe
rdd2=rdd1.map(lambda x:Row(name=x[0],age=int(x[1])))
#rdd转dataframe
df1=spark.createDataFrame(rdd2)
---------------------------------------------------------------------------------------
#rdd_to_dataframe2
#定义表头
schema=StructType([StructField('name',StringType(),True),StructField('age',IntegerType(),True)])
rdd1=sc.textFile("file:///opt/apps/spark/examples/src/main/resources/people.txt").map(lambda x:x.split(','))\
.map(lambda x:Row(x[0],int(x[1])))  #有了表头因此不用字段名了
df1=spark.createDataFrame(rdd1,schema)#前面数据，后面表头
df1.createOrReplaceTempView("people")
df2=spark.sql("SELECT * FROM people where age > 20")
#相对的spark.read.json，是目录
# df2.write.json("file:///home/hadoop/people2.json") 
# df2.write.text("file:///home/hadoop/people2.txt") 

#dataframe转rdd
rdd3=df2.rdd.map(lambda x:x.name+","+str(x.age))
rdd3.foreach(print)
---------------------------------------------------------------------------------------
#hbase_read
host = 'localhost'
table = 'student'
conf = {"hbase.zookeeper.quorum": host, "hbase.mapreduce.inputtable": table}
keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"
#read hbase's data by python
hbase_rdd = sc.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat","org.apache.hadoop.hbase.io.ImmutableBytesWritable","org.apache.hadoop.hbase.client.Result",keyConverter=keyConv,valueConverter=valueConv,conf=conf)
count = hbase_rdd.count()
hbase_rdd.cache()
output = hbase_rdd.collect()
for (k, v) in output:
        print (k, v)
#hbase_write
host = 'localhost'
table = 'student'
keyConv = "org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter"
valueConv = "org.apache.spark.examples.pythonconverters.StringListToPutConverter"
conf = {"hbase.zookeeper.quorum": host,"hbase.mapred.outputtable": table,"mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat","mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable","mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
rawData = ['3,info,name,Rongcheng','3,info,gender,M','3,info,age,26','4,info,name,Guanhua','4,info,gender,M','4,info,age,27']
#insert data into hbase by python
sc.parallelize(rawData).map(lambda x: (x[0],x.split(','))).saveAsNewAPIHadoopDataset(conf=conf,keyConverter=keyConv,valueConverter=valueConv)
---------------------------------------------------------------------------------------
#read_mysql
df1=spark.read.format('jdbc')\
    .option('driver','com.mysql.cj.jdbc.Driver')\
    .option('url','jdbc:mysql://localhost:3306/spark')\
    .option('dbtable','student')\
    .option('user','root')\
    .option('password','liujie')\
    .load()
#write_mysql.py 
schema=StructType([StructField('id',IntegerType(),True),StructField('name',StringType(),True),StructField('gender',StringType(),True),StructField('age',IntegerType(),True)])
rdd1=sc.parallelize(['3 rongcheng m 26','4 guanhua m 27']).map(lambda x:x.split(' ')).map(lambda x:Row(int(x[0]),x[1],x[2],int(x[3])))
df1=spark.createDataFrame(rdd1,schema=schema)
prop={}
prop['user']='root'
prop['password']='liujie'
prop['driver=']='com.mysql.cj.jdbc.Driver'
df1.write.jdbc("jdbc:mysql://localhost:3306/spark","student","append",prop)
 ---------------------------------------------------------------------------------------
# hive_read
from pyspark.sql import SparkSession,HiveContext  #老版本，.config("hive.metastore.uris"这段可以去掉
spark=SparkSession.builder.config(conf=SparkConf()).config("hive.metastore.uris","thrift://127.0.0.1:9083").enableHiveSupport().getOrCreate()
hc=HiveContext(spark)
#第一种方法
hc.sql("use spark")
df1=hc.sql("select * from student")
#第二种方法
df2=spark.sql("select * from spark.student")
#hive_write
hc=HiveContext(spark)
schema=StructType([StructField('no',IntegerType(),True),\
    StructField('name',StringType(),True),\
    StructField('sex',StringType(),True),\
    StructField('age',IntegerType(),True),\
    StructField('dept',StringType(),True)])
data=[(22190494,'xiaoming','男',20,'AI'),(22190499,'xiaomei','女',19,'AT')]
df1=spark.createDataFrame(data,schema)
df1.registerTempTable('temp')
hc.sql('insert into spark.student select * from temp')
---------------------------------------------------------------------------------------
#stream.py 
from pyspark.streaming import StreamingContext
conf=SparkConf().setMaster('local[2]').setAppName('a')  #涉及到流至少2个线程
ssc=StreamingContext(sc,5)  #响应时间
data=ssc.textFileStream('file:///home/hadoop/streaming')\
    .flatMap(lambda x:x.split(" "))\
    .map(lambda x: (x,1))
#socket streaming
data=ssc.socketTextStream(sys.argv[1],int(sys.argv[2])) 
#kafka
from pyspark.streaming.kafka import KafkaUtils
kQuorum,topic=sys.argv[1:]
kvs=KafkaUtils.\
    createStream(ssc,zkQuorum,"suibian",{topic:1})
data=kvs.map(lambda x:x[1]).flatMap(lambda x:x.split(' '))\
    .map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y)
data.pprint()  #流数据要用pprint打印
ssc.start()
ssc.awaitTermination()
#structed_streaming
from pyspark.sql.functions import split,explode
spark.sparkContext.setLogLevel('WARN')
#创建输入数据源
data=spark.readStream.format('socket')\
    .option('host','localhost')\
    .option('port','9999')\
    .load()
#定义流计算过程
words=data.select(explode(split(data.value,' ')).alias('word'))
wordcount=words.groupBy('word').count()
# 启动流计算并输出结果
query=wordcount.writeStream\
    .outputMode('complete')\
    .format('console')\
    .trigger(processingTime='8 seconds')\
    .start()
query.awaitTermination()

spark.stop() 
sc.stop() 
--------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
0 hello.py 
from pyspark import SparkConf,SparkContext  
conf=SparkConf().setMaster("local").setAppName("a")
sc=SparkContext(conf=conf)

ls=['hello world']
rdd3=sc.parallelize(ls)  #并行化
rdd3.foreach(print) 
 
--------------------------------------------------------------------------------------- 
001 sc.py 
from pyspark import SparkConf,SparkContext  #若没有开启pyspark必用该段
conf=SparkConf().setMaster("local").setAppName("aaaa")
sc=SparkContext(conf=conf)

# rdd1=sc.textFile("file:///home/hadoop/word.txt") #用本地的方式
# rdd2=sc.textFile("hdfs://192.168.134.19:9000/test/word.txt") #用hdfs的方式

ls=[22190494,"lsh",20,550]
rdd3=sc.parallelize(ls)  #并行化
rdd3.foreach(print) 
 
--------------------------------------------------------------------------------------- 
002 RDD1.py 
from pyspark import SparkConf,SparkContext
conf=SparkConf().setMaster("local").setAppName("b")
sc=SparkContext(conf=conf)
rdd1=sc.textFile("file:///home/hadoop/data1.txt")
#filter
rdd2=rdd1.filter(lambda x:"j" in x)
rdd2.foreach(print)
#map，映射单个结果
rdd3=rdd1.map(lambda x:x.split(' '))
rdd3.foreach(print)
#flatMap,映射多个结果 
rdd4=rdd1.flatMap(lambda x:x.split(' '))
rdd4.foreach(print)
#map高级
rdd5=rdd4.map(lambda x:(x,1))
rdd5.foreach(print)
#groupByKey,返回的不可输出的结果，可能需要配合聚合函数
rdd6=rdd5.groupByKey()
rdd6.foreach(print)
#reduceByKey
rdd7=rdd5.reduceByKey(lambda x,y:x+y)
rdd7.foreach(print)
sc.stop() 
 
--------------------------------------------------------------------------------------- 
003 RDD2.py 
from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
ls=[1,2,3,4,5]
rdd1=sc.parallelize(ls)
print(rdd1.count(),rdd1.collect(),rdd1.first(),rdd1.take(3),rdd1.reduce(lambda x,y:x+y))
rdd1.foreach(print)
sc.stop() 
 
--------------------------------------------------------------------------------------- 
004 persist.py 
from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
ls=["aa","bb","cc"]
rdd1=sc.parallelize(ls)
rdd1.cache()  #持久化操作。等价于rdd1.persist（MEMORY_ONLY)只存在内存
print(rdd1.count())
print(','.join(rdd1.collect()))
sc.stop() 
 
--------------------------------------------------------------------------------------- 
005 wordcounts.py 
from pyspark import SparkConf,SparkContext
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
rdd1=sc.textFile("file:///home/hadoop/data2.txt").flatMap(lambda x: x.split()).map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y)
# rdd2=rdd1.map(lambda x:x.split())
# rdd3=rdd1.flatMap(lambda x:x.split())
# rdd4=rdd3.map(lambda x:(x,1))
# rdd5=rdd4.reduceByKey(lambda x,y:x+y)
# rdd5.foreach(print)
rdd1.foreach(print)
sc.stop() 
 
--------------------------------------------------------------------------------------- 
006 key.py 
from pyspark import SparkConf,SparkContext
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
ls=[("hadoop",2),("spark",1),("hive",1),("spark",1)]
rdd1=sc.parallelize(ls)
rdd1.foreach(print)
# print(rdd1.keys())  #return 
# rdd1.keys().foreach(print)  #generate a new rdd with rdd's keys()
# rdd1.values().foreach(print)
# rdd1.sortByKey().foreach(print)  #sort by first and second
# rdd2=rdd1.sortBy(lambda x:x[0],ascending=False)  # sort by x[?]
# rdd2.foreach(print)
rdd3=rdd1.mapValues(lambda x:x+10)
rdd3.foreach(print)
sc.stop() 
 
--------------------------------------------------------------------------------------- 
007 book.py 
from pyspark import SparkConf,SparkContext
conf=SparkConf().setMaster("local").setAppName("aa")
sc=SparkContext(conf=conf)
ls=[("hadoop",6),("spark",2),("hadoop",4),("spark",6)]
rdd1=sc.parallelize(ls).map(lambda x:(x[0],(x[1],1)))
rdd1.foreach(print)

#reduceByKey=only transform rdd's key
rdd2=rdd1.reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1]))  
rdd2.foreach(print)

rdd3=rdd2.map(lambda x:(x[0],x[1][0]/x[1][1]))
rdd3.foreach(print)
sc.stop() 
 
--------------------------------------------------------------------------------------- 
008 sort.py 
from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName("a")
sc=SparkContext(conf=conf)
#use * to load all "file*.txt" file
rdd1=sc.textFile("file:///home/hadoop/rdd/file*.txt")
rdd1.repartition(1) #partition again to 1 part.or use "collect" to collect two files
# rdd1.foreach(print)
#if use sortByKey,you will need a tuple type for it.
rdd2=rdd1.map(lambda x:int(x.split(",")[2])).sortBy(lambda x:x,ascending=False)
rdd2.foreach(print)
print(rdd2.take(5))  #'.take' will return a list type
sc.stop() 
 
--------------------------------------------------------------------------------------- 
009 hbase.py 
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("ReadHBase")
sc = SparkContext(conf = conf)
host = 'localhost'
table = 'student'
conf = {"hbase.zookeeper.quorum": host, "hbase.mapreduce.inputtable": table}
keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"
#read hbase's data by python
hbase_rdd = sc.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat","org.apache.hadoop.hbase.io.ImmutableBytesWritable","org.apache.hadoop.hbase.client.Result",keyConverter=keyConv,valueConverter=valueConv,conf=conf)
count = hbase_rdd.count()
hbase_rdd.cache()
output = hbase_rdd.collect()
for (k, v) in output:
        print (k, v)
 
 
--------------------------------------------------------------------------------------- 
010 write.py 
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("ReadHBase")
sc = SparkContext(conf = conf)
host = 'localhost'
table = 'student'
keyConv = "org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter"
valueConv = "org.apache.spark.examples.pythonconverters.StringListToPutConverter"
conf = {"hbase.zookeeper.quorum": host,"hbase.mapred.outputtable": table,"mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat","mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable","mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
rawData = ['3,info,name,Rongcheng','3,info,gender,M','3,info,age,26','4,info,name,Guanhua','4,info,gender,M','4,info,age,27']
#insert data into hbase by python
sc.parallelize(rawData).map(lambda x: (x[0],x.split(','))).saveAsNewAPIHadoopDataset(conf=conf,keyConverter=keyConv,valueConverter=valueConv)
 
 
--------------------------------------------------------------------------------------- 
011 sort.py 
from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName('a')
sc=SparkContext(conf=conf)
rdd1=sc.textFile("file:///home/hadoop/file*.txt").repartition(1).map(lambda x:int(x))
rdd2=rdd1.sortBy(lambda x:x)
rdd2.foreach(print)
index=0
def getindex():
    global index
    index+=1
    return index
rdd3=rdd2.map(lambda x:(getindex(),x))
rdd3.foreach(print)
sc.stop() 
 
--------------------------------------------------------------------------------------- 
012 secondsort.py 
from operator import gt
from pyspark import SparkContext, SparkConf

class SecondarySortKey():
    def __init__(self, k):
        self.column1 = k[0]
        self.column2 = k[1]

    def __gt__(self, other): 
        if other.column1 == self.column1:
            return gt(self.column2,other.column2)
        else:
            return gt(self.column1, other.column1)
def main():
    conf = SparkConf().setAppName('spark_sort').setMaster('local[1]')
    sc = SparkContext(conf=conf)
    file="file:///home/hadoop/file4.txt"
    rdd1 = sc.textFile(file)
    rdd2 = rdd1.filter(lambda x:(len(x.strip()) > 0))
    rdd3 = rdd2.map(lambda x:((int(x.split(" ")[0]),int(x.split(" ")[1])),x))
    rdd4 = rdd3.map(lambda x: (SecondarySortKey(x[0]),x[1]))
    rdd5 = rdd4.sortByKey(False)
    rdd6 = rdd5.map(lambda x:x[1])
    rdd6.foreach(print)

if __name__ == '__main__':
    main()
 
 
--------------------------------------------------------------------------------------- 
013 acumulator.py 
from pyspark import SparkContext,SparkConf
conf=SparkConf().setMaster("local").setAppName('a')
sc=SparkContext(conf=conf)
a=sc.accumulator(0)  #initialize
ls=[1,2,3,4,5]
rdd1=sc.parallelize(ls)
rdd2=rdd1.map(lambda x:a.add(x))  #惰性
rdd2.count()  #需要任意一个转换操作
print(a.value)
sc.stop() 
 
--------------------------------------------------------------------------------------- 
014 spark.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()
df1=spark.read.json('file:///home/hadoop/people.json')
df1.show()
# df2=spark.read.csv('file:///home/hadoop/people.txt',header=True)
# df2.show()
df1.printSchema()
df1.select(df1['name'],df1.age+10).show()
df1.filter(df1.age>29).show()
df1.groupBy("age").count().show()
df2=df1.sort(df1.age.desc())
df2.show()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
015 schema.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()

df2=spark.read.csv('file:///home/hadoop/students.txt',header=True,sep=' ')
# df1.createOrReplaceTempView("students")
#用sql查询，属于schema
# df2=spark.sql("select * from students")
df2.show()
#利用rdd的dataframe查询
df2.groupBy("sex").count().show()
df2.select(df2['name']).show()
df2.filter(df2.age>20).show()
df2.groupBy("major").count().show()
df2=df2.sort(df2.age.desc())
df2.show()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
016 sql.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()
df1=spark.read.json('file:///home/hadoop/people.json')
df1.createOrReplaceTempView("people")
#利用sql语句查询
df2=spark.sql("select * from people where age>19")
df2.show()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
017 students_schema.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()

df1=spark.read.csv('file:///home/hadoop/students_schema.txt',header=True,sep=' ')
df1.createOrReplaceTempView("students_schema")

#1
spark.sql("select * from students_schema where name like '王%'").show()
#2
spark.sql("select * from students_schema where sex='男'").show()
#3
spark.sql("select department,count(*) from students_schema group by department").show()
#4
spark.sql("select sex,round(avg(age),2) from students_schema group by sex").show()

spark.stop() 
 
--------------------------------------------------------------------------------------- 
018 charter.py 
from pyspark import SparkConf,SparkContext  
conf=SparkConf().setMaster("local").setAppName("aaaa")
sc=SparkContext(conf=conf)
rdd=sc.textFile("file:///home/hadoop/chapter4-data1.txt")\
.map(lambda x:x.split(","))
# rdd.foreach(print)
# （1）该系总共有多少名学生。
rdd1 = rdd.map(lambda x: x[0]) 
distinct_rdd1 = rdd1.distinct()  #去重操作
print(distinct_rdd1.count())  #取元素总个数
# （2）该系共开设多少门课程。
rdd2 = rdd.map(lambda x: x[1]) 
distinct_rdd2 = rdd2.distinct()  
print(distinct_rdd2.count())
# （3）Tom 同学的总成绩平均分是多少。
rdd3 = rdd.filter(lambda x:x[0]=='Tom')
rdd3.foreach(print) 
score = rdd3.map(lambda x:int(x[2])) 
num = rdd3.count() #选课门数
#有reduce和reduceByKey，reduce用于只有数据需要求和的列，reduceByKey是用于至少两列的第二数据列的求和
sum_score = score.reduce(lambda x,y:x+y) #总成绩
avg = sum_score/num
print(avg)
# （4）每名同学的选修的课程门数。
#按键值对分组统计，映射后分组统计
rdd4 = rdd.map(lambda x:(x[0],1)) 
each_rdd4 = rdd4.reduceByKey(lambda x,y: x+y) 
each_rdd4.foreach(print)
# （5）该系 DataBase 课程共有多少人选修。
rdd5 = rdd.filter(lambda x:x[1]=='DataBase')
num = rdd5.count() 
print(num)
# （6）各门课程的平均分是多少。
rdd6 = rdd.map(lambda x:(x[1],(int(x[2]),1))) 
t = rdd6.reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1])) 
avg = t.map(lambda x:(x[0], round(x[1][0]/x[1][1],2)))
avg.foreach(print)
# （7）使用累加器计算共有多少人选修 DataBase 这门课。
rdd7 = rdd.filter(lambda x:x[1]=="DataBase")
accum = sc.accumulator(0) 
rdd7.foreach(lambda x:accum.add(1))
print(accum.value) 
 
--------------------------------------------------------------------------------------- 
020 employees.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()
df=spark.read.json('file:///home/hadoop/employees.json')
#1
df.show()
#2
df.distinct().show()
#3
df.drop("id").show()
#4
df.filter(df.age>30).show()
#5
df.groupBy("name").count().show()
#6
df.sort(df.name.asc()).show()
#7
for i in df.head(3):
    print(i)
#8
df.select(df.name.alias("username")).show()
#9
df.agg({"age": "mean"}).show()
#10
df.agg({"age": "min"}).show()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
021 rdd to dataframe.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,Row
conf=SparkConf().setMaster('local').setAppName('a')
sc=SparkContext(conf=conf)

#spark的session对象
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()
#当前是rdd，还没有转换成dataframe
rdd1=sc.textFile("file:///opt/apps/spark/examples/src/main/resources/people.txt").map(lambda x:x.split(','))

#转换成row型，为了转dataframe
rdd2=rdd1.map(lambda x:Row(name=x[0],age=int(x[1])))
# row = Row(name="Alice", age=11)
# print(row)
#rdd转dataframe
df1=spark.createDataFrame(rdd2)
# df1.show()

#sql版本
df1.createOrReplaceTempView("people") #表需要同要查询的一样
df2=spark.sql("select * from people where age>20")
df2.show()

#dataframe转rdd
rdd3=df2.rdd.map(lambda x:x.name+","+str(x.age))
rdd3.foreach(print)

sc.stop()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
022 rdd to dataframe2.py 
from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession,Row
from pyspark.sql.types import *
conf=SparkConf().setMaster("local").setAppName('a')
sc=SparkContext(conf=conf)  #创rdd
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()  #创dataframe

#定义表头
schema=StructType([StructField('name',StringType(),True),StructField('age',IntegerType(),True)])
rdd1=sc.textFile("file:///opt/apps/spark/examples/src/main/resources/people.txt").map(lambda x:x.split(','))\
.map(lambda x:Row(x[0],int(x[1])))  #有了表头因此不用字段名了
df1=spark.createDataFrame(rdd1,schema)#前面数据，后面表头
df1.createOrReplaceTempView("people")
df2=spark.sql("SELECT * FROM people where age > 20")
df2.show()
#相对的spark.read.json，是目录
# df2.write.json("file:///home/hadoop/people2.json") 
# df2.write.text("file:///home/hadoop/people2.txt") 

sc.stop()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
023 read_mysql.py 
from pyspark import SparkConf
from pyspark.sql import SparkSession
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()
# format('json')
df1=spark.read.format('jdbc')\
    .option('driver','com.mysql.cj.jdbc.Driver')\
    .option('url','jdbc:mysql://localhost:3306/spark')\
    .option('dbtable','student')\
    .option('user','root')\
    .option('password','liujie')\
    .load()
df1.show()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
024 write_mysql.py 
from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession,Row
from pyspark.sql.types import *
conf=SparkConf().setMaster('local').setAppName('a')
sc=SparkContext(conf=conf)
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()

schema=StructType([StructField('id',IntegerType(),True),StructField('name',StringType(),True),StructField('gender',StringType(),True),StructField('age',IntegerType(),True)])
rdd1=sc.parallelize(['3 rongcheng m 26','4 guanhua m 27']).map(lambda x:x.split(' ')).map(lambda x:Row(int(x[0]),x[1],x[2],int(x[3])))
df1=spark.createDataFrame(rdd1,schema=schema)
prop={}
prop['user']='root'
prop['password']='liujie'
prop['driver=']='com.mysql.cj.jdbc.Driver'
df1.write.jdbc("jdbc:mysql://localhost:3306/spark","student","append",prop)
print("yes")

spark.stop()
sc.stop() 
 
--------------------------------------------------------------------------------------- 
025 hive.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,HiveContext  #老版本，.config("hive.metastore.uris"这段可以去掉
spark=SparkSession.builder.config(conf=SparkConf()).config("hive.metastore.uris","thrift://127.0.0.1:9083").enableHiveSupport().getOrCreate()
hc=HiveContext(spark)
#第一种方法
# hc.sql("use spark")
# df1=hc.sql("select * from student")
# df1.show()
#第二种方法
df2=spark.sql("select * from spark.student")
df2.show() 
 
--------------------------------------------------------------------------------------- 
026 hive_write.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,HiveContext
from pyspark.sql.types import *
conf=SparkConf().setMaster("local").setAppName("a")
sc=SparkContext(conf=conf)
spark=SparkSession.builder.config(conf=SparkConf()).enableHiveSupport().getOrCreate()
hc=HiveContext(spark)
schema=StructType([StructField('no',IntegerType(),True),\
    StructField('name',StringType(),True),\
    StructField('sex',StringType(),True),\
    StructField('age',IntegerType(),True),\
    StructField('dept',StringType(),True)])
data=[(22190494,'xiaoming','男',20,'AI'),(22190499,'xiaomei','女',19,'AT')]
df1=spark.createDataFrame(data,schema)
df1.registerTempTable('temp')
hc.sql('insert into spark.student select * from temp')
print("very good") 
 
--------------------------------------------------------------------------------------- 
027 stream.py 
from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
conf=SparkConf().setMaster('local[2]').setAppName('a')  #涉及到流至少2个线程
sc=SparkContext(conf=conf)

ssc=StreamingContext(sc,5)  #响应时间
data=ssc.textFileStream('file:///home/hadoop/streaming')\
    .flatMap(lambda x:x.split(" "))\
    .map(lambda x: (x,1))
result=data.reduceByKey(lambda x,y:x+y)
result.pprint()  #流数据要用pprint打印
ssc.start()
ssc.awaitTermination()

sc.stop()
ssc.stop() 
 
--------------------------------------------------------------------------------------- 
028_socket.py 
from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
import sys
conf=SparkConf().setMaster('local[2]').setAppName('a')
sc=SparkContext(conf=conf)

ssc=StreamingContext(sc,5)  #响应时间
data=ssc.socketTextStream(sys.argv[1],int(sys.argv[2]))
res=data.flatMap(lambda x:x.split(' ')).map(lambda x: (x,1)).reduceByKey(lambda x,y:x+y)
res.pprint()#流数据要用pprint打印
ssc.start()
ssc.awaitTermination()

sc.stop()
ssc.stop() 
 
--------------------------------------------------------------------------------------- 
029_socket_tosql.py 
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
 
--------------------------------------------------------------------------------------- 
030kafka_wordcount.py 
import sys
from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
conf=SparkConf().setMaster('local[2]').setAppName('a')
sc=SparkContext(conf=conf)

ssc=StreamingContext(sc,1)
zkQuorum,topic=sys.argv[1:]
kvs=KafkaUtils.\
    createStream(ssc,zkQuorum,"suibian",{topic:1})
data=kvs.map(lambda x:x[1]).flatMap(lambda x:x.split(' '))\
    .map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y)
data.pprint()
ssc.start()
ssc.awaitTermination()

ssc.stop()
sc.stop() 
 
--------------------------------------------------------------------------------------- 
031kafka2.py 
from __future__ import print_function
import sys
from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: KafkaWordCount.py <zk> <topic>", file=sys.stderr)
        exit(-1)
    conf=SparkConf().setMaster('local[2]').setAppName('a')
    sc=SparkContext(conf=conf)
    ssc = StreamingContext(sc, 1)
    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils. \
        createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()
    ssc.start()
    ssc.awaitTermination() 
 
--------------------------------------------------------------------------------------- 
032structed_streaming.py 
#Structured Streaming 程序对每行英文语句进行拆分，并统计每个单词出现的频率
from pyspark.sql import SparkSession
from pyspark.sql.functions import split,explode
spark=SparkSession.builder.appName('a').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

#创建输入数据源
data=spark.readStream.format('socket')\
    .option('host','localhost')\
    .option('port','9999')\
    .load()
#定义流计算过程
words=data.select(explode(split(data.value,' ')).alias('word'))
wordcount=words.groupBy('word').count()
# 启动流计算并输出结果
query=wordcount.writeStream\
    .outputMode('complete')\
    .format('console')\
    .trigger(processingTime='8 seconds')\
    .start()
query.awaitTermination()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
033spark_generate.py 
# 导入需要用到的模块
import os
import shutil
import random
import time
TEST_DATA_TEMP_DIR = '/home/hadoop/tmp/'
TEST_DATA_DIR = '/home/hadoop/tmp/testdata/'
ACTION_DEF = ['login', 'logout', 'purchase']
DISTRICT_DEF = ['fujian', 'beijing', 'shanghai', 'guangzhou']
JSON_LINE_PATTERN = '{{"eventTime": {}, "action": "{}", "district": "{}"}}\n'
def test_setUp():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR, ignore_errors=True)
    os.mkdir(TEST_DATA_DIR)
def test_tearDown():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR, ignore_errors=True)
def write_and_move(filename, data):
    with open(TEST_DATA_TEMP_DIR + filename,
              "wt", encoding="utf-8") as f:
        f.write(data)
    shutil.move(TEST_DATA_TEMP_DIR + filename,
                TEST_DATA_DIR + filename)
if __name__ == "__main__":
    test_setUp()
    for i in range(1000):
        filename = 'e-mall-{}.json'.format(i)
        content = ''
        rndcount = list(range(100))
        random.shuffle(rndcount)
        for _ in rndcount:
            content += JSON_LINE_PATTERN.format(
                str(int(time.time())),
                random.choice(ACTION_DEF),
                random.choice(DISTRICT_DEF))
        write_and_move(filename, content)
        # time.sleep(1)
    # test_tearDown() 
 
--------------------------------------------------------------------------------------- 
034json_structed_streaming.py 
# 导入需要用到的模块
import os
import shutil
from pprint import pprint

from pyspark.sql import SparkSession
from pyspark.sql.functions import window, asc
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import TimestampType, StringType
# 定义JSON文件的路径常量
TEST_DATA_DIR_SPARK = 'file:///home/hadoop/tmp/testdata/'
if __name__ == "__main__":
    # 定义模式，为时间戳类型的eventTime、字符串类型的操作和省份组成
    schema = StructType([
        StructField("eventTime", TimestampType(), True),
        StructField("action", StringType(), True),
        StructField("district", StringType(), True)])

    spark = SparkSession\
        .builder\
        .appName("StructuredEMallPurchaseCount") \
        .getOrCreate()

    spark.sparkContext.setLogLevel('WARN')
    lines = spark\
        .readStream\
        .format("json") \
        .schema(schema) \
        .option("maxFilesPerTrigger", 100) \
        .load(TEST_DATA_DIR_SPARK)

    # 定义窗口
    windowDuration = '1 minutes'

    windowedCounts = lines\
        .filter("action = 'purchase'")\
        .groupBy('district', window('eventTime', windowDuration))\
        .count()\
        .sort(asc('window'))
    query = windowedCounts\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .option('truncate', 'false')\
        .trigger(processingTime="10 seconds")\
        .start()

    query.awaitTermination()
 
 
--------------------------------------------------------------------------------------- 
100 people.py 
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,Row
conf=SparkConf().setMaster('local').setAppName('a')
sc=SparkContext(conf=conf)
#spark的session对象
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()

#当前是rdd，还没有转换成dataframe
rdd1=sc.textFile("file:///home/hadoop/people.txt").map(lambda x:x.split(','))
#转换成row型，为了转dataframe
rdd2=rdd1.map(lambda x:Row(name=x[0],age=x[1]))
#rdd转dataframe
df1=spark.createDataFrame(rdd2)
df1.show()

#sql显示全部信息
df1.createOrReplaceTempView("people") 
df2=spark.sql("select * from people")
df2.show()

#dataframe转rdd
rdd3=df2.rdd.map(lambda x:x.name+","+str(x.age))
#rdd的方式显示信息
rdd3.foreach(print)

sc.stop()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
101_students.py 
from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession,Row
from pyspark.sql.types import *
conf=SparkConf().setMaster("local").setAppName('a')
sc=SparkContext(conf=conf)  #创rdd
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()  #创dataframe

#定义表头
schema=StructType([StructField('no',IntegerType(),True),\
    StructField('name',StringType(),True),\
    StructField('sex',StringType(),True),\
    StructField('age',IntegerType(),True),\
    StructField('dept',StringType(),True)])
rdd1=sc.textFile("file:///home/hadoop/students.txt")\
    .map(lambda x:x.split(' '))\
    .map(lambda x:Row(int(x[0]),x[1],x[2],int(x[3]),x[4]))  #有了表头因此不用字段名了
df1=spark.createDataFrame(rdd1,schema)  #前面数据，后面表头
df1.createOrReplaceTempView("students")
df2=spark.sql("SELECT * FROM students")
df2.show()
df2.groupBy("sex").count().show()
df2.select(df2['name']).show()
df2.filter(df2.age>20).show()
df2.groupBy("dept").count().show()
df2=df2.sort(df2.age.desc())
df2.show(n=5)

sc.stop()
spark.stop() 
 
--------------------------------------------------------------------------------------- 
