'''import re
import requests
from bs4 import BeautifulSoup
from .models import Profile
from datetime import datetime
import datetime
from selenium import webdriver
import time
def my_job():
    profiles = Profile.objects.all()
    for profile in profiles:
        #spoj
        y = profile.spoj_username
        pages = []
        count = 0
        count2 = 0
        output = " "
        stop = 0
        flag5 = 1
        today = datetime.date.today()
        url5 = 'http://www.spoj.com/users/' + y
        r5 = requests.get(url5)
        soup5 = BeautifulSoup(r5.content, "html.parser")
        x5 = soup5.find("div", {"class": "col-md-3"})
        if x5 is None:
            flag5 = 0
        if flag5 is 1:
            for a in range(0, 5):
                url = 'http://www.spoj.com/status/' + y + '/all/start=' + str(a * 20)
                pages.append(url)
            for item in pages:
                page = requests.get(item)
                soup = BeautifulSoup(page.content, "html.parser")
                artist_name_list = soup.find_all("tr", {"class": "kol1"})
                artist_name_list2 = soup.find_all("tr", {"class": "kol2"})
                artist_name_list3 = soup.find_all("tr", {"class": "kol3"})
                for i in artist_name_list:
                    count += 1
                    for j in i.contents[3].text:
                        if j != " ":
                            output += j
                        else:
                            output = output.strip()
                            x = int(output[:4])
                            y = int(output[5:7])
                            z = int(output[8:10])
                            some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                            pastday = today - datetime.timedelta(days=30)
                            past = pastday.strftime('%Y-%m-%d')
                            if (some2 > past):
                                count2 += 1
                            else:
                                stop = 1
                            output = " "
                            break
                    if (stop == 1):
                        break
                for i in artist_name_list2:
                    count += 1
                    for j in i.contents[3].text:
                        if j != " ":
                            output += j
                        else:
                            output = output.strip()
                            x = int(output[:4])
                            y = int(output[5:7])
                            z = int(output[8:10])
                            some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                            pastday = today - datetime.timedelta(days=10)
                            past = pastday.strftime('%Y-%m-%d')
                            if (some2 > past):
                                count2 += 1
                            else:
                                stop = 1
                            output = " "
                            break
                    if (stop == 1):
                        break
                for i in artist_name_list3:
                    count += 1
                    for j in i.contents[3].text:
                        if j != " ":
                            output += j
                        else:
                            output = output.strip()
                            x = int(output[:4])
                            y = int(output[5:7])
                            z = int(output[8:10])
                            some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                            pastday = today - datetime.timedelta(days=10)
                            past = pastday.strftime('%Y-%m-%d')
                            if (some2 > past):
                                count2 += 1
                            else:
                                stop = 1
                            output = " "
                            break
                    if (stop == 1):
                        break
                if (stop == 1):
                    break
        try:
            output = int(count2)
            profile.spoj_rating = output
            spoj_ouput = output
            profile.save()
        except ValueError:
            pass


        #codechef


        x = profile.codechef_username
        url = "https://www.codechef.com/recent/user?page=0&user_handle="+x+"&_=1510300136417"
        pages = []
        r = requests.get(url)
        today = datetime.date.today()
        soup = BeautifulSoup(r.content, "html.parser")
        output2 = " "
        for j in soup.text[12:]:
            if j != ",":
                output2 += j
            else:
                break
        output2 = int(output2)
        count = 0
        accepted = 0
        count2 = 0
        stop = 0
        num_of_pages = 0
        for a in range(0, output2):
            url = "https://www.codechef.com/recent/user?page=" + str(a) + "&user_handle="+x+"&_=1510300136417"
            pages.append(url)
        for i in pages:
            count += 1
        for item in pages:
            num_of_pages += 1
            r = requests.get(item)
            soup = BeautifulSoup(r.content, "html.parser")
            g_data3 = soup.find_all("td")
            count = 0
            for item3 in g_data3:
                if (count % 4 == 0):
                    output = item3.contents[0]
                    wordList = re.sub("[^\w]", " ", output).split()
                    if wordList.__len__() > 2:
                        streee = wordList[2]
                        if streee == 'ago':
                            case = today
                            case = case.replace(case.year - 2000)
                            case = case.strftime('%d\/%m\/%Y')
                            output = "12:12 PM " + case + "<\/td>"
                elif count % 2 == 0:
                    flag = 0
                    points = []
                    for j in item3.contents[0]:
                        flag += 1
                    if (flag == 6):
                        counter = 0
                        for j in item3.contents[0]:
                            counter += 1
                            if (counter == 3):
                                points.append(str(j))
                    if (points == ['100']):
                        accepted += 1
                        x = output
                        x = int(output[9:11])
                        y = int(output[13:15])
                        z = 2000
                        z = z + int(output[17:19])
                        some2 = datetime.date(z, y, x).strftime('%Y-%m-%d')
                        pastday = today - datetime.timedelta(days=11)
                        past = pastday.strftime('%Y-%m-%d')
                        if (some2 > past):
                            count2 += 1
                        else:
                            stop = 1
                        output = " "
                count += 1
                if (stop == 1):
                    break
            if (stop == 1):
                break
        try:
            output = int(count2)
            profile.codechef_rating = output
            codechef_output = output
            profile.save()
        except ValueError:
            pass

        #hacker earth

        z = profile.hacker_earth_username
        flag11 = 1
        count4 = 0
        if z == "":
            flag11 = 0
        if flag11 == 1:
            driver = webdriver.Chrome()
            driver.get('https://www.hackerearth.com/submissions/' + z)
            html = driver.page_source
            today = datetime.date.today()
            pastday = today - datetime.timedelta(days=30)
            past = pastday.strftime('%Y-%m-%d')
            count = 0
            count2 = 0
            count3 = 0
            count4 = 0
            array1 = []
            array2 = []
            array3 = []
            array4 = []
            flag10 = 1
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup.find_all("i"):
                count2 += 1
                output = tag.get('title')
                array1.append(output)
            if array1 is None:
                flag10 = 0
            if flag10 is 1:
                for tag2 in soup.find_all("span", {"class": "tool-tip gray-text"}):
                    out2 = tag2.get('title')
                    array2.append(out2[:10])
                for tag2 in soup.find_all("a", {"class": "hover-link gray-text tool-tip"}):
                    out2 = tag2.get('title')
                    x = int(out2[:4])
                    y = int(out2[5:7])
                    z = int(out2[8:10])
                    some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                    if past > some2:
                        break
                    else:
                        array2.append(out2[:10])
                array1 = array1[3:]
                i = 0
                while (i < len(array1) and count3 < len(array2)):
                    x = array1[i]
                    if x is None:
                        i += 2
                        count3 += 1
                    elif x[:17] == "Solution Accepted":
                        count += 1
                        i += 1
                        array3.append(x[:17])
                        array4.append(array2[count3])
                        count3 += 1
                    else:
                        i += 1
                        count += 1
                        count3 += 1
                for i in range(0, len(array4)):
                    x = int(array4[i][:4])
                    y = int(array4[i][5:7])
                    z = int(array4[i][8:10])
                    some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                    if (some2 > past):
                        count4 += 1
                time.sleep(40)
                driver.quit()
        try:
            output = count4
            print(output)
            profile.hacker_earth_rating = output
            profile.save()
            hackerearth_output = output
        except ValueError:
            pass

        try:
            total = int(spoj_ouput + codechef_output + hackerearth_output)
            profile.total_questions = total
            profile.save()
        except ValueError:
            pass

'''

import re
import requests
from bs4 import BeautifulSoup
from .models import Profile
from datetime import datetime
import datetime
def my_job():
    profiles = Profile.objects.all()
    for profile in profiles:
        #spoj
        y = profile.spoj_username
        pages = []
        count = 0
        count2 = 0
        output = " "
        stop = 0
        flag5 = 1
        today = datetime.date.today()
        url5 = 'http://www.spoj.com/users/' + y
        r5 = requests.get(url5)
        soup5 = BeautifulSoup(r5.content, "html.parser")
        x5 = soup5.find("div", {"class": "col-md-3"})
        if x5 is None:
            flag5 = 0
        if flag5 is 1:
            for a in range(0, 5):
                url = 'http://www.spoj.com/status/' + y + '/all/start=' + str(a * 20)
                pages.append(url)
            for item in pages:
                page = requests.get(item)
                soup = BeautifulSoup(page.content, "html.parser")
                artist_name_list = soup.find_all("tr", {"class": "kol1"})
                artist_name_list2 = soup.find_all("tr", {"class": "kol2"})
                artist_name_list3 = soup.find_all("tr", {"class": "kol3"})
                for i in artist_name_list:
                    count += 1
                    for j in i.contents[3].text:
                        if j != " ":
                            output += j
                        else:
                            output = output.strip()
                            x = int(output[:4])
                            y = int(output[5:7])
                            z = int(output[8:10])
                            some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                            pastday = today - datetime.timedelta(days=30)
                            past = pastday.strftime('%Y-%m-%d')
                            if (some2 > past):
                                count2 += 1
                            else:
                                stop = 1
                            output = " "
                            break
                    if (stop == 1):
                        break
                for i in artist_name_list2:
                    count += 1
                    for j in i.contents[3].text:
                        if j != " ":
                            output += j
                        else:
                            output = output.strip()
                            x = int(output[:4])
                            y = int(output[5:7])
                            z = int(output[8:10])
                            some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                            pastday = today - datetime.timedelta(days=10)
                            past = pastday.strftime('%Y-%m-%d')
                            if (some2 > past):
                                count2 += 1
                            else:
                                stop = 1
                            output = " "
                            break
                    if (stop == 1):
                        break
                for i in artist_name_list3:
                    count += 1
                    for j in i.contents[3].text:
                        if j != " ":
                            output += j
                        else:
                            output = output.strip()
                            x = int(output[:4])
                            y = int(output[5:7])
                            z = int(output[8:10])
                            some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                            pastday = today - datetime.timedelta(days=10)
                            past = pastday.strftime('%Y-%m-%d')
                            if (some2 > past):
                                count2 += 1
                            else:
                                stop = 1
                            output = " "
                            break
                    if (stop == 1):
                        break
                if (stop == 1):
                    break
        try:
            output = int(count2)
            profile.spoj_rating = output
            spoj_ouput = output
            profile.save()
        except ValueError:
            pass

        #codechef
        x = profile.codechef_username
        url = "https://www.codechef.com/recent/user?page=0&user_handle="+x+"&_=1510300136417"
        # mathecodician
        # sagar_sam
        #print(url)
        pages = []
        r = requests.get(url)
        today = datetime.date.today()
        soup = BeautifulSoup(r.content, "html.parser")
        output2 = " "
        for j in soup.text[12:]:
            if j != ",":
                output2 += j
            else:
                break

        output2 = int(output2)
        #print(output2)
        count = 0
        accepted = 0
        count2 = 0
        stop = 0
        num_of_pages = 0
        for a in range(0, output2):
            # for a in range(0, 10):
            url = "https://www.codechef.com/recent/user?page=" + str(a) + "&user_handle="+x+"&_=1510300136417"
            pages.append(url)

        for i in pages:
            count += 1

        for item in pages:
            num_of_pages += 1
            r = requests.get(item)
            soup = BeautifulSoup(r.content, "html.parser")
            g_data3 = soup.find_all("td")
            count = 0
            for item3 in g_data3:
                if (count % 4 == 0):
                    output = " "
                    output = item3.contents[0]
                    wordList = re.sub("[^\w]", " ", output).split()
                    if wordList.__len__() > 2:
                        streee = wordList[2]
                        if streee == 'ago':
                            case = today
                            case = case.replace(case.year - 2000)
                            case = case.strftime('%d\/%m\/%Y')
                            output = "12:12 PM " + case + "<\/td>"

                elif count % 2 == 0:
                    flag = 0
                    points = []
                    for j in item3.contents[0]:
                        flag += 1
                    if (flag == 6):
                        counter = 0
                        for j in item3.contents[0]:
                            counter += 1
                            if (counter == 3):
                                points.append(str(j))
                    if (points == ['100']):
                        accepted += 1
                        x = output
                        x = int(output[9:11])
                        y = int(output[13:15])
                        z = 2000
                        z = z + int(output[17:19])
                        someday = datetime.date(z, y, x)  # .strftime('%Y-%m-%d')
                        some2 = datetime.date(z, y, x).strftime('%Y-%m-%d')
                        pastday = today - datetime.timedelta(days=11)
                        past = pastday.strftime('%Y-%m-%d')
                        if (some2 > past):
                            count2 += 1
                        else:
                            stop = 1
                        output = " "
                count += 1
                if (stop == 1):
                    break
            if (stop == 1):
                break
        try:
            output = int(count2)
            print(output)
            profile.codechef_rating = output
            codechef_output = output
            profile.save()
        except ValueError:
            pass
