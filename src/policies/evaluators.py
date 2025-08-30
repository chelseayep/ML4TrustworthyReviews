
import re
from pydantic import BaseModel
from typing import Literal, List
import sys
sys.path.append('/Users/chelsea/Documents/ML4TrustworthyReviews/src')
from objects import Review, Business, OutputData, InputData
from llm import Model

class SpamPolicy:
    def evaluate(self, review: Review) -> bool:
        """
        Evaluate if the review is an advertisement based on presence of URLs and promotional keywords.
        """
        ad_keywords = ['buy', 'discount code', 'offer', 'sale', 'check out', 'subscribe', 'free', 'click here', 'coupon', 'link']
        review_text= review.input['text'].lower()
        keyword_count = sum(1 for kw in ad_keywords if kw in review_text)

        url_regex = r'(https?://\S+|www\.\S+)'
        url_present = re.search(url_regex, review_text) is not None
        
        is_spam = url_present or keyword_count > 2
       
        return is_spam
    


class QualityPolicy:
    def __init__(self, shared_model: Model):
        self.name = "QualityPolicy"
        self.model = shared_model

    def evaluate(self, review: Review) -> str:
        """
        Evaluate the quality of the review based on length and informativeness.
        Returns 'low', 'medium', or 'high'.
        """
        text = review.input['text']
        length = len(text.split())
        
        if length < 5:
            return 'low'

        else:
            coherence = self.coherence_assessment(review) 
            return coherence
           
    def coherence_assessment(self, review: Review) -> str:
        prompt= '''
    You are an expert in evaluating user reviews for businesses. Your task is to assess the coherence of a given review based on the following criteria:
    - Coherence: The review should make sense and be relevant to the business being reviewed. The sentiment should align wiht the rating given (out of 5)
    - Informativeness: High-quality reviews often provide specific details about the user's experience, including aspects like service, product quality, ambiance, etc.
    Reviews that are vague, and do not provide useful information about the business should be rated lower.
    Based on these criteria, classify the review into 'low', 'medium', or 'high' quality. Only respond with the category name, do NOT give explanation.

    "IMPORTANT: Respond ONLY with one of the three words: 'low', 'medium', or 'high'. Do not include any text before or after the word."
    Example:
    Review: "Great food and friendly staff. Will come again!" Rating: 5
    Output: "medium" (short but positive and relevant, could be more detailed)

    Review: "Long wait times and poor service. The food was mediocre at best." Rating: 5
    Output: "medium" (detailed and relevant, but sentiment does not match rating)

    Review: "good" Rating: 4
    Output: "low" (short and vague, lacks detail)

    Review: "The ambiance was wonderful, and the staff were attentive. The pasta was cooked to perfection, though the dessert menu was a bit limited." Rating: 4
    Output: "high" (detailed, relevant, and balanced)
    '''
        
        response= self.model.generate_structured(prompt,review.__repr__())
        return response
    


class EvaluationResult(BaseModel):
    relevance: str = ''
    credibility: str  = '' 

class RelevancePolicy:
    def __init__(self, shared_model: Model):
        self.name = "RelevancePolicy"
        self.description = "Evaluate if the review is relevant to the business."
        self.model = shared_model

        self.prompt= '''
You are an expert in evaluating user reviews for businesses. Your task is to assess a given review based on the following criteria:

1. Relevancy: 'relevant' or 'irrelevant'
- On-topic: The review should discuss aspects related to the business experience. This includes:
  * For restaurants/cafes: food, service, ambiance, staff, prices, atmosphere
  * For attractions/parks/waterfalls: scenery, atmosphere, crowds, accessibility, experience, feelings about the place
  * For hotels: rooms, service, amenities, location, cleanliness
  * For any business: customer experience, what it was like to visit/use the business
- The review should relate to what a visitor would experience at this specific business or location
- Reviews about the atmosphere, surroundings, feelings about a place, or visitor experience are RELEVANT
- Only mark as 'irrelevant' if the review discusses completely unrelated topics or could apply to any random business

Return in a single string: 'relevant' or 'irrelevant'

Examples:
Review: "Great food and friendly staff. Will come again!" Business: "A family-friendly Italian restaurant" 
Output: "relevant"

Review: "It was peaceful and quiet, beautiful scenery." Business: "A waterfall attraction"
Output: "relevant" (describes visitor experience at the location)

Review: "the food was good." Business: "A cafe serving breakfast and lunch"
Output: "relevant"

Review: "I love hiking and outdoor adventures." Business: "A cozy cafe in the city center"
Output: "irrelevant" (not about the cafe experience)

Review: "It was good." Business: "A boutique hotel"
Output: "irrelevant" (too vague, could apply to anything)

Review: "The area has mystical energy and peaceful atmosphere." Business: "Stepstone Falls waterfall"
Output: "relevant" (describes the experience of visiting the waterfall)

    '''

    def evaluate(self, review: Review) -> str:
        response= self.model.generate_structured(self.prompt,review.__repr__())
        # print("Relevance response: ", response)
        return response

class CredibilityPolicy:
    def __init__(self, shared_model: Model):
        self.name = "CredibilityPolicy"
        self.description = "Evaluate if the review is credible."
        self.model = shared_model

        self.prompt= '''
    You are an expert in evaluating user reviews for businesses. Your task is to assess a given review based on the following criteria:
    1. Credibility: 'credible' or 'not credible'
    - Genuine Experience: The review should reflect a real user experience, avoiding overly generic or vague statements. Statements where the user admits to not visiting the business (eg: I heard that.../ I will never go...) should be marked as 'not credible'.
    - Language Use: Credible reviews typically use natural language, while non-credible reviews may exhibit patterns indicative of bot-generated content.
    Based on these criteria, classify the review into the specified categories. Only respond with the category names, do NOT give explanation.
    Evaluate each of these criteria independently.

    Return in a single string: 'credible' or 'not credible'

    Examples:
    Review: "Great food and friendly staff. Will come again!" 
    Output: "credible"
    
    Review: "Best place in town! 5 stars!"
    Output: "not credible" (overly generic, lacks detail)

    Review: "The food was good." 
    Output: "credible" (short but positive and relevant)

    Review: "Sells pet products." 
    Output: "not credible" (too vague, could apply to any business, no personal experience)

    Review: "I heard that this place is terrible." 
    Output: "not credible" (admission of not visiting)

    Review: "Passed by this place, looks nice." 
    Output: "not credible" (no actual experience)

    Review: "The ambiance was wonderful, and the staff were attentive. The pasta was cooked to perfection, though the dessert menu was a bit limited."
    Output: "credible" (detailed and balanced)
    '''

    def evaluate(self, review: Review) -> str:
        response= self.model.generate_structured(self.prompt,review.__repr__())
        # print("Credibility response: ", response)
        return response


class PolicyEvaluator:
    def __init__(self):
        # Create single shared model instance
        self.shared_model = Model(model_name="Qwen/Qwen2.5-VL-3B-Instruct")
        
        # Pass shared model to policies that need LLM
        self.quality_policy = QualityPolicy(self.shared_model)
        self.ad_policy = SpamPolicy()  # No LLM needed
        self.relevance_policy = RelevancePolicy(self.shared_model)
        self.credibility_policy = CredibilityPolicy(self.shared_model)

    def evaluate(self, review: Review) -> Review:
        # Run non-LLM policy first (fastest)
        is_ad = self.ad_policy.evaluate(review)
        
        # If it's an ad, you might want to skip other evaluations
        if is_ad:
            review.evaluation = OutputData(
                review_quality='low',
                spam=is_ad, 
                relevance=False, 
                credible=False
            )
            return review
        
        if not review.input['business'].description:
            is_relevant= 'relevant'  # Default to relevant if no business description
        else:
            is_relevant = self.relevance_policy.evaluate(review)


        is_credible = self.credibility_policy.evaluate(review)
        quality = self.quality_policy.evaluate(review)

        review.evaluation = OutputData(
            review_quality=quality,
            spam=is_ad, 
            relevance=(is_relevant=='relevant'), 
            credible=(is_credible=='credible')
        )

        return review

    # def evaluate_batch(self, reviews: List[Review]) -> List[Review]:
    #     """
    #     Evaluate multiple reviews, potentially with batching optimizations
    #     """
    #     results = []
    #     for review in reviews:
    #         results.append(self.evaluate(review))
    #     return results

    def evaluate_batch(self, reviews: List[Review]) -> List[Review]:
        """
        Evaluate multiple reviews with batching optimizations
        """
        processed_reviews = []
        
        for review in reviews:
            print(f"Evaluating review ID: {review.id}")
            # Step 1: Quick ad detection (no LLM needed)
            is_ad = self.ad_policy.evaluate(review)
            
            if is_ad:
                review.evaluation = OutputData(
                    review_quaity='low',  # Note: keeping your original typo for consistency
                    spam=is_ad, 
                    relevance=False, 
                    credible=False
                )
                processed_reviews.append(review)
                continue
            
            # Step 2: LLM-based evaluations for non-ads
            is_relevant = self.relevance_policy.evaluate(review)
            is_credible = self.credibility_policy.evaluate(review)
            quality = self.quality_policy.evaluate(review)

            review.evaluation = OutputData(
                review_quaity=quality,  # Note: keeping your original typo
                spam=is_ad, 
                relevance=(is_relevant=='relevant'), 
                credible=(is_credible=='credible')
            )
            print(review)
            processed_reviews.append(review)
        
        return processed_reviews

test_review= Review(id=1,input=InputData(
        text= "This place was so peaceful and quiet....not many people out here so you feel the awesome alone in paradise feeling....the area is also full of great energy that has very mystical history surrounding the area.   It's near plain meeting house which has alot of folklore that surrounds the area",
       rating= 5,
        business= Business(
        gmap_id= "0x89e5ce1e71927ddb:0xc25de9369c417b1c",
        name= "Stepstone Falls",
        address= "Stepstone Falls, West Greenwich, RI 02817",
        description= "Set in a wooded area, this picturesque waterfall is a series of gentle cascades over broad ledges.",
        avg_rating= 4.6
        )))

# evaluation_result= PolicyEvaluator()
# policy=RelevancePolicy(evaluation_result.shared_model)
# relevance=policy.evaluate(test_review)
# review=evaluation_result.evaluate(test_review)
# print(review.evaluation)