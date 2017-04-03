
from selenium import webdriver
from mpipe import UnorderedStage,Pipeline
import json
import traceback
import signal




path=''
infile='2016-2017.txt'
outfile='2016-2017.json'


infile=open(path+infile).readlines()
outfile=open(path+outfile,'w')
errorfile=open(path+'errors','w')

def quitdriver(driver):
    try:
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()
        # driver = webdriver.PhantomJS(
        #     #   executable_path='/usr/local/lib/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs')
        #     executable_path='/usr/local/bin/phantomjs')
        # driver.set_page_load_timeout(20)
        return 'done'
    except:
        error = traceback.format_exc()
        return'error: quitting the driver ' + str(error)



def findele(driver,id):
    try:
        text=driver.find_element_by_id(id).text
        return text
    except:
        #print traceback.format_exc()
        return ''

def processpage(bundle):

    #todo: Can fetch faster with a single instance (can implement the shared memory implementation)

    driver = webdriver.PhantomJS(
           #executable_path='/usr/local/lib/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs')
        executable_path='/usr/local/bin/phantomjs')
    driver.set_page_load_timeout(20)

    id=bundle[0]
    url=bundle[1]

    try:
        driver.get(url)
    except:
        error = traceback.format_exc()
        bundle.append({})
        bundle.append(url+' '+str(error)+ str(quitdriver(driver)))
        return bundle
    #print driver.page_source

    #print url
    json={}
    json['publicationDate']=findele(driver,'detailsForm:publicationDate')
    json['personalAuthors']=findele(driver,'detailsForm:personalAuthors')
    json['summary']=findele(driver,'detailsForm:summary')
    json['sourceAgencies']=findele(driver,'detailsForm:sourceAgencies')
    json['corporateAuthors']=findele(driver,'detailsForm:corporateAuthors')
    json['supplementalNote']=findele(driver,'detailsForm:supplementalNote')
    json['documentType']=findele(driver,'detailsForm:documentType')
    json['titleNote']=findele(driver,'detailsForm:titleNote')
    json['issueNumber']=findele(driver,'detailsForm:issueNumber')
    json['contractNumbers']=findele(driver,'detailsForm:contractNumbers')
    json['itemAbbr']=findele(driver,'detailsForm:itemAbbr')
    json['itemTitle']=findele(driver,'detailsForm:itemTitle')
    json['categories'] = findele(driver, 'detailsForm:categories')
    json['keywords']=findele(driver, 'detailsForm:keywords')






    quitdriver(driver)
    bundle.append(json)
    bundle.append('')

    #html=driver.page_source
    return bundle


def writetofile(bundle):

    print bundle[0]

    if bundle[3]!='':
        errorfile.write(bundle[3] + '\n')
        errorfile.flush()
        return

    jso=bundle[2]
    data=json.dumps(jso)
    outfile.write(data+'\n')
    outfile.flush()




if __name__ == '__main__':


    infile=infile[1:]
    count=0

    stage1 = UnorderedStage(processpage, 6)
    stage2=UnorderedStage(writetofile, 1)
    stage1.link(stage2)
    pipe = Pipeline(stage1)





    for line in infile:
        line=line.strip()
        count+=1
        bundle=[]
        bundle.append(str(count))
        bundle.append('https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/' + line + '.xhtml')

        pipe.put(bundle)


