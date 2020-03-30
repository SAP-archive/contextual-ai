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
/*
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
          */


          stage('SonarQube') {
                 agent { label 'slave' }
                     when { branch 'XAI_NEW' }
                        steps {
                           lock(resource: "${env.JOB_NAME}/20") {
                              milestone 20
                                   measureDuration(script: this, measurementName: 'Sonar_duration') {
                                        unstash 'unit_results'
                                        unstash 'coverage_results'
                                        sh"""
                                            sed -i -- 's#<source>.*</source>#<source>${WORKSPACE}/proposed-amount-validation/pav-worker/accruals-proposed-amt-validation/</source>#g' coverage.xml
                                            rm -f coverage.xml--
                                        """
                                        executeSonarScan script: this, instance:'SAP_EE_sonar',  projectVersion: "${env.BRANCH_NAME}"
                             }
                          }

                        }
                    post { always { deleteDir() } }
                }

            stage('Vulas') {
                       agent { label 'slave' }
                             when { branch 'XAI_NEW' }
                                    steps {
                                       lock(resource: "${env.JOB_NAME}/80") {
                                          milestone 30
                                            measureDuration(script: this, measurementName: 'vulas_duration') {
                                               executeVulasScan script: this, scanType: 'pip',
                                                     dockerImage: 'docker.wdf.sap.corp:65351/centraljenkins/python3.6-vulas:latest'
                                               stash includes: 'target/vulas/report/**/*', name: 'vulas_results'
                                            }
                                         }
                                    }
                     post {
                        always {
                            deleteDir()
                        }
                      }
            }

            stage('Whitesource') {
                agent { label 'slave' }
                when { branch 'XAI_NEW' }
                steps {
                    lock(resource: "${env.JOB_NAME}/40") {
                        milestone 40
                        measureDuration(script: this, measurementName: 'whitesource_duration') {
                            script{
                                try{
                                    executeWhitesourceScan script: this, scanType: 'unifiedAgent',
                                        dockerImage: 'docker.wdf.sap.corp:65351/centraljenkins/python3.6-whitesource:latest',
                                        agentDownloadUrl: 'https://s3.amazonaws.com/unified-agent/wss-unified-agent-19.5.2.jar'
                                }catch(e){
                                    echo """
                                        Staged failed: executeWhitesourceScan
                                        Caught: ${e}
                                        """

                                }
                            }
                        }
                    }
                }
                post {
                    always {
                        deleteDir()
                    }
                }
            }

            stage('Checkmarx') {
               agent { label 'slave' }
                     when { branch 'XAI_NEW' }
                       steps {
                          lock(resource: "${env.JOB_NAME}/60") {
                            milestone 50
                             measureDuration(script: this, measurementName: 'checkmarx_duration') {
                              executeCheckmarxScan script: this
                    }
                }
            }
                post { always { deleteDir() } }
            }

            stage('PPMS Whitesource Compliance') {
                      agent { label 'slave' }
                         when { branch 'XAI_NEW' }
                                steps {
                                   lock(resource: "${env.JOB_NAME}/50") {
                                       milestone 60
                                       measureDuration(script: this, measurementName: 'PPMS_duration') {
                                          executePPMSComplianceCheck script: this, scanType: 'whitesource'
                             }
                          }
                       }
                      post { always { deleteDir() } }
                }


            stage('Create traceability report') {
               agent { label 'slave' }
                      when { branch 'XAI_NEW' }
                            steps {
                                  sapCreateTraceabilityReport(
                                        deliveryMappingFile: '.pipeline/delivery.mapping',
                                        requirementMappingFile: '.pipeline/requirement.mapping',
                                        failOnError: false )
                            }
            }
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
