import random
import string

def generate_variants(seed_words, num_variants=10000):
    variants = set()
    
    while len(variants) < num_variants:
        # Select a random word from the seed list
        word = random.choice(seed_words)
        
        # Generate a variant by adding random numbers and letters
        variant = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1, 5))) + word
        
        variants.add(variant)
    
    return list(variants)

# Read seed words from file
with open('seed.txt', 'r') as file:
    seed_words = [line.strip() for line in file]

# Generate variants
variants = generate_variants(seed_words)

# Write variants to file
with open('variants.txt', 'w') as file:
    file.write('\n'.join(variants))
