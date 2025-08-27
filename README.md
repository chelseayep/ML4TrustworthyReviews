# ML4TrustworthyReviews



requirements:
1. detect spam/ advertisements
- duplicate entries/ highly specific 
- regex of phone numbers/ 

2. review quality 
- did user actually go? (sentiment analysis)
- rating vs review contradiction
- length of review
- keywords (eg: we/ i) specifics 

- relevance to business (food review at restuarant vs car repair shop)
    - cosine distance to business description?

- keyword analysis: 
    - never been/ friend say/ 

analyse user history
- multiple comments within short period of time
- geographical spread
- consistent 1 star review
- review frequency


analyse business history
- average ratings
- repeated keywords in reviews vs comment


step 1 
expect singular review as input (reviews only) 
- analyse length
- semantic 
- image bool
- rating vs review contradiction
- keyword analysis 
- spam detection: phone number regex

1b: 
- images analysis (menu, image of restaurant) -> yes


step 2: 
batch reviews: 
- analyse user specific behaviour: 
    - user frequency
    - user credibility score?
- duplicate reviews or very similar repeated reviews within batch-> spam

step 3: batch reviews with business info as well
- business description vs review cosine similarity
- business location vs user review locations within time period



RULES:
- if no text/ shorter than 5 words, mark as low quality review or spam
- spam detection: emails, phone number

- mismatched review rating: high rating and low review vice versa





Test data:
- retrieved from google location review scraped from (n=200)
- annotated based on parameters manually (sentiment,)
- augmented using LLM to generate spam and irrelevant reviews which are lacking in the original dataset

