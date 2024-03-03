import json

import pandas as pd
from tabulate import tabulate

with open('database.json', 'r') as file:
    data = json.load(file)
    plugins_df = pd.DataFrame.from_dict(data, orient='index')

language_distribution = plugins_df['language'].value_counts()
plugins_df['activity_score'] = plugins_df['forks_count'] + plugins_df[
    'stargazers_count'] - plugins_df['open_issues_count']
average_activity_score = plugins_df['activity_score'].mean()

topics_series = plugins_df['topics'].explode().value_counts()

print(f"Total plugins: {len(plugins_df)}")
print(f"Lua plugins: {plugins_df[plugins_df['language'] == 'Lua'].shape[0]}")
print(
    f"Proportion of Lua plugins: {plugins_df[plugins_df['language'] == 'Lua'].shape[0] / len(plugins_df) * 100:.2f}%"
)
print(f"Average activity score: {average_activity_score:.2f}\n")

print("Language distribution:")
print(
    tabulate(
        language_distribution.reset_index().values,
        headers=['Language', 'Count']))

print("\nTopics distribution:")
if not topics_series.empty:
    print(
        tabulate(
            topics_series.reset_index().values, headers=['Topic', 'Count']))
else:
    print("No topics available.")

# Top plugins by forks, stars, and issues
top_forks = plugins_df.nlargest(5, 'forks_count')[['forks_count']]
top_stars = plugins_df.nlargest(5, 'stargazers_count')[['stargazers_count']]
top_issues = plugins_df.nlargest(5, 'open_issues_count')[['open_issues_count']]

print("Top 5 Plugins by Forks:")
print(
    tabulate(top_forks.reset_index().values, headers=['Plugin', 'Forks']), "\n")

print("Top 5 Plugins by Stars:")
print(
    tabulate(top_stars.reset_index().values, headers=['Plugin', 'Stars']), "\n")

print("Top 5 Plugins by Issues:")
print(
    tabulate(top_issues.reset_index().values, headers=['Plugin', 'Issues']),
    "\n")
