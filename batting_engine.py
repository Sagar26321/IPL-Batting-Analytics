import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURATION ---
DATA_FILE = 'IPL_Ball_by_Ball_2008_2022.csv'
MIN_BALLS = 500

# --- FUNCTION 1: DATA PIPELINE ---
def generate_batting_profiles(file_path, min_balls_faced):
    """Ingests ball-by-ball data and returns advanced batting metrics."""
    print(f"[INFO] Ingesting dataset: {file_path}...")
    df = pd.read_csv(file_path)

    # Feature Engineering
    df['is_four'] = df['batsman_run'] == 4
    df['is_six'] = df['batsman_run'] == 6
    df['is_dot'] = df['batsman_run'] == 0

    # Aggregation
    stats = df.groupby('batter').agg(
        total_runs=('batsman_run', 'sum'),
        balls_faced=('ID', 'count'), 
        fours=('is_four', 'sum'),
        sixes=('is_six', 'sum'),
        dots=('is_dot', 'sum')
    ).reset_index()

    # Filtering & Calculations
    established = stats[stats['balls_faced'] >= min_balls_faced].copy()
    established['strike_rate'] = (established['total_runs'] / established['balls_faced']) * 100
    established['boundary_runs'] = (established['fours'] * 4) + (established['sixes'] * 6)
    established['boundary_dependency_%'] = (established['boundary_runs'] / established['total_runs']) * 100
    established['dot_ball_%'] = (established['dots'] / established['balls_faced']) * 100

    # Final Output Formatting
    leaderboard = established.sort_values(by='total_runs', ascending=False).head(10)
    display_cols = ['batter', 'total_runs', 'strike_rate', 'boundary_dependency_%', 'dot_ball_%']
    
    return leaderboard[display_cols].round(2).set_index('batter')

# --- FUNCTION 2: VISUALIZATION ---
def plot_batting_dna(df):
    """Generates a scatter matrix of Batting Profiles."""
    print("[INFO] Generating Batting DNA Matrix...")
    
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 8))
    
    sns.scatterplot(
        data=df, 
        x='dot_ball_%', 
        y='boundary_dependency_%', 
        size='strike_rate',
        sizes=(100, 500), 
        alpha=0.7,
        color='crimson'
    )

    for player, row in df.iterrows():
        plt.text(
            row['dot_ball_%'] + 0.2, 
            row['boundary_dependency_%'], 
            player, 
            fontsize=10, 
            fontweight='bold'
        )

    plt.title("IPL Batting DNA: Anchors vs. Explosive Hitters", fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Dot Ball Percentage (Higher = Stagnant)", fontsize=12)
    plt.ylabel("Boundary Dependency % (Higher = Boundary Reliant)", fontsize=12)
    
    plt.axvline(df['dot_ball_%'].mean(), color='grey', linestyle='--', alpha=0.5)
    plt.axhline(df['boundary_dependency_%'].mean(), color='grey', linestyle='--', alpha=0.5)

    plt.savefig('batting_dna_matrix.png', dpi=300, bbox_inches='tight')
    print("[SUCCESS] Chart saved as 'batting_dna_matrix.png' in the current folder!")

# --- EXECUTION ---
if __name__ == "__main__":
    # 1. Generate the data
    top_batters = generate_batting_profiles(DATA_FILE, MIN_BALLS)
    print("\n--- ADVANCED BATTING PROFILES (TOP 10 RUN SCORERS) ---\n")
    print(top_batters)
    
    # 2. Calling the plotting function
    plot_batting_dna(top_batters)