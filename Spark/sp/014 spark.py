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