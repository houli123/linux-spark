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