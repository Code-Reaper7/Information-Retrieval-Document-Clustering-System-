import json

indexPath = "spectrum_index.json"          
mycollectionPath = "my_collection.json"



# 1. Load the inverted index


with open(indexPath, "r") as f:
    index = json.load(f)

print(f"Loaded index with {len(index)} terms.")



# 2. Helper: get postings

def docsForTerm(term: str, invIndex: dict) -> set:
    """Return set of doc IDs in which `term` appears."""
    return set(invIndex.get(term, []))


# 3. Define and run queries

sustainTerm = "sustain"
wasteTerms = ["wast", "wastag", "wasti", "wasteney"]

# Sustainability query
sustainDocs = docsForTerm(sustainTerm, index)

# Waste query (OR over waste stems)
wasteDocs = set()
for t in wasteTerms:
    wasteDocs |= docsForTerm(t, index)

# Intersection and union (My-collection)
bothDocs = sustainDocs & wasteDocs
myCollection = sorted(sustainDocs | wasteDocs)



# 4. Print stats for the report

print("\n=== Query stats ===")
print(f"Sustainability query term: {sustainTerm!r}")
print(f"Waste query terms: {', '.join(wasteTerms)}")

print(f"\nNumber of documents for sustainability: {len(sustainDocs)}")
print(f"Number of documents for waste:         {len(wasteDocs)}")
print(f"Number of documents in BOTH:           {len(bothDocs)}")
print(f"Size of My-collection (union):         {len(myCollection)}")



# 5. Save My-collection doc IDs


with open(mycollectionPath, "w") as f:
    json.dump(myCollection, f)

print(f"\nSaved My-collection doc IDs to: {mycollectionPath}")