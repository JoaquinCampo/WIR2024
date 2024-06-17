# Sample data
data = [
    {'label': 'Neutral', 'score': 0.9},
    {'label': 'Neutral', 'score': 0.85},
    {'label': 'Neutral', 'score': 0.8},
    {'label': 'Neutral', 'score': 0.7},
    {'label': 'Neutral', 'score': 0.95},
    {'label': 'Neutral', 'score': 0.88},
    {'label': 'Neutral', 'score': 0.92},
    {'label': 'Negative', 'score': 0.6},
    {'label': 'Positive', 'score': 0.55},
    {'label': 'Neutral', 'score': 0.97}
]

# Assign numerical values to each label
label_values = {'Negative': 0, 'Neutral': 0.5, 'Positive': 1}

# Convert data to a list of dictionaries with numerical label values
for item in data:
    item['label_value'] = label_values[item['label']]

# Calculate the weighted average score
weighted_sum = sum(item['label_value'] * item['score'] for item in data)
total_weight = sum(item['score'] for item in data)
weighted_average = weighted_sum / total_weight

# Ensure the result is between 0 and 1
assert 0 <= weighted_average <= 1, "The weighted average is out of bounds!"

# Print the result
print(weighted_average)
