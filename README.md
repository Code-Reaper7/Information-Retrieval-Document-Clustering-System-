# Information-Retrieval-Document-Clustering-System-

1 - Install through terminal Terminal code : pip install scrapy PyPDF2 nltk scikit-learn requests numpy

2 - Crawl Spectrum Terminal code : scrapy crawl spectrum -O pdfLinks.json If needed to change number of pdfs to crawl add -a maxPdfs= E.g : scrapy crawl spectrum -O pdfLinks.json -a maxPdfs=300 Output : pdfLinks.json

3 -Inverted Index Terminal code : python indexer.py Output : docsFile.json, InvertedIndex.json

4 - Build Sustainability/Waste Collection Terminal code : python buildCollections.py Output : MyCollections.json

5 - Clustering Terminal code : python cluster.py Output : clusterEntireIndex.json,clusterMyCollection.json
