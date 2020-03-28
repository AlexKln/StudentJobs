import bs4 as bs
import threading
from models import Job, User, JobSchema  # NOQA:F401
import urllib.request
import urllib.parse as urlparse


class Scraper:
    def __init__(self, db):
        self.db = db

    def scrape(self):
        sauce = urllib.request.urlopen(
            'https://www.linkedin.com/jobs/search?keywords=student&location=Israel&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&f_TP=1').read()  # NOQA
        soup = bs.BeautifulSoup(sauce, 'lxml')
        internalJobLinksList = soup.find_all(
            'a', {'class': "result-card__full-card-link"})

        try:
            self.db.session.query(Job).delete()  # DB cleanup
        except Exception:
            pass
        # self.db.session.commit()
        self.db.create_all()

        # LinkedIn jobs
        for aTag in internalJobLinksList:
            url = aTag.get('href')
            jobSauce = urllib.request.urlopen(url)
            jobSoup = bs.BeautifulSoup(jobSauce, 'lxml')
            # Checking if null before getting string:
            if (jobSoup.find('span', {'class': "topcard__flavor"})):
                jobCompany = jobSoup.find(
                    'span', {'class': "topcard__flavor"}).string
            else:
                jobCompany = 'Unknown'
            jobLocation = jobSoup.find(
                'span', {'class': "topcard__flavor--bullet"}).string
            jobTitle = aTag.string
            jobDescription = str(jobSoup.find(
                'div', {'class': "description__text--rich"}))
            jobExternalLinkViaLinkedIn = jobSoup.find(
                'a', {'class': "apply-button--link"})
            offsiteApply = jobSoup.find(
                'figure', {'class': "apply-button__offsite-apply-icon"})
            if (offsiteApply):  # Check if the job isn't of "Easy Apply" type
                jobExternalLinkViaLinkedIn = jobExternalLinkViaLinkedIn.get(
                    'href')
                jobExternalLinkParsed = urlparse.urlparse(
                    jobExternalLinkViaLinkedIn)
                jobExternalLinkClean = str(urlparse.parse_qs(
                    jobExternalLinkParsed.query)['url'][0])
            else:  # In the case of "Easy Apply", pass the indoor LinkedIn link
                jobExternalLinkClean = url
            # Make sure none of the links
            # Contain multiple occurences of 'https' (redirect cleanup)
            if (jobExternalLinkClean[1:].find('https') != -1):
                jobExternalLinkClean = jobExternalLinkClean[1:][
                    jobExternalLinkClean[1:].find(
                        'https'):]
            job = Job(company=jobCompany, title=jobTitle,
                      description=jobDescription, link=jobExternalLinkClean,
                      location=jobLocation)
            job.save_to_db()

        # Glassdoor jobs
        url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=student&locT=N&locId=119&locKeyword=Israel&jobType=all&fromAge=1&minSalary=0&includeNoSalaryJobs=true&radius=25&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'  # NOQA
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozzila/5.0'})
        sauce = urllib.request.urlopen(req).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        internalJobLinksList = soup.find_all('div', {'class': "jobHeader"})
        for aTag in internalJobLinksList:
            url = 'https://www.glassdoor.com' + str(aTag.find('a').get('href'))
            req = urllib.request.Request(
                url, headers={'User-Agent': 'Mozzila/5.0'})
            jobSauce = urllib.request.urlopen(req).read()
            jobSoup = bs.BeautifulSoup(jobSauce, 'lxml')
            jobLocation = jobSoup.find(
                'input', {'id': "sc.location"}).get('value') + ', IL'
            jobCompany = jobSoup.find(
                'span', {'class': "strong"}).string.strip()
            jobTitle = jobSoup.find('input', {'class': "keyword"}).get('value')
            jobDescription = str(jobSoup.find(
                'div', {'id': "JobDescriptionContainer"}))
            jobExternalLink = ""
            if jobSoup.find('div', {'class': "e1h54cx80"}).find('a'):
                req = urllib.request.Request(
                    "https://www.glassdoor.com/" + str(
                        jobSoup.find('div', {'class': "e1h54cx80"}
                                     ).find('a').get('data-job-url'))[1:],
                    headers={'User-Agent': 'Mozzila/5.0'})
                jobExternalLinkRedirect = urllib.request.urlopen(req)
                jobExternalLink = jobExternalLinkRedirect.geturl()
            else:
                # "Easy Apply" - In this case, provide the indoor apply link
                jobExternalLink = url
            job = Job(company=jobCompany, title=jobTitle,
                      description=jobDescription, link=jobExternalLink,
                      location=jobLocation)
            job.save_to_db()

        # Drushim jobs
        sauce = urllib.request.urlopen(
            'https://www.drushim.co.il/jobs/cat6/?src=bar&scope=2-3-4&experience=1').read()  # NOQA
        soup = bs.BeautifulSoup(sauce, 'lxml')
        internalJobList = soup.find_all('div', {'class': "jobContainer"})

        for aTag in internalJobList:
            jobExternalLink = aTag.find('a').get('action')  # CV link
            jobTitle = aTag.find(
                'h2', {'class': "jobName"}).string  # job title
            jobCompany = aTag.find(
                'span', {'class': "fieldTitle"}).string  # company name
            locationDetails = aTag.find_all(
                # company location
                'div', {'class': "fieldContainer horizontal"})
            if (locationDetails[2].find('span', {'class': "fieldText rtl"})):
                jobLocation = locationDetails[2].find(
                    'span', {'class': "fieldText rtl"}).string
            else:
                jobLocation = locationDetails[2].find(
                    'span', {'class': "fieldText ltr"}).string

            # get the introduction to the job
            descriptionDetails = aTag.find(
                # job description
                'div', {'class': "fieldContainer vertical first"})
            if (descriptionDetails.find('span', {'class': "fieldText rtl"})):
                jobDescription = str(descriptionDetails.find(
                    'span', {'class': "fieldText rtl"}))
            else:
                jobDescription = str(descriptionDetails.find(
                    'span', {'class': "fieldText ltr"}))

            # get the candidate requirements
            descriptionDetails = aTag.find(
                'div', {'class': "fieldContainer vertical"})
            if (descriptionDetails.find('span', {'class': "fieldText rtl"})):
                jobDescription = jobDescription + \
                    str(descriptionDetails.find(
                        'span', {'class': "fieldText rtl"}))
            else:
                jobDescription = jobDescription + \
                    str(descriptionDetails.find(
                        'span', {'class': "fieldText ltr"}))
            job = Job(company=jobCompany, title=jobTitle,
                      description=jobDescription, link=jobExternalLink,
                      location=jobLocation)
            job.save_to_db()

        # Indeed jobs
        sauce = urllib.request.urlopen(
            'https://il.indeed.com/jobs?as_and=student&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=25&l=israel&fromage=1&limit=10&sort=&psf=advsrch&from=advancedsearch').read()  # NOQA
        soup = bs.BeautifulSoup(sauce, 'lxml')
        internalJobList = soup.find_all(
            'div', {'class': "jobsearch-SerpJobCard unifiedRow row result"})

        for aTag in internalJobList:
            url = aTag.find('a').get('href')
            url = 'https://il.indeed.com' + url
            jobSauce = urllib.request.urlopen(url)
            jobSoup = bs.BeautifulSoup(jobSauce, 'lxml')
            jobTitle = jobSoup.find(
                'div', {'class': "jobsearch-JobInfoHeader-title-container"}
            ).string  # job title
            jobCompany = jobSoup.find(
                'div', {'class': "icl-u-lg-mr--sm icl-u-xs-mr--xs"}
            ).string if jobSoup.find(
                'div', {'class': "icl-u-lg-mr--sm icl-u-xs-mr--xs"}
            ) else "Unknown Company"  # company name
            jobLocation = jobSoup.find(
                'span',
                {'class': "jobsearch-JobMetadataHeader-iconLabel"}
            ).string  # company location
            jobDescription = str(jobSoup.find(
                'div', {'class': "jobsearch-jobDescriptionText"})
            )  # job description
            if (jobSoup.find('div', {'class': "icl-u-lg-hide"}).find('a')):
                jobExternalLink = jobSoup.find(
                    'div', {'class': "icl-u-lg-hide"}).find('a').get('href')
                req = urllib.request.Request(jobExternalLink, headers={
                                             'User-Agent': 'Mozzila/5.0'})
                jobExternalLinkRedirect = urllib.request.urlopen(req)
                jobExternalLink = jobExternalLinkRedirect.geturl()
            else:
                jobExternalLink = url
            job = Job(company=jobCompany, title=jobTitle,
                      description=jobDescription, link=jobExternalLink,
                      location=jobLocation)
            job.save_to_db()

        # self.db.session.commit()

    def activate(self):
        t = threading.Thread(name='scraper', target=self.scrape)
        t.daemon = True
        t.start()
