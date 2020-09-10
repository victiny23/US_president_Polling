from bs4 import BeautifulSoup
import requests


def scrape_poll_data():

    url = 'https://projects.fivethirtyeight.com/polls/president-general/'
    html_data = requests.get(url)

    soup = BeautifulSoup(html_data.content, 'html.parser')

    # print(soup.prettify())

    rows = soup.find_all(class_='visible-row')
    pollster_data_array = []
    for row in rows:
        date = row.find(class_='date-wrapper').text

        pollster_grade = row.find(class_='gradeText')
        if pollster_grade != None:
            pollster_grade = pollster_grade.text
        else:
            pollster_grade = 'None'

        pollster = row.find(class_='pollster-container')
        pollster_text = pollster.find_all("a")[-1].text

        # sample = row.find(class_='sample hide-mobile').text
        sample_size = row.find(class_='sample').text
        # sample_type = row.find(class_='sample-type hide-mobile').text
        sample_type = row.find(class_='sample-type').text

        leader = row.find(class_='leader').text
        net = row.find(class_='net').text

        answer = row.find_all(class_='answer')
        value = row.find_all(class_='value')

        if len(value) == 1:
            row_next = row.findNext("tr")
            print(row_next)
            answer_next = row_next.find(class_='answer')
            value_next = row_next.find(class_='value')

            answer.append(answer_next)
            value.append(value_next)

        first_person = answer[0].text
        second_person = answer[1].text

        first_value = value[0].find(class_='heat-map').text
        second_value = value[1].find(class_='heat-map').text

        pollster_data = {
            "date": date,
            "pollster_grade": pollster_grade,
            "pollster_name": pollster_text,
            "sample_size": sample_size,
            "sample_type": sample_type,
            "leader": leader,
            "net": net,
            "first_person": first_person,
            "first_value": first_value,
            "second_person": second_person,
            "second_value": second_value
        }

        pollster_data_array.append(pollster_data)

    return pollster_data_array
