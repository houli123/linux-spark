from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession
spark=SparkSession.builder.config(conf=SparkConf()).getOrCreate()
df1=spark.read.json('file:///home/hadoop/people.json')
df1.createOrReplaceTempView("people")
#利用sql语句查询
df2=spark.sql("select * from people where age>19")
df2.show()
spark.stop()