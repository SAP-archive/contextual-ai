pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('build') {
      steps {
        sh 'pip install --user -r test_requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'nose2 --with-coverage'
      }   
    }
  }
}
