import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    j={}
    
    if page =='':
        for p in corpus.keys():
           j[p]=1/len(corpus.keys())
        return j
    else:
        v1=damping_factor/(len(corpus[page]))
        v2=(1-damping_factor)/(len(corpus.keys()))
        for p in corpus[page]:
            j[p]=v1+v2

        for p in corpus.keys():
            if p not in j.keys():
                j[p]=v2
        return j


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    i=n
    dic={}
    page =random.choice(list(corpus.keys()))
    for key in corpus.keys():
        dic[key]=0
    while i>0:
        dic[page]+=1
        tran=transition_model(corpus,page,damping_factor)
        keys=list(tran.keys())
        values=list(tran.values())
        page = random.choices(keys, values, k=1)[0]
        i-=1
    for key in dic.keys():
        dic[key]/=n
    return dic
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dic={}
    for key in corpus.keys():
        dic[key]=1/len(corpus.keys())
    i={}
    for key in corpus.keys():
        i[key]=[]
    for key1 in corpus.keys():
        for key2 in corpus[key1]:
            i[key2].append(key1)

    # Define the damping factor
    d = damping_factor

    # Define the number of pages
    N = len(corpus)

    # Initialize the PageRank values to 1 / N
    pagerank = {}
    for page in corpus:
        pagerank[page] = 1 / N


    # Define a variable to store the difference between old and new PageRank values
    delta = 0

    # Define a threshold for convergence
    epsilon = 0.001

    # Repeat until convergence
    while True:
        # For each page, calculate its new PageRank using the formula
        new_pagerank = {}
        for page in corpus:
            new_pagerank[page] = (1 - d)/N + d * sum(pagerank[in_page] / len(corpus[in_page]) for in_page in i[page])
        
        # Update the PageRank values and calculate the difference
        delta = 0
        for page in corpus:
            delta += abs(new_pagerank[page] - pagerank[page])
            pagerank[page] = new_pagerank[page]
        
        # Check if the difference is below the threshold
        if delta < epsilon:
            break
    return new_pagerank
  


if __name__ == "__main__":
    main()
