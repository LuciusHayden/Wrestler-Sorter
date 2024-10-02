import numpy as np
import json
#define the maximum difference between the normalized attributes of a pair of wrestlers that will be considered for pairing
#in other words, losen or tighten the requirments for a pair to be "recommended"
set_difference = 0.05 
groupSize = 6

#open the json file containing all the info on the wrestlers

with open("wrestlers.json", 'r') as f:
    wrestlers_data = json.load(f)


# define the wrestler class (all the attributes of the wrestler)
class Wrestler:
    def __init__(self, name, age, weight , experience):
        self.name = name
        self.age = age
        self.weight = weight
        self.experience = experience
    
#define the class that sorts the wrestlers
class WrestlerSorter:
    def __init__(self, wrestlers, weights):
        self.wrestlers = wrestlers
        self.pairs = []
        self.unrecommended_pairs = []
        self.weights = weights #decides what has a higher priority

#normalize the data so that the values are between 0 and 1
    def normalize(self):
        attributes = np.array([[w.age, w.experience, w.weight] for w in self.wrestlers])
        
        # Min-Max normalization
        self.normalized_attributes = (attributes - attributes.min(axis=0)) / (attributes.max(axis=0) - attributes.min(axis=0))
        
        # Combine normalized attributes with wrestler objects
        for i, wrestler in enumerate(self.wrestlers):
            wrestler.normalized = self.normalized_attributes[i]

 #weigh the values, this is because weight is probably more important than experience or age           
    
# pair the wrestlers with similar scores
    def pair_wrestlers(self):
        self.normalize()

        for wrestler in wrestlers:
            wrestler.weighted_normalized = np.dot(wrestler.normalized, self.weights)
        
        self.wrestlers.sort(key=lambda w: w.weighted_normalized)
        # self.wrestlers.sort(key=lambda w: sum(w.normalized))
       
        
        #for every wrestler in the data set sort them into groups of groupSize
        for i in range(0, len(self.wrestlers) - 1, groupSize-1):
            pair = self.wrestlers[i:i+groupSize+1]    
            diff = np.abs(pair[0].weighted_normalized - pair[1].weighted_normalized) #try and come up with a maximum difference between two wrestlers (unused)
            self.pairs.append(pair) #if the difference isnt to big then add the pair to the list of recommended pairs


        # Handle odd number of wrestlers by leaving the last one unpaired
        if len(self.wrestlers) % groupSize != 0:
            self.unpaired = self.wrestlers[-1]
        else:
            self.unpaired = None

#code for printing the pairs to the terminal
    def print_pairs(self):
        
        for pair in self.pairs:
            print(f"Pair:{pair[0].name} ({pair[0].age}, {pair[0].experience}, {pair[0].weight}) and "
                f"{pair[1].name} ({pair[1].age}, {pair[1].experience}, {pair[1].weight}) and "
                f"{pair[2].name} ({pair[2].age}, {pair[2].experience}, {pair[2].weight}) and "
                f"{pair[3].name} ({pair[3].age}, {pair[3].experience}, {pair[3].weight}) and "
                f"{pair[4].name} ({pair[4].age}, {pair[4].experience}, {pair[4].weight})")

        if self.unpaired:
            print(f"Unpaired: {self.unpaired.name}")

   
# name, age, weight , experience
wrestlers = []
#gets the data from the json file
for w in wrestlers_data:
    name = w['name']
    age = w['age']
    experience = w['experience']
    weight = w['weight']
    w = Wrestler(name, age, experience, weight)
    wrestlers.append(w)
 
# Create a WrestlerPairing object (second parameter is the weights (which attributes are most important))
pairing = WrestlerSorter(wrestlers, [0.1, 0.7, 0.2]) #age, experience, weight


# Pair the wrestlers
pairing.pair_wrestlers()

# Print the pairs
pairing.print_pairs()
    
