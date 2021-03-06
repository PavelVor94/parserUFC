import lxml.html as html
import requests
from io import StringIO
from pandas import DataFrame
from threading import Thread
import time




list_events = []
all_figths = []
rows_counts = 0
start = time.time()



def connect_pasrsing(url):
    try:
        response = requests.get(url)
        return html.parse(StringIO(response.content.decode()))
    except:
        print("failed connect" , url)

def parsing_events():
    tree = connect_pasrsing('http://hosteddb.fightmetric.com/statistics/events/completed?page=all')
    rows = tree.xpath('//table[@class="b-statistics__table-events"]/tbody/tr')[1:]
    global rows_counts
    rows_counts = len(rows)
    for row in rows:
        cols = row.xpath('.//td')
        event_info = cols[0].xpath('.//a')
        list_events.append({
        "EVENT": event_info[0].text_content().strip(),
        "LINK":  event_info[0].attrib['href'],
        "DATE":  cols[0].xpath('.//span')[0].text_content().strip(),
        "LOCATION" : cols[1].text_content().strip()
        })
        parsing_event(event_info[0].attrib['href'],event_info[0].text_content().strip(),cols[1].text_content().strip())


def parsing_event(url, event_name, location):
    trees = connect_pasrsing(url)
    if trees:
        for row_in_page in trees.xpath('//tr[contains(@class, "b-fight-details__table-row")]')[1:]:
            colls = row_in_page.xpath('.//td')
            all_figths.append(
                {'FIGHTER_WIN': colls[1][0].text_content().strip(),
                 'FIGHTER_LOSE': colls[1][1].text_content().strip(),
                 'METHOD': colls[7][0].text_content().strip(),
                 'METHOD_DESC': colls[7][1].text_content().strip(),
                 'ROUND': colls[8][0].text_content().strip(),
                 'TIME': colls[9][0].text_content().strip(),
                 'EVENT_NAME': event_name,
                 'LOCATION': location}
                )
    print(f'competed {len(list_events)} of {rows_counts} --- {len(list_events)/rows_counts*100:.2f}%')

parsing_events()


events = DataFrame(list_events)
events.to_csv('./list.csv' , ';' , index=False)

events_result = DataFrame(all_figths)
events_result.to_csv('./result.csv' , ';' , index=False)

print(f'completed in {time.time()-start:.2f} seconds')