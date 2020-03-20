import bs4 as bs
import threading
from models import Job, User, JobSchema
import urllib.request
import urllib.parse as urlparse


sauce = urllib.request.urlopen(
    'https://www.drushim.co.il/jobs/cat6/?src=bar&scope=2-3-4&experience=1').read()
soup = bs.BeautifulSoup(sauce, 'lxml')
internalJobList = soup.find_all('div', {'class':"jobContainer"})


# Drushim jobs
for aTag in internalJobList:

    jobExternalLink = aTag.find('a').get('action') # CV link
    jobTitle = aTag.find('h2', {'class': "jobName"}).string #job title
    jobCompany = aTag.find('span', {'class': "fieldTitle"}).string #company name
    locationDetails = aTag.find_all('div', {'class': "fieldContainer horizontal"}) #company location
    if (locationDetails[2].find('span', {'class': "fieldText rtl"})):
        jobLocation = locationDetails[2].find('span', {'class': "fieldText rtl"}).string
    else:
        jobLocation = locationDetails[2].find('span', {'class': "fieldText ltr"}).string

    # get the introduction to the job
    descriptionDetails = aTag.find('div', {'class': "fieldContainer vertical first"}) #job description
    if (descriptionDetails.find('span', {'class': "fieldText rtl"})):
        jobDescription = str(descriptionDetails.find('span', {'class': "fieldText rtl"}))
    else:
        jobDescription = str(descriptionDetails.find('span', {'class': "fieldText ltr"}))

    # get the candidate requirements
    descriptionDetails = aTag.find('div', {'class': "fieldContainer vertical"})
    if (descriptionDetails.find('span', {'class': "fieldText rtl"})):
        jobDescription = jobDescription + str(descriptionDetails.find('span', {'class': "fieldText rtl"}))
    else:
        jobDescription = jobDescription + str(descriptionDetails.find('span', {'class': "fieldText ltr"}))

    print("Job title: " + jobTitle)
    print("Job company: " + jobCompany)
    print("Job location: " + jobLocation)
    print("Job details: " +  str(jobDescription))
    print(jobExternalLink + "\n")

    job = Job(company=jobCompany, title=jobTitle,
              description=jobDescription, link=jobExternalLink, location=jobLocation)
    job.save_to_db()


