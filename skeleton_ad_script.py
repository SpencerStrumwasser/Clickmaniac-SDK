import random
import datetime
from facebookads import adobjects
from facebookads.api import FacebookAdsApi
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.adaccountuser import AdAccountUser
from facebookads.adobjects.adimage import AdImage
from facebookads.adobjects.ad import Ad
from facebookads.adobjects.adcreative import AdCreative


my_app_id = '299363293779254'
my_app_secret = '3ec97126104c50bed63580b6968659fa'
my_access_token = 'EAAEQRPLI1TYBAHa3l1ucdSag0F63XY4YEA7S67rLgmFsXTDARSaO7ZCi8ZBpkKsZAdzU2QWam4SA4E5Vnyd7jKWpHRnvEu7e9yICGKkHFJ5MbJpwQAZAICS78jq82vRotMy5At7uUSmaMJ1ZBtakUoEKgW6hJu87tJH26nVzx5AZDZD'
my_campaign_id = '23842782741690444'

my_ad_account_id = 'act_356288071441451'
my_page_id = '103185246428488'

def get_campaign():
    """
    Fetching your campaign, and checking that you get the right result
    """
    campaign = Campaign(my_campaign_id)
    campaign.remote_read(fields=[Campaign.Field.name, Campaign.Field.objective])
    assert campaign[Campaign.Field.name] == 'We\'re Toast SDK'
    assert campaign[Campaign.Field.objective] == Campaign.Objective.page_likes
    return campaign


def get_ad_set(campaign):
    """
    Retrieving ad sets currently in your campaign 

    Idea for where to start: Use this function to check attributes 
    of the ad sets currently in your campaign and call the 
    create_new_ad_set function. Then return 
    """
    adsets = campaign.get_ad_sets()

    return create_new_ad_set()

def create_new_ad_set():
    """
    Creating a new ad set for the ad account

    You can use the adset.update method specified here:
    https://developers.facebook.com/docs/marketing-api/reference/ad-campaign
    """
    adset = AdSet(parent_id=my_ad_account_id)

    """
    UPDATE/CREATE ADSET HERE
    """
    adset[AdSet.Field.campaign_id] = my_campaign_id
    adset[AdSet.Field.name] = 'Toast_competition'
    adset[AdSet.Field.promoted_object] = {
        'page_id' : my_page_id,
    }
    adset[AdSet.Field.billing_event] = "IMPRESSIONS"
    adset[AdSet.Field.daily_budget] = 200
    adset[AdSet.Field.is_autobid] = True 
    
    adset[AdSet.Field.targeting] = {
        'geo_locations':{
            'countries':['IN']
        },
        'genders': [0],
        'age_min':18,
        'age_max': 40,
        'interests': []



    }

    adset.remote_create()




    image = AdImage(parent_id=my_ad_account_id)
    image[AdImage.Field.filename] = "dog_ads/3.jpg"
    image.remote_create()
    image_hash = image[AdImage.Field.hash]


    creative = AdCreative(parent_id = my_ad_account_id)
    creative[AdCreative.Field.title] = 'Puppy Love'
    creative[AdCreative.Field.body] = '"Like" to find ways to help man\'s best friend.'
    creative[AdCreative.Field.object_id] = my_page_id
    # creative[AdCreative.Field.object_url] = 'https://www.facebook.com/caltech.clickmaniac/'
    creative[AdCreative.Field.image_hash] = image_hash


    ad = Ad(parent_id = my_ad_account_id)
    ad[Ad.Field.name] = 'Pos'
    ad[Ad.Field.adset_id] = adset[AdSet.Field.id]
    ad[Ad.Field.creative] = creative

    ad.remote_create(params={
    'status': Ad.Status.active,
    })
    return adset


if __name__ == "__main__":
    """
    Main function to fetch your campaign, and create an adset
    if one does not exist
    """


    # Setting up the FacebookAdsApi 
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

    campaign = get_campaign()
    print campaign
    adset = get_ad_set(campaign)
    print adset
    # Fetching campaign
    if len(adset.get_ads()) > 0:
        print("# Ads:", len(adset.get_ads()))
    else:
        create_new_ad_set()