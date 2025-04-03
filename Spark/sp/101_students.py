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