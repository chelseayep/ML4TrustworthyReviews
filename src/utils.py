from objects import Review, InputData, OutputData, Business


def convert_dict_to_review(data: dict) -> Review:
    """
    Convert a dictionary to a Review object.
    """
    input_data = InputData(
        text=data.get('text'),
        rating=data.get('rating'),
        images=data.get('images'),
        time=data.get('time'),
        user=data.get('user'),
        business=Business(**data['business']) if data.get('business') else None
    )

    return Review(input=input_data)