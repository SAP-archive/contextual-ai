pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('build') {
      steps {
        sh 'sudo pip install -r test_requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'nose2 --with-coverage'
      }   
    }
  }
}
