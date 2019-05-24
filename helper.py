import requests
from bs4 import BeautifulSoup


def get_item_list_by_param(param):

    search_url = "https://us.tamrieltradecentre.com/api/pc/Trade/GetItemAutoComplete?term=" + param

    market_response = requests.get(search_url).json()

    return market_response


def scrap_item_data(item_id):

    search_url = "https://us.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=" + item_id + \
                 "&SortBy=LastSeen&Order=desc"

    item_data = requests.get(search_url).content

    parsed_data = BeautifulSoup(item_data, 'html.parser')

    item_table_html = parsed_data.find("table", {"class": "trade-list-table"})

    item_row_html = item_table_html.find_all("tr", {"class": "cursor-pointer"})

    for row in item_row_html:
        item_data_html = row.find_all("td")
        for each_index in range(len(item_data_html)):
            if len(item_data_html[2].find_all("div")) > 1:
                trader_location = item_data_html[2].find_all("div")[0].text.strip()
                trade_guild_name = item_data_html[2].find_all("div")[1].text.strip()
            else:
                trader_location = "Unknown"
                trade_guild_name = "Unknown"

            individual_price = item_data_html[3].find_all("img")[0].next_sibling.strip()
            item_counts = item_data_html[3].find_all("img")[1].next_sibling.strip()
            total_price = item_data_html[3].find_all("img")[2].next_sibling.strip()

            creation_date = item_data_html[4].attrs["data-mins-elapsed"]

            print(f"---------{creation_date} Mins Ago---------")
            print(f"Trader Location - {trader_location}")
            print(f"Trader Name - {trade_guild_name}")
            print(f"{individual_price} x {item_counts} = {total_price}")
            print("----------------------------\n")


def show_item_list_view(item_list):
    print("Response from Market")
    for i in range(len(item_list)):
        print(f"{i} - {item_list[i]['value']}")

    while True:
        item_id = input("Choose the item you want to check the price!\n")
        if len(item_list) > int(item_id) >= 0:
            break

        print(f"Please make selection within the range between (0 - {len(item_list) - 1})")

    print(f"Chosen Item {item_list[int(item_id)]['value']}")

    return item_id


item_list = get_item_list_by_param('Julianos')

user_choice = show_item_list_view(item_list)

scrap_item_data(user_choice)
