
from src.objects import Review
from src.llm import Model

class QualityPolicy:
    def __init__(self):
        self.name = "QualityPolicy"
        self.description = "Policy to evaluate the quality of reviews based on length, coherence, relevance, and credibility."
        self.model = Model(model_name="meta-llama/llama-4-maverick-17b-128e-instruct")

    def evaluate(self, review: Review) -> str:
        prompt='''You are an expert in evaluating the quality of user reviews for businesses. Your task is to assess the quality of a given review based on the following criteria:
        1. Length: Reviews should be sufficiently detailed. Very short reviews (e.g., less than 5 words) are typically low quality.
        2. Coherence: The review should make sense and be relevant to the business being reviewed. The sentiment should align wiht the rating given (out of 5)
        3. Informativeness: High-quality reviews often provide specific details about the user's experience, including aspects like service, product quality, ambiance, etc.
        
        Based on these criteria, classify the review into one of three categories: 'low', 'medium', or 'high' quality. Only respond with category name, do NOT give explaination.
        '''
        
        response= self.model.generate_structured(prompt,review.__repr__(), schema=None)
        return response

        

policy=QualityPolicy()
coherence=policy.evaluate_quality(Review(text="The food was great but the service was terrible.", language="en", rating=5, contains_images=False, contains_urls=False))
print("quality:", coherence)