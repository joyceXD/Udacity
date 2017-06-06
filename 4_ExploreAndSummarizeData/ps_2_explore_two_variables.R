# Pre-requisite
library(ggplot2)
library(dplyr)
library(gridExtra)
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
# the price of diamonds? Why or why not? No, because the line is biased towards
# the outliers on the right hand side.
# =============================================================================
df <- diamonds[(diamonds$volume != 0 & diamonds$volume < 800), ]
ggplot(data = df, mapping = aes(x = volume, y = price)) +
  geom_point(alpha = 0.1) +
  geom_smooth(method = "lm")

# ----------------------------------- 12 --------------------------------------
# Use the function dplyr package to create a new data frame containing
# info on diamonds by clarity. Name the data frame diamondsByClarity
# The data frame should contain the following variables in this order.
#       (1) mean_price
#       (2) median_price
#       (3) min_price
#       (4) max_price
#       (5) n
# where n is the number of diamonds in each level of clarity.
# =============================================================================
diamondsByClarity <- summarise(group_by(diamonds, clarity), 
                               mean_price = mean(price),
                               median_price = median(price),
                               min_price = min(price),
                               max_price = max(price),
                               n = n())

# ----------------------------------- 13 --------------------------------------
# We've created summary data frames with the mean price
# by clarity and color. You can run the code in R to
# verify what data is in the variables diamonds_mp_by_clarity
# and diamonds_mp_by_color.
# Your task is to write additional code to create two bar plots
# on one output image using the grid.arrange() function from the package
# gridExtra.
# =============================================================================
diamonds_mp_by_clarity <- summarise(group_by(diamonds, clarity), 
                                    mean_price = mean(price))

diamonds_mp_by_color <- summarise(group_by(diamonds, color), 
                                  mean_price = mean(price))

p1 <- ggplot(data = diamonds_mp_by_clarity, mapping = aes(x = clarity,
                                                          y = mean_price)) +
  geom_col()

p2 <- ggplot(data = diamonds_mp_by_color, mapping = aes(x = color,
                                                          y = mean_price)) +
  geom_col()

grid.arrange(p1, p2, ncol = 2)

# ----------------------------------- 14 --------------------------------------
# What do you notice in each of the bar charts for mean price by clarity and 
# mean price by color?
# These trends seem to go against our intuition.
# Mean price tends to decrease as clarity improves. 
# The same can be said for color.
# =============================================================================

# ----------------------------------- 15 --------------------------------------
# The Gapminder website contains over 500 data sets with information about
# the world's population. Your task is to continue the investigation you did at the
# end of Problem Set 3 or you can start fresh and choose a different
# data set from Gapminder.
# If you're feeling adventurous or want to try some data munging see if you can
# find a data set or scrape one from the web.
# In your investigation, examine pairs of variable and create 2-5 plots that make
# use of the techniques from Lesson 4.
# =============================================================================
