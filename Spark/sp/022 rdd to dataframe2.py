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