# ============================================================================
# CORD-19 Dataset Analysis - Part 1-3: Data Loading, Cleaning, and Analysis
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Configure plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# PART 1: DATA LOADING AND BASIC EXPLORATION
# ============================================================================

def load_and_explore_data(filepath):
    """Load dataset and perform initial exploration"""
    print("=" * 70)
    print("PART 1: DATA LOADING AND BASIC EXPLORATION")
    print("=" * 70)
    
    # Load the data
    df = pd.read_csv(filepath)
    print(f"\n✓ Data loaded successfully!")
    
    # DataFrame dimensions
    print(f"\nDataset Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Display first few rows
    print("\nFirst 3 rows:")
    print(df.head(3))
    
    # Data types
    print("\nData Types:")
    print(df.dtypes)
    
    # Missing values
    print("\nMissing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_info = pd.DataFrame({
        'Missing Count': missing,
        'Percentage': missing_pct
    })
    print(missing_info[missing_info['Missing Count'] > 0])
    
    # Basic statistics
    print("\nBasic Statistics (Numerical Columns):")
    print(df.describe())
    
    return df

# ============================================================================
# PART 2: DATA CLEANING AND PREPARATION
# ============================================================================

def clean_and_prepare_data(df):
    """Clean data and prepare for analysis"""
    print("\n" + "=" * 70)
    print("PART 2: DATA CLEANING AND PREPARATION")
    print("=" * 70)
    
    df_clean = df.copy()
    
    # Convert publish_time to datetime
    print("\nConverting publish_time to datetime...")
    df_clean['publish_time'] = pd.to_datetime(
        df_clean['publish_time'], 
        errors='coerce'
    )
    
    # Extract year from publication date
    print("Extracting publication year...")
    df_clean['year'] = df_clean['publish_time'].dt.year
    
    # Remove rows with no year information
    df_clean = df_clean.dropna(subset=['year'])
    df_clean['year'] = df_clean['year'].astype(int)
    print(f"✓ Rows after removing entries without year: {len(df_clean)}")
    
    # Create abstract word count
    print("Creating abstract word count...")
    df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').apply(
        lambda x: len(str(x).split())
    )
    
    # Fill missing journal names
    print("Filling missing journal names...")
    df_clean['journal'] = df_clean['journal'].fillna('Unknown')
    
    print(f"\n✓ Data cleaning complete! Final shape: {df_clean.shape}")
    
    return df_clean

# ============================================================================
# PART 3: DATA ANALYSIS AND VISUALIZATION
# ============================================================================

def perform_analysis(df_clean):
    """Perform data analysis and create visualizations"""
    print("\n" + "=" * 70)
    print("PART 3: DATA ANALYSIS AND VISUALIZATION")
    print("=" * 70)
    
    # Analysis 1: Papers by year
    print("\n--- Analysis 1: Publications by Year ---")
    papers_by_year = df_clean['year'].value_counts().sort_index()
    print(papers_by_year)
    
    # Analysis 2: Top journals
    print("\n--- Analysis 2: Top 10 Publishing Journals ---")
    top_journals = df_clean['journal'].value_counts().head(10)
    print(top_journals)
    
    # Analysis 3: Top sources
    print("\n--- Analysis 3: Top Publishing Sources ---")
    top_sources = df_clean['source'].value_counts().head(10)
    print(top_sources)
    
    # Analysis 4: Word frequency in titles
    print("\n--- Analysis 4: Most Frequent Words in Titles ---")
    all_words = []
    stop_words = {'a', 'the', 'and', 'or', 'of', 'in', 'to', 'for', 'with', 
                  'is', 'on', 'at', 'by', 'from', 'as', 'an', 'be', 'this', 
                  'that', 'are', 'have', 'has', 'was', 'were', 'been'}
    
    for title in df_clean['title'].dropna():
        words = str(title).lower().split()
        for word in words:
            # Remove punctuation and filter
            word = ''.join(c for c in word if c.isalnum())
            if word and word not in stop_words and len(word) > 3:
                all_words.append(word)
    
    top_words = Counter(all_words).most_common(15)
    print("Top 15 words:", top_words)
    
    # Create visualizations
    print("\n--- Creating Visualizations ---")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Visualization 1: Publications over time
    axes[0, 0].plot(papers_by_year.index, papers_by_year.values, 
                    marker='o', linewidth=2, markersize=8, color='#2E86AB')
    axes[0, 0].fill_between(papers_by_year.index, papers_by_year.values, 
                            alpha=0.3, color='#2E86AB')
    axes[0, 0].set_title('Publications by Year', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Year')
    axes[0, 0].set_ylabel('Number of Papers')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Visualization 2: Top journals
    top_journals.plot(kind='barh', ax=axes[0, 1], color='#A23B72')
    axes[0, 1].set_title('Top 10 Publishing Journals', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Number of Papers')
    axes[0, 1].invert_yaxis()
    
    # Visualization 3: Top sources
    top_sources.plot(kind='bar', ax=axes[1, 0], color='#F18F01')
    axes[1, 0].set_title('Top Publishing Sources', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Number of Papers')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Visualization 4: Top words in titles
    words, counts = zip(*top_words)
    axes[1, 1].barh(range(len(words)), counts, color='#C73E1D')
    axes[1, 1].set_yticks(range(len(words)))
    axes[1, 1].set_yticklabels(words)
    axes[1, 1].set_title('Top 15 Words in Paper Titles', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Frequency')
    axes[1, 1].invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('cord19_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Visualizations saved as 'cord19_analysis.png'")
    plt.show()
    
    return {
        'papers_by_year': papers_by_year,
        'top_journals': top_journals,
        'top_sources': top_sources,
        'top_words': top_words
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Load and explore
    df = load_and_explore_data('metadata.csv')
    
    # Clean and prepare
    df_clean = clean_and_prepare_data(df)
    
    # Analyze and visualize
    results = perform_analysis(df_clean)
    
    # Save cleaned data for Streamlit app
    df_clean.to_csv('cord19_cleaned.csv', index=False)
    print("\n✓ Cleaned data saved as 'cord19_cleaned.csv'")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)