import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud

from cdapython import Q
from tests.global_settings import integration_host, integration_table


class CustomDataFrame:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_df(self):
        return self.df

    def plot_column(self, column_name):
        """
        Generate a plot for a specific column based on its data type.
        """
        column = self.df[column_name]
        column_type = column.dtype

        if pd.api.types.is_numeric_dtype(column_type):
            self._plot_numerical_column(column_name)
        elif pd.api.types.is_string_dtype(column_type):
            self._plot_string_column(column_name)
        elif pd.api.types.is_dict_like(column):
            self._plot_dict_column(column_name)

    def _plot_numerical_column(self, column_name):
        """
        Generate a bar chart for a numerical column.
        """
        plt.bar(self.df.index, self.df[column_name])
        plt.title(f"{column_name} bar chart")
        plt.xlabel("Index")
        plt.ylabel(column_name)
        plt.show()

    def _plot_string_column(self, column_name):
        """
        Generate a word cloud for a string column.
        """
        text = " ".join(self.df[column_name])
        wordcloud = WordCloud(width=800, height=800, background_color="white").generate(
            text
        )
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.title(f"{column_name} word cloud")
        plt.show()

    def _plot_dict_column(self, column_name):
        """
        Generate a heatmap for a column of dictionaries.
        """
        keys = list(set(k for d in self.df[column_name] for k in d.keys()))
        values = [[d.get(k, 0) for k in keys] for d in self.df[column_name]]
        df = pd.DataFrame(values, columns=keys)

        plt.figure(figsize=(8, 8))
        sns.heatmap(df, cmap="coolwarm", annot=True, fmt=".0f")
        plt.title(f"{column_name} heatmap")
        plt.show()


df = CustomDataFrame(
    df=Q("sex = 'male'").set_host(integration_host).LIMIT(300).to_dataframe()
)
print(df.get_df().head())
df.plot_column("subject_identifier")
plt.show()
