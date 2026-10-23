import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Set page layout
st.set_page_config(page_title="Chess Analytics Dashboard", layout="wide", initial_sidebar_state="expanded")

# Title and Description
st.title("♟️ Chess Game Dataset Explorer")
st.markdown("Explore, visualize, and analyze structural relationships, openings, and player ratings from your chess dataset.")

# Load Data
@st.cache_data
def load_data():
    # In a local app environment, place 'games.csv' in the same directory
    try:
        df = pd.read_csv('games.csv')
    except FileNotFoundError:
        try:
            df = pd.read_csv('/content/games.csv')
        except FileNotFoundError:
            # Generate dummy fallback data to keep app functional if missing
            st.warning("Dataset 'games.csv' not found. Using sample dummy data for demonstration.")
            df = pd.DataFrame({
                'id': [f'game_{i}' for i in range(100)],
                'rated': np.random.choice([True, False], 100),
                'turns': np.random.randint(10, 120, 100),
                'victory_status': np.random.choice(['mate', 'resign', 'draw', 'outoftime'], 100),
                'winner': np.random.choice(['white', 'black', 'draw'], 100),
                'white_rating': np.random.randint(900, 2400, 100),
                'black_rating': np.random.randint(900, 2400, 100),
                'opening_name': np.random.choice(["Sicilian Defense", "Scandinavian Defense", "French Defense", "Queen's Gambit"], 100)
            })
    df = df.drop_duplicates()
    return df

df = load_data()

# --- Sidebar Controls ---
st.sidebar.header("🎯 Filters & Parameters")

# Filter 1: Rated Games
rated_filter = st.sidebar.multiselect(
    "Game Type (Rated)",
    options=[True, False],
    default=[True, False],
    format_func=lambda x: "Rated" if x else "Unrated"
)

# Filter 2: Victory Status
victory_filter = st.sidebar.multiselect(
    "Victory Status",
    options=df['victory_status'].unique(),
    default=df['victory_status'].unique()
)

# Filter 3: Rating Slider
min_rating = int(min(df['white_rating'].min(), df['black_rating'].min()))
max_rating = int(max(df['white_rating'].max(), df['black_rating'].max()))
rating_range = st.sidebar.slider(
    "Player Rating Range",
    min_value=min_rating,
    max_value=max_rating,
    value=(min_rating, max_rating)
)

# Apply Filters to dataset
filtered_df = df[
    (df['rated'].isin(rated_filter)) &
    (df['victory_status'].isin(victory_filter)) &
    (df['white_rating'] >= rating_range[0]) & (df['white_rating'] <= rating_range[1]) &
    (df['black_rating'] >= rating_range[0]) & (df['black_rating'] <= rating_range[1])
]

# --- Main Tabs Layout ---
tab1, tab2, tab3 = st.tabs(["📊 Custom Visualizations", "🏆 Openings Analysis", "📋 Dataset Overview"])

# TAB 1: Custom Visualizations
with tab1:
    st.subheader("Custom Plot Generator")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Plot Options**")
        chart_type = st.selectbox(
            "Choose Chart Type",
            ["Scatter Plot", "Box Plot", "Histogram", "Bar Chart", "Heatmap"]
        )
        
        # Numeric & Categorical columns determination
        num_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = filtered_df.select_dtypes(include=['object', 'bool']).columns.tolist()
        
        # Select inputs depending on chart selection
        if chart_type in ["Scatter Plot"]:
            x_axis = st.selectbox("X-Axis (Numeric)", num_cols, index=num_cols.index('white_rating') if 'white_rating' in num_cols else 0)
            y_axis = st.selectbox("Y-Axis (Numeric)", num_cols, index=num_cols.index('black_rating') if 'black_rating' in num_cols else 0)
            color_by = st.selectbox("Color By", [None] + cat_cols)
        elif chart_type in ["Box Plot"]:
            x_axis = st.selectbox("Category X-Axis", cat_cols, index=cat_cols.index('victory_status') if 'victory_status' in cat_cols else 0)
            y_axis = st.selectbox("Value Y-Axis (Numeric)", num_cols, index=num_cols.index('turns') if 'turns' in num_cols else 0)
        elif chart_type in ["Histogram"]:
            x_axis = st.selectbox("Select Field", num_cols, index=num_cols.index('turns') if 'turns' in num_cols else 0)
            bins = st.slider("Number of Bins", 5, 100, 20)
        elif chart_type in ["Bar Chart"]:
            x_axis = st.selectbox("Categorical Field", cat_cols, index=cat_cols.index('winner') if 'winner' in cat_cols else 0)
        
        palette = st.selectbox("Color Palette", ["viridis", "coolwarm", "Set2", "magma", "muted"])
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_ready = True
        
        if chart_type == "Scatter Plot":
            sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, hue=color_by, palette=palette, alpha=0.6, ax=ax)
            ax.set_title(f"{x_axis.title()} vs {y_axis.title()} Colored by {color_by or 'None'}")
            
        elif chart_type == "Box Plot":
            sns.boxplot(data=filtered_df, x=x_axis, y=y_axis, palette=palette, hue=x_axis, legend=False, ax=ax)
            ax.set_title(f"Distribution of {y_axis.title()} across {x_axis.title()}")
            
        elif chart_type == "Histogram":
            sns.histplot(data=filtered_df, x=x_axis, bins=bins, kde=True, color='skyblue', ax=ax)
            ax.set_title(f"Distribution of {x_axis.title()}")
            
        elif chart_type == "Bar Chart":
            order = filtered_df[x_axis].value_counts().index
            sns.countplot(data=filtered_df, x=x_axis, order=order, palette=palette, hue=x_axis, legend=False, ax=ax)
            ax.set_title(f"Count Distribution of {x_axis.title()}")
            
        elif chart_type == "Heatmap":
            corr_matrix = filtered_df[num_cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap=palette, fmt=".2f", ax=ax)
            ax.set_title("Correlation Heatmap of Numerical Features")
            
        # Rendering the plot inside Streamlit
        st.pyplot(fig)
        
        # Export functionality
        fn = io.BytesIO()
        fig.savefig(fn, format="png", dpi=300, bbox_inches='tight')
        fn.seek(0)
        
        st.download_button(
            label="💾 Export / Save Graph (PNG)",
            data=fn,
            file_name=f"{chart_type.lower().replace(' ', '_')}.png",
            mime="image/png"
        )

# TAB 2: Openings Analysis
with tab2:
    st.subheader("🏆 Top Chess Openings Insights")
    if 'opening_name' in filtered_df.columns:
        limit = st.slider("Select Number of Top Openings to Show", 5, 30, 15)
        top_list = filtered_df['opening_name'].value_counts().nlargest(limit).index
        df_top = filtered_df[filtered_df['opening_name'].isin(top_list)]
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("**Average Turns by Opening**")
            turn_stats = df_top.groupby('opening_name')['turns'].mean().sort_values(ascending=False).reset_index()
            fig_turns, ax_turns = plt.subplots(figsize=(10, 6))
            sns.barplot(data=turn_stats, y='opening_name', x='turns', palette='coolwarm', hue='opening_name', legend=False, ax=ax_turns)
            ax_turns.set_title(f"Average Number of Turns (Top {limit} Openings)")
            st.pyplot(fig_turns)
            
        with col_b:
            st.markdown("**Winner Distribution by Opening**")
            win_rates = df_top.groupby('opening_name')['winner'].value_counts(normalize=True).unstack(fill_value=0) * 100
            fig_wins, ax_wins = plt.subplots(figsize=(10, 6))
            win_rates.plot(kind='barh', stacked=True, color=['#4F4F4F', '#D3D3D3', '#FFA07A'], ax=ax_wins)
            ax_wins.set_title("Win/Draw/Loss Ratios per Opening")
            ax_wins.set_xlabel("Percentage (%)")
            st.pyplot(fig_wins)
    else:
        st.warning("Column 'opening_name' not available.")

# TAB 3: Dataset Overview
with tab3:
    st.subheader("📋 Filtered Dataset Exploration")
    st.dataframe(filtered_df.head(100))
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.write("**Summary Statistics**")
        st.write(filtered_df.describe())
    with col_y:
        st.write("**Dataset Dimensions**")
        st.metric("Total Available Games", f"{df.shape[0]:,}")
        st.metric("Active Filtered Games", f"{filtered_df.shape[0]:,}")
