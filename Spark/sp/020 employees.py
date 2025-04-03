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