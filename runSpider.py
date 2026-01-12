import os

print("\n===== Spectrum PDF Crawler =====")
limit = input("How many PDFs do you want to download? ")

# validate input
try:
    int(limit)
except ValueError:
    print("Invalid number. Please enter an integer.")
    exit()

output_file = f"spectrum_pdfs_{limit}.json"

cmd = f"scrapy crawl spectrumSpider -a limit={limit} -O {output_file}"

print(f"\nRunning: {cmd}\n")
os.system(cmd)