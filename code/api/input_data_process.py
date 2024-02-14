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
    
    review_df = review_df.rename(columns={'id': 'review_id'})
    corrected_review_shema = ['listing_id', 'review_id', 'date', 'reviewer_id', 'reviewer_name', 'comments']
    review_df[corrected_review_shema].to_parquet(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_reviews.parquet')

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
    
    calendar_df['price'] = calendar_df.price.replace('[\$,]','', regex=True).astype(float)    
    calendar_df[price_schema].to_parquet(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_calendar.parquet')
   
def process_neighborhood_data(neighborhood_df: pd.DataFrame, tenant_id: str, user_id: str) -> None:
    """
    Read input neighborhood_df and match it to the correct db schema for NEIGHBORHOOD table
    """
    neighborhood_schema = ['neighbourhood', 'neighbourhood_group', 'geometry']
    neighborhood_columns = neighborhood_df.columns
    matched_schema = all(c in neighborhood_columns for c in neighborhood_schema)
    if not matched_schema: 
        return
    neighborhood_df[neighborhood_schema].to_parquet(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_neighborhood.parquet')

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
        listing_df['price'] = listing_df.price.replace('[\$,]','', regex=True).astype(float)
        
        # Split table into sub tables
        listing_schema = [
        'listing_id', 'listing_url', 'name', 'description', 
        'neighbourhood', 'neighbourhood_group', 'neighborhood_overview', 
        'picture_url', 'host_id',  'latitude',
        'longitude', 'property_type', 'room_type', 'accommodates', 'bathrooms',
        'bathrooms_text', 'bedrooms', 'beds', 'price', 'minimum_nights', 
        'maximum_nights', 'has_availability',  'license', 'instant_bookable',
        'scrape_id'
        ]
        host_schema = [
        'host_id', 'host_url', 'host_name', 'host_since', 'host_location', 'host_about',
        'host_response_time', 'host_response_rate', 'host_acceptance_rate',
        'host_is_superhost', 'host_thumbnail_url', 'host_picture_url',
        'host_neighbourhood', 'host_listings_count',
        'host_total_listings_count', 'host_verifications',
        'host_has_profile_pic', 'host_identity_verified'
        ]
        listing_review_schema = [
        'listing_id', 'number_of_reviews',
        'number_of_reviews_ltm', 'number_of_reviews_l30d', 'first_review',
        'last_review', 'review_scores_rating', 'review_scores_accuracy',
        'review_scores_cleanliness', 'review_scores_checkin',
        'review_scores_communication', 'review_scores_location',
        'review_scores_value', 'reviews_per_month'
        ]
        scrape_schema = ['scrape_id', 'last_scraped', 'source']
        
        scrape_df = listing_df[scrape_schema].drop_duplicates().reset_index(drop=True)
        listing_review_df = listing_df[listing_review_schema].drop_duplicates().reset_index(drop=True)
        host_df = listing_df[host_schema].drop_duplicates(subset=['host_id']).reset_index(drop=True)
        listing_df = listing_df[listing_schema].reset_index(drop=True)
        
        # Save df to corresponding DB tables: 
        scrape_df.to_parquet(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_scrape.parquet')
        listing_review_df.to_parquet(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_listing-review.parquet')
        host_df.to_parquet(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_host.parquet')
        listing_df.to_parquet(f'{OUTPUT_PATH}/T-{tenant_id}_UID-{user_id}_listing.parquet')

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