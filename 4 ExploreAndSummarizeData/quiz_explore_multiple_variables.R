# Write code to create a new data frame,
# called 'pf.fc_by_age_gender', that contains
# information on each age AND gender group.

# The data frame should contain the following variables:

#    mean_friend_count,
#    median_friend_count,
#    n (the number of users in each age and gender grouping)

# Here is an example of the structure of your data frame. Your
# data values will be different. Note that if you are grouping by
# more than one variable, you will probably need to call the
# ungroup() function. 

#   age gender mean_friend_count median_friend_count    n
# 1  13 female          247.2953                 150  207
# 2  13   male          184.2342                  61  265
# 3  14 female          329.1938                 245  834
# 4  14   male          157.1204                  88 1201

# See the Instructor Note for two hints.
setwd("C:/Project/Udacity/4 ExploreAndSummarizeData")

# DO NOT DELETE THESE NEXT TWO LINES OF CODE
# ==============================================================
pf <- read.delim('./pseudo_facebook.tsv')
suppressMessages(library(dplyr))

# ENTER YOUR CODE BELOW THIS LINE.
# ==============================================================
pf.fc_by_age_gender <- pf %>% 
  filter(!is.na(gender)) %>%
  group_by(age, gender) %>% 
  summarise (mean_friend_count = mean(friend_count), 
             median_friend_count = median(friend_count),
             n = n()) %>%
  ungroup() %>%
  arrange(age)


# Create a line graph showing the
# median friend count over the ages
# for each gender. Be sure to use
# the data frame you just created,
# pf.fc_by_age_gender.

library(ggplot2)
ggplot(data = pf.fc_by_age_gender,
       aes(x = age, y = median_friend_count, group = gender, color = gender)) +
  geom_line()


#
library(reshape2)
pf.fc_by_age_gender.wide <- dcast(pf.fc_by_age_gender, age ~ gender, 
                                  value.var = 'median_friend_count')



