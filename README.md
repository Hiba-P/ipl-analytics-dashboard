📌 Project Overview
This project transforms raw IPL 2025 CSV data into a fully styled analytics dashboard using Python in Google Colab. It covers the complete data science workflow:
Raw CSV → Data Cleaning → EDA → Visualisation → Dashboard → ML Prediction
Dataset: Two CSV files from Kaggle — matches.csv (match-level) and deliveries.csv (ball-by-ball)
🎯 What's Inside
TaskTitleChart Type1Matches Won per TeamBar Chart2Most Successful TeamSeaborn Countplot3Toss Decision AnalysisDonut Pie Chart4Top 10 Player of the MatchHorizontal Bar5Venue AnalysisBar Chart6Team Performance DashboardSeaborn Barplot7Winning Percentage per TeamGradient Bar Chart8Full Dashboard (2×2 Grid)Multi-Panel Figure⭐ BonusTop Batters & BowlersHorizontal Bar🤖 MLMatch Winner PredictorRandom Forest
🖼️ Dashboard Preview
Run the notebook and your task8_full_dashboard.png will look like this ↓
┌─────────────────────┬────────────────────┐
│  🏆 Top 5 Teams     │  🎲 Toss Decisions │
│  by Wins (bar)      │  (donut chart)     │
├─────────────────────┼────────────────────┤
│  🏟️ Top 5 Venues   │  ⭐ Top 5 Player   │
│  (horiz. bar)       │  of Match (bar)    │
└─────────────────────┴────────────────────┘
🛠️ Tech Stack
LibraryPurposepandasData loading, cleaning, groupby analysismatplotlibBase plotting engine, subplot gridsseabornStyled countplots and barplotsscikit-learnRandom Forest, Label Encoding, train/test split
🚀 How to Run
Option A — Google Colab (Recommended)
Open Google Colab
Create a new notebook and paste the code from IPL_2025_Analytics_Dashboard.py
Download matches.csv and deliveries.csv from Kaggle IPL Dataset
Run Cell 2 — a file picker will appear; upload both CSVs
Run all remaining cells top to bottom
Option B — Local / VS Code
bashgit clone https://github.com/YOUR_USERNAME/ipl-2025-analytics-dashboard.git
cd ipl-2025-analytics-dashboard
pip install pandas matplotlib seaborn scikit-learn
# Place matches.csv and deliveries.csv in the project folder, then:
python IPL_2025_Analytics_Dashboard.py
📂 Repository Structure
ipl-2025-analytics-dashboard/
│
├── IPL_2025_Analytics_Dashboard.py   # Complete Python script
├── README.md                         # This file
├── requirements.txt                  # Dependencies
│
└── outputs/                          # Generated charts (after running)
    ├── task1_wins_bar.png
    ├── task2_seaborn_wins.png
    ├── task3_toss_donut.png
    ├── task4_top_players.png
    ├── task5_venues.png
    ├── task6_performance_dashboard.png
    ├── task7_win_percentage.png
    ├── task8_full_dashboard.png
    ├── bonus_top_batters.png
    ├── bonus_top_bowlers.png
    └── ml_feature_importance.png
🤖 ML Bonus — Match Winner Predictor
Uses a Random Forest Classifier trained on:
Team 1 & Team 2 (label-encoded)
Toss winner
Toss decision (bat / field)
pythonfrom sklearn.ensemble import RandomForestClassifier
# ...see notebook for full pipeline
Output: Accuracy score + feature importance plot showing which factors matter most for predicting the winner.
📊 Key Insights Uncovered
Which team dominated IPL 2025
Whether teams prefer batting or fielding after winning the toss
The most consistent match-winner (Player of the Match count)
Primary IPL venue by match count
Team winning percentages (normalised)
Top run-scorers and wicket-takers from ball-by-ball data
📦 requirements.txt
pandas
matplotlib
seaborn
scikit-learn
👩‍💻 Author
Hiba Puthiyedath
🔗 LinkedIn
💻 GitHub
📝 License
This project is open-source under the MIT License.
is this is the read me
