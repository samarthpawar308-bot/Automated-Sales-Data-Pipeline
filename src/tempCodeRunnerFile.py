    duplicate_reviews = df[
            df["review_id"].duplicated(keep=False)
        ]

        print("Duplicate review rows:", len(duplicate_reviews))

        print(duplicate_reviews[
            ["review_id", "order_id", "review_score"]
        ].head(10))

