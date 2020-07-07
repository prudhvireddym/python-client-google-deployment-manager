import httplib2
import pprint
import sys
from flask import jsonify
import os
import validators
import time
import pathlib
from pathlib import Path
import shutil




from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import requests

def main(argv):

  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'new-key.json',
      scopes='https://www.googleapis.com/auth/cloud-platform')


  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build("tasks", "v1", http=http)

  if(int(x)==12):
    os.system("gcloud projects list")
    instance = input("Enter your instance name:")
    conf_file=input("List the complete path of your config file:")
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
      os.system("gcloud deployment-manager deployments create "+instance+" --config "+clone[len(clone)-1])
    else:
      os.system("gcloud deployment-manager deployments create "+instance+" --config "+conf_file)
  else:
    project = input("Enter the name of the project: ")  
    if(int(x) ==(1 or 2 or 3 or 7 or 9 or 11)):
      deployment = input("Enter the name of the deployment:")
      if(int(x)==1):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment+'/cancelPreview',method="POST")
      elif(int(x)==2):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment+'/cancelPreview',method="DELETE")
        
      elif(int(x)==3):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment+'/cancelPreview',method="GET")
        
      elif(int(x)==7):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment+'/cancelPreview',method="PATCH")
        
      elif(int(x)==9):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment+'/stop',method="POST")
        
      elif(int(x)==11):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+deployment+'/cancelPreview',method="PUT")
        

        
    elif(int(x)==(4 or 8 or 10)):
      resource = input("Enter the resource name:")
      if(int(x)==4):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+resource+'/getIamPolicy',method="GET")
        
      if(int(x)==8):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+resource+'/setIamPolic',method="POST")
        
      if(int(x)==10):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments/'+resource+'/testIamPermissions',method="POST")
        

    else:
      if(int(x)==5):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments',method="POST")
        
      if(int(x)==6):
        content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/'+project+'/global/deployments',method="GET")
    print(content)  

  
    

  #content = http.request('https://www.googleapis.com/deploymentmanager/v2/projects/deployment-manager-test-282406/global/deployments',method="GET")
  #print(content[1][6])
  #pprint.p


if __name__ == '__main__':
  x = input("Enter the correspinding no if operation you wish to do\n 1.Cancel and removes the preview currently associated with the deployment.\n 2.Delete a deployment and all of the resources in the deployment.\n 3.Get information about a specific deployment.\n 4.Get the access control policy for a resource. May be empty if no such policy or resource exists\n 5.Create a deployment and all of the resources described by the deployment manifest.\n 6.List all deployments for a given project.\n 7.Patch a deployment and all of the resources described by the deployment manifest. This method supports patch semantics.\n 8.Set the access control policy on the specified resource. Replaces any existing policy\n 9.Stops an ongoing operation. This does not roll back any work that has already been completed, but prevents any new work from being started.\n 10.Returns permissions that a caller has on the specified resource\n 11.Updates a deployment and all of the resources described by the deployment manifest.\n 12.To deploy a resource from local file system \n:")
  main(sys.argv)
