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