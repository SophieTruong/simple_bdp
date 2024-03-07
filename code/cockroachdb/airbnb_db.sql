SET sql_safe_updates = FALSE;

DROP DATABASE IF EXISTS airbnb_test CASCADE;

USE default;
-- DROP DATABASE airbnb_test CASCADE;

CREATE DATABASE IF NOT EXISTS airbnb_test;

USE airbnb_test;

CREATE TABLE IF NOT EXISTS host (
    host_id INT PRIMARY KEY NOT NULL,
    host_url STRING,
    host_name STRING,
    host_since DATE,
    host_location STRING,
    host_about STRING,
    host_response_time STRING,
    host_response_rate FLOAT,
    host_acceptance_rate FLOAT,
    host_is_superhost BOOL,
    host_thumbnail_url STRING,
    host_picture_url STRING,
    host_neighbourhood STRING,
    host_listings_count INT,
    host_total_listings_count INT,
    host_verifications STRING,
    host_has_profile_pic BOOL,
    host_identity_verified BOOL);

CREATE TABLE IF NOT EXISTS neighbourhood (
    neighbourhood STRING PRIMARY KEY NOT NULL,
    neighbourhood_group STRING,
    geometry GEOMETRY);

CREATE TABLE IF NOT EXISTS listing (
    listing_id INT PRIMARY KEY NOT NULL,
    listing_url STRING,
    name STRING,
    description STRING,
    neighbourhood STRING,
    neighbourhood_group STRING,
    neighborhood_overview STRING,
    picture_url STRING,
    host_id INT,
    latitude FLOAT,
    longitude FLOAT,
    property_type STRING,
    room_type STRING,
    accommodates STRING,
    bathrooms FLOAT,
    bathrooms_text STRING,
    bedrooms FLOAT,
    beds FLOAT,
    price FLOAT,
    minimum_nights FLOAT,
    maximum_nights FLOAT,
    has_availability BOOL,
    license STRING,
    instant_bookable BOOL,
    scrape_id INT,
    number_of_reviews INT,
    number_of_reviews_ltm INT,
    number_of_reviews_l30d INT,
    first_review DATE,
    last_review DATE,
    review_scores_rating FLOAT,
    review_scores_accuracy FLOAT,
    review_scores_cleanliness FLOAT,
    review_scores_checkin FLOAT,
    review_scores_communication FLOAT,
    review_scores_location FLOAT,
    review_scores_value FLOAT,
    reviews_per_month FLOAT,
    last_scraped DATE,
    source STRING
    -- CONSTRAINT fk_neighborhood_ref_listing FOREIGN KEY (neighbourhood) REFERENCES neighbourhood(neighbourhood) ON DELETE CASCADE,
    -- CONSTRAINT fk_host_ref_listing FOREIGN KEY (host_id) REFERENCES host(host_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS calendar (
    listing_id INT,
    date DATE,
    available BOOL,
    price FLOAT,
    adjusted_price FLOAT,
    minimum_nights INT,
    maximum_nights INT,
    CONSTRAINT "primary" PRIMARY KEY (listing_id ASC, date ASC)
    -- CONSTRAINT fk_listing_ref_calendar FOREIGN KEY (listing_id) REFERENCES listing(listing_id) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS review (
    listing_id INT,
    date DATE,
    review_id INT PRIMARY KEY NOT NULL,
    reviewer_id STRING,
    reviewer_name STRING,
    comments STRING
    -- CONSTRAINT fk_listing_ref_review FOREIGN KEY (listing_id) REFERENCES listing(listing_id) ON DELETE CASCADE
    );