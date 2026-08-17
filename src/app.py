import streamlit as st
import pandas as pd
import plotly.express as px
from parser import parse_screentime_csv
import os
import io
from datetime import date


st.set_page_config(page_title='iPhone Screen Time Dashboard', layout='wide')

st.title('📱 iPhone Screen Time Dashboard')

# Load your_screentime.csv automatically
data_path = os.path.join(os.path.dirname(__file__), '..', 'sample_data', 'your_screentime.csv')
df, _ = parse_screentime_csv(data_path)

if df is not None:
    # Normalize date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Date range selector
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    with st.sidebar:
        st.header('Filters')
        date_range = st.date_input('Date range', value=[min_date, max_date])
        if isinstance(date_range, tuple) or isinstance(date_range, list):
            start_date, end_date = date_range[0], date_range[1]
        else:
            start_date = date_range
            end_date = date_range

        # Top N and app filters
        top_n = st.slider('Top N apps to display', min_value=3, max_value=50, value=10)

        overall_by_app = df.groupby('app', as_index=False)['minutes'].sum().sort_values('minutes', ascending=False)
        default_apps = overall_by_app['app'].head(top_n).tolist()
        selected_apps = st.multiselect('Apps to include', options=sorted(df['app'].unique()), default=default_apps)

    # Filter dataframe
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    if selected_apps:
        mask = mask & df['app'].isin(selected_apps)
    df_filt = df.loc[mask].copy()

    # KPIs
    st.header('Overview')
    total_minutes = df_filt['minutes'].sum()
    total_hours = total_minutes / 60
    days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1
    avg_per_day = total_minutes / days if days > 0 else 0
    avg_hours_per_day = avg_per_day / 60
    top_app = None
    try:
        top_app = df_filt.groupby('app')['minutes'].sum().idxmax()
    except Exception:
        top_app = None

    k1, k2, k3 = st.columns(3)
    k1.metric('Total hours', f"{total_hours:.1f}")
    k2.metric('Avg hours / day', f"{avg_hours_per_day:.1f}")
    k3.metric('Top app', top_app or '-')

    # Charts
    st.header('📊 Analytics')
    
    # Top apps bar chart
    col1, col2 = st.columns(2)
    with col1:
        by_app = df_filt.groupby('app', as_index=False)['minutes'].sum().sort_values('minutes', ascending=False).head(top_n)
        by_app['hours'] = by_app['minutes'] / 60
        fig1 = px.bar(
            by_app, 
            y='app', 
            x='hours', 
            orientation='h',
            title='Top Apps by Total Hours',
            labels={'hours': 'Hours', 'app': 'App'},
            text='hours'
        )
        fig1.update_traces(textposition='outside', texttemplate='%{text:.1f}h', marker_color='#1f77b4')
        fig1.update_layout(
            hovermode='y unified',
            height=400,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    # Daily usage line chart
    with col2:
        over_time = df_filt.groupby(df_filt['date'].dt.date, as_index=False)['minutes'].sum()
        over_time.rename(columns={'date': 'day'}, inplace=True)
        over_time['day'] = pd.to_datetime(over_time['day'])
        over_time['hours'] = over_time['minutes'] / 60
        fig2 = px.line(
            over_time, 
            x='day', 
            y='hours',
            title='Daily Usage Trend',
            labels={'hours': 'Hours', 'day': 'Date'},
            markers=True
        )
        fig2.update_traces(line=dict(color='#1f77b4', width=3), marker=dict(size=8))
        fig2.update_layout(
            hovermode='x unified',
            height=400,
            yaxis_title='Hours',
            xaxis_title='Date'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Per-app trends
    st.subheader('📈 App Usage Over Time')
    if selected_apps:
        trend = df_filt.groupby([df_filt['date'].dt.date, 'app'], as_index=False)['minutes'].sum()
        trend.rename(columns={'date': 'day'}, inplace=True)
        trend['day'] = pd.to_datetime(trend['day'])
        trend['hours'] = trend['minutes'] / 60
        fig3 = px.line(
            trend, 
            x='day', 
            y='hours', 
            color='app',
            title='Individual App Usage Trends',
            labels={'hours': 'Hours', 'day': 'Date', 'app': 'App'},
            markers=True
        )
        fig3.update_layout(
            hovermode='x unified',
            height=450,
            yaxis_title='Hours',
            xaxis_title='Date'
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info('Select at least one app in the sidebar to see per-app trends.')

    # Data section
    st.header('📋 Data')
    st.subheader('Raw data (filtered)')
    st.dataframe(df_filt, use_container_width=True)

    # Download button
    csv = df_filt.to_csv(index=False)
    st.download_button('⬇️ Download filtered CSV', data=csv, file_name='screentime_filtered.csv', mime='text/csv')
