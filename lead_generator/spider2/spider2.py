# encoding=utf8
# lead_generation
# Copyright (C) 2019 Hillotech, LLC All Rights Reserved
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import array as arr

import json

import requests

from bs4 import BeautifulSoup as soup

import time

# from ghost import Ghost

import random

import os
import os.path

# ghost = Ghost()  

# with ghost.start() as session:

# Leads Array. This will be what is outputted at the end of this file.
leads = {}

while True:

    # Try to run script, if proxy doesn't connect first time there is an exception error
    try:

        for cycle_count in open("spider2_cycle.txt"):
            current_cycle = cycle_count
            complete_url = "leads_cycle/cycle" + current_cycle + ".txt"
        exit

        #startTime = time.time()
        current_lead_number = 0
        # all_today.txt is a list of all the today files.
        # To get an updated all_today.txt run the get_urls/get_urls.py
        for current_url in open(complete_url):
                # Current URL that the spider is searching through

                # Rotate User Agents
                with open("../user_agents/user_agents.txt") as f:
                    lines = f.readlines()
                    line = random.choice(lines)
                    user_agent = line.rstrip('\r\n')
                # This checks the user agent and prints it
                # check_user_agent = 'https://httpbin.org/user-agent'
                headers = {'User-Agent': user_agent, 'Content-Type': 'application/x-www-form-urlencoded'}
                # print headers
                # response = requests.get(check_user_agent,headers=headers)
                # html = response.content
                # print(response.content)

                # Proxy List
                http_proxy  = "http://0000"
                https_proxy = "http://0000"
                ftp_proxy   = "ftp://0000"
                proxyDict = { 
                            "http"  : http_proxy, 
                            "https" : https_proxy, 
                            "ftp"   : ftp_proxy
                            }

                # This checks the ip address and prints it
                # check_ip_address = 'http://myip-address.com/'

                # So Cragslist won't block IP
                # time.sleep(1)

                # for i in range(100):
                #     try:
                #         ip_response = requests.get(check_ip_address,proxies=proxyDict)
                #        print(i)
                #     except:
                #         break
                # else:
                #     print("failed")
                #     sys.exit(1)


                # So Cragslist won't block IP
                # time.sleep(1)

                # ip_html = soup(ip_response.content, "html.parser")
                # ip_address = ip_html.find("div", {"class":"alert alert-success ip-centr"})
                #print(ip_address)

                # So Cragslist won't block IP
                time.sleep(1)

                # This is the request for Craiglists behind a rotating user agent header and proxy.
                for i in range(100):
                    try:
                        search = requests.get(current_url,headers=headers,proxies=proxyDict)
                        #print(i)
                    except:
                        break
                else:
                    print("failed")
                    sys.exit(1)

                # So Cragslist won't block IP
                time.sleep(1)

                # s_content is the full html page of the current URL.
                s_content = soup(search.content, "html.parser")
                # This looks for the nothing found alert. If it finds it in the HTML.
                # Then it means there are no results so the program will exit.
                # It then goes to the next url to do a search.
                zero_results = s_content.find("div", {"class":"alert alert-sm alert-warning"})
                if zero_results:

                    # If there are no results
                    # print("test")
                    # print current_url

                    exit # Exit the current loop and goes to next URL
                # This will reduce the number of duplicate posts
                else:

                    # If there are results
                    # print("notest")
                    # print current_url

                    # table is the full list of posts on the current url html page
                    remove_nearby = s_content.find_all("li", attrs={'class': "result-row"})

                    # Now we iterate through all the posts in the table
                    for post in remove_nearby:

                        # In the current post of the table if there is a specific tag
                        # <span class="nearby"></span>
                        # Then this is a duplicate posting.
                        nearby_results = post.find("span", {"class":"nearby"})
                        if nearby_results:

                            # If there are nearby results posts which are duplcates
                            # print("test1")
                            # print current_url
                            # print post

                            exit # Exit loop and look at next post in table
                        else:
                            table = post.find("a", attrs={'class': "result-title"})

                            # No nearby tag in current post of table 
                            # print("notest1")
                            # print current_url

                            # print(current_url)
                            # print(table.text)
                            # print(table.get('href'))

                            lead_title = table.text
                            lead_url = table.get('href')

                            leads[current_lead_number] = []

                            leads[current_lead_number].append({'title':lead_title})
                            leads[current_lead_number].append({'url':lead_url})

                            current_lead_number+=1

        # print "Total output =", i, ""
        # print ('The script took {0} second !'.format(time.time() - startTime))

        if (os.path.isfile("test_leads/lead2.json") == True):
            os.remove("test_leads/lead2.json")
        if (os.path.isfile("test_leads/out2_lead.json") == True):
            os.remove("test_leads/out2_lead.json")

        with open("test_leads/lead2.json", 'w') as outfile:  
            json.dump(leads, outfile)
        exit

        if current_cycle == "5":
            with open('spider2_cycle.txt', 'w') as text_file:  
                text_file.write("0")
            exit

        else:
            string_to_int = int(current_cycle)
            string_to_int += 1
            int_to_string = str(string_to_int)
            with open('spider2_cycle.txt', 'w') as text_file:  
                text_file.write(int_to_string)
            exit


    # If there is an exception error, if it's because first attempt at proxy connection fails
    except:
        # back to the top and try again.
        #print "continue"
        continue