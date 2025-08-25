from dataclasses import dataclass
from typing import List, Optional, TypedDict, Tuple


@dataclass
class Business:
    gmap_id: Optional[str]
    name: Optional[str]
    # address: Optional[str]
    # location: Optional[Tuple[float,float]]  # (latitude, longitude)
    # description: Optional[str]
    # avg_rating: Optional[float]   
    # no_of_reviews: Optional[int]
    # services: Optional[List[str]]
    # category: Optional[List[str]]

    def __repr__(self):
        return f"Business(id={self.gmap_id}, name={self.name})"

@dataclass
class User:
    user_id: Optional[int]
    name: Optional[str]
    # location: Optional[str]
    # reviews_given: Optional[int]
    # avg_rating: Optional[float]
    # credibility_score: float

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name})"

class InputData(TypedDict):
    text: Optional[str]
    rating: Optional[float]
    images: Optional[List[str]]
    time: Optional[int]
    user: Optional[User]
    business: Optional[Business]

class OutputData(TypedDict):
    review_quaity: int
    reasoning: str
    confidence: int
    spam: bool
    irrelevant: bool
    rant_without_visit: bool

@dataclass
class Review:
    text: str
    language: str
    rating: Optional[int]
    length: int
    contains_images: bool
    contains_urls: bool
    embeddings: Optional[List[float]] = None


