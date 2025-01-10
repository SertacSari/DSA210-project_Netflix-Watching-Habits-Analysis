# Netflix Watching Habits Analysis

## Description
This project analyzes my Netflix watching habits to identify patterns and trends over time. The primary focus is to investigate how my watching behavior changes during exam periods compared to regular times. Using my watching hours as the main data, the project aims to uncover insights about my routines and assess their alignment with my academic responsibilities.

## Hypothesis
My hypothesis is that my Netflix watching hours significantly decrease during exam periods, reflecting a shift in focus toward studying.

## Motivation
The motivation behind this project is twofold:
- To better understand how I balance my time between fun and studying.
- To assess whether my habits align with my goals for productivity, especially during critical periods like exams.
## Method
The analysis was conducted primarily in **Python** (with libraries such as `pandas`, `matplotlib`, `scipy`, and `sklearn`) to manage, visualize, and analyze the data. Additional tools like Excel were considered but not used. 

## Data Source
The primary data source for this project is my Netflix watching history, specifically the hours spent watching content over time. This data will be categorized and analyzed based on:
- Time periods (regular days vs. exam periods)
- Daily Watch Hours: Summed to assess total usage per day  
- Exam vs. Non-Exam: Comparison of means, plus statistical testing  

## Data Analysis Plan
1. **Data Cleaning**:
   - Imported and preprocessed Netflix data (converted timestamps, extracted watch duration in hours).  
   - Filtered by the profile of mine to focus on a single user’s data.

2. **Exploratory Data Analysis (EDA)**:
   - Generated line plots, histograms, and box plots to visualize overall trends in watch habits.  
   - Examined daily totals, quarterly (3-month) aggregates, and yearly box plots.

3. **Exam Period Analysis**:
   - Defined exam periods (from an academic calendar) and flagged days within those periods.  
   - Compared average daily watch hours in exam vs. non-exam days.

4. **Statistical Testing**:
   - Conducted a Welch’s t-test to check for significant differences in daily watch hours.
   - Found a p-value of **0.01**, indicating a statistically significant difference in watch hours between exam and non-exam periods.
   - 
5. **Machine Learning**  
   - **kMM (K-Means-like)**: A custom clustering approach to group days by watch hours and day of week.  
     - Showed how daily behavior clusters might vary (e.g., high weekend usage vs. low weekday usage).  
   - **KNN Regression**: Predicted daily watch hours from day of week (as a simple example).  
     - Compared actual vs. predicted watch hours to gauge model performance.

6. **Visualization**:
   - Created line charts for daily usage, histograms for distribution, 3-month aggregated plots, and box plots for yearly comparison.
   - Plotted KNN regression results (actual vs. predicted) and kMM cluster labels (using day_of_week & duration).
  
   ## Expected vs. Actual Outcome
   - **Expected**: That watch hours decrease significantly during exam periods.  
   - **Observed**: The t-test result (p-value = 0.01) supports the hypothesis that **Netflix watch hours do indeed decrease** during exam periods,    reinforcing the idea that studying displaces leisure time.

7. **Insights and Reflection**:
   - Understanding how Netflix usage changes with academic demands can inform better scheduling and possibly improve academic performance. 
8. **Expected Outcome**:
   - I expect to find clear patterns that show a decrease in Netflix watching hours during exam periods. These insights will help me evaluate how     well I manage my time and provide a basis for improving my habits.
9. ## Conclusion
   1. **Hypothesis Confirmation**: The statistically significant difference (p-value < 0.05) indicates we can **reject the null hypothesis** (no      difference). Exam periods show lower average Netflix hours, aligning with the original hypothesis.  
   2. **Time Management**: Insights confirm a shift in focus toward studying on exam days. This suggests current habits may be effectively            reducing entertainment time when needed.  
