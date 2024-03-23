# Because the <number> is not consist in all json files, we will use 'sectionId' instead
# Right now the relevant sectionId's = [
#       'POLICIES_DEFAULT',     --> here we need to explore what valuable
#       'BOOK_IT_SIDEBAR',      --> here only relevant maxGuestsCapacity (may be better than taking from metadata)
#       'LISTING_INFO',         --> here we can get all info as listed in website
#       'HIGHLIGHTS_DEFAULT'    --> here we can get all highlights and their description as appears in website
#       'MEET_YOUR_HOST'        --> here we can get host's rating, year of experience etc.
#       'AMENITIES_DEFAULT'     --> The most important, from here we get all amenities as we want
#       'TITLE_DEFAULT'         --> here we can get apartment name as appears in website. good for matching json to website
#       'WHAT_COUNTS_AS_A_PET_MODAL' --> need to check if there's pet allowance there
#       'SLEEPING_ARRANGEMENT_WITH_IMAGES' --> here we can get the sleeping beds count (?)
# ]
#           ^^^ NOTE: Use enum module for that macros (from enum import Enum) ^^^
# amenities = {
#     'Location features': ['private entrance'],
#     'Bedroom and laundry': ['Bed linen', 'SYSTEM_WASHER', 'Dryer'],
#     'Heating and cooling': ['SYSTEM_SNOWFLAKE', 'SYSTEM_THERMOMETER'],
#     'Kitchen and dining': ['SYSTEM_REFRIGERATOR', 'SYSTEM_COOKING_BASICS'],
#     'Internet and office': ['SYSTEM_WI_FI'],
#     'Entertainment': ['SYSTEM_TV']
#
# }
from enum import Enum
import math

class Section(Enum):
    POLICIES = 'POLICIES_DEFAULT'
    LISTING_INFO = 'LISTING_INFO'
    HIGHLIGHTS = 'HIGHLIGHTS_DEFAULT'
    HOST = 'MEET_YOUR_HOST'
    AMENITIES = 'AMENITIES_DEFAULT'
    SLEEP_ARRANGEMENT1 = 'SLEEPING_ARRANGEMENT_WITH_IMAGES'
    SLEEP_ARRANGEMENT2 = 'SLEEPING_ARRANGEMENT_DEFAULT'


class Apartment:
    def __init__(self, json_obj):
        self.data = json_obj['niobeMinimalClientData'][1][1]['data']['presentation']['stayProductDetailPage']['sections']

    def get_super_host(self):
        return self.data['metadata']['loggingContext']['eventDataLogging']['isSuperhost']

    def get_location(self):
        return self.data['metadata']['sharingConfig']['location']

    # def get_host_rate(self):
    #     sections_list = self.data['sections']
    #     for section in sections_list:
    #         if section['sectionId'] == Section.HOST.value:
    #             for host_stat in section['section']['cardData']['stats']:
    #                 if host_stat['label'] == 'Rating':
    #                     host_rate = float(host_stat['value'])
    #                     return host_rate
    #     return None

    def get_num_of_rooms(self):
        room_type = self.data['metadata']['loggingContext']['eventDataLogging']['roomType']
        if room_type.lower().find('private room') != -1:
            return 1

        else:
            sections_list = self.data['sections']
            for section in sections_list:
                if section['sectionId'] == Section.SLEEP_ARRANGEMENT1.value or section['sectionId'] == Section.SLEEP_ARRANGEMENT2.value:
                    room_count = len(section['section']['arrangementDetails'])
                    return room_count

            return math.ceil(self.data['metadata']['loggingContext']['eventDataLogging']['personCapacity'] / 2)


    def get_num_of_guests(self):
        return self.data['metadata']['loggingContext']['eventDataLogging']['personCapacity']

    def get_rate(self):
        return self.data['metadata']['sharingConfig']['starRating']

    def get_review_count(self):
        return self.data['metadata']['sharingConfig']['reviewCount']

    def get_pets_allowed(self):
        sections_list = self.data['sections']
        for section in sections_list:
            if section['sectionId'] == Section.POLICIES.value:
                for house_rule in section['section']['houseRulesSections']:
                    if house_rule['title'] == 'During your stay':
                        for item in house_rule['items']:
                            if item['title'] == 'No pets':
                                return False
                            elif item['title'] == 'Pets allowed':
                                return True

    def _get_amenity(self, amenity_icon_name, amenity_group):
        sections_list = self.data['sections']
        for section in sections_list:
            if section['sectionId'] == Section.AMENITIES.value:
                for group in section['section']['seeAllAmenitiesGroups']:
                    if group['title'] == amenity_group:
                        for amenity in group['amenities']:
                            if amenity['icon'] == amenity_icon_name:
                                return amenity['available']

    def get_wifi(self):
        return self._get_amenity('SYSTEM_WI_FI', 'Internet and office')

    def get_washer(self):
        return self._get_amenity('SYSTEM_WASHER', 'Bedroom and laundry')

    def get_bed_lines(self):
        return self._get_amenity('SYSTEM_BLANKETS', 'Bedroom and laundry')

    def get_tv(self):
        return self._get_amenity('SYSTEM_TV', 'Entertainment')

    def get_cooling(self):
        return self._get_amenity('SYSTEM_SNOWFLAKE', 'Heating and cooling')

    def get_heating(self):
        return self._get_amenity('SYSTEM_THERMOMETER', 'Heating and cooling')

    def get_smoke_alarm(self):
        return self._get_amenity('SYSTEM_DETECTOR_SMOKE', 'Privacy and safety')

    def get_kitchen(self):
        return self._get_amenity('SYSTEM_COOKING_BASICS', 'Kitchen and dining')

    def get_refrigerator(self):
        return self._get_amenity('SYSTEM_REFRIGERATOR', 'Kitchen and dining')

    def get_free_parking(self):
        return self._get_amenity('SYSTEM_MAPS_CAR_RENTAL', 'Parking and facilities')
