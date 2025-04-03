# Load necessary libraries
library(ggplot2)
library(MASS)  # For LDA

# Read dataset from external CSV file
data <- read.csv("data.csv")

# Ensure only numeric columns are used for analysis
numeric_data <- data[sapply(data, is.numeric)]

# Principal Component Analysis (PCA)
pca_result <- prcomp(numeric_data, scale. = TRUE)
print(summary(pca_result))

# Linear Discriminant Analysis (LDA) - Assuming 'Class' is categorical
if ("Class" %in% colnames(data)) {
  lda_result <- lda(Class ~ ., data = data)
  print(lda_result)
}

# Correlation Matrix
cor_matrix <- cor(numeric_data)
print(cor_matrix)

# Regression Analysis - Assuming 'y' is dependent and rest independent
if ("y" %in% colnames(data)) {
  regression_model <- lm(y ~ ., data = data)
  print(summary(regression_model))
}

# Analysis of Variance (ANOVA) - Assuming 'group' is categorical
if ("group" %in% colnames(data)) {
  anova_result <- aov(y ~ group, data = data)
  print(summary(anova_result))
}
