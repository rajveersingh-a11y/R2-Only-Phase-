import matplotlib.pyplot as plt
import seaborn as sns
from app.config import PLOTS_DIR

def generate_plots(pca_df, labels, final_df, explained_var):
    plt.figure(figsize=(8, 6))
    if len(pca_df.columns) >= 2:
        sns.scatterplot(x=pca_df.iloc[:, 0], y=pca_df.iloc[:, 1], hue=labels, palette="deep")
        plt.title("PCA Clusters")
        plt.xlabel("PC1")
        plt.ylabel("PC2")
    plt.savefig(PLOTS_DIR / "pca_scatter_clusters.png")
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.plot(explained_var['cumulative_variance'], marker='o')
    plt.title("PCA Cumulative Explained Variance")
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.savefig(PLOTS_DIR / "explained_variance.png")
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.countplot(data=final_df, x="assigned_phase", order=["A", "B", "C"], palette="viridis")
    plt.title("Final Phase Distribution")
    plt.savefig(PLOTS_DIR / "final_phase_distribution.png")
    plt.close()
