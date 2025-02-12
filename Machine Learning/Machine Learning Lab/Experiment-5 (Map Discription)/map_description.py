# Total records in the dataset
totalRecords = 10

# Unconditional probability of 'golf'
numberGolfRecreation = 4
probGolf = numberGolfRecreation / totalRecords
print("Unconditional probability of golf: {}".format(probGolf))

# Conditional probability of 'single' given 'medRisk' using Bayes' theorem
# P(single | medRisk) = P(medRisk ∩ single) / P(medRisk)

numberMedRiskSingle = 2  # Instances where both 'medRisk' and 'single' occur
numberMedRisk = 3  # Total occurrences of 'medRisk'

# Probabilities
probMedRiskSingle = numberMedRiskSingle / totalRecords
probMedRisk = numberMedRisk / totalRecords

# Conditional probability calculation
conditionalProbability = probMedRiskSingle / probMedRisk

print("Conditional probability of single given medRisk: {}".format(conditionalProbability))
