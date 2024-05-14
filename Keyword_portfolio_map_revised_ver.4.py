# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna(how='all')
    return data

def calculate_growth_and_share(data):
    data['Upload_Date'] = pd.to_datetime(data['Upload_Date'], utc=True)
    data['Quarter'] = data['Upload_Date'].dt.to_period('Q') #변경된 부분
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
    
    # missing value 처리 (전 분기값으로 대체)
    pivoted_data = quarterly_data.pivot_table(index='Keyword', columns='Quarter', values=['Frequency', 'Share'])
    pivoted_data = pivoted_data.sort_index(axis=1)
    pivoted_data['Frequency'] = pivoted_data['Frequency'].fillna(method='ffill', axis=1)
    pivoted_data['Share'] = pivoted_data['Share'].fillna(method='ffill', axis=1)
    
    quarterly_data = pivoted_data.reset_index().melt(id_vars='Keyword', var_name='Quarter', value_name='Value')
    quarterly_data = quarterly_data.drop_duplicates(subset=['Keyword', 'Quarter', 'Value'])
    quarterly_data = quarterly_data.reset_index(drop=True)
    
    frequency_data = quarterly_data[quarterly_data['Quarter'].str.contains('Frequency')]
    share_data = quarterly_data[quarterly_data['Quarter'].str.contains('Share')]
    frequency_data.columns = ['Keyword', 'Quarter', 'Frequency']
    share_data.columns = ['Keyword', 'Quarter', 'Share']
    frequency_data.loc[:, 'Quarter'] = frequency_data['Quarter'].str.replace('Frequency', '')
    share_data.loc[:, 'Quarter'] = share_data['Quarter'].str.replace('Share', '')

    frequency_data.loc[:, 'Frequency'] = frequency_data['Frequency'].fillna(0).astype(int)
    quarterly_data = pd.merge(frequency_data, share_data, on=['Keyword', 'Quarter'])
    
    # Growth 계산 시 이전 값과 동일한 경우 0으로 설정
    quarterly_data['Growth'] = quarterly_data.groupby('Keyword')['Frequency'].pct_change() * 100
    quarterly_data.loc[quarterly_data['Growth'].isin([np.inf, -np.inf]), 'Growth'] = 0
    quarterly_data['Share'] = quarterly_data['Share'] * 100 # Share 값을 백분율로 계산
    
    keyword_growth_rates = quarterly_data.groupby('Keyword')['Growth'].mean() #조회시점 내 평균 성장률
    keyword_frequencies = quarterly_data.groupby('Keyword')['Frequency'].sum() #빈도수 합계
    keyword_shares = quarterly_data.groupby('Keyword')['Share'].last() #조회시점 내 가장 최근 점유율
    
    keyword_portfolio = pd.DataFrame({
        'Keyword': keyword_growth_rates.index,
        'Growth': keyword_growth_rates,
        'Share': keyword_shares,
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
