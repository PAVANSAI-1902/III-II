# Load necessary libraries
library(ggplot2)

# Read dataset from external CSV file
data <- read.csv("data.csv")

# Remove non-numeric columns (if any)
numeric_data <- data[sapply(data, is.numeric)]

# Perform PCA (scale the data for better results)
pca_result <- prcomp(numeric_data, scale. = TRUE)

# Convert PCA results into a dataframe
pca_df <- as.data.frame(pca_result$x)

# Variance explained by each principal component
explained_variance <- (pca_result$sdev)^2
explained_variance_ratio <- explained_variance / sum(explained_variance)

# Create a dataframe for plotting
variance_df <- data.frame(
  Principal_Component = paste0("PC", 1:length(explained_variance_ratio)),
  Variance_Explained = explained_variance_ratio
)

# Plot bar graph of explained variance
ggplot(variance_df, aes(x = Principal_Component, y = Variance_Explained)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  ggtitle("Explained Variance by Principal Components") +
  xlab("Principal Component") +
  ylab("Variance Explained") +
  theme_minimal()
