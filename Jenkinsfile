node ('Slave'){
  echo 'Hello World'

  stage('execution'){
       sh '''
       cd /opt/jenkins/workspace/coding_session2_pipeline/Weather/home-assignments/session2/
       chmod +x ./exercise1.py
       python3 exercise1.py --city London
       '''
   }

}