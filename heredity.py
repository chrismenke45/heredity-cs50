import csv
import itertools
import sys

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

# COMMENTED CODE BELOW WAS USED TO CALCULATE JOINT_PROBS_TABLE, DOESNT NEED TO BE RAN EVERYTHIME
# pass_genes_probs_table = []
# def pass_gene_prob(gene_count):
#     if gene_count == 2:
#         return 1 - PROBS["mutation"]
#     elif gene_count == 1:
#         return 0.5
#     else: 
#         return PROBS["mutation"]
# for mother_gene_count in range(3):
#     pass_genes_probs_table.append([])
#     mother_pass_gene_prob = pass_gene_prob(mother_gene_count)
#     for father_gene_count in range(3):
#         pass_genes_probs_table[mother_gene_count].append([])
#         father_pass_gene_prob = pass_gene_prob(father_gene_count)
        
#         #add prob of child having 0 genes
#         pass_genes_probs_table[mother_gene_count][father_gene_count].append(round(((1 - mother_pass_gene_prob) * (1 - father_pass_gene_prob)), 4))
#         #add prob of child having 1 gene
#         pass_genes_probs_table[mother_gene_count][father_gene_count].append(round(((1 - mother_pass_gene_prob) * father_pass_gene_prob + (1 - father_pass_gene_prob) * mother_pass_gene_prob), 4))
#         #add prob of child having 2 genes
#         pass_genes_probs_table[mother_gene_count][father_gene_count].append(round((mother_pass_gene_prob * father_pass_gene_prob), 4))

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
    # Probability table to show chance of child have gene using indexing by mother's gene count, then father's gene count and then the child's gene count
    # Ex: Probability of child having 0 genes if the mother has 1 gene and the father has 2 genes: JOINT_PROBS_TABLE[1][2][0] == 0.005
    JOINT_PROBS_TABLE = [
        [
            [0.9801, 0.0198, 0.0001],
            [0.495, 0.5, 0.005],
            [0.0099, 0.9802, 0.0099]
        ],
        [
            [0.495, 0.5, 0.005],
            [0.25, 0.5, 0.25],
            [0.005, 0.5, 0.495]
        ],
        [
            [0.0099, 0.9802, 0.0099],
            [0.005, 0.5, 0.495],
            [0.0001, 0.0198, .9801]
        ]
    ]
    probability = 1
    for person in people:
        if person in two_genes:
            person_gene_count = 2
        elif person in one_gene:
            person_gene_count = 1
        else:
            person_gene_count = 0
        mother_gene_count = None
        father_gene_count = None
        if(people[person]["mother"]):
            if people[person]["mother"] in two_genes:
                mother_gene_count = 2
            elif people[person]["mother"] in one_gene:
                mother_gene_count = 1
            else:
                mother_gene_count = 0
        if(people[person]["father"]):
            if people[person]["father"] in two_genes:
                father_gene_count = 2
            elif people[person]["father"] in one_gene:
                father_gene_count = 1
            else:
                father_gene_count = 0
        if type(father_gene_count) == int and type(mother_gene_count) == int:
            person_gene_prob = JOINT_PROBS_TABLE[mother_gene_count][father_gene_count][person_gene_count]
        else:
            person_gene_prob = PROBS["gene"][person_gene_count]
        probability *= person_gene_prob
        probability *= PROBS["trait"][person_gene_count][person in have_trait]
    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # print(probabilities)
    for person in probabilities:
        gene_total = sum(probabilities[person]["gene"].values())
        for gene_count in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_count] /= gene_total

        trait_total = sum(probabilities[person]["trait"].values())
        for trait_bool in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait_bool] /= trait_total


if __name__ == "__main__":
    main()
