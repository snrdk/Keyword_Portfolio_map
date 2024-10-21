# Keyword Portfolio Map

This project is a collection of Python scripts used to generate keyword portfolio maps. Each script classifies and visualizes keywords based on their growth rate and market share, inspired by the BCG Matrix (Henderson, 1970). The BCG Matrix categorizes businesses and technologies according to their relative market share and market growth rate. Similarly, this project maps keywords by comparing their growth rate and market share within a specific period.

## Contents

**Keyword portfolio**
<div align="center">
    <img src="https://github.com/user-attachments/assets/f6338085-0cab-4edd-a994-333009705f0b" alt="Untitled (2)" width="600"/>
</p>
</div>


The purpose of this task is to categorize the types of keywords. 

## Key Metrics

1. **Market Share**: The ratio of a specific keyword's frequency to the total frequency of all keywords in each quarter.  
   **Formula**:  
   $\text{GrowthRate}(k_i, t)=\displaystyle\frac{Value_t}{\text{Value}_{t_1}}\times100$

2. **Growth Rate**: The percentage change in a keyword's frequency compared to the previous quarter.  
   **Formula**:  
   $GrowthRate(k_i, t)=\displaystyle\frac{Value_t}{Value_{t-1}}\times100$  
   For frequency-based growth rate, $\text{Value}$ is defined as the frequency.

## Notation
- $\text{keyword}_{i}$: The i-th keyword
- $\text{t}$: The t-th quarter

  
## File Description

### 1. `Keyword_portfolio_map.py`
- Initial version of the keyword portfolio map generation script.
- Calculates keyword frequency and relative share per quarter.
- Classifies keywords into "Emerging", "Hot", "Mature", and "Niche" categories based on growth rate and relative share.

### 2. `Keyword_portfolio_map_revised_ver.2.py`
- Revised version of the keyword portfolio map generation script.
- Considers yearly keyword frequency and market share for calculations.
- Classifies keywords into "Emerging", "Hot", "Mature", and "Niche" categories based on growth rate and market share.

### 3. `Keyword_portfolio_map_revised_ver.3.py`
- Further revised version of the keyword portfolio map generation script.
- Handles missing values by replacing them with the previous quarter's values.
- Sets the growth rate to 0 when the current value is the same as the previous value.
- Calculates market share as a percentage.

### 4. `Keyword_portfolio_map_revised_ver.4.py`
- Improves the growth rate calculation logic from version 3.
- Calculates the average growth rate, total frequency, and most recent market share of keywords within the analysis period.

### 5. `Keyword_portfolio_map_revised_ver.5.py`
- The latest version of the keyword portfolio map generation script.
- Allows specifying the path of the input file directly.


## Requirements

- Python 3.x
- pandas
- numpy


## Pilot experiment result  
<div align="center">
    <img src="https://github.com/user-attachments/assets/a77c8c34-130a-42d5-ae5a-9ff34f09e4b6" alt="Untitled (3)" width="600"/>
</p>
</div>
|              | Median              |                  |         | Mean               |                  |         |
|--------------|---------------------|------------------|---------|--------------------|------------------|---------|
|              | Degree              | Betweenness       | Share   | Degree             | Betweenness       | Share   |
| Emerging     | 40                  | 43               | 54      | 40                 | 55               | 60      |
| Hot          | 58                  | 55               | 44      | 37                 | 22               | 17      |
| Mature       | 40                  | 43               | 54      | 42                 | 25               | 40      |
| Niche        | 58                  | 55               | 44      | 77                 | 94               | 79      |

- Among Mean and Median values, using Median as a basis can lead to a more robust distribution of results.

- The metric values generated in networks vary depending on the size of the network.
  - Centrality can vary depending on the search keyword (combination of search terms AND OR conditions), and as a result, the keyword's influence may appear differently in networks other than the one where the search was conducted.
  - The meaning of the metric changes depending on the search conditions, which affects the interpretation of the labeled data in the visualization.

- Issues with keyword mapping visualization and clustering:
  - When visualizing keyword metrics, there's often a problem where most keywords cluster together in a quadrant, making it difficult to interpret the scatter plot effectively.
