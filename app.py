print("Starting app.py...")
from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64

app = Flask(__name__)

DATA_FOLDER = "data"

def load_all_data():
    """Load all CSV files and combine them"""
    all_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]
    
    if not all_files:
        return None
    
    dataframes = []
    for file in all_files:
        filepath = os.path.join(DATA_FOLDER, file)
        df = pd.read_csv(filepath)
        dataframes.append(df)
    
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

def create_chart_base64(fig):
    """Convert matplotlib figure to base64 string for HTML"""
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)
    return image_base64

@app.route('/')
def home():
    """Home page"""
    df = load_all_data()
    
    if df is None:
        return "<h1>No data available. Run flight_tracker.py first!</h1>"
    
    stats = {
        'total_flights': len(df),
        'domestic_flights': len(df[df['route_type'] == 'domestic']),
        'international_flights': len(df[df['route_type'] == 'international']),
        'total_airlines': df['airline'].nunique(),
        'total_routes': df['route'].nunique(),
        'date_range': f"{df['date'].min()} to {df['date'].max()}"
    }
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DFW Flight Tracker</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            .header {{
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }}
            .header h1 {{
                font-size: 48px;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .header p {{
                font-size: 20px;
                opacity: 0.9;
                margin-top: 10px;
            }}
            .nav {{
                display: flex;
                gap: 20px;
                justify-content: center;
                margin-bottom: 40px;
            }}
            .nav a {{
                background: white;
                color: #667eea;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                transition: transform 0.2s;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .nav a:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.2);
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .stat-number {{
                font-size: 48px;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }}
            .stat-label {{
                font-size: 16px;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .emoji {{
                font-size: 40px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✈️ DFW Flight Tracker</h1>
                <p>Real-time Flight Operations Intelligence System</p>
                <p style="font-size: 16px; opacity: 0.8;">Data Range: {stats['date_range']}</p>
            </div>
            
            <div class="nav">
                <a href="/domestic">🇺🇸 Domestic Flights</a>
                <a href="/international">🌍 International Flights</a>
                <a href="/overview">📊 Complete Overview</a>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="emoji">✈️</div>
                    <div class="stat-number">{stats['total_flights']}</div>
                    <div class="stat-label">Total Flights</div>
                </div>
                
                <div class="stat-card">
                    <div class="emoji">🇺🇸</div>
                    <div class="stat-number">{stats['domestic_flights']}</div>
                    <div class="stat-label">Domestic</div>
                </div>
                
                <div class="stat-card">
                    <div class="emoji">🌍</div>
                    <div class="stat-number">{stats['international_flights']}</div>
                    <div class="stat-label">International</div>
                </div>
                
                <div class="stat-card">
                    <div class="emoji">🏢</div>
                    <div class="stat-number">{stats['total_airlines']}</div>
                    <div class="stat-label">Airlines</div>
                </div>
                
                <div class="stat-card">
                    <div class="emoji">🛫</div>
                    <div class="stat-number">{stats['total_routes']}</div>
                    <div class="stat-label">Routes</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/domestic')
def domestic():
    """Domestic flights page"""
    df = load_all_data()
    domestic_df = df[df['route_type'] == 'domestic']
    
    # Create charts
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('🇺🇸 Domestic Flights Analysis', fontsize=16, fontweight='bold')
    
    # Chart 1: Top Airlines
    top_airlines = domestic_df['airline'].value_counts().head(10)
    axes[0, 0].barh(top_airlines.index, top_airlines.values, color='skyblue')
    axes[0, 0].set_xlabel('Number of Flights')
    axes[0, 0].set_title('Top 10 Airlines')
    axes[0, 0].invert_yaxis()
    
    # Chart 2: Routes
    routes = domestic_df['route'].value_counts()
    axes[0, 1].bar(range(len(routes)), routes.values, color='lightcoral')
    axes[0, 1].set_xticks(range(len(routes)))
    axes[0, 1].set_xticklabels(routes.index, rotation=45, ha='right')
    axes[0, 1].set_ylabel('Number of Flights')
    axes[0, 1].set_title('Flights by Route')
    
    # Chart 3: Status
    status = domestic_df['status'].value_counts()
    axes[1, 0].pie(status.values, labels=status.index, autopct='%1.1f%%', startangle=90)
    axes[1, 0].set_title('Flight Status Distribution')
    
    # Chart 4: Daily trends
    daily = domestic_df.groupby('date').size()
    axes[1, 1].plot(daily.index, daily.values, marker='o', linewidth=2, markersize=8, color='green')
    axes[1, 1].set_xlabel('Date')
    axes[1, 1].set_ylabel('Number of Flights')
    axes[1, 1].set_title('Daily Flight Count')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    chart_base64 = create_chart_base64(fig)
    
    stats = {
        'total': len(domestic_df),
        'airlines': domestic_df['airline'].nunique(),
        'routes': domestic_df['route'].nunique(),
        'top_airline': domestic_df['airline'].value_counts().index[0],
        'top_route': domestic_df['route'].value_counts().index[0]
    }
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Domestic Flights - DFW Tracker</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            .header {{
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }}
            .header h1 {{
                font-size: 42px;
                margin: 0;
            }}
            .back-btn {{
                display: inline-block;
                background: white;
                color: #667eea;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .stats {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                gap: 20px;
            }}
            .stat-item {{
                text-align: center;
            }}
            .stat-value {{
                font-size: 32px;
                font-weight: bold;
                color: #667eea;
            }}
            .stat-text {{
                color: #666;
                margin-top: 5px;
            }}
            .chart-container {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .chart-container img {{
                width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Home</a>
            
            <div class="header">
                <h1>🇺🇸 Domestic Flights Analysis</h1>
            </div>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{stats['total']}</div>
                    <div class="stat-text">Total Flights</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['airlines']}</div>
                    <div class="stat-text">Airlines</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['routes']}</div>
                    <div class="stat-text">Routes</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['top_airline']}</div>
                    <div class="stat-text">Top Airline</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['top_route'].split(' to ')[-1]}</div>
                    <div class="stat-text">Busiest Destination</div>
                </div>
            </div>
            
            <div class="chart-container">
                <img src="data:image/png;base64,{chart_base64}" alt="Domestic Charts">
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/international')
def international():
    """International flights page"""
    df = load_all_data()
    intl_df = df[df['route_type'] == 'international']
    
    # Create charts
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('🌍 International Flights Analysis', fontsize=16, fontweight='bold')
    
    # Chart 1: Top Airlines
    top_airlines = intl_df['airline'].value_counts().head(10)
    axes[0, 0].barh(top_airlines.index, top_airlines.values, color='lightgreen')
    axes[0, 0].set_xlabel('Number of Flights')
    axes[0, 0].set_title('Top 10 Airlines')
    axes[0, 0].invert_yaxis()
    
    # Chart 2: Routes
    routes = intl_df['route'].value_counts()
    axes[0, 1].bar(range(len(routes)), routes.values, color='gold')
    axes[0, 1].set_xticks(range(len(routes)))
    axes[0, 1].set_xticklabels(routes.index, rotation=45, ha='right')
    axes[0, 1].set_ylabel('Number of Flights')
    axes[0, 1].set_title('Flights by Route')
    
    # Chart 3: Status
    status = intl_df['status'].value_counts()
    axes[1, 0].pie(status.values, labels=status.index, autopct='%1.1f%%', startangle=90)
    axes[1, 0].set_title('Flight Status Distribution')
    
    # Chart 4: Daily trends
    daily = intl_df.groupby('date').size()
    axes[1, 1].plot(daily.index, daily.values, marker='o', linewidth=2, markersize=8, color='purple')
    axes[1, 1].set_xlabel('Date')
    axes[1, 1].set_ylabel('Number of Flights')
    axes[1, 1].set_title('Daily Flight Count')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    chart_base64 = create_chart_base64(fig)
    
    stats = {
        'total': len(intl_df),
        'airlines': intl_df['airline'].nunique(),
        'routes': intl_df['route'].nunique(),
        'top_airline': intl_df['airline'].value_counts().index[0],
        'top_route': intl_df['route'].value_counts().index[0]
    }
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>International Flights - DFW Tracker</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            .header {{
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }}
            .header h1 {{
                font-size: 42px;
                margin: 0;
            }}
            .back-btn {{
                display: inline-block;
                background: white;
                color: #11998e;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .stats {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                gap: 20px;
            }}
            .stat-item {{
                text-align: center;
            }}
            .stat-value {{
                font-size: 32px;
                font-weight: bold;
                color: #11998e;
            }}
            .stat-text {{
                color: #666;
                margin-top: 5px;
            }}
            .chart-container {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .chart-container img {{
                width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Home</a>
            
            <div class="header">
                <h1>🌍 International Flights Analysis</h1>
            </div>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{stats['total']}</div>
                    <div class="stat-text">Total Flights</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['airlines']}</div>
                    <div class="stat-text">Airlines</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['routes']}</div>
                    <div class="stat-text">Routes</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['top_airline']}</div>
                    <div class="stat-text">Top Airline</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['top_route'].split(' to ')[-1]}</div>
                    <div class="stat-text">Busiest Destination</div>
                </div>
            </div>
            
            <div class="chart-container">
                <img src="data:image/png;base64,{chart_base64}" alt="International Charts">
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/overview')
def overview():
    """Combined overview page"""
    df = load_all_data()
    
    # Create comparison chart
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('📊 Complete Overview - DFW Flight Operations', fontsize=16, fontweight='bold')
    
    # Chart 1: Domestic vs International
    type_counts = df['route_type'].value_counts()
    axes[0, 0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen'])
    axes[0, 0].set_title('Domestic vs International Split')
    
    # Chart 2: All Airlines
    top_airlines = df['airline'].value_counts().head(15)
    axes[0, 1].barh(top_airlines.index, top_airlines.values, color='coral')
    axes[0, 1].set_xlabel('Number of Flights')
    axes[0, 1].set_title('Top 15 Airlines (All Flights)')
    axes[0, 1].invert_yaxis()
    
    # Chart 3: All Routes
    top_routes = df['route'].value_counts().head(10)
    axes[1, 0].bar(range(len(top_routes)), top_routes.values, color='purple')
    axes[1, 0].set_xticks(range(len(top_routes)))
    axes[1, 0].set_xticklabels(top_routes.index, rotation=45, ha='right')
    axes[1, 0].set_ylabel('Number of Flights')
    axes[1, 0].set_title('Top 10 Routes')
    
    # Chart 4: Status breakdown
    status = df['status'].value_counts()
    colors_status = ['green', 'blue', 'orange', 'red', 'gray']
    axes[1, 1].bar(status.index, status.values, color=colors_status[:len(status)])
    axes[1, 1].set_ylabel('Number of Flights')
    axes[1, 1].set_title('Flight Status Overview')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    chart_base64 = create_chart_base64(fig)
    
    domestic_df = df[df['route_type'] == 'domestic']
    intl_df = df[df['route_type'] == 'international']
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Overview - DFW Flight Tracker</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            .header {{
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }}
            .header h1 {{
                font-size: 42px;
                margin: 0;
            }}
            .back-btn {{
                display: inline-block;
                background: white;
                color: #f5576c;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .comparison {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 30px;
            }}
            .comparison-card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .comparison-card h2 {{
                margin-top: 0;
                color: #f5576c;
            }}
            .stat-row {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }}
            .chart-container {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .chart-container img {{
                width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Back to Home</a>
            
            <div class="header">
                <h1>📊 Complete Flight Operations Overview</h1>
            </div>
            
            <div class="comparison">
                <div class="comparison-card">
                    <h2>🇺🇸 Domestic Operations</h2>
                    <div class="stat-row">
                        <span>Total Flights:</span>
                        <strong>{len(domestic_df)}</strong>
                    </div>
                    <div class="stat-row">
                        <span>Airlines:</span>
                        <strong>{domestic_df['airline'].nunique()}</strong>
                    </div>
                    <div class="stat-row">
                        <span>Routes:</span>
                        <strong>{domestic_df['route'].nunique()}</strong>
                    </div>
                    <div class="stat-row">
                        <span>Top Airline:</span>
                        <strong>{domestic_df['airline'].value_counts().index[0]}</strong>
                    </div>
                </div>
                
                <div class="comparison-card">
                    <h2>🌍 International Operations</h2>
                    <div class="stat-row">
                        <span>Total Flights:</span>
                        <strong>{len(intl_df)}</strong>
                    </div>
                    <div class="stat-row">
                        <span>Airlines:</span>
                        <strong>{intl_df['airline'].nunique()}</strong>
                    </div>
                    <div class="stat-row">
                        <span>Routes:</span>
                        <strong>{intl_df['route'].nunique()}</strong>
                    </div>
                    <div class="stat-row">
                        <span>Top Airline:</span>
                        <strong>{intl_df['airline'].value_counts().index[0]}</strong>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <img src="data:image/png;base64,{chart_base64}" alt="Overview Charts">
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("="*70)
    print("🌐 Starting DFW Flight Tracker Web Interface")
    print("="*70)
    print("\n📍 Open your browser and go to: http://127.0.0.1:5000")
    print("\n✈️ Available pages:")
    print("   - Home: http://127.0.0.1:5000/")
    print("   - Domestic: http://127.0.0.1:5000/domestic")
    print("   - International: http://127.0.0.1:5000/international")
    print("   - Overview: http://127.0.0.1:5000/overview")
    print("\n⚠️  Press CTRL+C to stop the server")
    print("="*70)
    print()
    
    app.run(debug=True, port=5001)