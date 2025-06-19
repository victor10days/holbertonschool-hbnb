class Review:
    def __init__(self, review_id: int, user_id: int, product_id: int, rating: float, comment: str):
        self.review_id = review_id
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f"Review(review_id={self.review_id}, user_id={self.user_id}, product_id={self.product_id}, rating={self.rating}, comment='{self.comment}')"
