import seaborn as sns
import matplotlib.pyplot as plt


class Report:
    def __init__(self):
        self.COLOURS = {
            "Low": "yellow",
            "Medium": "orange",
            "High": "red",
            "Critical": "purple",
        }

    def summary_vulnerabilities(self, df, name):
        df_no_duplicates_subset = df.drop_duplicates(subset=["Name", "Risk"])
        risk_counts = df_no_duplicates_subset["Risk"].value_counts()
        # Plotting as a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(
            risk_counts,
            labels=risk_counts.index,
            autopct=lambda p: f"{round(p * sum(risk_counts)/100,1)}",
            colors=[self.COLOURS[risk] for risk in risk_counts.index],
        )
        plt.title("Distribution of Vulnerabilities by Risk Level")
        plt.savefig(name, bbox_inches="tight", dpi=600)

    def summary_vulnerabilities_per_hosts(self, df, name):
        df["Host"] = df["Host"].str.split(", ")
        df_exploded = df.explode("Host")
        df = df_exploded[["Host", "Risk"]]
        # Count the number of vulnerabilities per host
        host_counts = df["Host"].value_counts().nlargest(10)
        # Filter the DataFrame for the top 10 hosts
        df_top10 = df[df["Host"].isin(host_counts.index)]
        # Plot the bar chart
        plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
        ax = sns.countplot(x="Host", hue="Risk", data=df_top10, palette=self.COLOURS)
        plt.title("Top 10 Hosts with Most Vulnerabilities")
        plt.xlabel("Host")
        plt.ylabel("Count")
        plt.legend(title="Risk")
        # Annotate the bars with counts
        for p in ax.patches:
            height = p.get_height() if p.get_height() > 0 else 0
            ax.text(
                p.get_x() + p.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom" if height > 0 else "top",
            )
        plt.xticks(
            rotation=45, ha="right"
        )  # Rotate x-axis labels for better readability
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        plt.savefig(f"summary_hosts_top10_{name}", dpi=600)
