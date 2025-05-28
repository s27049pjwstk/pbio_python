#!/usr/bin/env python3
from Bio import Entrez
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import re

matplotlib.use('TkAgg')


class NCBIRetriever:

    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key
        Entrez.email = email
        Entrez.api_key = api_key
        Entrez.tool = 'BioScriptEx10'

    def search_taxid(self, taxid, minlen, maxlen):
        print(f"Searching for records with taxID: {taxid}")
        try:
            handle = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")
            records = Entrez.read(handle)
            organism_name = records[0]["ScientificName"]
            print(f"Organism: {organism_name} (TaxID: {taxid})")

            search_term = f"txid{taxid}[Organism]{minlen}:{maxlen}[SLEN]"
            handle = Entrez.esearch(
                db="nucleotide",
                term=search_term,
                usehistory="y"
            )
            search_results = Entrez.read(handle)
            count = int(search_results["Count"])
            if count == 0:
                print(f"No records found for {organism_name}")
                return None
            print(f"Found {count} records")

            self.webenv = search_results["WebEnv"]
            self.query_key = search_results["QueryKey"]
            self.count = count

            return count

        except Exception as e:
            print(f"Error searching TaxID {taxid}: {e}")
            return None

    def fetch_records(self, start=0, max_records=10):
        if not hasattr(self, 'webenv') or not hasattr(self, 'query_key'):
            print("No search results to fetch. Run search_taxid() first.")
            return []
        try:
            batch_size = min(max_records, 500)

            handle = Entrez.efetch(
                db="nucleotide",
                rettype="gb",
                retmode="text",
                retstart=start,
                retmax=batch_size,
                webenv=self.webenv,
                query_key=self.query_key
            )
            records_text = handle.read()
            return records_text

        except Exception as e:
            print(f"Error fetching records: {e}")
            return ""


def parse_genbank_records(records_text):
    sequences = records_text.strip().split('//')[:-1]
    parsed_records = []

    for sequence in sequences:
        accession = re.search(r"ACCESSION\s+(\S+)", sequence).group(1)
        length = int(re.search(r"LOCUS\s+\S+\s+(\d+)\s+bp", sequence).group(1))
        description = re.sub(r'\s+', ' ',
                             re.search(r"DEFINITION\s+(.+?)(?=\nACCESSION)", sequence, re.DOTALL).group(1).strip())
        parsed_records.append({
            'accession_number': accession,
            'seq_length': length,
            'seq_description': description
        })
    return parsed_records


def save_csv(records):
    if not records:
        print("No records to save.")
        return

    df = pd.DataFrame(records)
    df.to_csv("raport.csv", index=False)
    print(f"Saved {len(records)} records to raport.csv")


def create_graph(records):
    df = pd.DataFrame(records)
    df = df.sort_values('seq_length', ascending=False).reset_index(drop=True)

    plt.plot(
        range(len(df)),
        df['seq_length'],
        marker='o'
    )
    plt.xlabel('Accession Number')
    plt.ylabel('Sequence Length')
    plt.title('Descending graph of sequence length')

    plt.xticks(range(len(df)), df['accession_number'], rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig("graph.png")
    plt.show()

    print(f"Graph saved as graph.png")
    print("\nRecords summary (by length desc):")
    print(df[['accession_number', 'seq_length']])


def main():
    email = input("Enter your email address for NCBI: ")
    api_key = input("Enter your NCBI API key: ")
    taxid = input("Enter taxonomic ID (taxid) of the organism: ")
    min_seq_len = input("Enter min sequence length: ")
    max_seq_len = input("Enter max sequence length: ")

    retriever = NCBIRetriever(email, api_key)
    count = retriever.search_taxid(taxid, min_seq_len, max_seq_len)

    if not count:
        print("No records found. Exiting.")
        return
    print("\nFetching sample records...")
    sample_records = retriever.fetch_records(start=0, max_records=5)

    parsed_records = parse_genbank_records(sample_records)

    save_csv(parsed_records)
    create_graph(parsed_records)

    output_file = f"taxid_{taxid}_sample.gb"
    with open(output_file, "w") as f:
        f.write(sample_records)

    print(f"Saved sample records to {output_file}")


if __name__ == "__main__":
    main()
