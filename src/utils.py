from objects import Review, InputData, OutputData, Business, GroundTruth
import json 
import ast

def convert_dict_to_review(id,data: dict) -> Review:
    """
    Convert a dictionary to a Review object.
    """

    business_data = ast.literal_eval(data['business'])
    

    input_data = InputData(
        text=data.get('text'),
        rating=data.get('rating'),
        images=data.get('images'),
        time=data.get('time'),
        user=data.get('user'),
        business= Business(**business_data)  
    )

    truth= GroundTruth(
        spam=data.get('spam')== "TRUE",
        relevance=data.get('relevance') == "TRUE",
        credible=data.get('credible')== "TRUE",
        _sentiment=data.get('sentiment'),
        _informative=data.get('usefullness')
    )


    return Review(id=id,
                  input=input_data,
                  truth=truth
                  )