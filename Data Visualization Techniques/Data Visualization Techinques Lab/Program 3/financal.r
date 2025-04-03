# Load necessary libraries
library(ggplot2)
library(pheatmap)

# Read dataset from external CSV file
data <- read.csv("data.csv")

# Ensure only numeric columns are used for analysis
numeric_data <- data[sapply(data, is.numeric)]

# K-means Clustering (Assuming 3 clusters)
set.seed(123)  # For reproducibility
kmeans_result <- kmeans(numeric_data, centers = 3)
data$Cluster <- as.factor(kmeans_result$cluster)

# Plot histogram of a selected financial variable (e.g., "Stock_Price")
ggplot(data, aes(x = Stock_Price)) + 
  geom_histogram(binwidth = 5, fill = "steelblue", color = "black") +
  ggtitle("Stock Price Distribution") +
  xlab("Stock Price") +
  ylab("Frequency") +
  theme_minimal()

# Generate a heatmap of the correlation matrix
cor_matrix <- cor(numeric_data)
pheatmap(cor_matrix, main = "Correlation Heatmap")