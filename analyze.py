print("🚀 Starting analyze.py...")
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

DATA_FOLDER = "data"

def load_all_data():
    """
    Load all CSV files and combine them
    """
    print("="*70)
    print("📂 LOADING DATA")
    print("="*70)
    
    all_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]
    
    if not all_files:
        print("❌ No CSV files found!")
        return None
    
    print(f"Found {len(all_files)} CSV files")
    
    dataframes = []
    for file in all_files:
        filepath = os.path.join(DATA_FOLDER, file)
        df = pd.read_csv(filepath)
        dataframes.append(df)
        print(f"  ✅ Loaded: {file} ({len(df)} records)")
    
    # Combine all data
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    print(f"\n📊 Total records: {len(combined_df)}")
    print("="*70)
    
    return combined_df

def basic_statistics(df):
    """
    Show basic statistics about the data
    """
    print("\n" + "="*70)
    print("📈 BASIC STATISTICS")
    print("="*70)
    
    print(f"\nTotal flights collected: {len(df)}")
    print(f"Collection period: {df['date'].min()} to {df['date'].max()}")
    print(f"Number of unique dates: {df['date'].nunique()}")
    
    print("\n--- Breakdown by Type ---")
    print(df['route_type'].value_counts())
    
    print("\n--- Top 10 Airlines ---")
    print(df['airline'].value_counts().head(10))
    
    print("\n--- Top Routes ---")
    print(df['route'].value_counts().head(10))
    
    print("\n--- Flight Status ---")
    print(df['status'].value_counts())

def analyze_domestic_vs_international(df):
    """
    Compare domestic and international flights
    """
    print("\n" + "="*70)
    print("🇺🇸🌍 DOMESTIC vs INTERNATIONAL COMPARISON")
    print("="*70)
    
    domestic = df[df['route_type'] == 'domestic']
    international = df[df['route_type'] == 'international']
    
    print(f"\n🇺🇸 Domestic Flights: {len(domestic)}")
    print(f"  - Unique routes: {domestic['route'].nunique()}")
    print(f"  - Unique airlines: {domestic['airline'].nunique()}")
    print(f"  - Top airline: {domestic['airline'].value_counts().index[0]}")
    
    print(f"\n🌍 International Flights: {len(international)}")
    print(f"  - Unique routes: {international['route'].nunique()}")
    print(f"  - Unique airlines: {international['airline'].nunique()}")
    print(f"  - Top airline: {international['airline'].value_counts().index[0]}")

def analyze_by_date(df):
    """
    Show how data changes by date
    """
    print("\n" + "="*70)
    print("📅 DAILY BREAKDOWN")
    print("="*70)
    
    daily_counts = df.groupby('date').size()
    
    print("\nFlights collected per day:")
    for date, count in daily_counts.items():
        print(f"  {date}: {count} flights")
    
    # Show if there are differences between days
    if len(daily_counts) > 1:
        print("\n📊 Day-to-day changes:")
        for i in range(1, len(daily_counts)):
            prev_date = daily_counts.index[i-1]
            curr_date = daily_counts.index[i]
            change = daily_counts.iloc[i] - daily_counts.iloc[i-1]
            print(f"  {prev_date} → {curr_date}: {change:+d} flights")

def create_visualizations(df):
    """
    Create basic charts
    """
    print("\n" + "="*70)
    print("📊 CREATING VISUALIZATIONS")
    print("="*70)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('DFW Flight Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Domestic vs International
    route_counts = df['route_type'].value_counts()
    axes[0, 0].pie(route_counts.values, labels=route_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0, 0].set_title('Domestic vs International Flights')
    
    # 2. Top 10 Airlines
    top_airlines = df['airline'].value_counts().head(10)
    axes[0, 1].barh(top_airlines.index, top_airlines.values, color='skyblue')
    axes[0, 1].set_xlabel('Number of Flights')
    axes[0, 1].set_title('Top 10 Airlines')
    axes[0, 1].invert_yaxis()
    
    # 3. Top Routes
    top_routes = df['route'].value_counts().head(8)
    axes[1, 0].bar(range(len(top_routes)), top_routes.values, color='coral')
    axes[1, 0].set_xticks(range(len(top_routes)))
    axes[1, 0].set_xticklabels(top_routes.index, rotation=45, ha='right')
    axes[1, 0].set_ylabel('Number of Flights')
    axes[1, 0].set_title('Top 8 Routes from DFW')
    
    # 4. Flights by Date
    daily_counts = df.groupby('date').size()
    axes[1, 1].plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2, markersize=8)
    axes[1, 1].set_xlabel('Date')
    axes[1, 1].set_ylabel('Number of Flights')
    axes[1, 1].set_title('Daily Flight Collection')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save the figure
    output_file = 'dfw_flight_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved as: {output_file}")
    
    # Show the plot
    plt.show()
    print("✅ Charts displayed!")

def main():
    """
    Main analysis function
    """
    print("\n" + "="*70)
    print("✈️  DFW FLIGHT DATA ANALYSIS")
    print("="*70)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    df = load_all_data()
    
    if df is None:
        print("No data to analyze!")
        return
    
    # Run analyses
    basic_statistics(df)
    analyze_domestic_vs_international(df)
    analyze_by_date(df)
    
    # Create visualizations
    create_visualizations(df)
    
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    main()

