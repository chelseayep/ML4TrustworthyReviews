import pandas as pd
import json
from typing import TypedDict, List, Optional
from dataclasses import asdict
from objects import InputData, OutputData, Review, Business, User
import random

def _parse_csv_row(row: pd.Series) -> InputData:
    text= row.get('text', None)
    rating= row.get('rating', None)
    images= row.get('photo', None)
    if pd.isna(images) or images is None:
        images = None
    time = row.get('time', None)
    
    user= User(user_id=row.get('id', None),
        name=row.get('author_name', None))
    
    business = Business(gmap_id=row.get("gmap_id", None),
                        name=row.get('business_name', None))

    json= InputData(
        text=text if pd.notna(text) else None,
        rating=rating if pd.notna(rating) else None,
        images=images if pd.notna(images) else None,
        time=time if pd.notna(time) else None,
        user= user,
        business= business
    )
    return json
    
def parse_csv(path: str) -> list[InputData]:
    df=pd.read_csv(path)
    input_data_list = []
    for _, row in df.iterrows():
        input_data = _parse_csv_row(row)
        input_data_list.append(input_data)
    return input_data_list



def parse_json(path: str,max_lines: int, business_info_path: Optional[str] ) -> list[InputData]:

    input_data_list = []
    random.seed(42)  # For reproducibility
    
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            user = User(
                user_id=data.get('user_id', None),
                name=data.get('name', None))
            
            business = _get_business_by_gmap_id(business_info_path, data.get('gmap_id', None)) if business_info_path else Business(name=data.get('business_name', None), gmap_id=data.get('gmap_id', None))

            input_data = InputData(
                text=data.get('text', None),
                rating=data.get('rating', None),
                images=data.get('pics', None),
                time=data.get('time', None),
                user=user,
                business=business
            )
            
            # Reservoir sampling logic
            if len(input_data_list) < max_lines:
                input_data_list.append(input_data)
            else:
                # Random chance to replace existing item
                j = random.randint(0, i)
                if j < max_lines:
                    input_data_list[j] = input_data
                    
    return input_data_list


def _get_business_by_gmap_id(business_info_path: str, target_id: str) -> Business | None:
    """
    Fetch a business from a JSON file where gmap_id matches target_id.
    Returns a Business object or None if not found.
    """
    with open(business_info_path, 'r', encoding='utf-8') as f:
       for line in f:
            data = json.loads(line)
            if data.get("gmap_id") == target_id:
                return Business(
                    gmap_id=data.get("gmap_id"),
                    name=data.get("name"),
                    address=data.get("address"),
                    description=data.get("description"),
                    avg_rating=data.get("avg_rating"),
                )

def save_to_json(data: List[InputData], path: str):
    """Convert nested dataclasses to dicts and save to JSON."""
    serializable_data = []
    for item in data:
        # Make a shallow copy
        d = dict(item)
        # Convert nested dataclasses
        d['user'] = asdict(d['user'])
        d['business'] = asdict(d['business'])
        serializable_data.append(d)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(serializable_data, f, ensure_ascii=False, indent=2)

# # data= parse_csv("../data/raw/archive/reviews.csv")

data= parse_json("../data/raw/rhode_island/review-Rhode_Island.json", "../data/raw/rhode_island/meta-Rhode_Island.json", max_lines=100)
save_to_json(data, "../data/processed/test_output2.json")