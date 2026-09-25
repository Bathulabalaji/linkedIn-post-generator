
import json
import pandas as pd


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            self.df["length"] = self.df["line_count"].apply(self.catergorize_length)
            all_tags = self.df["tags"].apply(lambda x:x).sum()
            self.unique_tags = set(list(all_tags))


    def catergorize_length(self, line_count):
        if line_count<5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"
    def get_tags(self):
        return self.unique_tags


    def get_posts(self, tag, length, language):
        df_filtered = self.df[
            (self.df["length"]==length) & 
            (self.df["language"]==language) &
            (self.df["tags"].apply(lambda tags: tag in tags))
        ]

        return df_filtered.to_dict(orient="records")


fs = FewShotPosts()
