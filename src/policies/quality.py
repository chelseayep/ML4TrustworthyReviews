from objects import Review, Business, OutputData, InputData
from llm import Model
import re
from pydantic import BaseModel
from typing import Literal


class AdvertisementPolicy:
    def evaluate(self, review: Review) -> bool:
        """
        Evaluate if the review is an advertisement based on presence of URLs and promotional keywords.
        """
        ad_keywords = ['buy', 'discount code', 'offer', 'sale', 'check out', 'subscribe', 'free', 'click here']
        review_text= review.input['text'].lower()
        keyword_count = sum(1 for kw in ad_keywords if kw in review_text)

        url_regex = r'(https?://\S+|www\.\S+)'
        url_present = re.search(url_regex, review_text) is not None
        
        is_ad = url_present or keyword_count > 0
       
        return is_ad
    
class EvaluationResult(BaseModel):
    quality: str
    relevance: str
    credibility: str

class CompositePolicy:
    def __init__(self):
        self.name = "CompositePolicy"
        self.description = "Composite policy combining quality, relevancy, and credibility evaluations."
        self.model = Model(model_name="meta-llama/llama-4-maverick-17b-128e-instruct")

        self.prompt='''
    You are an expert in evaluating user reviews for businesses. Your task is to assess a given review based on the following criteria:
    1. Quality: 'low', 'medium', or 'high' 
    - Length: Reviews should be sufficiently detailed. Very short reviews (e.g., less than 5 words) are typically low quality.
    - Coherence: The review should make sense and be relevant to the business being reviewed. The sentiment should align wiht the rating given (out of 5)
    - Informativeness: High-quality reviews often provide specific details about the user's experience, including aspects like service, product quality, ambiance, etc.
        
    2. Relevancy: 'relevant' or 'irrelevant'
    - On-topic: The review should discuss aspects related to the business, such as products, services, customer experience, ambiance, etc. Reference the business description if available.

    3. Credibility: 'credible' or 'not credible'
    - Genuine Experience: The review should reflect a real user experience, avoiding overly generic or vague statements. Statements where the user admits to not visiting the business (eg: I heard that.../ I will never go...) should be marked as 'not credible'.
    - Language Use: Credible reviews typically use natural language, while non-credible reviews may exhibit patterns indicative of bot-generated content.

    Based on these criteria, classify the review into the specified categories. Only respond with the category names, do NOT give explanation.
    Evaluate each of these criteria independently.
    '''


    def evaluate(self, review: Review) -> EvaluationResult:
        response= self.model.generate_structured(self.prompt,review.__repr__(), schema=EvaluationResult)
        print(f"response_type: f{type(response)}")
        return response


class PolicyEvaluator:
    def __init__(self):
        self.ad_policy = AdvertisementPolicy()
        self.eval_policy = CompositePolicy()

    def evaluate(self, review: Review) -> Review:
        
        is_ad = self.ad_policy.evaluate(review)
        composite_eval = self.eval_policy.evaluate(review)
        review.evaluation = OutputData(review_quaity=composite_eval.quality,
                                       spam=is_ad, 
                                       relevance=(composite_eval.relevance=='relevant'), 
                                       credible=(composite_eval.credibility=='credible')
            
        )

        return review




policy=CompositePolicy()
if __name__ == "__main__":

    review=Review(input=InputData(
        text= "This place was so peaceful and quiet....not many people out here so you feel the awesome alone in paradise feeling....the area is also full of great energy that has very mystical history surrounding the area.   It's near plain meeting house which has alot of folklore that surrounds the area",
       rating= 5,
        business= Business(
        gmap_id= "0x89e5ce1e71927ddb:0xc25de9369c417b1c",
        name= "Stepstone Falls",
        address= "Stepstone Falls, West Greenwich, RI 02817",
        description= "Set in a wooded area, this picturesque waterfall is a series of gentle cascades over broad ledges.",
        avg_rating= 4.6
        )))
    
    result= policy.evaluate(review)
    print(result)