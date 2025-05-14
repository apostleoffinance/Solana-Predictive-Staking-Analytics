from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

# Page configuration
st.set_page_config(page_title="Solana Validators Dashboard", layout="wide")

# Load the data
df_validators = joblib.load('df_validators.joblib')
df_expanded = joblib.load('df_expanded.joblib')
df_cleaned = joblib.load('df_cleaned.joblib')
df_tps = joblib.load('df_tps.joblib')
df_supply = joblib.load('df_supply.joblib')
df_fees = joblib.load('df_fees.joblib')
df_inflation = joblib.load('df_inflation.joblib')
df_epochs = joblib.load('df_epochs.joblib')

# Prepare merged DataFrame
df_expanded['vote_account'] = df_expanded['votePubkey']
df_merge = df_validators.merge(df_expanded, how = 'left', on = ['vote_account', 'epoch'] )
df_merge["active_stake_SOL"] = df_merge["active_stake"] / 1e9
df_merge['name'] = df_merge['name'].replace([None, 'None'], 'Unknown')

# # Sidebar
# st.sidebar.title("Navigation")
# section = st.sidebar.radio("Go to", ["Overview", "Validator Performance", "Rewards"])

# Navigation at the top of the page
st.markdown(
    """
    <div style="background: linear-gradient(90deg, #00FFF0 0%, #8A4AF3 100%); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <h2 style="color: white; text-align: center; margin: 0;">Solana Validators Dashboard</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Navigation buttons (horizontal radio buttons)
section = st.radio(
    "Navigate to Section",
    ["Overview", "Validator Performance", "Staking Reward"],
    index=0,  # Default to Overview
    format_func=lambda x: x,  # Display labels as-is
    horizontal=True,  # Horizontal layout
    key="nav_radio",
    help="Select a section to explore the dashboard."
)

# Add some styling to the radio buttons using CSS
st.markdown(
    """
    <style>
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    div[role="radiogroup"] label {
        margin: 0 15px;
        font-size: 18px;
        color: #00FFF0;
        background-color: #8A4AF3;
        padding: 8px 16px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    div[role="radiogroup"] label:hover {
        background-color: #9945FF;
    }
    div[role="radiogroup"] input[type="radio"]:checked + label {
        background-color: #00FFF0;
        color: #8A4AF3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Overview ---
if section == "Overview":
    with st.container():
        st.markdown(
        """
        <div style="border: 1px solid #CCC; padding: 10px; border-radius: 5px; background-color: #8A4AF3;">
        """,
        unsafe_allow_html=True,
        )
        
        st.title("Network Overview")

        total_validators = df_expanded['vote_account'].nunique()

        # Circulating and non-circulating supply
        # Use numbers for calculations and display-formatted strings for metrics only
        circulating_val = int(df_supply['circulating_sol'][0])
        non_circulating_val = int(df_supply['nonCirculating_sol'][0])

        circulating = f"{circulating_val:,}"
        non_circulating = f"{non_circulating_val:,}"

        # TPS and fees
        tps = f"{int(df_tps['tps'][0]):,}"
        avg_fee_usd = df_fees['avg_fee_usd'][0]

        # Latest stake
        df_epochs['total_reward_SOL'] = df_epochs['total_rewards'] / 1e9
        df_epochs['total_active_stake_SOL'] = df_epochs['total_active_stake'] / 1e9
        df_epochs['total_reward_SOL'] = df_epochs['total_reward_SOL'].astype(object)
        df_epochs['total_active_stake_SOL'] = df_epochs['total_active_stake_SOL'].astype(object)
        df_epochs.loc[0, ['total_reward_SOL', 'total_active_stake_SOL']] = 'ongoing'
        concluded_epochs = df_epochs[df_epochs['total_active_stake_SOL'] != 'ongoing']
        latest_concluded = concluded_epochs.sort_values(by='epoch', ascending=False).iloc[0]
        latest_active_stake_SOL = f"{int(latest_concluded['total_active_stake_SOL']):,}"

        latest_epoch = latest_concluded['epoch']

    
        col1,col2,col3 = st.columns(3)
        col1.metric("Validators", total_validators)
        col2.metric("Epoch", f"{latest_epoch}")
        col3.metric("TPS", f"{tps}")

        col4, col5 = st.columns(2)
        
        col4.metric("Avg Fee (USD)", f"${avg_fee_usd:.6f}")
        col5.metric("Total Active Stake (SOL)", f"{latest_active_stake_SOL} SOL")
        
        # Spacer
    st.markdown("---")

    with st.container():
        st.markdown(
        """
        <div style="border: 1px solid #CCC; padding: 10px; border-radius: 5px; background-color: #8A4AF3;">
        """,
        unsafe_allow_html=True,
    )

        # Token Supply Pie Chart Section
        st.subheader("SOL Supply Breakdown")

        col6, col7 = st.columns(2)
        #col1.metric("Validators", total_validators)
        col6.metric("Circulating Supply", f"{circulating} SOL")
        col7.metric("Non-Circulating Supply", f"{non_circulating} SOL")


        supply_data = pd.DataFrame({
        'Supply Type': ['Circulating', 'Non-Circulating'],
        'Amount': [circulating_val, non_circulating_val]
        })

        fig = px.pie(
            supply_data,
            names='Supply Type',
            values='Amount',
            title="Solana Token Supply Distribution",
            hole=0.4,
        )

        fig.update_traces(
            textinfo='label+percent',
            hovertemplate='%{label}: %{value:,.0f} SOL<br>(%{percent})',
            marker=dict(colors=['#00FFF0', '#8A4AF3'])
        )

        st.plotly_chart(fig, use_container_width=True)

        
# --- Validator Performance ---
elif section == "Validator Performance":
    with st.container():
        st.markdown(
            """
            <div style="border: 1px solid #CCC; padding: 10px; border-radius: 5px; background-color: #8A4AF3;">
            """,
            unsafe_allow_html=True,
        )
        
        st.title("Validator Performance")

        # Prepare data for filtering
        latest_epoch = df_cleaned['epoch'].max()
        df_cleaned = df_cleaned.dropna()
        df_cleaned = df_cleaned[~((df_cleaned['epoch'] == latest_epoch) & df_cleaned['total_rewards'].isna() & df_cleaned['total_active_stake'].isna())].reset_index(drop=True)

        # Search inputs
        vote_account_search = st.text_input("Search by Vote Account", key="vote_account_search")
        name_search = st.text_input("Search by Name", key="name_search")

        # Filter the data
        filtered_data = df_cleaned.copy()
        if vote_account_search:
            filtered_data = filtered_data[filtered_data['vote_account'].str.contains(vote_account_search, case=False, na=False)]
        if name_search:
            filtered_data = filtered_data[filtered_data['name'].str.contains(name_search, case=False, na=False)]

        # Create previous_validator_performance from filtered_data with selected columns
        previous_validator_performance = filtered_data[
            ['name', 'activatedStake_SOL', 'commission', 'credits_earned', 'details']
        ]

        # Display previous_validator_performance as the first table with pagination
        st.subheader(f"Previous Validator Performance (Epoch {latest_epoch})")

        # Pagination
        rows_per_page = 100
        total_rows = len(previous_validator_performance)
        total_pages = (total_rows - 1) // rows_per_page + 1
        page_options = [f"{i*rows_per_page + 1}-{min((i+1)*rows_per_page, total_rows)}" for i in range(total_pages)]
        
        if total_rows > rows_per_page:
            selected_range = st.selectbox(
                "Select Range of Validators to View",
                page_options,
                index=0,
                key="validator_page_select"
            )
            start_idx = int(selected_range.split('-')[0]) - 1
            end_idx = int(selected_range.split('-')[1])
            display_data = previous_validator_performance.iloc[start_idx:end_idx]
        else:
            display_data = previous_validator_performance

        # Format the table for display
        display_data = display_data.copy()
        display_data['activatedStake_SOL'] = display_data['activatedStake_SOL'].round(2)
        display_data = display_data.rename(columns={
            'name': 'Name',
            'activatedStake_SOL': 'Active Stake (SOL)',
            'commission': 'Commission (%)',
            'credits_earned': 'Epoch Credits',
            'details': 'Details'
        })

        # Display the table
        st.dataframe(display_data, use_container_width=True)


                # Spacer
        st.markdown("---")

        with st.container():
            st.markdown(
            """
            <div style="border: 1px solid #CCC; padding: 10px; border-radius: 5px; background-color: #8A4AF3;">
            """,
            unsafe_allow_html=True,
        )

        # Bar Chart: Top 10 Validators by Active Stake from df_merge
        # Prepare top_10_validators
        df_merge['name'] = df_merge['name'].replace([None, 'None'], 'Unknown')
        df_merge['active_stake_SOL'] = pd.to_numeric(df_merge['active_stake_SOL'], errors='coerce')
        top_10_validators = df_merge[['name', 'active_stake_SOL']].sort_values(
            by='active_stake_SOL', ascending=False).head(10)
        top_10_validators.reset_index(drop=True, inplace=True)

        st.subheader("Top 10 Validators by Active Stake")
        stake_fig = px.bar(
            top_10_validators,
            x='name',
            y='active_stake_SOL',
            title="Top 10 Validators by Active Stake",
            labels={'active_stake_SOL': 'Active Stake (SOL)', 'name': 'Validator'},
            text_auto='.2f'
        )
        stake_fig.update_traces(marker_color='#00FFF0')  # Use Solana cyan
        stake_fig.update_layout(
            yaxis_tickformat=',.2f',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_tickangle=-45  # Rotate x-axis labels for readability
        )
        st.plotly_chart(stake_fig, use_container_width=True)


# --- Staking Reward ---
elif section == "Staking Reward":
    with st.container():
        st.markdown(
            """
            <div style="border: 1px solid #CCC; padding: 10px; border-radius: 5px; background-color: #8A4AF3;">
            """,
            unsafe_allow_html=True,
        )
        
        st.title("Staking Reward")

        # Prepare staking rewards data
        df_epochs = df_epochs.copy()
        df_epochs['total_reward_SOL'] = df_epochs['total_rewards'] / 1e9
        df_epochs['total_active_stake_SOL'] = df_epochs['total_active_stake'] / 1e9

        # Convert to object type to allow string + float
        df_epochs['total_reward_SOL'] = df_epochs['total_reward_SOL'].astype('object')
        df_epochs['total_active_stake_SOL'] = df_epochs['total_active_stake_SOL'].astype('object')

        df_epochs.loc[0, ['total_reward_SOL', 'total_active_stake_SOL']] = 'ongoing'

        staking_rewards = df_epochs[
            ['epoch', 'total_reward_SOL', 'total_active_stake_SOL']
        ]

         # Pagination setup
        rows_per_page = 10
        total_rows = len(staking_rewards)
        total_pages = (total_rows - 1) // rows_per_page + 1

        # Initialize session state for page navigation
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("Previous 10") and st.session_state.current_page > 0:
                st.session_state.current_page -= 1
        with col2:
            st.write(f"Page {st.session_state.current_page + 1} of {total_pages} (Showing rows {st.session_state.current_page * rows_per_page + 1} to {min((st.session_state.current_page + 1) * rows_per_page, total_rows)})")
        with col3:
            if st.button("Next 10") and (st.session_state.current_page + 1) < total_pages:
                st.session_state.current_page += 1

        # Slice the data for the current page
        start_idx = st.session_state.current_page * rows_per_page
        end_idx = min((st.session_state.current_page + 1) * rows_per_page, total_rows)
        display_rewards = staking_rewards.iloc[start_idx:end_idx].copy()

        # Display staking rewards table
        st.subheader("Staking Rewards by Epoch")
        display_rewards = display_rewards.rename(columns={
            'epoch': 'Epoch',
            'total_reward_SOL': 'Total Reward (SOL)',
            'total_active_stake_SOL': 'Total Active Stake (SOL)'
        })

        # Format numerical values where not 'ongoing'
        display_rewards['Total Reward (SOL)'] = display_rewards['Total Reward (SOL)'].apply(
            lambda x: f"{float(x):,.2f}" if x != 'ongoing' else x
        )
        display_rewards['Total Active Stake (SOL)'] = display_rewards['Total Active Stake (SOL)'].apply(
            lambda x: f"{float(x):,.2f}" if x != 'ongoing' else x
        )

        st.dataframe(display_rewards, use_container_width=True)

        
        # Staking Rewards and Active Stake per Epoch Graph
        # Filter out 'ongoing' rows and convert types
        staking_rewards_filtered = staking_rewards[
            staking_rewards['total_active_stake_SOL'] != 'ongoing'
        ].copy()

        staking_rewards_filtered['total_reward_SOL'] = staking_rewards_filtered['total_reward_SOL'].astype(float)
        staking_rewards_filtered['total_active_stake_SOL'] = staking_rewards_filtered['total_active_stake_SOL'].astype(float)

        fig, ax1 = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#0e1117')  # Dark background for the figure
        ax1.set_facecolor('#0e1117')        # Dark background for the bar axis

        # Bar for rewards
        ax1.bar(
            staking_rewards_filtered['epoch'], 
            staking_rewards_filtered['total_reward_SOL'], 
            color="#00FFF0", 
            label='Total Reward (SOL)'
        )
        ax1.set_xlabel("Epoch")
        ax1.set_ylabel("Reward (SOL)", color="#00FFF0")
        ax1.tick_params(axis='y', labelcolor="#00FFF0")

        # Line for active stake
        ax2 = ax1.twinx()
        ax2.plot(
            staking_rewards_filtered['epoch'], 
            staking_rewards_filtered['total_active_stake_SOL'], 
            color="#8A4AF3", 
            marker='o', 
            label='Total Active Stake (SOL)'
        )
        ax2.set_ylabel("Active Stake (SOL)", color="#8A4AF3")
        ax2.tick_params(axis='y', labelcolor="#8A4AF3")

        # Titles and layout
        fig.suptitle("Staking Rewards and Active Stake per Epoch")
        fig.tight_layout()

        # Display in Streamlit
        st.pyplot(fig)

        st.markdown("---")

