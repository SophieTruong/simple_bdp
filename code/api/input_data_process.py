'''
This file responsible for processing input data into CSV files corresponding to DB schema
TODO: 
    - find a better way to capture 'tenant', 'user' IDs
    - reduce the restrictions imposing with strict input file names
'''

import os
import pandas as pd
import geopandas as gpd

INPUT_PATH = './data_temp/'
OUTPUT_PATH = './data_processed'

if not os.path.exists(OUTPUT_PATH):
    try:
        os.makedirs(OUTPUT_PATH)
    except Exception as e:
        print(e)

def process_file_extension(input_path) -> pd.DataFrame or None:
    """
    Use the correct read method w.r.t file extension and returns a pandas dataframe
    TODO: Make this less strict
    """
    if input_path.split('.')[-1] == 'geojson':
        return gpd.read_file(input_path)
    if input_path.split('.')[-1] == 'gz':
        return pd.read_csv(input_path, compression='gzip', header=0, sep=',', quotechar='"')
    if input_path.split('.')[-1] == 'csv':
        return pd.read_csv(input_path)
    return

def process_review_data(review_df: pd.DataFrame, tenant_id: str, user_id: str) -> None:
    """
    Read input review_df and match it to the correct db schema for REVIEW table
    """
    review_schema = ['listing_id', 'id', 'date', 'reviewer_id', 'reviewer_name', 'comments']
    review_columns = review_df.columns
    
    # TODO: remove bottle neck
    matched_schema = all(c in review_columns for c in review_schema)
    if not matched_schema: 
        return
    
    corrected_review_shema = ['listing_id', 'review_id', 'date', 'reviewer_id', 'reviewer_name', 'comments']
    review_df = review_df.rename(columns={'id': 'review_id'})
    review_df = review_df[corrected_review_shema]
    review_df = review_df.astype({
        'listing_id': 'int64', 
        'review_id': 'int64', 
        'reviewer_id':'int64', 
        'reviewer_name': str, 
        'comments': str
        })
    review_df['date'] = pd.to_datetime(review_df['date'])     
      
    review_df.to_csv(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_reviews.csv')

def process_calendar_price_data(calendar_df: pd.DataFrame, tenant_id: str, user_id: str) -> None:
    """
    Read input calendar_df and match it to the correct db schema for PRICE table
    """
    price_schema = ['listing_id','date','available','price','adjusted_price','minimum_nights','maximum_nights']
    calendar_columns = calendar_df.columns
    
    # TODO: remove bottle neck
    matched_schema = all(c in calendar_columns for c in price_schema)
    if not matched_schema: 
        return
    
    calendar_df= calendar_df[price_schema]
    calendar_df = calendar_df.astype({
        'listing_id': 'int64',
        'available': bool,
        'adjusted_price': 'float32',
        'minimum_nights': 'int32',
        'maximum_nights': 'int32'
        })
    calendar_df['date'] = pd.to_datetime(calendar_df['date'])        
        
    calendar_df['price'] = calendar_df.price.replace('[\$,]','', regex=True).astype(float) 
    calendar_df.to_csv(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_calendar.csv')
   
def process_neighborhood_data(neighborhood_df: pd.DataFrame, tenant_id: str, user_id: str) -> None:
    """
    Read input neighborhood_df and match it to the correct db schema for NEIGHBORHOOD table
    """
    neighborhood_schema = ['neighbourhood', 'neighbourhood_group', 'geometry']
    neighborhood_columns = neighborhood_df.columns
    matched_schema = all(c in neighborhood_columns for c in neighborhood_schema)
    if not matched_schema: 
        return
    neighborhood_df[neighborhood_schema].to_csv(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_neighbourhood.csv')

def process_listing_data(listing_df: pd.DataFrame, tenant_id: str, user_id: str) -> None:
    """
    Read input listing_df and match it to the correct db schema for LISTING, LISTING_REVIEW, HOST, and SCRAPE tables
    """
    minimal_schema = ['id', 'scrape_id', 'host_id', 'neighbourhood']
    if listing_df.shape[1] > 70 and all(c in listing_df.columns for c in minimal_schema):
       
        # Transform listing df:
        listing_df = listing_df.drop(columns=['neighbourhood',
                                              'amenities' # reduce the complexity because this column has Json type
                                              ])
        new_column_names = {"id": "listing_id", 
                            "neighbourhood_cleansed": "neighbourhood", 
                            "neighbourhood_group_cleansed": "neighbourhood_group"}
        listing_df = listing_df.rename(columns=new_column_names)
        
        # Split table into sub tables
        host_schema = [
        'host_id', 'host_url', 'host_name', 'host_since', 'host_location', 'host_about',
        'host_response_time', 'host_response_rate', 'host_acceptance_rate',
        'host_is_superhost', 'host_thumbnail_url', 'host_picture_url',
        'host_neighbourhood', 'host_listings_count',
        'host_total_listings_count', 'host_verifications',
        'host_has_profile_pic', 'host_identity_verified'
        ]
                
        host_df = listing_df[host_schema].drop_duplicates(subset=['host_id'])
        host_df['host_response_rate'] = host_df['host_response_rate'].replace('[%]','', regex=True).astype(float)
        host_df['host_acceptance_rate'] = host_df['host_acceptance_rate'].replace('[%]','', regex=True).astype(float)
        host_df = host_df.astype({
        'host_id': 'int64', 
        'host_url': str, 
        'host_name': str, 
        'host_location': str, 
        'host_about': str,
        'host_response_time': str, 
        'host_response_rate': 'float32', 
        'host_acceptance_rate': 'float32',
        'host_is_superhost': bool, 
        'host_thumbnail_url': str, 
        'host_picture_url': str,
        'host_neighbourhood': str, 
        'host_listings_count': 'int32',
        'host_total_listings_count': 'int32', 
        'host_verifications': str,
        'host_has_profile_pic': bool,
        'host_identity_verified': bool
        })
        host_df['host_since'] = pd.to_datetime(host_df['host_since'])   
        
        listing_df = listing_df.drop(columns=host_schema[1:])
        listing_df = listing_df.astype({
        'listing_id': 'int64', 'listing_url': str, 'name': str, 'description': str, 
        'neighbourhood': str, 'neighbourhood_group': str, 'neighborhood_overview': str, 
        'picture_url': str, 'host_id': 'int64',  'latitude': 'float32', 'longitude': 'float32', 
        'property_type': str, 'room_type': str, 'accommodates': 'float32', 'bathrooms':'float32',
        'bathrooms_text': str, 'bedrooms': 'float32', 'beds': 'float32',
        'minimum_nights': 'float32', 'maximum_nights': 'float32', 'has_availability': bool,  
        'license': str, 'instant_bookable': bool,
        'number_of_reviews': 'int32', 'number_of_reviews_ltm': 'int32', 'number_of_reviews_l30d': 'int32',
        'review_scores_rating': 'float32', 'review_scores_accuracy': 'float32',
        'review_scores_cleanliness': 'float32', 'review_scores_checkin': 'float32',
        'review_scores_communication': 'float32', 'review_scores_location': 'float32',
        'review_scores_value': 'float32', 'reviews_per_month': 'float32',
        'scrape_id': 'int64', 'source': str
        })
        listing_df['first_review'] = pd.to_datetime(listing_df['first_review'])
        listing_df['last_review'] = pd.to_datetime(listing_df['last_review'])
        listing_df['last_scraped'] = pd.to_datetime(listing_df['last_scraped'])  
        listing_df['price'] = listing_df.price.replace('[\$,]','', regex=True).astype(float)
        
        host_df.to_csv(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_host.csv', index=False)
        listing_df.to_csv(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_listing.csv', index=False)

def input_data_split(input_file: str) -> None:    
    if not os.path.exists(INPUT_PATH):
        return
    input_file_path = INPUT_PATH + input_file
    df = process_file_extension(input_file_path)
    if df is not None:
        if 'review' in input_file_path:
            return process_review_data(df, 'tenant1', 'user1')
        if ('calendar' or 'price') in input_file_path:
            return process_calendar_price_data(df, 'tenant1', 'user1')
        if ('neighbourhoods' or 'neighborhoods') in input_file_path:
            return process_neighborhood_data(df, 'tenant1', 'user1')
        if ('listing' or 'list') in input_file_path:
            return process_listing_data(df, 'tenant1', 'user1')
        # TODO: Make this less strict
        return 'Name of input data is not in corresponding to the platform accepted names (review, calendar, price, neighborhood, listing, etc.)'
    return