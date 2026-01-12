# Information-Retrieval-Document-Clustering-System-

Install through terminal Terminal code : pip install scrapy PyPDF2 nltk scikit-learn requests numpy
Crawl Spectrum Terminal code : scrapy crawl spectrum -O pdfLinks.json If needed to change number of pdfs to crawl add -a maxPdfs= E.g : scrapy crawl spectrum -O pdfLinks.json -a maxPdfs=300 Output : pdfLinks.json
Inverted Index Terminal code : python indexer.py Output : docsFile.json, InvertedIndex.json
Build Sustainability/Waste Collection Terminal code : python buildCollections.py Output : MyCollections.json
Clustering Terminal code : python cluster.py Output : clusterEntireIndex.json,clusterMyCollection.json
