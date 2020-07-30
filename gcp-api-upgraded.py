import httplib2
import pprint
import sys
import os
import validators
import time
import pathlib
from pathlib import Path
import shutil
import json
from operator import itemgetter 
from sys import platform
import subprocess



from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import requests

import subprocess
import os
import re 
import ast
import random

projects_parsed = []
Projects_dict= {}

Deployments_dict = {
    "Deployment_message":"The below resourses were added successfully"
}



def get_projects():
    projects = (str(subprocess.check_output('gcloud projects list',shell=True))).split('\\r\\n')

    for i in range(1,len(projects)):
        projects_parsed.append(re.sub('  +', '\n', projects[i]))

    for j in range(0,len(projects_parsed)-1):
        Projects_dict.update( {"Projects "+str(j+1) : projects_parsed[j].split('\n')} )

    projects_json= json.dumps(Projects_dict)
    return projects_json

def get_deployment_output(cmnd):
    deployments_parse = (str(subprocess.check_output(cmnd,shell=True))).split('\\r\\n')
    Deployments_dict.update( {"Resources Added": deployments_parse[1:len(deployments_parse)-1]} )
    deployments_json = json.dumps(Deployments_dict)
    return deployments_json

    



def main(argv):

  deployment_list=[1,2,3,7,9,11]
  resourse_list = [4,8,10]
  content = None
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'new-key2.json',
      scopes='https://www.googleapis.com/auth/cloud-platform')


  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build("tasks", "v1", http=http)

  if(int(x)==12):
    print(get_projects())
    project = input("Enter the name of the project:")
    instance = input("Enter your instance name:")
    conf_file= input("List the complete path of your config file or its github url:")
    valid=validators.url(conf_file)
    if(valid==True):
      clone = conf_file.split('/')
      git_url = clone[0]+'/'+clone[1]+'/'+clone[2]+'/'+clone[3]+'/'+clone[4]+'.git'
      print(git_url)
      dirpath = Path(os.path.abspath(os.getcwd()),clone[4])
      print(dirpath)
      if not (dirpath.exists() and dirpath.is_dir()):
        os.system("git clone "+git_url)
        time.sleep(5)
      for i in range(4, len(clone)-1):
        isFile = (os.path.isfile(clone[i]) or os.path.isdir(clone[i]))
        if(isFile):  
          os.chdir(clone[i])
          os.system('pwd')
          time.sleep(1)
      cmnd = "gcloud deployment-manager deployments create "+instance+" --config "+clone[len(clone)-1]
      print(["=" for i in range(50)])
      try: 
        print(get_deployment_output(cmnd))
      except:
            Deployments_dict.update( {"Deployment_message":"Could not deploy your instance check logs for error"} )
            print(json.dumps(Deployments_dict))

    else:
      cmnd ="gcloud deployment-manager deployments create "+instance+" --config "+conf_file
      print(["=" for i in range(50)])
      try: 
        print(get_deployment_output(cmnd))
      except:
            Deployments_dict.update( {"Deployment_message":"Could not deploy your instance check logs for error"} )
            print(json.dumps(Deployments_dict))
    #content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+instance,method="GET")
    #new_obj = json.loads(content[1])
    #print(new_obj)

  else:
    print(int(x))
    project = input("Enter the name of the project: ")  
    if((int(x)) in deployment_list):
      deployment = input("Enter the name of the deployment:")
      if(int(x)==1):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment,method="POST")
        

      elif(int(x)==2):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment,method="DELETE")
        

      elif(int(x)==3):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment,method="GET")
        new_obj = json.loads(content[1])
        

      elif(int(x)==7):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment,method="PATCH")
        

      elif(int(x)==9):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment+'/setIamPolicy',method="POST")
        

      elif(int(x)==11):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment,method="PUT")
        

        
    elif(int(x) in resourse_list):
      resource = input("Enter the resource name:")
      if(int(x)==4):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+resource+'/getIamPolicy',method="GET")
        

      if(int(x)==8):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+resource+'/setIamPolicy',method="POST")
        

      if(int(x)==10):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+resource+'/testIamPermissions',method="POST")
        

    else:
      if(int(x)==5):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments',method="POST")
        

      if(int(x)==6):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments',method="GET")
        #json_data = eval(content)
    new_obj = json.loads(content[1])
    print(new_obj)#['deployments'][0]['name']

    

if __name__ == '__main__':
  x = input("1.Cancel and removes the preview currently associated with the deployment.\n 2.Delete a deployment and all of the resources in the deployment.\n 3.Get information about a specific deployment.\n 4.Get the access control policy for a resource. May be empty if no such policy or resource exists\n 5.Create a deployment and all of the resources described by the deployment manifest.\n 6.List all deployments for a given project.\n 7.Patch a deployment and all of the resources described by the deployment manifest. This method supports patch semantics.\n 8.Set the access control policy on the specified resource. Replaces any existing policy\n 9.Stops an ongoing operation. This does not roll back any work that has already been completed, but prevents any new work from being started.\n 10.Returns permissions that a caller has on the specified resource\n 11.Updates a deployment and all of the resources described by the deployment manifest.\n 12.To deploy a resource from local file system or directly from github \nEnter the correspinding no of operation you wish to do:")
  main(sys.argv)

#for cmm
