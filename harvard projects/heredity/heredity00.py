import csv
import itertools
import sys
import sympy as sp

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)

    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    i0=zeroGene(people,two_genes,one_gene,have_trait)
    i1=oneGene(people,two_genes,one_gene,have_trait)
    i2=twoGene(people,two_genes,one_gene,have_trait)
    joint=i0*i1*i2
    return joint
    raise NotImplementedError


def oneGene(people,two_genes, one_gene, have_trait):
    join_list=[]
    sum=1
    for person in one_gene:
        if people[person]['father']==None and people[person]['mother']==None:
            personGen1=PROBS["gene"][1]
            if person in have_trait:
                personTrait=PROBS["trait"][1][True]
            else :
                personTrait=PROBS["trait"][1][False]
                
            join_list.append(personGen1)
            join_list.append(personTrait) 
        else:
            personGen1= 0.9802
            join_list.append(personGen1)
            if person in have_trait:
                personTrait=PROBS["trait"][1][True]
            else :
                personTrait=PROBS["trait"][1][False]
            join_list.append(personTrait)
            
    for i in range(len(join_list)):
        sum*=join_list[i]
    return sum

def zeroGene(people,two_genes, one_gene, have_trait):
    join_list=[]
    sum=1
    for person in people:
        if people[person]['father']==None and people[person]['mother']==None:
            if person not in two_genes and person not in one_gene:
                personGen0=PROBS["gene"][0]
                if person in have_trait:
                    personTrait=PROBS["trait"][0][True]
                else :
                    personTrait=PROBS["trait"][0][False]
                    
                join_list.append(personGen0)
                join_list.append(personTrait) 
        elif person not in two_genes and person not in one_gene:
            personGen0=PROBS["gene"][0]*PROBS["gene"][0]
            if person in have_trait:
                personTrait=PROBS["trait"][0][True]
            else :
                personTrait=PROBS["trait"][0][False]
                
            join_list.append(personGen0)
            join_list.append(personTrait)
    for i in range(len(join_list)):
        sum*=join_list[i]
    return sum

def twoGene(people,two_genes, one_gene, have_trait):
    join_list=[]
    sum=1
    for person in two_genes:
        if people[person]['father']==None and people[person]['mother']==None:
            personGen2=PROBS["gene"][2]
            if person in have_trait:
                personTrait=PROBS["trait"][2][True]
            else :
                personTrait=PROBS["trait"][2][False]
                
            join_list.append(personGen2)
            join_list.append(personTrait)
        else:
            if people[person]['father'] in two_genes and people[person]['mother'] in two_genes:
                personGen2=PROBS["gene"][2]*PROBS["gene"][2]
            elif people[person]['father'] in two_genes and people[person]['mother'] in one_gene:
                personGen2=PROBS["gene"][2]*PROBS["gene"][1]
            elif people[person]['father'] in one_gene and people[person]['mother'] in two_genes:
                personGen2=PROBS["gene"][1]*PROBS["gene"][2]
            elif people[person]['father'] in one_gene and people[person]['mother'] in one_gene:
                personGen2=PROBS["gene"][1]*PROBS["gene"][1]
            elif people[person]['father']not in one_gene and people[person]['father'] not in two_genes and people[person]['mother'] in one_gene:
                personGen2=0.01*PROBS["gene"][1]
            elif people[person]['father'] not in one_gene and people[person]['father'] not in two_genes and people[person]['mother'] in two_genes:
                personGen2=0.01*PROBS["gene"][2]
            elif people[person]['mother'] not in one_gene and people[person]['mother'] not in two_genes and people[person]['father'] in one_gene:
                personGen2=0.01*PROBS["gene"][1]
            elif people[person]['mother'] not in one_gene and people[person]['mother'] not in two_genes and people[person]['father'] in two_genes:
                personGen2=0.01*PROBS["gene"][2]
            elif people[person]['father'] not in one_gene and people[person]['father'] not in two_genes and people[person]['mother'] not in one_gene and people[person]['mother'] not in two_genes:
                personGen2=0.01*0.01
            join_list.append(personGen2)
            if person in have_trait:
                personTrait=PROBS["trait"][2][True]
            else :
                personTrait=PROBS["trait"][2][False]
            join_list.append(personTrait)
            
    for i in range(len(join_list)):
        sum*=join_list[i]
    return sum
                
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1]+=p   
        elif person in two_genes: 
            probabilities[person]["gene"][2]+=p
        else:
            probabilities[person]["gene"][0]+=p
              
        if person in have_trait:
            probabilities[person]["trait"][True]+=p
        else:
            probabilities[person]["trait"][False]+=p
            



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for p in probabilities:
        i = sp.Symbol('i') # define i as a symbol
        solution_gene = sp.solve(i * probabilities[p]['gene'][0] + i * probabilities[p]['gene'][1]+i*probabilities[p]['gene'][2] - 1, i) # solve for i
        solution_trait = sp.solve(i * probabilities[p]['trait'][True] + i * probabilities[p]['trait'][False] - 1, i) # solve for i
        probabilities[p]['trait'][True]*=solution_trait[0]
        probabilities[p]['trait'][False]*=solution_trait[0]
        
        for k in range(3):
            probabilities[p]['gene'][k]*=solution_gene[0]




'''dist_father = DiscreteDistribution({
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },


    # Mutation probability
    "mutation": 0.01
    })

# Create a Node object for the node 'rain' using Node
node_father = Node(dist_father, name='father')

dist_mather = DiscreteDistribution({
    "gene": {
        2: 0,
        1: 0,
        0: 0
    },


    # Mutation probability
    "mutation": 0.01
    })
node_mather = Node(dist_mather, name='mother')'''


if __name__ == "__main__":
    main()


""" if people[person]['father'] in two_genes and people[person]['mother'] in two_genes:
                personGen1=PROBS["gene"][2]*(1-PROBS["gene"][2])+PROBS["gene"][2]*(1-PROBS["gene"][2])
            elif people[person]['father'] in two_genes and people[person]['mother'] in one_gene:
                personGen1=PROBS["gene"][2]*(1- PROBS["gene"][1])+(1- PROBS["gene"][2])*PROBS["gene"][1]
            elif people[person]['father'] in one_gene and people[person]['mother'] in two_genes:
                personGen1=PROBS["gene"][2]*(1-PROBS["gene"][1])+(1-PROBS["gene"][2])*PROBS["gene"][1]
            elif people[person]['father'] in one_gene and people[person]['mother'] in one_gene:
                personGen1=PROBS["gene"][1]*(1-PROBS["gene"][1])+PROBS["gene"][1]*(1- PROBS["gene"][1])
            else:5"""