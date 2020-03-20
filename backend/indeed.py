import bs4 as bs
import threading
from models import Job, User, JobSchema
import urllib.request
import urllib.parse as urlparse


sauce = urllib.request.urlopen(
    'https://il.indeed.com/jobs?as_and=student&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=25&l=israel&fromage=1&limit=10&sort=&psf=advsrch&from=advancedsearch').read()
soup = bs.BeautifulSoup(sauce, 'lxml')
internalJobList = soup.find_all('div', {'class':"jobsearch-SerpJobCard unifiedRow row result"})
# Indeed jobs
for aTag in internalJobList:
    url = aTag.find('a').get('href')
    url = 'https://il.indeed.com' + url
    jobSauce = urllib.request.urlopen(url)
    jobSoup = bs.BeautifulSoup(jobSauce, 'lxml')
    jobTitle = jobSoup.find('div', {'class':"jobsearch-JobInfoHeader-title-container"}).string # job title
    jobCompany = jobSoup.find('div', {'class':"icl-u-lg-mr--sm icl-u-xs-mr--xs"}).string #company name
    jobLocation = jobSoup.find('span', {'class':"jobsearch-JobMetadataHeader-iconLabel"}).string #company location
    jobDescription = jobSoup.find('div', {'class': "jobsearch-jobDescriptionText"}) #job description
    if (jobSoup.find('div', {'class': "icl-u-lg-hide"}).find('a')):
        jobExternalLink = jobSoup.find('div', {'class': "icl-u-lg-hide"}).find('a').get('href')
        req = urllib.request.Request(jobExternalLink, headers={'User-Agent': 'Mozzila/5.0'})
        jobExternalLinkRedirect = urllib.request.urlopen(req)
        jobExternalLink = jobExternalLinkRedirect.geturl()
    else:
        jobExternalLink = url

    print("Job title: " + jobTitle)
    print("Job company: " + jobCompany)
    print("Job location: " + jobLocation)
    print("Job details: " +  str(jobDescription))
    print(jobExternalLink + "\n")

    job = Job(company=jobCompany, title=jobTitle,
              description=jobDescription, link=jobExternalLink, location=jobLocation)
    job.save_to_db()