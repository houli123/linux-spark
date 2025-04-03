from operator import gt
from pyspark import SparkContext, SparkConf

class SecondarySortKey():
    def __init__(self, k):
        self.column1 = k[0]
        self.column2 = k[1]

    def __gt__(self, other): 
        if other.column1 == self.column1:
            return gt(self.column2,other.column2)
        else:
            return gt(self.column1, other.column1)
def main():
    conf = SparkConf().setAppName('spark_sort').setMaster('local[1]')
    sc = SparkContext(conf=conf)
    file="file:///home/hadoop/file4.txt"
    rdd1 = sc.textFile(file)
    rdd2 = rdd1.filter(lambda x:(len(x.strip()) > 0))
    rdd3 = rdd2.map(lambda x:((int(x.split(" ")[0]),int(x.split(" ")[1])),x))
    rdd4 = rdd3.map(lambda x: (SecondarySortKey(x[0]),x[1]))
    rdd5 = rdd4.sortByKey(False)
    rdd6 = rdd5.map(lambda x:x[1])
    rdd6.foreach(print)

if __name__ == '__main__':
    main()
