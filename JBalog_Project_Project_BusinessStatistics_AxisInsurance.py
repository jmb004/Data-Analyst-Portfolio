#!/usr/bin/env python
# coding: utf-8

# # Objective 
# Post Graduate Program in Data Science and Business Analytics - Statistical Analysis of a fictious company, Axis Insurance, and their Claims Data.

# # Data background and contents

# **AxisInsurance.csv** - given by Post Graduate Program in Data Science and Business Analytics. Contains information about customers of a fictious company, Axis Insurance product and their claimants.

# ## Data Dictionary

# `Age` - This is an integer indicating the age of the primary beneficiary (excluding those above 64 years, since they are generally covered by the government).
# 
# `Sex` - This is the policy holder's gender, either male or female.
# 
# `BMI` - This is the body mass index (BMI), which provides a sense of how over or underweight a person is relative to their height. BMI is equal to weight (in kilograms) divided by height (in meters) squared. An ideal BMI is within the range of 18.5 to 24.9.
# 
# `Children` - This is an integer indicating the number of children/dependents covered by the insurance plan.
# 
# `Smoker` - This is yes or no depending on whether the insured regularly smokes tobacco.
# 
# `Region` - This is the beneficiary's place of residence in the U.S., divided into four geographic regions - northeast, southeast, southwest, or northwest.
# 
# `Charges` - Individual medical costs billed to health insurance

# # Define the problem and perform an Exploratory Data Analysis

# ### Problem definition

# Leveraging customer information is of paramount importance for most businesses. In the case of an insurance company, the attributes of customers like the ones mentioned below can be crucial in making business decisions. Hence, knowing to explore and generate value out of such data can be an invaluable skill to have. The problem is understanding who the claimants are and the statistical revelevance of the relationships between their attributes.

# ### Statistical Questions

# 1. Prove (or disprove) that the medical claims made by the people who smoke is greater than those who don't.
# 2. Prove (or disprove) with statistical evidence that the BMI of females is different from that of males.
# 3. Is the proportion of smokers significantly different across different regions?
# 4. Is the mean BMI of women with no children, one child and two children the same?

# # Exploratory Data Analysis

# ### Install & import modules and set coding rules

# In[1]:


# https://nbconvert.readthedocs.io/en/latest/install.html#installing-tex.

# Install needed libraries
get_ipython().system('pip3 install pandas_profiling')
get_ipython().system('pip install scipy==1.6.1')

# Import exporting utilities
import dataframe_image as dfi
get_ipython().system('pip install dataframe-image # for printing out tables')
get_ipython().system('pip install nbconvert # for printing to non-ipynb formats')
get_ipython().system('pip install nbconvert[webpdf]')

# Warning packages
import warnings
warnings.filterwarnings('ignore')

# Data analsys packages
import pandas as pd
import pandas_profiling
import numpy as np
from scipy import stats
from scipy.stats import mode

# Data visualization packages
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# check scipy version for using attributes of testing functions
import scipy
scipy.__version__


# ### Importing the dataset into Python & understanding the structure of the dataset

# In[421]:


df = pd.read_csv("AxisInsurance.csv") # import dataset and make a dataframe

pd.set_option('display.float_format', lambda x: '%.2f' % x) # To supress numerical display in scientific notations

# Set the juypter notebook viewer to show all rows when printing a series
pd.set_option('display.max_colwidth', 50000) 
pd.set_option('display.max_rows', 50000)


# In[249]:


# Create a copy of the dataframe
df = df.copy()


# In[250]:


# View top 5 rows of dataframe
df.head()


# In[6]:


# View bottom 5 rows of dataframe
df.tail()


# In[7]:


# View shape of the dataframe
df.shape


# In[8]:


# Find object types
df.dtypes


# In[9]:


# Check memory size
df.memory_usage().sum()/1000


# In[10]:


# Explore dataframe information, check dtype, and nulls.
df.info()


# In[11]:


# Adjust dtypes to work with all categories.
df[df.select_dtypes(['object']).columns] = df.select_dtypes(['object']).apply(lambda x: x.astype('category')) # convert dtypes to standard int64 or category


# In[12]:


# check dtype change
df.info()


# In[13]:


# 5 (Quantile) Statistics for numerical variables
df.describe()


# In[431]:


# Convert children to category for further analysis
df.children.astype('category')


# In[434]:


log_ch = np.log(df["charges"]).describe() # make a log of the numbers to make it closer to normal curve that depends on normal assumption


# In[439]:


sns.histplt(log_ch)


# In[14]:


# Basic statistics for Categorical variables
df.describe(include=["category"])


# In[440]:


# Function from GreatLearning on %'s for bar graphs
def per_on_bar(plot,feature):
    total = len(feature)
    for p in ax.patches:
        perc = '{:1.f}%'.format(100*p.get_height()/total)
        x = p.get_x() + p.get_width() / 2 - 0.05
        y = p.get_y() + g.get_height()
        ax.annotate(perc, (x,y), size=12)
    plt.show()


# In[15]:


# Subset the dataframe based on numeric and categorical types
numerical_features=df.select_dtypes(include=["int64","float64"])
global numerical_features
#type(numerical_features)


# In[16]:


categoricals=df.select_dtypes(include=["object", "category", "string"])
global categoricals
#type(categoricals)


# In[17]:


# Function to perform statistical analysis on every numeric and categorical variable in the dataframe
pd.set_option('display.max_colwidth', 5000)
def univar_num(dataframe): # argument is the whole dataframe
    
    # Print statistics for numeric variables
    print('Value counts of numeric features \n', numerical_features.value_counts()) # value counts of each feature
    print('\n Mode Analysis \n',numerical_features.mode()) # Mode (or most popular)
    print('\n Sum Analysis \n',numerical_features.sum()) # Sum analysis
    print('\n Variance analysis \n',numerical_features.var()) # Variance analysis
    print('\n Absolute Deviation or Mean Absolute Deviation \n',numerical_features.mad()) # Absolute Deviation or Mean Absolute Deviation
    print('\n  Skew analysis \n ',numerical_features.skew()) # Skew analysis
    
    # Print counts for categorical variables (df.describe(include=["category"]))
    print('\n Frequency for categorical features \n', [categoricals.apply(lambda x: x.value_counts())]) # Value counts of each feature
    #raise Exception("End to kill infinite loop") 
    
    return


# In[18]:


# Run dataframe through function
pd.set_option('display.max_colwidth', 5000)
univar_num(numerical_features)


# ### Univariate analysis

# In[19]:


# Frequency tables for every feature
for (column_name,column_data) in df.iteritems(): # for every column in the dataframe return the column name and Series of data
    display((column_name,column_data.value_counts()))


# In[259]:


# Function to create distribution and statistical plots for each numerical feature in the dataframe
def univar_vis(dataframe):
    
    sns.set(style="ticks")
    sns.set_style("darkgrid")
    
    for (column_name_c,column_data_c) in categoricals.iteritems():

        print(column_name_c, "Count Plot")
        plt.figure(figsize=(20,10))
        sns.countplot(x=column_data_c) # Bar plot against a numeric variable
        plt.show()

        print(column_name_c, "Distribution Plot")
        sns.displot(data = column_data_c) # distribution plot
        plt.figure(figsize=(20,10))
        plt.show()
    
    # Univariate visualization of numeric variables
    for (column_name,column_data) in numerical_features.iteritems():

        print(column_name, "Histogram") 
        sns.histplot(column_data, kde=True) #histogram
        plt.figure(figsize=(20,10))
        plt.show()

        print(column_name, "Distribution Plot")
        plt.figure(figsize=(20,10))
        sns.displot(data = column_data) # distribution plot
        plt.show()

        print(column_name, "Density Plot")
        sns.kdeplot(data=df, x=numerical_features[column_name]) # Kernel distribution
        plt.figure(figsize=(20,10))
        plt.show()

        print(column_name, "Box Plot")
        sns.boxplot(data = df, y = column_data) # Box plot
        plt.figure(figsize=(20,10))
        plt.show()
            

        #raise Exception("End to kill infinite loop") 
        
    return


# In[260]:


# Run dataframe through function
univar_vis(df)


# In[428]:


### Code from Mounika of GreatLearning as given in the Uber Case study ###

# While doing uni-variate analysis of numerical variables we want to study their central tendency 
# and dispersion.
# Let us write a function that will help us create boxplot and histogram for any input numerical 
# variable.
# This function takes the numerical column as the input and returns the boxplots 
# and histograms for the variable.
# Let us see if this help us write faster and cleaner code.
def histogram_boxplot(feature, figsize=(15,10), bins = None):
    """ Boxplot and histogram combined
    feature: 1-d feature array
    figsize: size of fig (default (9,8))
    bins: number of bins (default None / auto)
    """
    f2, (ax_box2, ax_hist2) = plt.subplots(nrows = 2, # Number of rows of the subplot grid= 2
                                           sharex = True, # x-axis will be shared among all subplots
                                           gridspec_kw = {"height_ratios": (.25, .75)}, 
                                           figsize = figsize 
                                           ) # creating the 2 subplots
    sns.boxplot(feature, ax=ax_box2, showmeans=True, color='red') # boxplot will be created and a star will indicate the mean value of the column
    sns.distplot(feature, kde=F, ax=ax_hist2, bins=bins) if bins else sns.distplot(feature, kde=False, ax=ax_hist2) # For histogram
    ax_hist2.axvline(np.mean(feature), color='g', linestyle='--') # Add mean to the histogram
    ax_hist2.axvline(np.median(feature), color='black', linestyle='-') # Add median to the histogram


# In[429]:


display(numerical_features.apply(lambda x: histogram_boxplot(x)))


# ### Bivariate analysis

# In[261]:


# Covariance analysis
df.cov()


# In[262]:


# Correlation Analysis
corr = df.corr()
print(corr)


# 

# In[443]:


# Plot the heatmap of correlations
plt.figure(figsize=(16,12))
display("Looking for anything close to one, anything above .8 is of interest.")
sns.heatmap(corr, annot=True,cmap='coolwarm',
        fmt=".1f",
     ### Categorical variables   xticklabels=corr.columns,
        yticklabels=corr.columns)


# In[441]:


sns.pairplot(df)
plt.show()


# In[400]:


# Bivariate visualization of categorical against numerical variables
def bi_var(dataframe):
    
    for (column_name_c,column_data_c) in categoricals.iteritems():
        
        for (column_name,column_data) in numerical_features.iteritems():
        
            print(column_name_c,"by",column_name, "Bar Plot")
            plt.figure(figsize=(15,10))
            sns.barplot(x=column_data_c, y=column_data) # Bar plot against a numeric variable
            plt.show()
        
            print(column_name_c,"by",column_name, "Box Plot")
            plt.figure(figsize=(15,10))
            sns.boxplot(data = df, x = column_data_c, y=column_data, palette="rainbow") # Box plot against a numeric variable
            plt.show()
            
            print(column_name_c,"by",column_name, "Strip Plot")
            plt.figure(figsize=(15,10))
            sns.stripplot(x=column_data_c, y=column_data) # Scatter plot against a numeric variable
            plt.show()
            
            print(column_name_c,"by",column_name, "Swarm Plot")
            sns.swarmplot(x=column_data_c, y=column_data) # Swarm plot against a numeric variable
            plt.figure(figsize=(15,10))
            plt.show()
            
    raise Exception("End to kill infinite loop")
    
    return


# In[401]:


bi_var(df)


# In[426]:


# Cross the categorical variables with charges and see the spread across the other categorical variables
for (column_name_c,column_data_c) in numerical_features.iteritems():
    for (column_name,column_data) in categoricals.iteritems():
        sns.histplot(x=column_data_c, y=df.charges, data=df, hue=column_name, multiple='stack',shrink=0.8)
        plt.figure(figsize=(20,20))
        plt.show()


# ### Key meaningful observations on individual variables and the relationship between variables

# `Age` - 
# * Claims data shows from age 18 - 64.
# * The most popular age is 18 years old.
# * Age is evenly distributed across categorical variables.
# 
# `Sex` - 
# * There are more Males present in the claims data than Females.
# * Males tend to have higher (more outliers) BMI than Females.
# * Males more total charges than Females.
# 
# 
# `BMI` - 
# * The average BMI is 30.66 which is above an ideal level.
# * The highest BMI of all claimants is 53.13 and most records come from non 
# * The distribution is nearly normalized.
# 
# 
# `Children` - 
# * Most claimants have no children.
# * There are more non-smokers with 0-5 children than smokers.
# * Children tend to live in the Southwest region.
# 
# 
# `Smoker` - 
# * There are more non-smokers than smokers in this sample.
# * Smokers charges are higher than non-smokers.
# * Smokers show a greater number of children reported.
# 
# 
# `Region` - 
# * The Southeast is over-represented in the sample.
# * The Southeast and Northeast have slightly higher mean charges.
# * The Southwest has the most claimants with 4 or 5 children.
# 
# 
# `Charges` -
# * 13,270 is the average claim charge.
# * Total charges for 1338 claims is 17,755,824.99.
# * More than 50% of charges are below 10k.

# ### Illustrate the insights based on EDA

# Our main insights were:
# 
#     1. There are no strong linear correlations (@95% CI) between Age, Charges, BMI, and # of Children.
#     
#     2. The addage applies: is there more in one category over another because there is in reality (population) or is in this data (sample)? I.e., The Southeast region and 0 Children shows stronger numbers but because it is over-represented in the sample.
#     
#     3. The bulk of the sample is of claimants who have charges below 30k and tend to be Male and Non-Smokers with a BMI range of 20-40. 

# # Statistical Analysis

# ## Assumptions

# 1. Level of significance (significance value or alpha) is 0.05 or a 95% Confidence Interval
# 2. The dataset is a simple random sample of the population.
# 3. The population standard deviation is not known to us.
# 4. The population is normally distributed.
# 5. The currency to be US dollars.

# ## T1. Prove (or disprove) that the medical claims made by the people who smoke is greater than those who don't.

# Is the mean of the charges where Smoker = "Yes" equal to or greater than the mean of the Smoker = "No"?

# ### Perform the hypothesis test

# 1. Is the sigma known or unknown?

# No, Sigma is unknown as the dataset is a random sample from the population. But we can look at the standard deviation for the the variable or feature of interest: charges and make that a 'sub-sample' std.

# In[359]:


# find the standard deviation for the sample (whole dataset) as s.
s = df.charges.std()
print("The sample standard deviation for 'charges' is" ,str(round(s,2)))


# 2. Is the sample size < or > 30?

# In[293]:


# Find the sample size
pop = len(df)
print("The sample sizes for this problem is",pop,".")


# The sample size is greater than 30 since we are looking at the whole sample (dataset).

# 3. Is the sample normally distributed?

# Samples are drawn from a normal distribution - Since the sample size is 1338 (which is > 30), Central Limit Theorem states that the distribution of sample means will be normal. If the sample size was less than 30, we would have been able to apply z test only if we knew that the population distribution was normal.  

# ### Hypothesis formulation

# Let $\mu$ be the mean medical claims made by the people who smoke.
# 
# The null hypothesis: mean medical claims (charges) made by the people who smoke is equal to those who don't.
# 
# >$H_0:\mu_1< or =\mu_2$  Ho = "Mean charges of smokers is less than or equal to non-smokers"
# 
# The alternate hypothesis:  
# 
# >$H_a:\mu_1>\mu_2$  Ha = "Mean charges of smokers is greater than non-smokers"

# ### Select the appropriate test

# Because the problem statement is framed as a "greater than" issue between a sub-sample of the sample as smokers and non-smokers, then we can use Two Sample (Independent) T-test for Equality of Means.
# 
# One-tailed T-test

# ### Let's test whether the T-test assumptions are satisfied or not
# 
# * Continuous data - Yes, the charges is measured on a continuous scale.
# * Normally distributed populations or Sample sizes > 30 - Since the sample sizes are greater than 30, Central Limit Theorem states that the distribution of sample means will be normal.
# * Independent populations - As we are taking random samples for two different type of smokers, the two samples are from two independent populations.
# * Unequal population standard deviations - As the sub-sample standard deviations are different, the population standard deviations may be assumed to be different.
# * Random sampling from the population - Yes, we are informed that the collected sample a simple random sample.
# 
# We can use two sample T-test for this problem.

# ### Data collection and preparation
# #### Collect Data

# In[137]:


# Isolate the feautres of interest into series
df_charges = df.charges
df_smoker = df.smoker


# In[445]:


df_smoker.value_counts()


# In[309]:


# Turn the categorical variable into a binary for numerical analysis
df_smoker_cat = df.smoker.astype('category').cat.codes


# In[358]:


# Calculate the mean of charges for all (total) smokers
x_bar1=df[df['smoker']=='yes']['charges'].mean()
print('The mean of charges for smoker group is ' + str(round(x_bar1, 2)))
# Calculate the mean of charges for all (total) non-smokers
x_bar2=df[df['smoker']=='no']['charges'].mean()
print('The mean of charges for non-smoker group is ' + str(round(x_bar2, 2)))

# Calculate the std of charges for all (total) smokers
s1=df[df['smoker']=='yes']['charges'].std()
print('The standard deviation of charges for smoker group is ' + str(round(s1, 2)))
# Calculate the std of charges for all (total) non-smokers
s2=df[df['smoker']=='no']['charges'].std()
print('The standard deviation of chargs for non-smoker group is ' + str(round(s2, 2)))


# #### Find the critical value

# In[139]:


# import the required function
from scipy.stats import norm

# find the critical value
critical_val = norm.ppf(1-.05)
critical_val


# Observation: The standard deviation for the sub-samples of charges for smokers to non-smokers are unequal.

# ### Visual analysis

# In[132]:


sns.boxplot(x="smoker", y="charges", data = df)
plt.grid()
plt.show()


# #### Set Level of Significance, 𝛂

# In[140]:


# Given in project
alpha_value = 0.05 # as the inverse of a 95% confidence interval


# #### Calculate Test Statistic 

# In[330]:


mu = df.charges.mean()
print("The sample mean for 'charges' is", str(round(mu,2)))


# In[342]:


# Calculate the sample size for smokers
sm = len(df[df['smoker']=='yes'])


# In[346]:


# Calculate the sample size for non-smokers
ns = len(df[df['smoker']=='no'])


# In[353]:


# Calculate the test statistic for smokers
test_stat1 = (x_bar1 - mu) / (s/np.sqrt(sm))
test_stat1


# In[354]:


# Calculate the test statistic for non-smokers
test_stat2 = (x_bar2 - mu) / (s/np.sqrt(ns))
test_stat2


# ### Find the p-value

# In[447]:


x = np.array(df[df['smoker']=='yes'].charges)
y = np.array(df[df['smoker']=='no'].charges)


# In[454]:


df[df['smoker']=='yes'].charges


# In[455]:


#  Independent t-test
from scipy.stats import ttest_ind

# find the p-value
# code taken originally from https://github.com/exploripy/exploripy#categorical-vs-target
# assumes unequal population variances
test_stat, p_value= stats.ttest_ind(x,y, alternative = 'greater') # same sample for both category's being tests so equal_var= True
print('One sample t test \nt statistic: {0} p value: {1} '.format(test_stat, p_value))


# ### Conclusion based on the p-value

# In[456]:


print('Level of significance: %.2f' %alpha_value)
if p_value < alpha_value: 
    print('We have evidence to reject the null hypothesis since p value {0} is less than the Level of significance'.format(p_value))
else:
    print('We have no evidence to reject the null hypothesis since p value {0} is greater than the Level of significance'.format(p_value)) 


# As the p-value (~4.13-283) is less than the level of significance, we can reject the null hypothesis. Hence, we do have enough evidence at 95% confidence (or 5% significance) to support the claim that medical claims (charges) made by the people who smoke is greater than those who don't. Therefore, we have evidence to support that charges for smokers are probably higher than for non-smokers.

# ## T2. Prove (or disprove) with statistical evidence that the BMI of females is different from that of males.

# ### Perform the hypothesis test

# 1. Is the sigma known or unknown?

# No, Sigma is unknown as the dataset is a random sample from the population.

# 2. Is the sample size < or > 30?

# In[293]:


# Find the sample size
pop = len(df)
print("The sample sizes for this problem is",pop,".")


# The sample size is greater than 30 since we are looking at the whole sample (dataset).

# 3. Is the sample normally distributed?

# Samples are drawn from a normal distribution - Since the sample size is 1338 (which is > 30), Central Limit Theorem states that the distribution of sample means will be normal. If the sample size was less than 30, we would have been able to apply z test only if we knew that the population distribution was normal.  

# ### Hypothesis formulation

# ### Let's write the null and alternative hypothesis
# Let $\mu$ be the mean bmi made by the Males and Females.
# 
# The null hypothesis: 
# 
# >$H_0:\mu_1 = \mu_2 -> \mu_1 - \mu_2 = 0$  Ho = "Mean BMI of Males is equal to Females."
# 
# 
# The alternate hypothesis:  
# 
# >$H_a:\mu_1 = \mu_2 -> \mu_1 - \mu_2= 0$  Ha = "Mean BMI of Males is not equal to Females."

# #### Set Level of Significance, 𝛂

# In[140]:


# Given in project
alpha_value = 0.05 # as the inverse of a 95% confidence interval


# ### Visual analysis

# In[397]:


sns.boxplot(x="sex", y="bmi", data = df)
plt.grid()
plt.show()


# ### Select the appropriate test

# #### Let's test whether the T-test assumptions are satisfied or not
# 
# * Continuous data - Yes, the BMI is measured on a continuous scale.
# * Normally distributed populations - Yes, it is assumed that the population is normally distributed.
# * Independent populations - As the two sets of sexes are two different expresions of sex, the populations are indepedent.
# * Random sampling from the population - Yes, we are informed that the collected sample is a simple random sample.
# 
# We can use a Two-Tail test for the Two Samples so we use a Two Sample (Independent) T-Test.

# ### Data collection and preparation

# In[457]:


df.sex.value_counts()


# In[372]:


# find the sample means and sample standard deviations for the two samples
print('The mean BMI of Male is ' + str(df[df['sex']=='male']['bmi'].mean()))
print('The mean BMI of Female is ' + str(df[df['sex']=='female']['bmi'].mean()))
print('The standard deviation of BMI of Male is ' + str(round(df[df['sex']=='male']['bmi'].std(),2)))
print('The standard deviation of BMI of Female is ' + str(round(df[df['sex']=='female']['bmi'].std(),2)))


# ### Find the p-value

# In[479]:


x = np.array(df[df.sex=="male"].bmi)
y = np.array(df[df.sex=="female"].bmi)

test_stat, p_value= stats.ttest_ind(x,y, alternative = 'greater')


# ### Conclusion based on the p-value

# In[480]:


print('Level of significance: %.2f' %alpha_value)
if p_value < alpha_value: 
    print('We have evidence to reject the null hypothesis since p value {0} is less than the Level of significance'.format(p_value))
else:
    print('We have no evidence to reject the null hypothesis since p value {0} is greater than the Level of significance'.format(p_value)) 


# As the p-value (~0.45) is greater than the level of significance, we cannot reject the null hypothesis. Hence, we do not have enough evidence to support the claim that there is unequal variance between the BMI of Male and Female claimants.

# ## T3. Is the proportion of smokers significantly different across different regions?

# ### Create a contingency table/cross tab, Use the function : stats.chi2_contingency

# ### Perform the hypothesis test

# 1. Is the sigma known or unknown?

# No, Sigma is unknown as the dataset is a random sample from the population.

# 2. Is the sample size < or > 30?

# In[293]:


# Find the sample size
pop = len(df)
print("The sample sizes for this problem is",pop,".")


# The sample size is greater than 30 since we are looking at the whole sample (dataset).

# 3. Is the sample normally distributed?

# Samples are drawn from a normal distribution - Since the sample size is 1338 (which is > 30), Central Limit Theorem states that the distribution of sample means will be normal. If the sample size was less than 30, we would have been able to apply z test only if we knew that the population distribution was normal.  

# ### Hypothesis formulation

# We will test the null hypothesis that the proportions (% spread) of smokers across regions are equal. Region has an effect on smoking habits.
# 
# >$H_0:$ Region has no effect on smoking habits.
# 
# against the alternate hypothesis
# 
# >$H_a:$ Region has an effect on smoking habits.

# #### Set Level of Significance, 𝛂

# In[140]:


# Given in project
alpha_value = 0.05 # as the inverse of a 95% confidence interval


# ### Visual analysis

# In[125]:


sns.countplot(df.region,data=df, hue=df.smoker)
plt.grid()
plt.show()


# ### Select the appropriate test

# In[298]:


# Calculate the std of smokers in all regions
df.region.value_counts("smoker").std()


# In[302]:


# Get percent in each categorical variable breakdown
df_smoker.groupby(df.region).value_counts("smoker")


# In[68]:


# Make a pseduo pivot table of region vs smoker
df_smoker.groupby(df.region).value_counts()


# #### Let's test whether the assumptions are satisfied or not for the Chi-Square Test for Independence
# 
# * Categorical variables - Yes
# * Expected value of the number of sample observations in each level of the variable is at least 5 - Yes, the number of observations in each level is greater than 5.
# * Random sampling from the population - Yes, we are assuming that the collected sample is a simple random sample.
# 
# Yes - all criteria are met for this test.
# 

# ### Data collection and preparation

# In[465]:


# create contingency table
cont = pd.crosstab(df.region,df.smoker)
cont


# In[468]:


pd.crosstab(df.region,df.smoker, normalize="index").plot(kind="bar", stacked=True, fig=(8.8))


# ### Find the p-value

# In[482]:


# import the required function
from scipy.stats import chi2_contingency

crosstab = pd.crosstab(df.region, df.smoker)

# find the p-value
chi, p_value, dof, expected = chi2_contingency(crosstab)
print(chi,"\n", dof,"\n","The expected frequencies, based on the marginal sums of the table.","\n", expected, "\n", 'The p-value is', p_value)


# ### Conclusion based on the p-value

# In[297]:


alpha_value = 0.05
print('Level of significance: %.2f' %alpha_value)
if p_value < alpha_value: 
    print('We have evidence to reject the null hypothesis since p value {0} is less than the Level of significance'.format(p_value))
else:
    print('We have no evidence to reject the null hypothesis since p value {0} is greater than the Level of significance'.format(p_value)) 


# As the p-value is greater than 0.05, we cannot reject the null hypothesis and assume that the variables ‘smoker' and 'region' are independent. So the proportion of smokers is the same. Region has no effect.

# ## T4. Is the mean BMI of women with no children, one child and two children the same? Explain your answer with statistical evidence.

# ### Perform the hypothesis test

# 1. Is the sigma known or unknown?

# No, Sigma is unknown as the dataset is a random sample from the population.

# 2. Is the sample size < or > 30?

# In[293]:


# Find the sample size
pop = len(df)
print("The sample sizes for this problem is",pop,".")


# The sample size is greater than 30 since we are looking at the whole sample (dataset).

# 3. Is the sample normally distributed?

# Samples are drawn from a normal distribution - Since the sample size is 1338 (which is > 30), Central Limit Theorem states that the distribution of sample means will be normal. If the sample size was less than 30, we would have been able to apply z test only if we knew that the population distribution was normal.  

# ### Hypothesis formulation

# Let $\mu_1, \mu_2, \mu_3$ be the means BMI of women with no children, one child and two children the same.
# 
# We will test the null hypothesis
# 
# >$H_0: \mu_1 = \mu_2 = \mu_3$ All of the means BMI of women with no children, one child and two children are the same.
# 
# against the alternative hypothesis
# 
# >$H_a: $ At least one of the means BMI of women with no children, one child and two children are not the same.
# 

# ### Visual analysis

# In[242]:


df.iloc[:,2:4].hist(figsize=(10,5))
plt.show()


# In[244]:


sns.boxplot(x="children", y="bmi", data=df)
plt.grid()
plt.show()


# ### Select the appropriate test

# ANOVA is used for testing more than 2 means.

# ### Data collection and preparation

# In[ ]:


# Get counts for each mean feature of interest
df_anova = df.loc[df['children'] < 3 ]


# In[ ]:


df_anova.describe()


# In[484]:


# look at the data to look for an indication of the answer (get an assumption) - get the means of sex and children by BMI (variable of interst)
df.groupby(["sex","children"])["bmi"].mean()


# ### Find the p-value

# In[485]:


#import the required function
from scipy.stats import f_oneway

zero = df[(df.sex=='female') & (df.children==0)]["bmi"]
one = df[(df.sex=='female') & (df.children==1)]["bmi"]
two = df[(df.sex=='female') & (df.children==2)]["bmi"]

# perform one-way anova test
test_stat, p_value = f_oneway(zero,one,two)
print('The p-value is ' + str(p_value))


# ### Conclusion based on the p-value

# In[486]:


print('Level of significance: %.2f' %alpha_value)
if p_value < alpha_value: 
    print('We have evidence to reject the null hypothesis since p value {0} is less than the Level of significance'.format(p_value))
else:
    print('We have no evidence to reject the null hypothesis since p value {0} is greater than the Level of significance'.format(p_value)) 


# As the p-value is much greater (~0.71) than the significance level, we can not reject the null hypothesis. Hence, we do not have enough statistical significance to conclude that all of the means BMI of women with no children, one child and two children are the same. Therefore, number of children has no effect on BMI, statistically speaking.

# # ---------------------------------------------**The End**-------------------------------------------------
