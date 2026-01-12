# experiments_clustering.py

import json
import math
from collections import defaultdict

import numpy as np
from sklearn.cluster import KMeans

#  Paths to your files 
indexPath = "spectrum_index.json"
myCollectionPath = "my_collection.json"
pdfsPath = "spectrum_pdfs_1000.json"


# 1. Load data


def loadingIndexAndCollection():
    with open(indexPath, "r") as f:
        index = json.load(f)

    with open(myCollectionPath, "r") as f:
        docIds = json.load(f)

    with open(pdfsPath, "r") as f:
        pdfs = json.load(f)

    # Global number of documents 
    allDocuments = set()
    for postings in index.values():
        for d in postings:
            allDocuments.add(d)

    NumGlobal = len(allDocuments)
    NumLocal = len(docIds)

    print(f"Loaded index with {len(index)} terms.")
    print(f"Global docs in index: {NumGlobal}")
    print(f"Docs in My-collection: {NumLocal}")

    return index, docIds, pdfs, NumGlobal, NumLocal



# 2. Build a TF–IDF matrix from the inverted index
#    - We only use docs in My-collection
#    - TF is binary (term present/not present in doc)
#    - Two IDF are made global and local 

def tfIdfMatrix(index, myDocIds, NumGlobal, NumLocal, dfMode="global"):
    
    myDocSet = set(myDocIds)

    # Vocabulary = all terms that appear in at least one doc in My-collection
    vocab = []
    for term, postings in index.items():
        if myDocSet.intersection(postings):
            vocab.append(term)

    print(f"Vocabulary size (terms that appear in My-collection): {len(vocab)}")

    termToIndex = {t: j for j, t in enumerate(vocab)}
    docToRows = {doc_id: i for i, doc_id in enumerate(myDocIds)}

    # Preallocate dense matrix (54 x ~20k). This is fine in memory.
    X = np.zeros((len(myDocIds), len(vocab)), dtype=float)

    for term, postings in index.items():
        # Skip terms that are not in My-collection vocab
        if term not in termToIndex:
            continue

        j = termToIndex[term]

        # Docs from My-collection that contain this term
        DocsInMy = myDocSet.intersection(postings)
        if not DocsInMy:
            continue

        # Document frequency and IDF
        if dfMode == "global":
            df = len(postings)  # df over all docs in the index
            idf = math.log((NumGlobal + 1) / (df + 1)) + 1.0
        else:  # 'local'
            df = len(DocsInMy)  # df only within My-collection
            idf = math.log((NumLocal + 1) / (df + 1)) + 1.0

        # Binary TF: if term appears in doc, TF = 1
        for DocId in DocsInMy:
            i = docToRows[DocId]
            X[i, j] = idf

    # Optional: L2-normalize each document vector (row)
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    X = X / norms

    return X, vocab, myDocIds



# 3. K-means clustering and top terms


def runningKmeans(X, kValues=(2, 10, 20), randomState=0):
    results = {}
    for k in kValues:
        km = KMeans(n_clusters=k, random_state=randomState, n_init=10)
        labels = km.fit_predict(X)
        print(f"[INFO] k={k} -> inertia={km.inertia_:.4f}")
        results[k] = (km, labels)
    return results


def TopTerms(km, vocab, top_n=50):
   
    centers = km.cluster_centers_  # shape (k, n_terms)
    order = np.argsort(centers, axis=1)[:, ::-1]  # descending

    ClusterTerms = {}
    for cluster_id in range(centers.shape[0]):
        top_indices = order[cluster_id, :top_n]
        terms = [vocab[j] for j in top_indices]
        ClusterTerms[cluster_id] = terms
    return ClusterTerms


def printingSummary(k, labels, my_doc_ids, pdf_meta, cluster_terms, top_n_for_print=20):
    
    print("\n============================")
    print(f"   SUMMARY FOR k = {k}")
    print("============================")

    # Map cluster -> list of row indices
    clusterToRows = defaultdict(list)
    for row_idx, c in enumerate(labels):
        clusterToRows[c].append(row_idx)

    for clusId, rows in clusterToRows.items():
        print("\n----------------------------------------")
        print(f"Cluster {clusId}  |  size = {len(rows)}")
        print("----------------------------------------")

        # Top terms
        terms = cluster_terms[clusId][:top_n_for_print]
        print("Top terms (by TF–IDF weight):")
        print(", ".join(terms))

        # Example docs
        print("\nExample documents in this cluster:")
        for row_idx in rows[:3]:  # show up to 3 examples
            doc_id = my_doc_ids[row_idx]
            meta = pdf_meta[doc_id]
            pdf_url = meta.get("pdf_url", "")
            filename = pdf_url.split("/")[-1] if pdf_url else f"doc_{doc_id}.pdf"
            print(f"  doc_id={doc_id:3d}  |  {filename}")



# 4. Convenience helper: recompute and print query stats
#    (sustainability vs waste)


def docsForTerm(term, inv_index):
    return set(inv_index.get(term, []))


def printQueryStats(index, my_doc_ids):
    Sustain = "sustain"
    Waste = ["wast", "wastag", "wasti", "wasteney"]

    SustainDocs = docsForTerm(Sustain, index)
    wasteDocs = set()
    for t in Waste:
        wasteDocs |= docsForTerm(t, index)

    both = SustainDocs & wasteDocs
    union = SustainDocs | wasteDocs

    print("\n============================")
    print("   QUERY STATISTICS")
    print("============================")
    print(f"Sustainability docs       : {len(SustainDocs)}")
    print(f"Waste docs               : {len(wasteDocs)}")
    print(f"Docs returned by both    : {len(both)}")
    print(f"My-collection (union)    : {len(union)}")
    print(f"my_collection.json size  : {len(my_doc_ids)}")
    print("============================\n")



# 5. Main


def main(df_mode="global"):
    # 1) load data
    index, my_doc_ids, pdf_meta, N_global, N_local = loadingIndexAndCollection()

    # Optional: recompute & print stats for the queries
    printQueryStats(index, my_doc_ids)

    # 2) build TF-IDF matrix
    print(f"Building TF–IDF matrix using df_mode='{df_mode}' ...")
    X, vocab, my_doc_ids_ordered = tfIdfMatrix(
        index, my_doc_ids, N_global, N_local, dfMode=df_mode
    )

    # 3) run k-means
    k_values = (2, 10, 20)
    results = runningKmeans(X, kValues=k_values)

    # 4) for each k, print summary with top terms and example docs
    for k in k_values:
        km, labels = results[k]
        cluster_terms = TopTerms(km, vocab, top_n=50)
        printingSummary(k, labels, my_doc_ids_ordered, pdf_meta, cluster_terms)


if __name__ == "__main__":
    print("\n==============================")
    print(" Running GLOBAL DF ")
    print("==============================\n")
    
    main(df_mode="global")   # Required run

    print("\n\n==============================")
    print(" Running LOCAL DF  ")
    print("==============================\n")

    main(df_mode="local") 
