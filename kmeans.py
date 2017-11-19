from numpy import array
from math import sqrt
from pyspark import SparkContext
from random import randint
from pyspark.sql import SparkSession
from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark.mllib.feature import HashingTF, IDF

sc = SparkContext(appName="kmeans")  # SparkContext
#spark = SparkSession.builder.appName("kmeans").getOrCreate()
#sc = spark.sparkContext

#documents = sc.wholeTextFiles("/home/pipe/datasets/gutenberg/*.txt")
docs = sc.wholeTextFiles("/home/pipe/datasets/gutenberg/*.txt")
words = docs.values().map(lambda line: line.split(" "))

hashingTF = HashingTF()
tf = hashingTF.transform(words)
idf = IDF().fit(tf)
tfidf = idf.transform(tf)

k = randint(3,6)

clusters = KMeans.train(tfidf, k, maxIterations=10, initializationMode="random")

#clusters.save(sc, "/home/pipe/Downloads/target/org/apache/spark/PythonKMeansExample/KMeansModel5")
#sameModel = KMeansModel.load(sc, "/home/pipe/Downloads/target/org/apache/spark/PythonKMeansExample/KMeansModel5")

print(clusters.predict(tfidf).collect())
print("")

docsArray = docs.keys().collect()
clustersArray = clusters.predict(tfidf).collect()
for x in range(k):
    print "en el cluster " + str(x) +  " estan:"
    for j in range(clustersArray.__len__()):
        if clustersArray[j]==x:
            print docsArray[j]
    print("")