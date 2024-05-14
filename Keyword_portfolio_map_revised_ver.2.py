# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna(how='all')
    return data

def calculate_growth_and_share(data):
    data['Upload_Date'] = pd.to_datetime(data['Upload_Date'], utc=True)
    data['Quarter'] = data['Upload_Date'].dt.to_period('Q')
    data['Keyword_Frequency'] = data['Keyword'].astype(str).fillna('').apply(lambda x: len(x.split(',')))
    
    keyword_metrics = {}
    year_keywords = [kw.strip().lower() for kws in data['Keyword'].astype(str).fillna('') for kw in kws.split(',') if kw.strip()]
    year_keyword_counts = pd.Series(year_keywords).value_counts()
    year_total_frequency = year_keyword_counts.sum()
    
    for quarter, group in data.groupby('Quarter'):
        quarter_keywords = [kw.strip().lower() for kws in group['Keyword'].astype(str).fillna('') for kw in kws.split(',') if kw.strip()]
        quarter_keyword_counts = pd.Series(quarter_keywords).value_counts()
        
        for keyword, count in quarter_keyword_counts.items():
            if keyword not in keyword_metrics:
                keyword_metrics[keyword] = []
            
            share = year_keyword_counts[keyword] / year_total_frequency if keyword in year_keyword_counts else 0
            keyword_metrics[keyword].append({
                'Quarter': quarter,
                'Keyword': keyword,
                'Frequency': count,
                'Share': share
            })
    
    quarterly_data = pd.DataFrame([metric for metrics in keyword_metrics.values() for metric in metrics])
    quarterly_data['Growth'] = quarterly_data.groupby('Keyword')['Frequency'].pct_change() * 100
    quarterly_data = quarterly_data.dropna(subset=['Growth'])
    
    keyword_growth_rates = quarterly_data.groupby('Keyword')['Growth'].mean()
    keyword_frequencies = quarterly_data.groupby('Keyword')['Frequency'].sum()
    
    keyword_portfolio = pd.DataFrame({
        'Keyword': keyword_growth_rates.index,
        'Growth': keyword_growth_rates,
        'Share': [keyword_metrics[kw][-1]['Share'] for kw in keyword_growth_rates.index],
        'Frequency': keyword_frequencies
    })
    
    growth_cutoff = keyword_portfolio['Growth'].mean()
    #growth_cutoff = keyword_portfolio['Growth'].median()
    share_cutoff = keyword_portfolio['Share'].mean()
    #share_cutoff = keyword_portfolio['Share'].median()
    
    keyword_portfolio['Label'] = np.where(
        (keyword_portfolio['Growth'] >= growth_cutoff) & (keyword_portfolio['Share'] < share_cutoff),
        'Emerging',
        np.where(
            (keyword_portfolio['Growth'] >= growth_cutoff) & (keyword_portfolio['Share'] >= share_cutoff),
            'Hot',
            np.where(
                (keyword_portfolio['Growth'] < growth_cutoff) & (keyword_portfolio['Share'] >= share_cutoff),
                'Mature',
                'Niche'
            )
        )
    )
    
    return keyword_portfolio