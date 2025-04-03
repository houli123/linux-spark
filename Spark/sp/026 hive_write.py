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