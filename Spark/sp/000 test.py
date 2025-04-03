if __name__ == '__main__':
  from pyspark import SparkConf, SparkContext
  conf = SparkConf().setMaster("local").setAppName("My App")
  sc = SparkContext(conf = conf)
  # logFile = "file:///opt/apps/spark/README.md"
  # logData = sc.textFile(logFile, 2).cache()
  # numAs = logData.filter(lambda line: 'a' in line).count()
  # numBs = logData.filter(lambda line: 'b' in line).count()
  # print('Lines with a: %s, Lines with b: %s' % (numAs, numBs))
  
  sc.stop()