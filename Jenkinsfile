pipeline {
  agent { dockerfile true }
  stages {
    stage('test') {
      steps {
        sh 'nose2 --with-coverage'
      }   
    }
  }
}
