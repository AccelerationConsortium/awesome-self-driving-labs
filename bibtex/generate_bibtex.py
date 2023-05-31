import os
import urllib.request
import requests
import re

def download_and_write(filepath,outfile="readme.md"):
    """
    If we want to download upstream
    """
    # Create a file object to write the downloaded file to.
    with open(outfile, 'wb') as f:
        response = requests.get(fileurl, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
                                                                                                                    
def extract_dois(filepath,url=False):
    if url:
        outfile = download_and_write(filepath)
    else:
        outfile = filepath
        
    # Regular expression pattern for DOIs
    doi_pattern = r'\[.*?\]\((https?://doi\.org/[-._;()/:a-zA-Z0-9]+)\)'
    with open(outfile, 'r') as f:
        md_file_content = f.read()
        # Find all DOIs in the file
        matches = re.findall(doi_pattern, md_file_content, re.IGNORECASE)
        unique_dois = list(set(matches))

    return unique_dois


def generate_unique_citation_key(citation_key, existing_keys):
        """
    NOT TESTED/USED: Generate a unique citation key by appending letters in sequence if necessary.
    """
        new_key = citation_key
        suffix = ord('a')

        while new_key in existing_keys:
            new_key = f"{citation_key}{chr(suffix)}"
            suffix += 1

        return new_key


def update_citation_keys(bibtex_entries, bibtex_entry, citation_keys):
    """
    NOT TESTED/USED: Modifies `bibtex_entries` to ensure uniqueness in the list of BibTeX entries.
    """
    match = re.search(r'@(\w+){(\w+),', bibtex_entry)
    if match:
        entry_type, citation_key = match.groups()
        # Generate a unique citation key if there are duplicates
        if citation_key in citation_keys:
            citation_key = generate_unique_citation_key(citation_key, citation_keys)
            bibtex_entry = bibtex_entry.replace("@{}{{{}, ".format(entry_type, match.group(2)),
                                    "@{}{{{}, ".format(entry_type, citation_key))
            
        citation_keys.add(citation_key)
        
    return bibtex_entries.append(bibtex_entry)

def download_and_save_bibs(dois,bibname="references.bib"):

    #os.makedirs('bibtex', exist_ok=True)

    # Header to ask the server to return a BibTeX entry
    headers = {
        'Accept': 'application/x-bibtex',
    }
    
    bibtex_entries = []
    citation_keys = set()
    
    for doi in dois:
      print(doi)
      # Send the GET request
      req = urllib.request.Request(doi, headers=headers)
      with urllib.request.urlopen(req) as response:
          # Decode the BibTeX entry and append it to the list
          bibtex_entry = response.read().decode()

          # TODO: test/utlize
          #update_citation_keys(bibtex_entries, bibtex_entry, citation_keys)

          bibtex_entries.append(bibtex_entry)

    bibtex_string = "\n".join(bibtex_entries)
          
    with open(bibname, 'w') as f:
        f.write(bibtex_string)


if __name__ == '__main__':
    # Upstream URL.
    #filepath = 'https://raw.githubusercontent.com/sgbaird/awesome-self-driving-labs/main/readme.md'
    filepath = "../readme.md"
    unique_dois = extract_dois(filepath)
    download_and_save_bibs(unique_dois)
