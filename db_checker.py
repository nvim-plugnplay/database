import argparse
import json

import pandas as pd
from rich.console import Console
from rich.table import Table

class DatabaseAnalyzer:

    def __init__(self, database_path='database.json'):
        self.database_path = database_path
        self.plugins_df = None
        self.console = Console()
        self.load_database()

    def load_database(self):
        with open(self.database_path, 'r') as file:
            data = json.load(file)
        self.plugins_df = pd.DataFrame.from_dict(data, orient='index')
        self.plugins_df['activity_score'] = (
            self.plugins_df['forks_count'] +
            self.plugins_df['stargazers_count'] -
            self.plugins_df['open_issues_count'])
        self.simplify_language_distribution()

    def simplify_language_distribution(self):
        # Ensure all None values are replaced with 'Unknown' or another placeholder
        # This step ensures that there will be no KeyError when accessing language_counts
        self.plugins_df['language'] = self.plugins_df['language'].fillna(
            'Unknown')

        # Recalculate language counts after filling None values
        language_counts = self.plugins_df['language'].value_counts()

        # Use get to safely access the count for each language, defaulting to 0 if not found
        # This approach avoids KeyError for languages not present in language_counts
        self.plugins_df['simplified_language'] = self.plugins_df[
            'language'].apply(
                lambda x: x if language_counts.get(x, 0) > 1 else 'Other')

    def calculate_statistics(self):
        stats_df = self.plugins_df[[
            'forks_count', 'stargazers_count', 'open_issues_count',
            'activity_score'
        ]].agg(['mean', 'std']).transpose()
        return stats_df

    def get_language_distribution(self):
        return self.plugins_df['simplified_language'].value_counts()

    def get_average_activity_score_by_language(self):
        # Calculate average activity score by language
        return self.plugins_df.groupby(
            'simplified_language')['activity_score'].mean().sort_values(
                ascending=False)

    def get_topics_distribution(self):
        topics_series = self.plugins_df['topics'].explode().value_counts()
        return topics_series.head(10)  # Only the top 5 topics

    def print_summary(self):
        self.console.print(
            f"Total plugins: {len(self.plugins_df)}", style="bold green")

        stats_df = self.calculate_statistics()
        self.console.print("\nStatistical Summary:", style="bold underline")
        self.print_table(stats_df, ['Metric', 'Mean', 'Standard Deviation'])

        lang_dist = self.get_language_distribution()
        self.console.print("\nLanguage distribution:", style="bold underline")
        self.print_table(lang_dist, ['Language', 'Count'])

        avg_activity_score_by_lang = self.get_average_activity_score_by_language(
        )
        self.console.print(
            "\nAverage Activity Score by Language:", style="bold underline")
        self.print_table(
            avg_activity_score_by_lang, ['Language', 'Average Activity Score'])

        topics_distribution = self.get_topics_distribution()
        self.console.print("\nTop Topics distribution:", style="bold underline")
        self.print_table(topics_distribution, ['Topic', 'Count'])

    def print_table(self, data, columns):
        table = Table(show_header=True, header_style="bold magenta")
        for column in columns:
            table.add_column(column, style="dim")
        if isinstance(data, pd.Series):
            for index, value in data.items():
                table.add_row(str(index), str(value))
        else:
            for index, row in data.iterrows():
                table.add_row(index, f"{row['mean']:.2f}", f"{row['std']:.2f}")
        self.console.print(table)

    def print_top_plugins(self):
        # Define the categories and their corresponding column names in the DataFrame
        categories = {
            "Stars": "stargazers_count",
            "Issues": "open_issues_count",
            "Forks": "forks_count"
        }

        for category, column_name in categories.items():
            self.console.print(
                f"\nTop 10 Plugins by {category}:",
                style="bold underline magenta")
            top_plugins = self.plugins_df.nlargest(10,
                                                   column_name)[[column_name]]

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Plugin", style="dim", justify="left")
            table.add_column(category, style="dim", justify="right")

            for plugin_name, row in top_plugins.iterrows():
                table.add_row(plugin_name, str(row[column_name]))

            self.console.print(table)

        total_plugins = len(self.plugins_df)
        lua_plugins = len(self.plugins_df[self.plugins_df['language'] == 'Lua'])
        proportion_lua = (lua_plugins/total_plugins) * 100
        average_activity_score = self.plugins_df['activity_score'].mean()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Total Plugins", style="dim", justify="right")
        table.add_column("Lua Plugins", style="dim", justify="right")
        table.add_column(
            "Proportion of Lua Plugins (%)", style="dim", justify="right")
        table.add_column("Average Activity Score", style="dim", justify="right")

        table.add_row(
            str(total_plugins), str(lua_plugins), f"{proportion_lua:.2f}",
            f"{average_activity_score:.2f}")

        self.console.print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check the database')
    parser.add_argument(
        '--database',
        help='Path to the database file',
        default='database.json',
        type=str)

    args = parser.parse_args()
    analyzer = DatabaseAnalyzer(database_path=args.database)
    analyzer.print_summary()
    analyzer.print_top_plugins()
