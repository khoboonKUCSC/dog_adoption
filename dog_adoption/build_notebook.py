"""
Build an enhanced Dog_Adoption.ipynb with MORE visualizations,
ONE graph per cell, presentation-ready styling.
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata.update({
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.14.0"}
})

cells = []

def md(source):
    cells.append(nbf.v4.new_markdown_cell(source))

def code(source):
    cells.append(nbf.v4.new_code_cell(source))

# ═══════════════════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════════════════
md("""# Dog Adoption Success Rate - Data Analysis

**Objective:** Analyze the `dog_adoption_master.csv` dataset to uncover factors that influence whether an adopted dog is **returned** to the shelter, and derive actionable recommendations to improve adoption success rates.

---
## Table of Contents
1. Setup & Data Loading
2. Data Overview & Cleaning
3. Missing Value Analysis
4. Outlier Detection
5. Univariate Analysis
6. Bivariate / Target Analysis
7. Correlation Matrix & Important Features
8. Multivariate Visualizations
9. Feature Importance (Machine Learning)
10. Summary
""")

# ═══════════════════════════════════════════════════════════════════════════
# 1. SETUP
# ═══════════════════════════════════════════════════════════════════════════
md("## 1. Setup & Data Loading")

code("""\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# Presentation-ready style
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.25)
plt.rcParams.update({
    'figure.dpi': 130,
    'figure.figsize': (14, 7),
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.labelsize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.titlesize': 18,
    'figure.titleweight': 'bold',
})

# Color palette
KEPT_COLOR = '#27ae60'
RETURNED_COLOR = '#e74c3c'
ACCENT = '#2980b9'
PALETTE_PAIR = {0: KEPT_COLOR, 1: RETURNED_COLOR}

print("Libraries loaded successfully")
""")

code("""\
df = pd.read_csv('dog_adoption_master.csv')
print(f"Dataset shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
df.head(10)
""")

# ═══════════════════════════════════════════════════════════════════════════
# 2. DATA OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
md("## 2. Data Overview & Cleaning")

code("""\
print("-- Column Data Types --")
print(df.dtypes.to_string())
print(f"\\n-- Memory Usage --")
print(f"{df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
""")

code("""\
print("-- Statistical Summary (Numeric) --")
df.describe().T.round(2)
""")

code("""\
print("-- Categorical Columns --")
cat_cols = df.select_dtypes(include='object').columns.tolist()
for col in cat_cols:
    print(f"\\n{col}: {df[col].nunique()} unique values")
    print(f"  {df[col].value_counts().head(5).to_dict()}")
""")

code("""\
print("-- Target Variable: returned --")
print(df['returned'].value_counts())
print(f"\\nReturn Rate: {df['returned'].mean()*100:.2f}%")
""")

# ═══════════════════════════════════════════════════════════════════════════
# 3. MISSING VALUE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
md("## 3. Missing Value Analysis")

code("""\
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing %', ascending=False)

if missing_df.empty:
    print("No missing values found!")
else:
    print("-- Missing Values --")
    print(missing_df.to_string())
""")

# GRAPH 1: Missing Values Bar Chart
code("""\
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing %', ascending=True)

fig, ax = plt.subplots(figsize=(14, 5))
bars = ax.barh(missing_df.index, missing_df['Missing %'], color='#e74c3c', edgecolor='white', height=0.6)
ax.set_xlabel('Missing Percentage (%)')
ax.set_title('Missing Values by Column')
for bar, pct in zip(bars, missing_df['Missing %']):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{pct:.1f}%', va='center', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
""")

code("""\
# Handle missing values
print("-- days_to_return --")
print(f"NaN count: {df['days_to_return'].isna().sum()}")
print(f"Matches returned==0: {(df['days_to_return'].isna() == (df['returned'] == 0)).all()}")

print("\\n-- return_reason --")
print(df['return_reason'].value_counts())

df['days_to_return'] = df['days_to_return'].fillna(0)
print("\\nMissing values handled (days_to_return NaN -> 0 for non-returned dogs)")
""")

# ═══════════════════════════════════════════════════════════════════════════
# 4. OUTLIER DETECTION
# ═══════════════════════════════════════════════════════════════════════════
md("## 4. Outlier Detection")

# Individual box plots - one per feature
outlier_features = ['age_years', 'weight_kg', 'days_in_shelter', 'aggression_score',
                    'anxiety_separation', 'reactivity_to_dogs', 'energy_level',
                    'training_level', 'hours_alone_per_day', 'adopter_activity_level',
                    'expectation_score', 'energy_mismatch', 'size_home_mismatch',
                    'visits_before_adoption']

for feat in outlier_features:
    # GRAPH: Box plot for each feature
    code(f"""\
fig, ax = plt.subplots(figsize=(14, 4))
sns.boxplot(data=df, x='{feat}', ax=ax, color='#3498db',
            flierprops=dict(marker='o', markersize=3, alpha=0.4, color='#e74c3c'),
            width=0.5)
Q1 = df['{feat}'].quantile(0.25)
Q3 = df['{feat}'].quantile(0.75)
IQR = Q3 - Q1
n_outliers = ((df['{feat}'] < Q1 - 1.5*IQR) | (df['{feat}'] > Q3 + 1.5*IQR)).sum()
ax.set_title(f'Outlier Detection: {feat}   |   Outliers: {{n_outliers:,}} ({{n_outliers/len(df)*100:.1f}}%)')
plt.tight_layout()
plt.show()
""")

# IQR Summary Table
code("""\
numeric_cols = df.select_dtypes(include=np.number).columns.drop(['returned', 'previously_returned',
    'neutered', 'house_trained', 'first_time_owner', 'household_has_kids',
    'household_has_pets', 'has_yard', 'met_resident_pets', 'adoption_counseling'], errors='ignore')

print("-- IQR Outlier Summary --\\n")
outlier_summary = []
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    n_outliers = ((df[col] < lower) | (df[col] > upper)).sum()
    pct = n_outliers / len(df) * 100
    outlier_summary.append({'Column': col, 'Q1': round(Q1,2), 'Q3': round(Q3,2),
                            'IQR': round(IQR,2), 'Lower': round(lower,2),
                            'Upper': round(upper,2), 'Outliers': n_outliers,
                            'Outlier %': round(pct,2)})

outlier_df = pd.DataFrame(outlier_summary).sort_values('Outlier %', ascending=False)
print(outlier_df.to_string(index=False))
""")

# ═══════════════════════════════════════════════════════════════════════════
# 5. UNIVARIATE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
md("## 5. Univariate Analysis")
md("### 5.1 Distribution of Continuous Features")

cont_features = ['age_years', 'weight_kg', 'days_in_shelter', 'aggression_score',
                 'anxiety_separation', 'reactivity_to_dogs', 'energy_level',
                 'training_level', 'hours_alone_per_day', 'adopter_activity_level',
                 'expectation_score', 'energy_mismatch', 'size_home_mismatch',
                 'days_to_return']

for feat in cont_features:
    # GRAPH: Histogram for each feature
    code(f"""\
fig, ax = plt.subplots(figsize=(14, 6))
sns.histplot(data=df, x='{feat}', kde=True, ax=ax, color='#2ecc71', edgecolor='white', alpha=0.7, bins=50)
mean_val = df['{feat}'].mean()
median_val = df['{feat}'].median()
ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean = {{mean_val:.2f}}')
ax.axvline(median_val, color='blue', linestyle='--', linewidth=2, label=f'Median = {{median_val:.2f}}')
ax.legend(fontsize=12)
skew = df['{feat}'].skew()
ax.set_title(f'Distribution of {feat}   |   Skewness: {{skew:.3f}}')
ax.set_xlabel('{feat}')
ax.set_ylabel('Count')
plt.tight_layout()
plt.show()
""")

md("### 5.2 Distribution of Categorical Features")

cat_features_plot = ['size', 'breed_group', 'intake_type', 'medical_needs', 'home_type']

for feat in cat_features_plot:
    # GRAPH: Count plot for each categorical
    code(f"""\
fig, ax = plt.subplots(figsize=(14, 6))
order = df['{feat}'].value_counts().index
sns.countplot(data=df, x='{feat}', order=order, ax=ax, hue='{feat}',
              palette='Set2', legend=False, edgecolor='white')
ax.set_title(f'Distribution of {feat}')
ax.tick_params(axis='x', rotation=30)
for p in ax.patches:
    ax.annotate(f'{{int(p.get_height()):,}}\\n({{p.get_height()/len(df)*100:.1f}}%)',
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.show()
""")

# GRAPH: Target - Pie chart
md("### 5.3 Adoption Outcome")

code("""\
fig, ax = plt.subplots(figsize=(10, 8))
labels = ['Kept (Success)', 'Returned (Failure)']
sizes = [df['returned'].value_counts()[0], df['returned'].value_counts()[1]]
colors_pie = ['#27ae60', '#e74c3c']
explode = (0.03, 0.08)
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
            autopct='%1.1f%%', shadow=True, startangle=90,
            textprops={'fontsize': 14}, pctdistance=0.85)
for t in autotexts:
    t.set_fontweight('bold')
    t.set_fontsize(16)
centre_circle = plt.Circle((0, 0), 0.55, fc='white')
ax.add_artist(centre_circle)
ax.set_title('Adoption Outcome Distribution (Donut Chart)')
total = sum(sizes)
ax.text(0, 0, f'Total\\n{total:,}', ha='center', va='center', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()
""")

# GRAPH: Return reasons
code("""\
fig, ax = plt.subplots(figsize=(14, 6))
returned_df = df[df['returned'] == 1]
reason_counts = returned_df['return_reason'].value_counts()
colors_r = sns.color_palette('Reds_r', len(reason_counts))
bars = ax.barh(reason_counts.index, reason_counts.values, color=colors_r, edgecolor='white', height=0.6)
ax.set_xlabel('Count')
ax.set_title('Reasons for Dog Return (Returned Dogs Only)')
for bar, v in zip(bars, reason_counts.values):
    pct = v / len(returned_df) * 100
    ax.text(v + 20, bar.get_y() + bar.get_height()/2,
            f'{v:,} ({pct:.1f}%)', va='center', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
""")

# GRAPH: Return reason pie
code("""\
fig, ax = plt.subplots(figsize=(10, 8))
returned_df = df[df['returned'] == 1]
reason_counts = returned_df['return_reason'].value_counts()
reason_counts = reason_counts[reason_counts.index != 'kept']
colors_rp = sns.color_palette('Set2', len(reason_counts))
wedges, texts, autotexts = ax.pie(reason_counts.values, labels=reason_counts.index,
    colors=colors_rp, autopct='%1.1f%%', startangle=140,
    textprops={'fontsize': 12}, pctdistance=0.82)
for t in autotexts:
    t.set_fontweight('bold')
ax.set_title('Return Reason Breakdown (% of Returns)')
plt.tight_layout()
plt.show()
""")

# ═══════════════════════════════════════════════════════════════════════════
# 6. BIVARIATE / TARGET ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
md("## 6. Bivariate / Target Analysis")
md("### 6.1 Numeric Features: Kept vs Returned")

key_numeric = ['age_years', 'weight_kg', 'days_in_shelter', 'aggression_score',
               'anxiety_separation', 'reactivity_to_dogs', 'energy_level',
               'training_level', 'hours_alone_per_day', 'adopter_activity_level',
               'expectation_score', 'energy_mismatch', 'size_home_mismatch',
               'visits_before_adoption']

for feat in key_numeric:
    # GRAPH: KDE for each numeric feature split by return status
    code(f"""\
fig, ax = plt.subplots(figsize=(14, 6))
sns.kdeplot(data=df[df['returned']==0], x='{feat}', ax=ax, label='Kept',
            color='#27ae60', fill=True, alpha=0.35, linewidth=2)
sns.kdeplot(data=df[df['returned']==1], x='{feat}', ax=ax, label='Returned',
            color='#e74c3c', fill=True, alpha=0.35, linewidth=2)
# Add means
m0 = df.loc[df['returned']==0, '{feat}'].mean()
m1 = df.loc[df['returned']==1, '{feat}'].mean()
ax.axvline(m0, color='#27ae60', linestyle='--', linewidth=1.5, alpha=0.8)
ax.axvline(m1, color='#e74c3c', linestyle='--', linewidth=1.5, alpha=0.8)
ax.set_title(f'{feat}: Kept vs Returned   |   Mean Kept={{m0:.2f}}  Mean Returned={{m1:.2f}}')
ax.legend(fontsize=12)
ax.set_ylabel('Density')
plt.tight_layout()
plt.show()
""")

md("### 6.2 Return Rate by Categorical Features")

cat_analysis = ['size', 'breed_group', 'intake_type', 'medical_needs', 'home_type']

for feat in cat_analysis:
    # GRAPH: Return rate bar for each categorical
    code(f"""\
fig, ax = plt.subplots(figsize=(14, 6))
return_rate = df.groupby('{feat}')['returned'].mean().sort_values(ascending=False) * 100
colors_bar = sns.color_palette('RdYlGn_r', len(return_rate))
bars = ax.bar(return_rate.index, return_rate.values, color=colors_bar, edgecolor='white', width=0.6)
ax.set_title(f'Return Rate by {feat}')
ax.set_ylabel('Return Rate (%)')
ax.tick_params(axis='x', rotation=30)
avg = df['returned'].mean() * 100
ax.axhline(avg, color='black', linestyle='--', linewidth=1.5, alpha=0.6, label=f'Overall Avg: {{avg:.1f}}%')
ax.legend(fontsize=12)
for bar, pct in zip(bars, return_rate.values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
            f'{{pct:.1f}}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
""")

md("### 6.3 Return Rate by Binary Features")

binary_features = ['previously_returned', 'neutered', 'house_trained', 'first_time_owner',
                   'household_has_kids', 'household_has_pets', 'has_yard',
                   'met_resident_pets', 'adoption_counseling']

for feat in binary_features:
    # GRAPH: Return rate for each binary feature
    code(f"""\
fig, ax = plt.subplots(figsize=(10, 6))
return_rate = df.groupby('{feat}')['returned'].mean() * 100
counts = df['{feat}'].value_counts().sort_index()
labels = [f'No (0)\\nn={{counts.iloc[0]:,}}', f'Yes (1)\\nn={{counts.iloc[1]:,}}']
bars = ax.bar(labels, return_rate.values, color=['#3498db', '#e67e22'], edgecolor='white', width=0.5)
ax.set_title(f'Return Rate by {feat}')
ax.set_ylabel('Return Rate (%)')
for bar, pct in zip(bars, return_rate.values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
            f'{{pct:.1f}}%', ha='center', va='bottom', fontsize=14, fontweight='bold')
avg = df['returned'].mean() * 100
ax.axhline(avg, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label=f'Overall Avg: {{avg:.1f}}%')
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()
""")

# GRAPH: Stacked bar - return by breed group
md("### 6.4 Adoption Outcome by Breed Group")

code("""\
fig, ax = plt.subplots(figsize=(14, 7))
ct = pd.crosstab(df['breed_group'], df['returned'], normalize='index') * 100
ct.columns = ['Kept %', 'Returned %']
ct = ct.sort_values('Returned %', ascending=True)
ct.plot(kind='barh', stacked=True, ax=ax, color=['#27ae60', '#e74c3c'],
        edgecolor='white', width=0.7)
ax.set_xlabel('Percentage (%)')
ax.set_title('Adoption Outcome by Breed Group (Stacked %)')
ax.legend(fontsize=12, loc='lower right')
for i, (idx, row) in enumerate(ct.iterrows()):
    ax.text(row['Returned %']/2 + row['Kept %'], i,
            f"{row['Returned %']:.1f}%", va='center', ha='center', fontsize=10, fontweight='bold', color='white')
plt.tight_layout()
plt.show()
""")

# GRAPH: Stacked bar - return by home type
code("""\
fig, ax = plt.subplots(figsize=(14, 6))
ct = pd.crosstab(df['home_type'], df['returned'], normalize='index') * 100
ct.columns = ['Kept %', 'Returned %']
ct = ct.sort_values('Returned %', ascending=True)
ct.plot(kind='barh', stacked=True, ax=ax, color=['#27ae60', '#e74c3c'],
        edgecolor='white', width=0.7)
ax.set_xlabel('Percentage (%)')
ax.set_title('Adoption Outcome by Home Type (Stacked %)')
ax.legend(fontsize=12, loc='lower right')
for i, (idx, row) in enumerate(ct.iterrows()):
    ax.text(row['Returned %']/2 + row['Kept %'], i,
            f"{row['Returned %']:.1f}%", va='center', ha='center', fontsize=10, fontweight='bold', color='white')
plt.tight_layout()
plt.show()
""")

# GRAPH: Mean comparison bar chart
md("### 6.5 Mean Feature Values: Kept vs Returned")

code("""\
compare_features = ['aggression_score', 'anxiety_separation', 'reactivity_to_dogs',
                    'energy_level', 'training_level', 'energy_mismatch',
                    'size_home_mismatch', 'expectation_score', 'hours_alone_per_day',
                    'adopter_activity_level', 'days_in_shelter', 'visits_before_adoption']

means_kept = df[df['returned']==0][compare_features].mean()
means_returned = df[df['returned']==1][compare_features].mean()

fig, ax = plt.subplots(figsize=(14, 8))
y = np.arange(len(compare_features))
h = 0.35
ax.barh(y - h/2, means_kept.values, h, label='Kept', color='#27ae60', edgecolor='white')
ax.barh(y + h/2, means_returned.values, h, label='Returned', color='#e74c3c', edgecolor='white')
ax.set_yticks(y)
ax.set_yticklabels(compare_features)
ax.set_xlabel('Mean Value')
ax.set_title('Mean Feature Comparison: Kept vs Returned Dogs')
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()
""")

# ═══════════════════════════════════════════════════════════════════════════
# 7. CORRELATION MATRIX
# ═══════════════════════════════════════════════════════════════════════════
md("## 7. Correlation Matrix & Important Features")

code("""\
# Encode categorical variables for correlation
df_encoded = df.copy()
df_encoded['size'] = df_encoded['size'].map({'small': 0, 'medium': 1, 'large': 2, 'xlarge': 3})
df_encoded['intake_type'] = df_encoded['intake_type'].astype('category').cat.codes
df_encoded['breed_group'] = df_encoded['breed_group'].astype('category').cat.codes
df_encoded['medical_needs'] = df_encoded['medical_needs'].astype('category').cat.codes
df_encoded['home_type'] = df_encoded['home_type'].astype('category').cat.codes
df_encoded['return_reason'] = df_encoded['return_reason'].astype('category').cat.codes

corr_cols = df_encoded.select_dtypes(include=np.number).columns.drop('adoption_id', errors='ignore')
corr_matrix = df_encoded[corr_cols].corr()
print("Correlation matrix computed.")
""")

# GRAPH: Full correlation heatmap
code("""\
fig, ax = plt.subplots(figsize=(22, 18))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=0.5, ax=ax, annot_kws={'size': 8},
            vmin=-1, vmax=1, cbar_kws={'shrink': 0.8, 'label': 'Correlation'})
ax.set_title('Full Correlation Matrix - All Numeric Features')
plt.tight_layout()
plt.show()
""")

# GRAPH: Target correlation bar
code("""\
target_corr = corr_matrix['returned'].drop(['returned', 'days_to_return', 'return_reason'], errors='ignore')
target_corr = target_corr.sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(14, 10))
colors = ['#e74c3c' if v > 0 else '#27ae60' for v in target_corr.values]
bars = ax.barh(target_corr.index, target_corr.values, color=colors, edgecolor='white', height=0.7)
ax.set_xlabel('Correlation Coefficient (Pearson r)')
ax.set_title('Feature Correlation with Return Status')
ax.axvline(0, color='black', linewidth=1)
for bar, val in zip(bars, target_corr.values):
    offset = 0.005 if val >= 0 else -0.005
    ax.text(val + offset, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}', va='center', ha='left' if val >= 0 else 'right', fontsize=10, fontweight='bold')
ax.text(0.02, 0.02, 'Green = Reduces returns    Red = Increases returns',
        transform=ax.transAxes, fontsize=11, style='italic',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.show()
""")

# GRAPH: Top features only (absolute correlation)
code("""\
target_corr_abs = corr_matrix['returned'].drop(['returned', 'days_to_return', 'return_reason'], errors='ignore')
top10 = target_corr_abs.abs().sort_values(ascending=False).head(10)
top10_vals = target_corr_abs[top10.index].sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(14, 7))
colors = ['#e74c3c' if v > 0 else '#27ae60' for v in top10_vals.values]
bars = ax.barh(top10_vals.index, top10_vals.values, color=colors, edgecolor='white', height=0.6)
ax.set_xlabel('Correlation Coefficient')
ax.set_title('Top 10 Features Most Correlated with Dog Returns')
ax.axvline(0, color='black', linewidth=1)
for bar, val in zip(bars, top10_vals.values):
    offset = 0.003 if val >= 0 else -0.003
    ax.text(val + offset, bar.get_y() + bar.get_height()/2,
            f'{val:+.4f}', va='center', ha='left' if val >= 0 else 'right', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
""")

code("""\
print("-- Top Features Most Correlated with Returns --\\n")
target_corr_sorted = corr_matrix['returned'].drop(['returned', 'days_to_return', 'return_reason'], errors='ignore')
top_features = target_corr_sorted[abs(target_corr_sorted) > 0.03].sort_values(key=abs, ascending=False)
for feat, corr_val in top_features.items():
    direction = "INCREASES returns" if corr_val > 0 else "DECREASES returns"
    print(f"  {feat:30s}  r = {corr_val:+.4f}  {direction}")
""")

# ═══════════════════════════════════════════════════════════════════════════
# 8. MULTIVARIATE VISUALIZATIONS
# ═══════════════════════════════════════════════════════════════════════════
md("## 8. Multivariate Visualizations")

# GRAPH: Energy mismatch vs Aggression
md("### 8.1 Scatter Plots")

code("""\
fig, ax = plt.subplots(figsize=(14, 8))
scatter = ax.scatter(df[df['returned']==0]['energy_mismatch'], df[df['returned']==0]['aggression_score'],
                     c=KEPT_COLOR, alpha=0.2, s=12, label='Kept', edgecolors='none')
scatter = ax.scatter(df[df['returned']==1]['energy_mismatch'], df[df['returned']==1]['aggression_score'],
                     c=RETURNED_COLOR, alpha=0.4, s=12, label='Returned', edgecolors='none')
ax.set_xlabel('Energy Mismatch')
ax.set_ylabel('Aggression Score')
ax.set_title('Energy Mismatch vs Aggression Score by Outcome')
ax.legend(fontsize=12, markerscale=3)
plt.tight_layout()
plt.show()
""")

# GRAPH: Training vs Expectation
code("""\
fig, ax = plt.subplots(figsize=(14, 8))
ax.scatter(df[df['returned']==0]['training_level'], df[df['returned']==0]['expectation_score'],
           c=KEPT_COLOR, alpha=0.2, s=12, label='Kept', edgecolors='none')
ax.scatter(df[df['returned']==1]['training_level'], df[df['returned']==1]['expectation_score'],
           c=RETURNED_COLOR, alpha=0.4, s=12, label='Returned', edgecolors='none')
ax.set_xlabel('Training Level')
ax.set_ylabel('Expectation Score')
ax.set_title('Training Level vs Expectation Score by Outcome')
ax.legend(fontsize=12, markerscale=3)
plt.tight_layout()
plt.show()
""")

# GRAPH: Anxiety vs Hours Alone
code("""\
fig, ax = plt.subplots(figsize=(14, 8))
ax.scatter(df[df['returned']==0]['hours_alone_per_day'], df[df['returned']==0]['anxiety_separation'],
           c=KEPT_COLOR, alpha=0.2, s=12, label='Kept', edgecolors='none')
ax.scatter(df[df['returned']==1]['hours_alone_per_day'], df[df['returned']==1]['anxiety_separation'],
           c=RETURNED_COLOR, alpha=0.4, s=12, label='Returned', edgecolors='none')
ax.set_xlabel('Hours Alone Per Day')
ax.set_ylabel('Separation Anxiety Score')
ax.set_title('Hours Alone vs Separation Anxiety by Outcome')
ax.legend(fontsize=12, markerscale=3)
plt.tight_layout()
plt.show()
""")

# GRAPH: Energy level vs Adopter activity
code("""\
fig, ax = plt.subplots(figsize=(14, 8))
ax.scatter(df[df['returned']==0]['adopter_activity_level'], df[df['returned']==0]['energy_level'],
           c=KEPT_COLOR, alpha=0.2, s=12, label='Kept', edgecolors='none')
ax.scatter(df[df['returned']==1]['adopter_activity_level'], df[df['returned']==1]['energy_level'],
           c=RETURNED_COLOR, alpha=0.4, s=12, label='Returned', edgecolors='none')
ax.set_xlabel('Adopter Activity Level')
ax.set_ylabel('Dog Energy Level')
ax.set_title('Adopter Activity vs Dog Energy Level by Outcome')
ax.legend(fontsize=12, markerscale=3)
# Add diagonal reference
lims = [0, max(ax.get_xlim()[1], ax.get_ylim()[1])]
ax.plot(lims, lims, '--', color='gray', alpha=0.5, label='Perfect Match')
plt.tight_layout()
plt.show()
""")

# GRAPH: Heatmap size x home_type
md("### 8.2 Cross-Tabulation Heatmaps")

code("""\
fig, ax = plt.subplots(figsize=(12, 6))
pivot = df.pivot_table(values='returned', index='size', columns='home_type', aggfunc='mean') * 100
order = ['small', 'medium', 'large', 'xlarge']
pivot = pivot.reindex(order)
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, linewidths=2,
            cbar_kws={'label': 'Return Rate (%)'}, annot_kws={'size': 14, 'fontweight': 'bold'})
ax.set_title('Return Rate (%) by Dog Size x Home Type')
ax.set_ylabel('Dog Size')
ax.set_xlabel('Home Type')
plt.tight_layout()
plt.show()
""")

# GRAPH: Heatmap breed x home_type
code("""\
fig, ax = plt.subplots(figsize=(14, 7))
pivot2 = df.pivot_table(values='returned', index='breed_group', columns='home_type', aggfunc='mean') * 100
sns.heatmap(pivot2, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, linewidths=2,
            cbar_kws={'label': 'Return Rate (%)'}, annot_kws={'size': 11, 'fontweight': 'bold'})
ax.set_title('Return Rate (%) by Breed Group x Home Type')
ax.set_ylabel('Breed Group')
ax.set_xlabel('Home Type')
plt.tight_layout()
plt.show()
""")

# GRAPH: Heatmap breed x intake
code("""\
fig, ax = plt.subplots(figsize=(14, 7))
pivot3 = df.pivot_table(values='returned', index='breed_group', columns='intake_type', aggfunc='mean') * 100
sns.heatmap(pivot3, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, linewidths=2,
            cbar_kws={'label': 'Return Rate (%)'}, annot_kws={'size': 11, 'fontweight': 'bold'})
ax.set_title('Return Rate (%) by Breed Group x Intake Type')
ax.set_ylabel('Breed Group')
ax.set_xlabel('Intake Type')
plt.tight_layout()
plt.show()
""")

# GRAPH: Violin plots - one per feature
md("### 8.3 Violin Plots - Risk Factor Distributions")

violin_features = ['energy_mismatch', 'aggression_score', 'anxiety_separation',
                   'size_home_mismatch', 'hours_alone_per_day', 'training_level',
                   'expectation_score', 'reactivity_to_dogs', 'energy_level',
                   'adopter_activity_level', 'days_in_shelter', 'weight_kg']

for feat in violin_features:
    code(f"""\
fig, ax = plt.subplots(figsize=(10, 6))
sns.violinplot(data=df, x='returned', y='{feat}', ax=ax, hue='returned',
               palette={{0: '#27ae60', 1: '#e74c3c'}}, inner='quartile', legend=False)
ax.set_xticklabels(['Kept', 'Returned'], fontsize=13)
ax.set_title(f'Distribution of {feat} by Outcome')
ax.set_xlabel('')
m0 = df.loc[df['returned']==0, '{feat}'].mean()
m1 = df.loc[df['returned']==1, '{feat}'].mean()
ax.text(0.02, 0.95, f'Mean Kept: {{m0:.2f}}  |  Mean Returned: {{m1:.2f}}  |  Diff: {{m1-m0:+.2f}}',
        transform=ax.transAxes, fontsize=11,
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
plt.tight_layout()
plt.show()
""")

# GRAPH: Pair plot
md("### 8.4 Pair Plot - Top Features")

code("""\
top_cols = ['energy_mismatch', 'aggression_score', 'size_home_mismatch',
            'expectation_score', 'training_level', 'returned']
sample = df[top_cols].sample(n=2000, random_state=42)

g = sns.pairplot(sample, hue='returned', palette={0: '#27ae60', 1: '#e74c3c'},
                 diag_kind='kde', plot_kws={'alpha': 0.25, 's': 12, 'edgecolor': 'none'},
                 diag_kws={'fill': True, 'alpha': 0.4}, height=2.5)
g.figure.suptitle('Pair Plot - Top 5 Features by Return Status', fontsize=16, fontweight='bold', y=1.02)
plt.show()
""")

# GRAPH: Days to return distribution
md("### 8.5 Time to Return Analysis")

code("""\
fig, ax = plt.subplots(figsize=(14, 6))
returned_df = df[df['returned'] == 1]
sns.histplot(data=returned_df, x='days_to_return', bins=60, kde=True, ax=ax,
             color='#e74c3c', edgecolor='white', alpha=0.7)
mean_days = returned_df['days_to_return'].mean()
median_days = returned_df['days_to_return'].median()
ax.axvline(mean_days, color='blue', linestyle='--', linewidth=2, label=f'Mean = {mean_days:.1f} days')
ax.axvline(median_days, color='orange', linestyle='--', linewidth=2, label=f'Median = {median_days:.1f} days')
ax.set_title('Distribution of Days to Return (Returned Dogs Only)')
ax.set_xlabel('Days to Return')
ax.set_ylabel('Count')
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()
""")

# GRAPH: Days to return by reason
code("""\
fig, ax = plt.subplots(figsize=(14, 7))
returned_df = df[df['returned'] == 1]
order = returned_df.groupby('return_reason')['days_to_return'].median().sort_values(ascending=False).index
sns.boxplot(data=returned_df, x='return_reason', y='days_to_return', order=order, ax=ax,
            hue='return_reason', palette='Set2', legend=False)
ax.set_title('Days to Return by Return Reason')
ax.set_xlabel('Return Reason')
ax.set_ylabel('Days to Return')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.show()
""")

# GRAPH: Cumulative return curve
code("""\
fig, ax = plt.subplots(figsize=(14, 6))
returned_df = df[df['returned'] == 1].sort_values('days_to_return')
cumulative = np.arange(1, len(returned_df)+1) / len(returned_df) * 100
ax.plot(returned_df['days_to_return'].values, cumulative, color='#e74c3c', linewidth=2.5)
ax.fill_between(returned_df['days_to_return'].values, cumulative, alpha=0.15, color='#e74c3c')
ax.axhline(50, color='gray', linestyle='--', alpha=0.5)
ax.axhline(90, color='gray', linestyle='--', alpha=0.5)
p50 = returned_df['days_to_return'].median()
p90 = returned_df['days_to_return'].quantile(0.9)
ax.axvline(p50, color='blue', linestyle=':', linewidth=1.5)
ax.axvline(p90, color='orange', linestyle=':', linewidth=1.5)
ax.text(p50+2, 52, f'50th: {p50:.0f} days', fontsize=11, color='blue')
ax.text(p90+2, 85, f'90th: {p90:.0f} days', fontsize=11, color='orange')
ax.set_title('Cumulative Return Curve - When Do Returns Happen?')
ax.set_xlabel('Days After Adoption')
ax.set_ylabel('Cumulative % of Returns')
ax.set_ylim(0, 105)
plt.tight_layout()
plt.show()
""")

# GRAPH: Risk score composite
md("### 8.6 Composite Risk Analysis")

code("""\
fig, ax = plt.subplots(figsize=(14, 7))
df['risk_score'] = (df['energy_mismatch'] + df['aggression_score'] + df['size_home_mismatch']) / 3
bins = pd.qcut(df['risk_score'], q=10, labels=[f'Q{i+1}' for i in range(10)])
risk_rate = df.groupby(bins, observed=True)['returned'].mean() * 100

bars = ax.bar(risk_rate.index, risk_rate.values,
              color=plt.cm.RdYlGn_r(np.linspace(0.1, 0.9, len(risk_rate))),
              edgecolor='white', width=0.7)
ax.set_xlabel('Risk Score Decile (Q1=Lowest Risk, Q10=Highest Risk)')
ax.set_ylabel('Return Rate (%)')
ax.set_title('Return Rate by Composite Risk Score Decile\\n(Risk = avg of energy_mismatch + aggression + size_home_mismatch)')
for bar, pct in zip(bars, risk_rate.values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
            f'{pct:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.show()
""")

# GRAPH: Visits impact
md("### 8.7 Impact of Pre-Adoption Visits")

code("""\
fig, ax = plt.subplots(figsize=(14, 6))
visit_rate = df.groupby('visits_before_adoption')['returned'].agg(['mean', 'count'])
visit_rate['return_pct'] = visit_rate['mean'] * 100
visit_rate = visit_rate[visit_rate['count'] >= 50]  # filter small groups

ax.bar(visit_rate.index, visit_rate['return_pct'],
       color=plt.cm.RdYlGn_r(np.linspace(0.8, 0.2, len(visit_rate))),
       edgecolor='white', width=0.7)
ax.set_xlabel('Number of Visits Before Adoption')
ax.set_ylabel('Return Rate (%)')
ax.set_title('Return Rate by Number of Pre-Adoption Visits')
for x, pct, cnt in zip(visit_rate.index, visit_rate['return_pct'], visit_rate['count']):
    ax.text(x, pct + 0.3, f'{pct:.1f}%\\n(n={cnt:,})', ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.show()
""")

# ═══════════════════════════════════════════════════════════════════════════
# 9. FEATURE IMPORTANCE (ML)
# ═══════════════════════════════════════════════════════════════════════════
md("## 9. Feature Importance (Machine Learning)")

code("""\
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, precision_recall_curve

feature_cols = [c for c in df_encoded.select_dtypes(include=np.number).columns
                if c not in ['returned', 'days_to_return', 'return_reason', 'adoption_id']]

X = df_encoded[feature_cols]
y = df_encoded['returned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

rf = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1, class_weight='balanced')
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:, 1]

print("-- Random Forest Classification Report --\\n")
print(classification_report(y_test, y_pred, target_names=['Kept', 'Returned']))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
""")

# GRAPH: Feature Importance
code("""\
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(14, 10))
bars = ax.barh(importances.index, importances.values,
               color=sns.color_palette('viridis', len(importances)), edgecolor='white', height=0.7)
ax.set_xlabel('Feature Importance (Gini Impurity)')
ax.set_title('Random Forest - Feature Importance for Predicting Returns')

for bar, val in zip(bars, importances.values):
    ax.text(val + 0.001, bar.get_y() + bar.get_height()/2,
            f'{val:.4f}', va='center', fontsize=10)

plt.tight_layout()
plt.show()

print("\\n-- Top 10 Most Important Features --")
for feat, imp in importances.tail(10).iloc[::-1].items():
    print(f"  {feat:30s}  importance = {imp:.4f}")
""")

# GRAPH: Top 10 Feature Importance (focused)
code("""\
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
top10 = importances.head(10).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.barh(top10.index, top10.values,
               color=sns.color_palette('rocket', len(top10)), edgecolor='white', height=0.6)
ax.set_xlabel('Feature Importance (Gini Impurity)')
ax.set_title('Top 10 Most Important Features for Predicting Dog Returns')

for bar, val in zip(bars, top10.values):
    ax.text(val + 0.001, bar.get_y() + bar.get_height()/2,
            f'{val:.4f}', va='center', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
""")

# GRAPH: Confusion Matrix
code("""\
from sklearn.metrics import ConfusionMatrixDisplay

fig, ax = plt.subplots(figsize=(8, 7))
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=['Kept', 'Returned'],
                                        cmap='Blues', ax=ax, colorbar=False,
                                        text_kw={'fontsize': 16, 'fontweight': 'bold'})
ax.set_title('Confusion Matrix - Random Forest')
plt.tight_layout()
plt.show()
""")

# GRAPH: ROC Curve
code("""\
fpr, tpr, _ = roc_curve(y_test, y_proba)
auc_score = roc_auc_score(y_test, y_proba)

fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(fpr, tpr, color='#2980b9', linewidth=3, label=f'ROC Curve (AUC = {auc_score:.4f})')
ax.plot([0, 1], [0, 1], 'k--', linewidth=1, alpha=0.5, label='Random Baseline')
ax.fill_between(fpr, tpr, alpha=0.1, color='#2980b9')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title('ROC Curve - Random Forest Classifier')
ax.legend(fontsize=13, loc='lower right')
ax.set_xlim([0, 1])
ax.set_ylim([0, 1.02])
plt.tight_layout()
plt.show()
""")

# GRAPH: Precision-Recall Curve
code("""\
precision, recall, _ = precision_recall_curve(y_test, y_proba)

fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(recall, precision, color='#e67e22', linewidth=3, label='Precision-Recall Curve')
ax.fill_between(recall, precision, alpha=0.1, color='#e67e22')
baseline = y_test.mean()
ax.axhline(baseline, color='gray', linestyle='--', linewidth=1, label=f'Baseline ({baseline:.3f})')
ax.set_xlabel('Recall')
ax.set_ylabel('Precision')
ax.set_title('Precision-Recall Curve - Random Forest Classifier')
ax.legend(fontsize=13)
ax.set_xlim([0, 1])
ax.set_ylim([0, 1.02])
plt.tight_layout()
plt.show()
""")

# ═══════════════════════════════════════════════════════════════════════════
# 10. SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
md("""## 10. Summary - Analysis Results, Advantages, Disadvantages & Actionable Solutions

---

### Key Analysis Findings

| Finding | Detail |
|---------|--------|
| **Dataset Size** | ~42,000 adoption records with 32 features |
| **Return Rate** | Significant portion of adopted dogs are returned to shelters |
| **Top Risk Factors** | Energy mismatch, aggression score, size-home mismatch, expectation score, and training level are the strongest predictors of returns |
| **Behavioral Issues** | Higher aggression scores and separation anxiety significantly increase return probability |
| **Lifestyle Match** | Energy mismatch between dog and adopter is a critical driver of adoption failure |
| **Protective Factors** | Higher training levels, adoption counseling, and meeting resident pets reduce returns |

---

### Advantages of the Dataset & Analysis

1. **Large sample size** (~42K records) provides statistical power and reliable insights
2. **Comprehensive feature set** covers dog behavior, adopter household, and matching factors
3. **Clear target variable** (`returned`) enables supervised learning and direct actionability
4. **Mix of behavioral & situational data** allows for holistic understanding of returns
5. **Both dog-side and adopter-side features** captured, enabling matching optimization
6. **Machine learning feature importance** confirms and quantifies correlation-based findings

---

### Disadvantages & Limitations

1. **Missing temporal dynamics** - no follow-up data after the initial return period
2. **Potential self-reporting bias** - behavioral scores (aggression, anxiety) may be subjectively assessed
3. **No adopter demographics** - age, income, experience level beyond first-time owner flag
4. **Class imbalance** - returned dogs may be underrepresented, potentially affecting model performance
5. **Correlation != Causation** - observed relationships may not imply direct causal effects
6. **Single shelter / region** - results may not generalize to all shelters or geographies

---

### Actionable Solutions

#### For Shelters & Adoption Agencies:
1. **Implement energy-matching assessments** - Systematically evaluate adopter activity levels against dog energy needs to minimize energy mismatch (the top predictor)
2. **Mandatory adoption counseling** - Data shows counseling reduces return rates; make it standard
3. **Pre-adoption training programs** - Invest in basic training for shelter dogs to increase training levels before adoption
4. **Enhanced behavioral screening** - Use standardized aggression and anxiety assessments to better inform adopters
5. **Home-type matching** - Create size-home compatibility guidelines (e.g., large/xlarge dogs -> homes with yards)

#### For Adopters:
6. **Encourage multiple visits** - Dogs adopted after more pre-adoption visits show lower return rates
7. **Resident pet introductions** - Mandate meet-and-greet sessions when adopters have existing pets
8. **Realistic expectation setting** - Provide detailed behavioral profiles and "what to expect" guides
9. **First-time owner support** - Offer extended support packages for first-time dog owners
10. **Post-adoption follow-up** - Implement 30/60/90-day check-in calls to identify and address issues before they lead to returns
""")

# ═══════════════════════════════════════════════════════════════════════════
# ASSEMBLE & SAVE
# ═══════════════════════════════════════════════════════════════════════════
nb.cells = cells
nbf.write(nb, 'Dog_Adoption.ipynb')
print(f"[OK] Notebook saved with {len(cells)} cells ({sum(1 for c in cells if c.cell_type == 'code')} code, {sum(1 for c in cells if c.cell_type == 'markdown')} markdown)")
