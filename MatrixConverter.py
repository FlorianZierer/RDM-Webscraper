import numpy as np

# Sample data
article_quality = [5, 25, 5, 10, 15, 20, 10, 5, 25, 0]
num_articles = len(article_quality)

# Step 1: Create distance matrix
distance_matrix = np.zeros((num_articles, num_articles))
for i in range(num_articles):
    for j in range(i+1, num_articles):
        distance_matrix[i, j] = abs(article_quality[j] - article_quality[i])
        distance_matrix[j, i] = distance_matrix[i, j]

# Step 2: Extract upper triangle matrix
upper_triangle = distance_matrix[np.triu_indices(num_articles, 1)]

# Step 3: Convert upper triangle to vector
quality_vector = upper_triangle

print("Distance Matrix:")
print(distance_matrix)
print("\nUpper Triangle Matrix:")
print(upper_triangle)
print("\nQuality Representation Vector:")
print(quality_vector)