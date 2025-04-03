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