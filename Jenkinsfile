node ('Slave'){
  echo 'Hello World'

  stage('Checkout'){
       dir('Weather') {
           git url: 'https://github.com/hila3000/opsschool3-coding.git'
       }
   }
  sh '''
  cd /opt/jenkins/workspace/coding_session2_pipeline/Weather/home-assignments/session2/
  chmod +x ./exercise1.py
  python3 exercise1.py --city London
  '''
}



