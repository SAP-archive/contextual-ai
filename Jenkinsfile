#!/usr/bin/env groovy
@Library(['piper-lib', 'piper-lib-os']) _

pipeline {
    agent { label 'slave' }
    parameters{
        booleanParam(defaultValue: false, description: '\'true\' will create a release artifact on Nexus', name: 'PROMOTE')
    }
    stages{
    /*
        stage('Pull-request voting') {
            when { branch "PR-*" }
            steps {
                script {
                    deleteDir()
                    checkout scm
                    setupPipelineEnvironment script: this
                    measureDuration(script: this, measurementName: 'voter_duration') {
                        sh """
                             echo "add simple tests that should run as part of PR check, e.g. unit tests"
                           """
                    }
                }
            }
            post { always { deleteDir() } }
        }
*/
            stage('Unit tests') {
                 agent { label 'slave' }
                       when { branch 'XAI_NEW' }
                        steps {
                          script{
                            sh """
                                echo "add unit tests"
                                chmod +x scripts/run_unit_tests.sh
                                ./scripts/run_unit_tests.sh
                              """

                            junit allowEmptyResults: true, testResults: "nosetests_result.xml"
                            stash includes: 'nosetests_result.xml', name: 'unit_results'
                            stash includes: 'coverage.xml', name: 'coverage_results'
                           }

                       publishTestResults(
                        junit: [updateResults: true, archive: true, pattern:'nosetests_result.xml'],
                        cobertura: [archive: true, pattern: 'coverage.xml'],
                        allowUnstableBuilds: true
                     )


				          // publish python results from pylint
                checksPublishResults script: this, archive: true, tasks: true,
                    pylint: [pattern: '**/pylint.out', thresholds: [fail: [all: '3999', low: '1999', normal: '1999', high: '1999']]],
                    aggregation: [thresholds: [fail: [all: '3999', low: '1999', normal: '1999', high: '1999']]]

                    }

            }

        stage('Central Build') {
             agent { label 'slave' }
                  when { branch 'XAI_NEW' }
                    steps {
                       script{
                             lock(resource: "${env.JOB_NAME}/10", inversePrecedence: true) {
                                  milestone 10
                                  deleteDir()
                                  checkout scm

                                  setupPipelineEnvironment script: this
                                  measureDuration(script: this, measurementName: 'build_duration') {
                                  if ("${params.PROMOTE}" == "true"){
                                            setVersion script:this, versioningTemplate: "${env.VERSION}",commitVersion: false
                                        } else {
                                            setVersion script:this
                                   }
                                  stashFiles(script: this) {
                                          executeBuild script: this, buildType: 'xMakeStage', xMakeBuildQuality: 'Release'
                                  }


                               // publishTestResults cobertura: [archive: true, pattern: 'coverage.xml']
                             }
                       }
                  }
              }
           post { always { deleteDir() } }
          }

          /* add other pipelines here */


            stage('Promote') {
                agent { label 'slave' }
                   when { branch 'XAI_NEW' }
                        steps {
                          script{
                            lock(resource: "${env.JOB_NAME}/90", inversePrecedence: true) {
                                milestone 90
                                if ("${params.PROMOTE}" == "true") {
                                      measureDuration(script: this, measurementName: 'promote_duration') {
                                          executeBuild script: this, buildType: 'xMakePromote',xMakeBuildQuality: 'Release', xMakeShipmentType: 'indirectshipment'
                                      }
                                   }
                                }
                            }
                        }
                 post { always { deleteDir() } }
                }
            }
               // Send notification mail when pipeline fails
         }
