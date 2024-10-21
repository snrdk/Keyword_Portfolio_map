# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna(how='all')
    return data

def calculate_growth_and_share(data):
    data['Quarter'] = pd.to_datetime(data['Upload_Date']).dt.to_period('Q')
    
    keyword_quarterly_metrics = {}
    
    for quarter, group in data.groupby('Quarter'):
        quarter_keywords = [kw.strip().lower() for kws in group['Keyphrase'] for kw in kws.split(',') if kw.strip()]
        quarter_keyword_counts = pd.Series(quarter_keywords).value_counts()
        quarter_total_frequency = quarter_keyword_counts.sum()
        quarter_mean_frequency = quarter_total_frequency / len(quarter_keyword_counts)
        
        for keyword, count in quarter_keyword_counts.items():
            if keyword not in keyword_quarterly_metrics:
                keyword_quarterly_metrics[keyword] = []
            
            share_of_average = count / quarter_mean_frequency #share rate
            
            keyword_quarterly_metrics[keyword].append({
                'Quarter': quarter,
                'Keyword': keyword,
                'Frequency': count,
                'Relative share to average': share_of_average 
            })
    
    quarterly_growth = pd.DataFrame(
        [metric for metrics in keyword_quarterly_metrics.values() for metric in metrics]
    )
    
    quarterly_growth['Growth'] = quarterly_growth.groupby('Keyword')['Frequency'].pct_change() * 100 #growth rate
    
    # Remove rows with NaN growth
    quarterly_growth = quarterly_growth.dropna(subset=['Growth'])
    
    growth_cutoff = quarterly_growth['Growth'].mean()
    #growth_cutoff = quarterly_growth['Growth'].median()
    share_cutoff = quarterly_growth['Relative share to average'].mean()
    #share_cutoff = quarterly_growth['Relative share to average'].median()
    
    quarterly_growth['Quadrant'] = np.where(
        (quarterly_growth['Growth'] >= growth_cutoff) & (quarterly_growth['Relative share to average'] < share_cutoff),
        'Emerging',
        np.where(
            (quarterly_growth['Growth'] >= growth_cutoff) & (quarterly_growth['Relative share to average'] >= share_cutoff),
            'Hot',
            np.where(
                (quarterly_growth['Growth'] < growth_cutoff) & (quarterly_growth['Relative share to average'] >= share_cutoff),
                'Mature',
                'Niche'
            )
        )
    )
    
    return quarterly_growth
