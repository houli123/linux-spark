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