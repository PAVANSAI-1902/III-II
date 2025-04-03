# Load necessary libraries
library(ggplot2)

# Read dataset from external CSV file
data <- read.csv("data.csv")

# Display first few rows of the dataset
head(data)

# Create a scatter plot (assuming 'x' and 'y' columns exist in dataset)
ggplot(data, aes(x = x, y = y)) +
  geom_point(color = "blue") +
  ggtitle("Scatter Plot of Data") +
  xlab("X Values") +
  ylab("Y Values") +
  theme_minimal()
