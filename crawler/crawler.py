import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from apartment import Apartment
import time
import argparse
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check_in', dest='check_in', required=True)
    parser.add_argument('--check_out', dest='check_out', required=True)

    return parser.parse_args()


def clean_date(check_in_date, check_out_date):
    seperators = ['.', '/']

    for index, item in enumerate(seperators):
        if item in check_in_date:
            seperator = seperators[index]
            break

    check_in_values = check_in_date.split(seperator)
    check_out_values = check_out_date.split(seperator)

    # Making sure year is in format of yyyy and not yy
    if len(check_in_values[2]) < 4:
        check_in_values[2] = '20' + check_in_values[2]
    if len(check_out_values[2]) < 4:
        check_out_values[2] = '20' + check_out_values[2]

    # Making sure month in format of mm and not m
    if len(check_in_values[1]) < 2:
        check_in_values[1] = '0' + check_in_values[1]
    if len(check_out_values[1]) < 2:
        check_out_values[1] = '0' + check_out_values[1]

    # Making sure day in format of dd and not d
    if len(check_in_values[0]) < 2:
        check_in_values[0] = '0' + check_in_values[0]
    if len(check_out_values[0]) < 2:
        check_out_values[0] = '0' + check_out_values[0]

    return (
        f'{check_in_values[2]}-{check_in_values[1]}-{check_in_values[0]}',
        f'{check_out_values[2]}-{check_out_values[1]}-{check_out_values[0]}'
    )


def get_df(base_url):
    # Set up empty lists for data
    rates = []
    num_of_guests = []
    num_of_rooms = []
    pets_allowed = []
    wifi = []
    super_host = []
    review_count = []
    washer = []
    bed_lines = []
    tv = []
    cooling = []
    heating = []
    smoke_alarm = []
    kitchen = []
    refrigerator = []
    free_parking = []
    prices = []
    locations = []
    apartment_names = []

    try:
        # Loop through the first 15 pages of search results
        for i in range(1, 16):
            print(f"Working on page #{i}...")
            current_url = base_url + f'&page={i}'

            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, "html.parser")

            prices_div = soup.find_all('div', class_='_1jo4hgw')
            apartments_div = soup.find_all('div', class_='t1jojoys dir dir-ltr')

            for aprt in apartments_div:
                apartment_names.append(aprt.text)

            for div in prices_div:
                price_str = div.text.split()

                if len(price_str) > 2:
                    prices.append(int(price_str[1][1:].replace(',', '')))
                else:
                    prices.append(int(price_str[0][1:].replace(',', '')))

            # Find all apartments on the page
            apartments = soup.find_all("div", class_="lxq01kf l1tup9az dir dir-ltr")

            # Loop through each apartment and click on it to get the detailed information
            for index, apartment in tqdm(enumerate(apartments), total=len(apartments), leave=False):
                try:
                    url = "https://www.airbnb.com" + apartment.find("a")["href"]
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, "html.parser")

                    json_data = soup.find('script', id='data-state').text
                    json_obj = json.loads(json_data)

                    # Creating an Apartment object
                    curr_apartment = Apartment(json_obj)

                    # Appending the return value of each apartment to relevant list
                    num_of_rooms.append(curr_apartment.get_num_of_rooms())
                    num_of_guests.append(curr_apartment.get_num_of_guests())
                    rates.append(curr_apartment.get_rate())
                    wifi.append(curr_apartment.get_wifi())
                    pets_allowed.append(curr_apartment.get_pets_allowed())
                    free_parking.append(curr_apartment.get_free_parking())
                    refrigerator.append(curr_apartment.get_refrigerator())
                    kitchen.append(curr_apartment.get_kitchen())
                    smoke_alarm.append(curr_apartment.get_smoke_alarm())
                    heating.append(curr_apartment.get_heating())
                    cooling.append(curr_apartment.get_cooling())
                    tv.append(curr_apartment.get_tv())
                    bed_lines.append(curr_apartment.get_bed_lines())
                    washer.append(curr_apartment.get_washer())
                    review_count.append(curr_apartment.get_review_count())
                    super_host.append(curr_apartment.get_super_host())
                    locations.append(curr_apartment.get_location())


                    # Added 2 seconds sleep between each request in order to prevent block by the website
                    time.sleep(1)
                except Exception as e:
                    print("************** Unknown Error occured **************")
                    print(f"Exception caught: {e}")
                    print("\nAdding None values instead...")
                    num_of_rooms.append(None)
                    num_of_guests.append(None)
                    rates.append(None)
                    wifi.append(None)
                    pets_allowed.append(None)
                    free_parking.append(None)
                    refrigerator.append(None)
                    kitchen.append(None)
                    smoke_alarm.append(None)
                    heating.append(None)
                    cooling.append(None)
                    tv.append(None)
                    bed_lines.append(None)
                    washer.append(None)
                    review_count.append(None)
                    super_host.append(None)
                    locations.append(None)


    except Exception as e:
        print(e)
        print("current url: ", current_url)

    # print("len of locations: ", len(locations))
    # print("len of apartment_names: ", len(apartment_names))
    # print("len of num_of_rooms: ", len(num_of_rooms))
    # print("len of num_of_guests: ", len(num_of_guests))
    # print("len of pets_allowed: ", len(pets_allowed))
    # print("len of wifi: ", len(wifi))
    # print("len of free_parking: ", len(free_parking))
    # print("len of refrigerator: ", len(refrigerator))
    # print("len of kitchen: ", len(kitchen))
    # print("len of smoke_alarm: ", len(smoke_alarm))
    # print("len of cooling: ", len(cooling))
    # print("len of heating: ", len(heating))
    # print("len of tv: ", len(tv))
    # print("len of bed_lines: ", len(bed_lines))
    # print("len of washer: ", len(washer))
    # print("len of super_host: ", len(super_host))
    # print("len of prices: ", len(prices))
    # print("len of review_count: ", len(review_count))
    # print("len of rates: ", len(rates))

    # Create pandas dataframe from data
    data = {
        "Location": locations,
        "Name": apartment_names,
        "Rooms": num_of_rooms,
        "Guests": num_of_guests,
        "Pets": pets_allowed,
        "Wifi": wifi,
        'Free_parking': free_parking,
        'Refrigerator': refrigerator,
        'Kitchen': kitchen,
        'Smoke_alarm': smoke_alarm,
        'Cooling': cooling,
        'Heating': heating,
        'TV': tv,
        'Bed_lines': bed_lines,
        'Washer': washer,
        'Super_host': super_host,
        'Price': prices,
        'Review_count': review_count,
        'Total_rate': rates
    }
    df = pd.DataFrame(data)
    return df


def main():
    # The list of all df after we extract them from the function
    df_list = []

    for index, url in enumerate(urls):
        print("################################################")
        print(f'\t\tURL #{index + 1}')
        print("################################################")

        # df = get_df(url)
        # df.to_csv(f'data_output{index + 1}.csv')
        df_list.append(get_df(url))

    # Appending all df into one big df
    if len(urls) > 1:
        df_concatenated = pd.concat(df_list, axis=0)
    elif len(urls) == 1:
        df_concatenated = pd.DataFrame(df_list[0])

    # Saving all data to csv file
    df_concatenated.to_csv('new_data_output.csv')

if __name__ == "__main__":
    print("Starting crawler...", end='\n\n')
    start_time = time.time()
    args = parse_args()
    check_in, check_out = clean_date(args.check_in, args.check_out)

    # NOTE: in order to check functionality of new method on existing file,
    #       uncomment the below block
    # with open("pet_allowed/apartment.json", 'r') as file:
    #     data = json.load(file)
    #     apart = Apartment(data)
    #     host_rating = apart.get_wifi()
    #     print(type(host_rating), host_rating)
    #     exit(0)

    # Each url is the first page out of 15 pages
    urls = [
        f"https://www.airbnb.com/s/Los-Angeles--CA--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/New-York--NY--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/Miami--Florida--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/Chicago--IL--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/Washington--DC--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/Boston--MA--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/Baltimore--MD--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/San-Francisco--CA--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/Seattle--WA--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/Phonex-Az--Phoenix--AZ--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query",
        f"https://www.airbnb.com/s/San-Antonio--TX--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query"
        # f"https://www.airbnb.com/s/Orlando--FL--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query"
        # f"https://www.airbnb.com/s/Orlando--FL--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}&source=structured_search_input_header&search_type=search_query"
    ]

    main()
    end_time = time.time()

    print(f"Total time for crawling: {end_time - start_time} seconds")
