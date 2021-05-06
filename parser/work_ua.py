import requests
from bs4 import BeautifulSoup as bs


dict_city = {"николаев": "mykolaiv_nk", "киев": "kyiv",
             "харьков": "kharkiv", "одесса": "odesa"}


def work(user_input, city):
    city = city.lower()
    if city not in dict_city:
        return None

    job = user_input

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.100 Safari/537.36'
    }

    base_url = 'https://www.work.ua/jobs-mykolaiv_nk-бариста/?page=1'

    def remove_gaps(value):
        value = value.replace("        ", " ")  # x8
        value = value.replace("       ", " ")  # x7
        value = value.replace("      ", " ")  # x6
        value = value.replace("     ", " ")  # x5
        value = value.replace("    ", " ")  # x4
        value = value.replace("   ", "\n")  # x3
        value = value.replace(u"\xa0", " ")
        value = value.replace(u"\u2060", " ")
        return value

    def parser(headers, base_url, job):

        jobs = {}
        urls = []

        session = requests.Session()
        request = session.get(base_url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            try:
                pagination = soup.find(
                    'span', attrs={'class': 'text-default'}).text
                pagination_id = list(pagination)
                count = int(pagination_id[-1]) + 1
                for i in range(1, count):
                    url = f'https://www.work.ua/jobs-{dict_city[city]}-{job}/?page={i}'
                    if url not in urls:
                        urls.append(url)
            except:
                pass

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all(
                'div', attrs={'class': 'card card-hover card-visited wordwrap job-link'})
            counter = 0
            for div in divs:
                title = div.find('a').text
                href = 'http://work.ua' + div.find('a')['href']
                info = div.find('p', attrs={'class': 'overflow'}).text

                jobs[counter] = {
                    "title": remove_gaps(title),
                    "href": remove_gaps(href),
                    "info": remove_gaps(info),
                }

                counter += 1

            return jobs

    jobs = parser(headers, base_url, job)

    return jobs
