# ============================================================
# 🏏 IPL 2025 ANALYTICS DASHBOARD
# Tools: Python · Pandas · Matplotlib · Seaborn
# Platform: Google Colab
# ============================================================

# ── CELL 1: Install & Import Libraries ──────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Custom IPL Colour Palette ────────────────────────────────
IPL_COLORS = [
    "#1B3A6B",   # deep navy
    "#D4AF37",   # gold
    "#E8552E",   # ipl orange
    "#2ECC71",   # emerald
    "#9B59B6",   # purple
    "#E74C3C",   # red
    "#3498DB",   # blue
    "#F39C12",   # amber
    "#1ABC9C",   # teal
    "#E91E63",   # pink
]

BACKGROUND   = "#F8F9FA"
CARD_BG      = "#FFFFFF"
TEXT_DARK    = "#1A1A2E"
ACCENT_GOLD  = "#D4AF37"
ACCENT_BLUE  = "#1B3A6B"

# Apply a clean, professional Matplotlib style
plt.rcParams.update({
    "figure.facecolor"   : BACKGROUND,
    "axes.facecolor"     : CARD_BG,
    "axes.edgecolor"     : "#DEE2E6",
    "axes.titlesize"     : 14,
    "axes.titleweight"   : "bold",
    "axes.titlecolor"    : TEXT_DARK,
    "axes.labelcolor"    : TEXT_DARK,
    "axes.labelsize"     : 11,
    "xtick.color"        : TEXT_DARK,
    "ytick.color"        : TEXT_DARK,
    "xtick.labelsize"    : 9,
    "ytick.labelsize"    : 9,
    "grid.color"         : "#E9ECEF",
    "grid.linestyle"     : "--",
    "grid.alpha"         : 0.7,
    "font.family"        : "DejaVu Sans",
    "legend.framealpha"  : 0.9,
    "figure.dpi"         : 120,
})

print("✅ Libraries imported. IPL colour palette ready.")


# ── CELL 2: Upload Dataset ───────────────────────────────────
from google.colab import files
print("📂 Upload matches.csv and deliveries.csv ...")
uploaded = files.upload()


# ── CELL 3: Load & Quick-Inspect ────────────────────────────
matches    = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

print(f"✅ matches.csv   → {matches.shape[0]:,} rows  ×  {matches.shape[1]} columns")
print(f"✅ deliveries.csv → {deliveries.shape[0]:,} rows  ×  {deliveries.shape[1]} columns")
matches.head()


# ── CELL 4: Data Audit ──────────────────────────────────────
print("═" * 50)
print("MATCHES — Column info")
print("═" * 50)
matches.info()

print("\n" + "═" * 50)
print("MATCHES — Missing values")
print("═" * 50)
print(matches.isnull().sum()[matches.isnull().sum() > 0])

print("\n" + "═" * 50)
print("MATCHES — Statistical summary")
print("═" * 50)
matches.describe()


# ── CELL 5: Data Cleaning ───────────────────────────────────
# Drop rows where 'winner' is null (super-overs / no results)
before = len(matches)
matches_clean = matches.dropna(subset=['winner']).copy()
after  = len(matches_clean)
print(f"Dropped {before - after} rows with no result  →  {after} valid matches remaining.")

# Standardise team name column if needed
matches_clean['winner'] = matches_clean['winner'].str.strip()
matches_clean['team1']  = matches_clean['team1'].str.strip()
matches_clean['team2']  = matches_clean['team2'].str.strip()

print("\nUnique teams in dataset:")
all_teams = pd.Series(
    list(matches_clean['team1'].unique()) +
    list(matches_clean['team2'].unique())
).unique()
print(sorted(all_teams))


# ────────────────────────────────────────────────────────────
# HELPER — adds value labels on top of every bar
# ────────────────────────────────────────────────────────────
def add_bar_labels(ax, fmt="{:.0f}", color="white", fontsize=9, pad=3):
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(
                fmt.format(h),
                (p.get_x() + p.get_width() / 2, h + pad),
                ha="center", va="bottom",
                fontsize=fontsize, color=TEXT_DARK, fontweight="bold"
            )


# ────────────────────────────────────────────────────────────
# TASK 1 — Matches Won per Team (Basic Bar Chart)
# ────────────────────────────────────────────────────────────
team_wins = matches_clean['winner'].value_counts()

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BACKGROUND)

bars = ax.bar(
    team_wins.index, team_wins.values,
    color=IPL_COLORS[:len(team_wins)],
    edgecolor="white", linewidth=0.8,
    width=0.65
)
add_bar_labels(ax)

ax.set_title("🏆  Matches Won by Each Team — IPL 2025", pad=15, fontsize=15)
ax.set_xlabel("Team", labelpad=10)
ax.set_ylabel("Number of Wins", labelpad=10)
ax.set_xticklabels(team_wins.index, rotation=40, ha='right')
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig("task1_wins_bar.png", dpi=150, bbox_inches='tight')
plt.show()
print(f"\n📌 Most wins:  {team_wins.idxmax()}  ({team_wins.max()} wins)")


# ────────────────────────────────────────────────────────────
# TASK 2 — Most Successful Team (Seaborn Countplot)
# ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BACKGROUND)

order = matches_clean['winner'].value_counts().index
palette = dict(zip(order, IPL_COLORS[:len(order)]))

sns.countplot(
    x='winner', data=matches_clean,
    order=order, palette=palette,
    edgecolor='white', linewidth=0.8,
    ax=ax
)
add_bar_labels(ax)

ax.set_title("🥇  Most Successful Team — IPL 2025", pad=15, fontsize=15)
ax.set_xlabel("Team", labelpad=10)
ax.set_ylabel("Wins", labelpad=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right')
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig("task2_seaborn_wins.png", dpi=150, bbox_inches='tight')
plt.show()


# ────────────────────────────────────────────────────────────
# TASK 3 — Toss Decision Analysis (Donut Chart)
# ────────────────────────────────────────────────────────────
toss_counts = matches_clean['toss_decision'].value_counts()

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor(BACKGROUND)

wedges, texts, autotexts = ax.pie(
    toss_counts.values,
    labels=toss_counts.index,
    autopct="%1.1f%%",
    colors=[ACCENT_BLUE, ACCENT_GOLD],
    startangle=140,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    textprops=dict(fontsize=12)
)
for autotext in autotexts:
    autotext.set_fontsize(13)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Centre label
ax.text(0, 0, "TOSS\nDECISION", ha='center', va='center',
        fontsize=13, fontweight='bold', color=TEXT_DARK)

ax.set_title("🎲  Toss Decision Breakdown — IPL 2025", pad=20, fontsize=15)
plt.tight_layout()
plt.savefig("task3_toss_donut.png", dpi=150, bbox_inches='tight')
plt.show()

dominant = toss_counts.idxmax()
print(f"\n📌 Teams prefer to  '{dominant}'  after winning the toss  ({toss_counts[dominant]} times)")


# ────────────────────────────────────────────────────────────
# TASK 4 — Top 10 Player of the Match Winners
# ────────────────────────────────────────────────────────────
top_players = matches_clean['player_of_match'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BACKGROUND)

colors_grad = sns.color_palette("YlOrRd", n_colors=10)[::-1]
bars = ax.barh(
    top_players.index[::-1], top_players.values[::-1],
    color=colors_grad, edgecolor='white', linewidth=0.8
)

for i, (val, bar) in enumerate(zip(top_players.values[::-1], bars)):
    ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
            f" {val}", va='center', fontsize=10, fontweight='bold', color=TEXT_DARK)

ax.set_title("⭐  Top 10 Player of the Match Winners — IPL 2025", pad=15, fontsize=15)
ax.set_xlabel("Awards Won", labelpad=10)
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig("task4_top_players.png", dpi=150, bbox_inches='tight')
plt.show()

print(f"\n📌 Most Player of Match awards:  {top_players.idxmax()}  ({top_players.max()} awards)")


# ────────────────────────────────────────────────────────────
# TASK 5 — Top 10 Venues by Match Count
# ────────────────────────────────────────────────────────────
venue_counts = matches_clean['venue'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BACKGROUND)

colors_venue = sns.color_palette("Blues_r", n_colors=10)
bars = ax.bar(
    range(len(venue_counts)), venue_counts.values,
    color=colors_venue, edgecolor='white', linewidth=0.8, width=0.65
)
ax.set_xticks(range(len(venue_counts)))
ax.set_xticklabels(
    [v[:30] + '…' if len(v) > 30 else v for v in venue_counts.index],
    rotation=35, ha='right', fontsize=8
)

add_bar_labels(ax, pad=0.2)
ax.set_title("🏟️  Top 10 IPL Venues by Matches Hosted — IPL 2025", pad=15, fontsize=15)
ax.set_xlabel("Venue", labelpad=10)
ax.set_ylabel("Matches Hosted", labelpad=10)
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig("task5_venues.png", dpi=150, bbox_inches='tight')
plt.show()

print(f"\n📌 Primary venue:  {venue_counts.idxmax()}  ({venue_counts.max()} matches)")


# ────────────────────────────────────────────────────────────
# TASK 6 — Team Performance Dashboard (Seaborn Barplot)
# ────────────────────────────────────────────────────────────
team_wins_sorted = matches_clean['winner'].value_counts().reset_index()
team_wins_sorted.columns = ['team', 'wins']

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BACKGROUND)

sns.barplot(
    x='team', y='wins', data=team_wins_sorted,
    palette=IPL_COLORS[:len(team_wins_sorted)],
    edgecolor='white', linewidth=0.8, ax=ax
)
add_bar_labels(ax)

ax.set_title("📊  Team Performance Dashboard — IPL 2025", pad=15, fontsize=15)
ax.set_xlabel("Team", labelpad=10)
ax.set_ylabel("Total Wins", labelpad=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right')
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig("task6_performance_dashboard.png", dpi=150, bbox_inches='tight')
plt.show()


# ────────────────────────────────────────────────────────────
# TASK 7 — Winning Percentage per Team
# ────────────────────────────────────────────────────────────
total_matches = len(matches_clean)
wins          = matches_clean['winner'].value_counts()
win_pct       = ((wins / total_matches) * 100).round(2)

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BACKGROUND)

colors_pct = sns.color_palette("RdYlGn", n_colors=len(win_pct))[::-1]
bars = ax.bar(
    win_pct.index, win_pct.values,
    color=colors_pct, edgecolor='white', linewidth=0.8, width=0.65
)
add_bar_labels(ax, fmt="{:.1f}%", pad=0.1)

ax.set_title("📈  Winning Percentage per Team — IPL 2025", pad=15, fontsize=15)
ax.set_xlabel("Team", labelpad=10)
ax.set_ylabel("Win %", labelpad=10)
ax.set_xticklabels(win_pct.index, rotation=40, ha='right')
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig("task7_win_percentage.png", dpi=150, bbox_inches='tight')
plt.show()

print("\nTop 5 Win Percentages:")
print(win_pct.head(5).to_string())


# ────────────────────────────────────────────────────────────
# TASK 8 — FULL DASHBOARD  (2 × 2 Grid)
# ────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 12), facecolor=BACKGROUND)
fig.suptitle(
    "🏏  IPL 2025 — Complete Analytics Dashboard",
    fontsize=20, fontweight='bold', color=TEXT_DARK, y=0.98
)

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

# ── Panel 1: Top 5 Teams by Wins ────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
top5_wins = matches_clean['winner'].value_counts().head(5)
bars1 = ax1.bar(
    top5_wins.index, top5_wins.values,
    color=IPL_COLORS[:5], edgecolor='white', linewidth=0.8
)
add_bar_labels(ax1, pad=0.2)
ax1.set_title("🏆  Top 5 Teams by Wins")
ax1.set_xlabel("Team"); ax1.set_ylabel("Wins")
ax1.set_xticklabels(top5_wins.index, rotation=30, ha='right', fontsize=8)
ax1.yaxis.grid(True); ax1.set_axisbelow(True)
ax1.spines[['top','right']].set_visible(False)

# ── Panel 2: Toss Decision Donut ────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
toss = matches_clean['toss_decision'].value_counts()
wedges, texts, autotexts = ax2.pie(
    toss.values, labels=toss.index, autopct="%1.1f%%",
    colors=[ACCENT_BLUE, ACCENT_GOLD], startangle=140,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2),
    textprops=dict(fontsize=11)
)
for at in autotexts:
    at.set_fontsize(12); at.set_fontweight('bold'); at.set_color('white')
ax2.text(0, 0, "TOSS", ha='center', va='center',
         fontsize=11, fontweight='bold', color=TEXT_DARK)
ax2.set_title("🎲  Toss Decisions")

# ── Panel 3: Top 5 Venues ───────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
top5_venues = matches_clean['venue'].value_counts().head(5)
short_names = [v.split(',')[0][:22] for v in top5_venues.index]
colors_v    = sns.color_palette("Blues_r", n_colors=5)
bars3 = ax3.barh(
    range(5), top5_venues.values[::-1],
    color=colors_v, edgecolor='white', linewidth=0.8
)
ax3.set_yticks(range(5))
ax3.set_yticklabels(short_names[::-1], fontsize=8)
for val, bar in zip(top5_venues.values[::-1], bars3):
    ax3.text(val + 0.1, bar.get_y() + bar.get_height()/2,
             f' {val}', va='center', fontsize=9, fontweight='bold', color=TEXT_DARK)
ax3.set_title("🏟️  Top 5 Venues")
ax3.set_xlabel("Matches")
ax3.xaxis.grid(True); ax3.set_axisbelow(True)
ax3.spines[['top','right']].set_visible(False)

# ── Panel 4: Top 5 Player of Match ─────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
top5_players = matches_clean['player_of_match'].value_counts().head(5)
colors_p     = sns.color_palette("YlOrRd", n_colors=5)[::-1]
bars4 = ax4.barh(
    range(5), top5_players.values[::-1],
    color=colors_p, edgecolor='white', linewidth=0.8
)
ax4.set_yticks(range(5))
ax4.set_yticklabels(top5_players.index[::-1], fontsize=9)
for val, bar in zip(top5_players.values[::-1], bars4):
    ax4.text(val + 0.05, bar.get_y() + bar.get_height()/2,
             f' {val}', va='center', fontsize=9, fontweight='bold', color=TEXT_DARK)
ax4.set_title("⭐  Top 5 Player of Match")
ax4.set_xlabel("Awards")
ax4.xaxis.grid(True); ax4.set_axisbelow(True)
ax4.spines[['top','right']].set_visible(False)

plt.savefig("task8_full_dashboard.png", dpi=150, bbox_inches='tight')
plt.show()
print("✅ Full 2×2 dashboard saved as  task8_full_dashboard.png")


# ────────────────────────────────────────────────────────────
# BONUS — Deliveries Analysis  (from deliveries.csv)
# ────────────────────────────────────────────────────────────

# Top Run-Scorers
top_batters = (
    deliveries.groupby('batter')['batsman_runs']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BACKGROUND)
colors_bat = sns.color_palette("OrRd", n_colors=10)[::-1]
ax.barh(top_batters.index[::-1], top_batters.values[::-1],
        color=colors_bat, edgecolor='white', linewidth=0.8)
for val, bar in zip(top_batters.values[::-1], ax.patches):
    ax.text(val + 2, bar.get_y() + bar.get_height()/2,
            f' {val}', va='center', fontsize=9, fontweight='bold', color=TEXT_DARK)
ax.set_title("🏏  Top 10 Run-Scorers — IPL 2025", pad=15, fontsize=15)
ax.set_xlabel("Total Runs", labelpad=10)
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig("bonus_top_batters.png", dpi=150, bbox_inches='tight')
plt.show()

# Top Wicket-Takers
top_bowlers = (
    deliveries[deliveries['dismissal_kind'].notna()]
    .groupby('bowler')['dismissal_kind']
    .count()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BACKGROUND)
colors_bowl = sns.color_palette("PuBuGn", n_colors=10)[::-1]
ax.barh(top_bowlers.index[::-1], top_bowlers.values[::-1],
        color=colors_bowl, edgecolor='white', linewidth=0.8)
for val, bar in zip(top_bowlers.values[::-1], ax.patches):
    ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
            f' {val}', va='center', fontsize=9, fontweight='bold', color=TEXT_DARK)
ax.set_title("🎯  Top 10 Wicket-Takers — IPL 2025", pad=15, fontsize=15)
ax.set_xlabel("Total Wickets", labelpad=10)
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig("bonus_top_bowlers.png", dpi=150, bbox_inches='tight')
plt.show()


# ────────────────────────────────────────────────────────────
# ML BONUS — Predict Match Winner (Random Forest)
# ────────────────────────────────────────────────────────────
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

ml_df = matches_clean[['team1','team2','toss_winner','toss_decision','winner']].dropna().copy()

le = LabelEncoder()
ml_df['team1_enc']        = le.fit_transform(ml_df['team1'])
ml_df['team2_enc']        = le.fit_transform(ml_df['team2'])
ml_df['toss_winner_enc']  = le.fit_transform(ml_df['toss_winner'])
ml_df['toss_decision_enc']= le.fit_transform(ml_df['toss_decision'])
ml_df['winner_enc']       = le.fit_transform(ml_df['winner'])

X = ml_df[['team1_enc','team2_enc','toss_winner_enc','toss_decision_enc']]
y = ml_df['winner_enc']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred   = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'═'*50}")
print(f"  🤖  ML Model — Random Forest Classifier")
print(f"{'═'*50}")
print(f"  Accuracy  :  {accuracy:.2%}")
print(f"  Train size:  {len(X_train)}  |  Test size: {len(X_test)}")
print(f"{'═'*50}")

# Feature Importance Plot
fi = pd.Series(
    model.feature_importances_,
    index=['Team 1','Team 2','Toss Winner','Toss Decision']
).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(BACKGROUND)
fi.plot(kind='barh', ax=ax, color=[ACCENT_BLUE, ACCENT_GOLD, "#2ECC71", "#E8552E"],
        edgecolor='white', linewidth=0.8)
ax.set_title("🤖  Feature Importance — Match Winner Prediction", pad=12, fontsize=14)
ax.set_xlabel("Importance Score")
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig("ml_feature_importance.png", dpi=150, bbox_inches='tight')
plt.show()

print("\n🎉  All tasks complete! Your IPL 2025 Analytics Dashboard is ready.")
