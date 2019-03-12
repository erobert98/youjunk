from app.models import Article
from app.db_util import add_link
import csv
import re

def confirm_newLink(item):
    A = Article.query.filter_by(link = item).first()
    if A is None:
        return True
    else:
        return False




def add_from_csv(f):  
    # f = open('./articles.csv')
    # csv_f = csv.reader(f, dialect='UTF8')
    # print('ok')
    # for row in csv_f:
     #        print(row[7])

    list_urls = []            
    with open(f, newline='', encoding='latin1') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
                try:
                    url =row[0]
                    # link = str(row)
                    # print(link)
                    link = clean_url(url)
                    if link is None:
                        raise ValueError
                    add_link(link)
                except Exception as e:
                    pass



def clean_url(var): #MAKE THIS WORKFOR OPTIMAZAITONDASDASJSA
    # list_urls = ["http://www.nytimes.com/2017/04/05/opinion/filibusters-arent-the-problem.html?smid=fb-nytopinion&smtyp=cur","https://washingtonpress.com/2018/11/20/ocasio-cortez-just-hilariously-dunked-on-sarah-palin-after-she-tried-to-mock-her-knowledge/?fbclid=IwAR2aNWRBojr5SLt8jSQdgHYsH3VKqSzXI8zGO0MIYUdujI0A77eFKsr6gCQ","https://ilovemyfreedom.org/plot-twist-feinstein-walks-back-fbi-investigation-says-results-should-be-closely-held/?utm_source=dtp&utm_medium=facebook"]
    # while item < len(list_urls):
    # print('hello')
    # print(list_urls)
        # break
    # return url
    # print(url)
    if 'http:' in var:
        url = var.replace('http', 'https')
    else:
        url = var

    try:
        if 'https://www.facebook.com/' in url:
            print('fb')
            return None
        if 'https://m.youtube.com/' in url:
            print('youtube')
            return None
        if 'https://youtu.be/' in url:
            return None 
        if 'https://twitter.com/' in url:
            return None
        # print(f"{url} and {url[0]}")
        # url = str(url)
        # print(url)
        if '?utm' in url:
            # regex = "\[\'(...*)(?=(\?|#)utm)...*"  #replace instead of regex [0] [1]
            regex = "(...*)(?=(\?|#)utm)"

            matches = re.findall(regex, url, re.MULTILINE)
            # print(f"this is the match : {matches}")
            var = matches[0][0]
            # print(matches)
            test = confirm_newLink(var)
            if test:
                print(f'new link {var}')
                return var
            else:
                print(f'already added {matches[0][0]}')
                return None

        if '?smid=' in url:
            # print('suh')
            # print(url)
            # print(str(url))
            regex2 = "(.*)(?=(\?)smid)...*"  #replace instead of regex [0] [1]
            # regex2 = "(\[\'().*)(?=(\?)smid)...*"  #replace instead of regex [0] [1]
            matches = re.findall(regex2, url, re.MULTILINE)
            # print(matches)

            test = confirm_newLink(matches[0][0])
            if test:
                # print(f'new link {matches[0][0]}')
                return matches[0][0]
                # break
            else:
                print(f'already added {matches[0][0]}')
                return None



        elif '?fbclid' in url:
            # print('suh')
            # print(url)
            # print(str(url))
            # regex2 = "(...*)(?=(\?)fbc)...*"  #replace instead of regex [0] [1]
            regex2 = "(...*)(?=(\?)fbc)...*"  #replace instead of regex [0] [1]
            matches = re.findall(regex2, url, re.MULTILINE)
            # print(matches)
            test = confirm_newLink(matches[0][0])
            if test:
                print(f'new link {matches[0][0]}')
                return matches[0][0]
            
            else:
                print(f'already added {matches[0][0]}')
                return None
        else:
            # print(url)
            test = confirm_newLink(url)
            if test:
                print(f" NATURALLY CLEAN SENT URL {url}")
                return url
            else:
                print(f'already added {url}')
                return None
        # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
        #     # time.sleep(5)
    except Exception as e:
        # URLS.append(url) # 
        print(e)