from dataclasses import dataclass
from typing import List, Optional, TypedDict, Tuple

@dataclass
class Business:
    gmap_id: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    avg_rating: Optional[float] = None  

    def __repr__(self):
        return f"Business(id={self.gmap_id}, name={self.name}, address={self.address}, description={self.description}, avg_rating={self.avg_rating})"
@dataclass
class User:
    user_id: Optional[int]
    name: Optional[str]

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name})"

class InputData(TypedDict):
    text: Optional[str]
    rating: Optional[float]
    images: Optional[List[str]]
    time: Optional[int]
    user: Optional[User]
    business: Optional[Business]

    def __repr__(self):
        return f"InputData(text={self.text}, rating={self.rating}, images={self.images}, time={self.time}, user={self.user}, business={self.business})"

class OutputData(TypedDict):
    review_quaity = ['low', 'medium', 'high'] #based on length, reveiw and rating coherence, informative
    spam: bool #includes advertisments, promotional content
    relevance: bool # on-topic , relative to business description (if available)
    credible: bool # shows genuine user experience, not bot like


class GroundTruth(TypedDict):
    spam: bool
    relevance: bool
    credible: bool
    _sentiment: int
    _informative: bool
    
@dataclass
class Review:
    id: int
    input: InputData
    evaluation: Optional[OutputData] = None
    truth: GroundTruth = None

    def __repr__(self):
        business_desc= self.input['business'].description if self.input['business'] and self.input['business'].description else ''
        return f"Review(text={self.input.get('text', '')}, rating={self.input.get('rating', None)}, business_description={business_desc})"
    
