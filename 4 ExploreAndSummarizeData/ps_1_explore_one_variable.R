library(dplyr)
library(ggplot2)
library(plyr)
library(tidyr)

# load dataset
data(diamonds)

# look at the price distribution
hist(diamonds$price, breaks = 30)

# number of diamonds with price of 15000 or more
nrow(diamonds[diamonds$price >= 15000, ])

# price histogram by cut
ggplot(diamonds, aes(x=price))+
  geom_histogram()+
  facet_grid(~cut)+
  theme_bw()

# price summary by cut
ddply(diamonds, ~cut, summarise, 
      min=min(price), max=max(price), median=median(price))

# histogram of price by cut, with y axis free scale
qplot(x = price, data = diamonds) + facet_wrap(~cut, scales = "free")

# histogram of price per carat and facet it by cut. 
# adjust the bin width and transform the scale of the x-axis using log10.
ggplot(diamonds, aes(x=price/carat))+
  geom_histogram()+
  facet_grid(~cut, scales = "free")+
  scale_x_continuous(trans = "log10")+
  theme_bw()

# price summary by color
ddply(diamonds, ~color, summarise,
      quantile=matrix(quantile(price, probs=c(0.25,0.50,0.75)), ncol=3))

# price per Carat Box Plots by Color
ggplot(diamonds, aes(x=color, y=price/carat))+
  geom_boxplot()+
  theme_bw()

# weight of diamonds using frequency polygon
ggplot(diamonds, aes(carat)) +
  geom_histogram(stat = "bin", 
                 breaks=seq(0, 5, by = 0.01), 
                 binwidth = 0.01) +
  scale_y_continuous(breaks = seq(0, 12000, by = 1000))

#
