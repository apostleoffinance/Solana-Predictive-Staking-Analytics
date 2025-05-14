# Solana Validators Dashboard

## Solana Validators Dashboard Python Streamlit

A web-based dashboard to visualize and analyze Solana blockchain validator performance, staking rewards, and network overview metrics. Built with Streamlit, Pandas, Plotly, and Matplotlib, this dashboard provides an interactive interface to explore validator data, staking rewards, and token supply breakdowns.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features) §
* [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Dependencies](#dependencies)
* [Data Sources](#data-sources)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

The Solana Validators Dashboard is an interactive tool designed to provide insights into the Solana blockchain's validator ecosystem. It offers three main sections:

* **Network Overview**: Displays key metrics like total validators, current epoch, TPS (transactions per second), average fees, total active stake, and a breakdown of circulating vs. non-circulating SOL supply.

* **Validator Performance**: Allows users to search and filter validators by vote account or name, view performance metrics, and see the top 10 validators by active stake.

* **Staking Reward**: Shows staking rewards and active stake per epoch in a paginated table, along with a dual-axis graph visualizing historical rewards and stakes.

The dashboard uses a dark theme with Solana-inspired colors (`#00FFF0` for cyan and `#8A4AF3` for purple) to create a visually appealing and cohesive interface.

---

## Features

* **Interactive Navigation**: Horizontal radio buttons for switching between sections (Overview, Validator Performance, Staking Reward).

* **Network Metrics**:

  * Total validators, current epoch, TPS, average fees, and total active stake.
  * Pie chart for SOL supply distribution (circulating vs. non-circulating).

* **Validator Performance**:

  * Searchable table with pagination (100 rows per page) for validator details (name, active stake, commission, epoch credits, details).
  * Bar chart of the top 10 validators by active stake.

* **Staking Rewards**:

  * Paginated table (10 rows per page) showing staking rewards and active stake per epoch, with "ongoing" status for the latest epoch.
  * Dual-axis graph (bar for rewards, line for active stake) with a dark background (`#0e1117`).

* **Responsive Design**: Built with Streamlit’s `layout="wide"` for optimal viewing on larger screens.

* **Custom Styling**: Solana-themed colors and CSS for navigation buttons.

---

## Installation

### Prerequisites

* Python 3.8 or higher
* Git

### Steps

1. **Clone the Repository:**

```bash
git clone https://github.com/yourusername/solana-validators-dashboard.git
cd solana-validators-dashboard
```

2. **Set Up a Virtual Environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Download or Prepare Data Files:**
   The dashboard expects the following `.joblib` files in the project directory:

* `df_validators.joblib`
* `df_expanded.joblib`
* `df_cleaned.joblib`
* `df_tps.joblib`
* `df_supply.joblib`
* `df_fees.joblib`
* `df_inflation.joblib`
* `df_epochs.joblib`

These files contain preprocessed Solana blockchain data. You can generate them using a data pipeline or download them from a trusted source.

5. **Run the Dashboard:**

```bash
streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501` to view the dashboard.

---

## Usage

### Launch the Dashboard:

* Run the app as described in the installation steps.
* The dashboard will open in your default web browser.

### Navigate Sections:

* Use the horizontal radio buttons at the top to switch between "Overview," "Validator Performance," and "Staking Reward."

### Explore Features:

* **Overview**: View network metrics and the SOL supply pie chart.
* **Validator Performance**:

  * Search validators by vote account or name.
  * Navigate the paginated table (100 rows per page).
  * View the top 10 validators by active stake.
* **Staking Reward**:

  * Browse the paginated table (10 rows per page) using "Previous 10" and "Next 10" buttons.
  * Analyze historical staking rewards and active stake in the dual-axis graph.

---

## Project Structure

```
solana-validators-dashboard/
├── app.py                  # Main Streamlit application script
├── requirements.txt        # List of Python dependencies
├── df_validators.joblib    # Validator data
├── df_expanded.joblib      # Expanded validator data
├── df_cleaned.joblib       # Cleaned validator data
├── df_tps.joblib           # TPS data
├── df_supply.joblib        # Supply data
├── df_fees.joblib          # Fees data
├── df_inflation.joblib     # Inflation data
├── df_epochs.joblib        # Epoch data
├── screenshots/            # Directory for dashboard screenshots
│   ├── network_overview.png
│   ├── validator_performance.png
│   └── staking_reward.png
└── README.md               # Project documentation
```

---

## Dependencies

The project relies on the following Python libraries:

* `streamlit` - For building the interactive web app
* `pandas` - For data manipulation
* `numpy` - For numerical operations
* `joblib` - For loading preprocessed data
* `plotly.express` - For interactive visualizations (pie chart, bar chart)
* `matplotlib.pyplot` - For static visualizations (dual-axis graph)

Install them using the `requirements.txt` file:

```plaintext
streamlit==1.10.0
pandas==1.5.0
numpy==1.23.0
joblib==1.2.0
plotly==5.10.0
matplotlib==3.6.0
```

Create the requirements.txt file with the above content, or generate it using:

```bash
pip freeze > requirements.txt
```

---

## Data Sources

The dashboard uses preprocessed `.joblib` files containing Solana blockchain data from Helius API and Validator.app API:

* **Validator data**: `df_validators`, `df_expanded`, `df_cleaned`
* **Network metrics**: `df_tps`, `df_supply`, `df_fees`, `df_inflation`
* **Epoch data**: `df_epochs`

These files are assumed to be generated from Solana blockchain APIs or datasets (e.g., Solana RPC endpoints, public validator datasets). To replicate the data:

* Fetch validator and epoch data using Solana’s RPC API (`getVoteAccounts`, `getEpochInfo`).
* Process the data with Pandas to create the required DataFrames.
* Save them as `.joblib` files using `joblib.dump()`.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:

```bash
git checkout -b feature/your-feature
```

3. Make your changes and commit:

```bash
git commit -m "Add your feature"
```

4. Push to your branch:

```bash
git push origin feature/your-feature
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Created on May 14, 2025, by \[Apostle of Finance].**

Feel free to star ⭐ the repository if you find it useful!
