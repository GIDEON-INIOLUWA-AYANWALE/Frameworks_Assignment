# ============================================================================
# PART 4: STREAMLIT APPLICATION - CORD-19 Data Explorer
# ============================================================================
# Save this file as: app.py
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="CORD-19 Explorer",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure style
sns.set_style("whitegrid")

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_data():
    """Load cleaned data with caching"""
    try:
        df = pd.read_csv('cord19_cleaned.csv')
        df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("❌ Please run the analysis script first to generate 'cord19_cleaned.csv'")
        return None

# Load the data
df = load_data()

if df is not None:
    # ========================================================================
    # SIDEBAR - FILTERS AND NAVIGATION
    # ========================================================================
    
    st.sidebar.title("🔧 Controls & Filters")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Select a page:",
        ["📊 Dashboard", "🔍 Detailed Analysis", "📄 Data Sample"]
    )
    
    # Year filter
    min_year, max_year = int(df['year'].min()), int(df['year'].max())
    year_range = st.sidebar.slider(
        "Filter by Publication Year:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Journal filter
    all_journals = sorted(df['journal'].unique())
    selected_journals = st.sidebar.multiselect(
        "Filter by Journal(s):",
        all_journals,
        default=all_journals[:5] if len(all_journals) > 5 else all_journals
    )
    
    # Apply filters
    df_filtered = df[
        (df['year'] >= year_range[0]) & 
        (df['year'] <= year_range[1]) &
        (df['journal'].isin(selected_journals))
    ]
    
    st.sidebar.markdown("---")
    st.sidebar.metric("Filtered Papers", len(df_filtered))
    st.sidebar.metric("Total Papers", len(df))
    
    # ========================================================================
    # PAGE 1: DASHBOARD
    # ========================================================================
    
    if page == "📊 Dashboard":
        st.title("🦠 CORD-19 Research Explorer")
        st.markdown("Interactive analysis of COVID-19 research papers from the CORD-19 dataset")
        st.markdown("---")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Papers", f"{len(df_filtered):,}")
        with col2:
            st.metric("Unique Journals", df_filtered['journal'].nunique())
        with col3:
            st.metric("Years Covered", f"{int(df_filtered['year'].min())}-{int(df_filtered['year'].max())}")
        with col4:
            avg_words = df_filtered['abstract_word_count'].mean()
            st.metric("Avg Abstract Length", f"{avg_words:.0f} words")
        
        st.markdown("---")
        
        # Row 1: Publications over time
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Publications Over Time")
            papers_by_year = df_filtered['year'].value_counts().sort_index()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(papers_by_year.index, papers_by_year.values, 
                   marker='o', linewidth=2.5, markersize=8, color='#2E86AB')
            ax.fill_between(papers_by_year.index, papers_by_year.values, 
                            alpha=0.3, color='#2E86AB')
            ax.set_xlabel('Year', fontsize=11)
            ax.set_ylabel('Number of Papers', fontsize=11)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.subheader("🏆 Top 10 Publishing Journals")
            top_journals = df_filtered['journal'].value_counts().head(10)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            top_journals.plot(kind='barh', ax=ax, color='#A23B72')
            ax.set_xlabel('Number of Papers', fontsize=11)
            ax.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig)
        
        # Row 2: Sources and abstracts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Top Publishing Sources")
            top_sources = df_filtered['source'].value_counts().head(8)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            top_sources.plot(kind='bar', ax=ax, color='#F18F01')
            ax.set_ylabel('Number of Papers', fontsize=11)
            ax.set_xlabel('')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.subheader("📊 Abstract Word Count Distribution")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(df_filtered['abstract_word_count'].dropna(), 
                   bins=50, color='#C73E1D', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Word Count', fontsize=11)
            ax.set_ylabel('Frequency', fontsize=11)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            st.pyplot(fig)
    
    # ========================================================================
    # PAGE 2: DETAILED ANALYSIS
    # ========================================================================
    
    elif page == "🔍 Detailed Analysis":
        st.title("🔍 Detailed Analysis")
        st.markdown("---")
        
        # Word frequency in titles
        st.subheader("📝 Most Frequent Words in Paper Titles")
        
        all_words = []
        stop_words = {'a', 'the', 'and', 'or', 'of', 'in', 'to', 'for', 'with',
                     'is', 'on', 'at', 'by', 'from', 'as', 'an', 'be', 'this',
                     'that', 'are', 'have', 'has', 'was', 'were', 'been', 'covid',
                     'coronavirus', 'virus', 'sars', 'cov', '19', 'disease'}
        
        for title in df_filtered['title'].dropna():
            words = str(title).lower().split()
            for word in words:
                word = ''.join(c for c in word if c.isalnum())
                if word and word not in stop_words and len(word) > 3:
                    all_words.append(word)
        
        top_words = Counter(all_words).most_common(20)
        words, counts = zip(*top_words) if top_words else ([], [])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(range(len(words)), counts, color='#2E86AB')
        ax.set_yticks(range(len(words)))
        ax.set_yticklabels(words)
        ax.set_xlabel('Frequency', fontsize=11)
        ax.set_title('Top 20 Words in Paper Titles', fontsize=13, fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
        
        # Statistics section
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Publication Statistics")
            stats_data = {
                'Metric': [
                    'Total Papers',
                    'Unique Journals',
                    'Unique Authors',
                    'Avg Abstract Length',
                    'Min Abstract Length',
                    'Max Abstract Length'
                ],
                'Value': [
                    f"{len(df_filtered):,}",
                    f"{df_filtered['journal'].nunique():,}",
                    f"{df_filtered['authors'].notna().sum():,}",
                    f"{df_filtered['abstract_word_count'].mean():.0f} words",
                    f"{df_filtered['abstract_word_count'].min():.0f} words",
                    f"{df_filtered['abstract_word_count'].max():.0f} words"
                ]
            }
            st.table(pd.DataFrame(stats_data))
        
        with col2:
            st.subheader("🗓️ Year-wise Breakdown")
            year_stats = df_filtered['year'].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(year_stats.index, year_stats.values, color='#A23B72', alpha=0.8)
            ax.set_xlabel('Year', fontsize=11)
            ax.set_ylabel('Number of Papers', fontsize=11)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            st.pyplot(fig)
    
    # ========================================================================
    # PAGE 3: DATA SAMPLE
    # ========================================================================
    
    elif page == "📄 Data Sample":
        st.title("📄 Data Sample & Exploration")
        st.markdown("---")
        
        # Display options
        col1, col2 = st.columns(2)
        
        with col1:
            num_rows = st.slider("Number of rows to display:", 5, 50, 10)
        with col2:
            sort_by = st.selectbox("Sort by:", ['publish_time', 'abstract_word_count', 'journal'])
        
        # Display data
        df_display = df_filtered.sort_values(by=sort_by, ascending=False)[
            ['title', 'authors', 'journal', 'year', 'abstract_word_count']
        ].head(num_rows)
        
        st.dataframe(df_display, use_container_width=True)
        
        # Download option
        csv = df_display.to_csv(index=False)
        st.download_button(
            label="📥 Download Current View as CSV",
            data=csv,
            file_name="cord19_sample.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.subheader("🔎 Search Papers")
        
        search_term = st.text_input("Search in titles and abstracts:")
        if search_term:
            search_results = df_filtered[
                (df_filtered['title'].str.contains(search_term, case=False, na=False)) |
                (df_filtered['abstract'].str.contains(search_term, case=False, na=False))
            ][['title', 'authors', 'journal', 'year']]
            
            st.write(f"Found {len(search_results)} papers matching '{search_term}'")
            st.dataframe(search_results, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 12px;'>"
        "CORD-19 Data Explorer | Built with Streamlit | "
        "Data: Allen Institute for AI"
        "</div>",
        unsafe_allow_html=True
    )