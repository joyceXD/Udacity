# Pre-requisite
library(ggplot2)
data("diamonds")

# ----------------------------------- 1 ---------------------------------------
# In this problem set, you'll continue to explore the diamonds data set.
# Your first task is to create a scatterplot of price vs x
# using the ggplot syntax.
# This assignment is not graded and will be marked as correct when you submit.
# =============================================================================
ggplot(data = diamonds, mapping = aes(x = x, y = price)) +
  geom_point() +
  labs(title = "Diamond data: price vs. x", x = "x", y = "price")

# ----------------------------------- 2 ---------------------------------------
# Findings: outliers such as when x is 0, and the relationship between x and
# price is exponential.

# ----------------------------------- 3 ---------------------------------------
# What is the correlation between price and x? 
# What is the correlation between price and y?
# What is the correlation between price and z?
# =============================================================================
cor(diamonds$x, diamonds$price)
cor(diamonds$y, diamonds$price)
cor(diamonds$z, diamonds$price)

# ----------------------------------- 4 ---------------------------------------
# Create a simple scatter plot of price vs depth.
# =============================================================================
ggplot(data = diamonds, mapping = aes(x = depth, y = price)) +
  geom_point() +
  ggtitle("Diamonds data: price vs. depth") +
  xlab("depth") +
  ylab("price")

# ----------------------------------- 5 ---------------------------------------
# Change the code to make the transparency of the
# points to be 1/100 of what they are now and mark
# the x-axis every 2 units. See the instructor notes
# for two hints.
# =============================================================================
ggplot(data = diamonds, mapping = aes(x = depth, y = price)) +
  geom_point(alpha = 1/100) +
  scale_x_continuous(breaks = seq(0, 100, by = 2))
  
  
# ----------------------------------- 6 ---------------------------------------
# Based on the scatter plot of depth vs. price, most diamonds are between what
# values of depth? 58~64
# =============================================================================

# ----------------------------------- 7 ---------------------------------------
# What's the correlation of depth vs. price? -0.0106474
# Based on the correlation coefficient would you use depth to predict the 
# price of a diamond? No. Because there is no strong correlation between the 
# two.
# =============================================================================

# ----------------------------------- 8 ---------------------------------------
# Create a scatterplot of price vs carat and omit the top 1% of price and carat
# values.
# =============================================================================
df <- diamonds[(diamonds$price < quantile(diamonds$price, 0.99) &
                 diamonds$carat < quantile(diamonds$carat, 0.99)), ]
ggplot(data = df, mapping = aes(x = carat, y = price)) +
  geom_point()

# ----------------------------------- 9 ---------------------------------------
# Create a scatterplot of price vs. volume (x * y * z).
# This is a very rough approximation for a diamond's volume.
# Create a new variable for volume in the diamonds data frame.
# =============================================================================
diamonds$volume <- diamonds$x * diamonds$y * diamonds$z
ggplot(data = diamonds, mapping = aes(x = volume, y = price)) +
  geom_point()

# ----------------------------------- 10 --------------------------------------
# What's the correlation of price and volume? Exclude diamonds that have a 
# volume of 0 or that are greater than or equal to 800.
# =============================================================================
df <- diamonds[(diamonds$volume != 0 & diamonds$volume < 800), ]
cor(df$volume, df$price)

# ----------------------------------- 11 --------------------------------------
# Subset the data to exclude diamonds with a volume
# greater than or equal to 800. Also, exclude diamonds
# with a volume of 0. Adjust the transparency of the
# points and add a linear model to the plot. (See the
# Instructor Notes or look up the documentation of
# geom_smooth() for more details about smoothers.)
# Do you think this would be a useful model to estimate
# the price of diamonds? Why or why not?
# =============================================================================

# ----------------------------------- 12 --------------------------------------
# =============================================================================

# ----------------------------------- 13 --------------------------------------
# =============================================================================

# ----------------------------------- 14 --------------------------------------
# =============================================================================

# ----------------------------------- 15 --------------------------------------
# =============================================================================

# ----------------------------------- 16 --------------------------------------
# =============================================================================
