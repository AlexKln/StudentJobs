import bs4 as bs
from models import Job, User, JobSchema
import urllib.request
import urllib.parse as urlparse

class Scraper:
    def __init__(self, db):
        self.db = db

    def scrape(self):
        sauce = urllib.request.urlopen('https://www.linkedin.com/jobs/search?keywords=student&location=Israel&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&f_TP=1').read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        linkedInJobNum = soup.find('span', {'class':"results-context-header__job-count"}).string
        internalJobLinksList = soup.find_all('a', {'class':"result-card__full-card-link"})

        try:
            self.db.session.query(Job).delete() # DB cleanup
        except:
            pass
        # self.db.session.commit()
        self.db.create_all()

        # LinkedIn jobs
        for aTag in internalJobLinksList:
            url = aTag.get('href')
            jobSauce = urllib.request.urlopen(url)
            jobSoup = bs.BeautifulSoup(jobSauce, 'lxml')
            if (jobSoup.find('span', {'class': "topcard__flavor"})): # Checking if null before getting string:
                jobCompany = jobSoup.find('span', {'class': "topcard__flavor"}).string
            else:
                jobCompany = 'Unknown'
            jobLocation = jobSoup.find('span', {'class': "topbar__company-info-meta"}).string
            jobTitle = aTag.string
            jobDescription = str(jobSoup.find('div', {'class': "description__text--rich"}))
            jobExternalLinkViaLinkedIn = jobSoup.find('a', {'class':"apply-button--link"})
            offsiteApply = jobSoup.find('figure', {'class': "apply-button__offsite-apply-icon"})
            if (offsiteApply): # Check if the job isn't of "Easy Apply" type
                jobExternalLinkViaLinkedIn = jobExternalLinkViaLinkedIn.get('href')
                jobExternalLinkParsed = urlparse.urlparse(jobExternalLinkViaLinkedIn)
                jobExternalLinkClean = str(urlparse.parse_qs(jobExternalLinkParsed.query)['url'][0])
            else: # In the case of "Easy Apply", passing the indoor LinkedIn link
                jobExternalLinkClean = url
            # Make sure none of the links
            # Contain multiple occurences of 'https' (redirect cleanup)
            if (jobExternalLinkClean[1:].find('https') != -1):
                jobExternalLinkClean = jobExternalLinkClean[1:][jobExternalLinkClean[1:].find('https'):]
            job = Job(company=jobCompany, title=jobTitle,
                      description=jobDescription, link=jobExternalLinkClean, location=jobLocation)
            job.save_to_db()

        # Glassdoor jobs
        url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=student&locT=N&locId=119&locKeyword=Israel&jobType=all&fromAge=1&minSalary=0&includeNoSalaryJobs=true&radius=25&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozzila/5.0'})
        sauce = urllib.request.urlopen(req).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        internalJobLinksList = soup.find_all('div', {'class': "jobHeader"})
        # internalJobLinksList = internalJobDivList.get('a')
        for aTag in internalJobLinksList:
            url = 'https://www.glassdoor.com' + str(aTag.find('a').get('href'))
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozzila/5.0'})
            jobSauce = urllib.request.urlopen(req).read()
            jobSoup = bs.BeautifulSoup(jobSauce, 'lxml')
            jobLocation = jobSoup.find('span', {'class': "subtle"}).string[3:] + ', IL'
            jobCompany = jobSoup.find('span', {'class': "strong"}).string.strip()
            jobTitle = jobSoup.find('input', {'class': "keyword"}).get('value')
            jobDescription = str(jobSoup.find('div', {'class': "jobDescriptionContent"}))
            jobExternalLink = str(jobSoup.find('div', {'class': "regToApplyArrowBoxContainer"}).find('a').get('data-job-url'))
            if (jobExternalLink.find('http') == -1): # Indoor glassdoor links are of "Easy Apply" type
                jobExternalLink = url                # In this case, providing the indoor apply link
            job = Job(company=jobCompany, title=jobTitle,
                      description=jobDescription, link=jobExternalLink, location=jobLocation)
            job.save_to_db()

        # self.db.session.commit()
