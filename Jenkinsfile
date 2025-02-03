pipeline {
    agent any
    stages {
        stage('Preparar entorno') {
            steps {
                script {
                    // Verificar si Docker está instalado y funcionando
                    sh 'docker --version'
                }
            }
        }
        stage('Construir imagen Docker') {
            steps {
                script {
                    // Construir la imagen Docker
                    sh 'docker build -t my-app:latest .'
                }
            }
        }
        stage('Ejecutar contenedor') {
            steps {
                script {
                    // Iniciar el contenedor en modo background
                    sh 'docker run -d --name my-app-container -p 8080:8080 my-app:latest'
                }
            }
        }
        stage('Ejecutar pruebas') {
            steps {
                script {
                    // Ejecutar pruebas dentro del contenedor
                    sh 'docker exec my-app-container npm test'
                }
            }
        }
    }
    post {
        always {
            // Imprimir logs del contenedor
            script {
                sh 'docker logs my-app-container'
            }
        }
        success {
            // Dejar el contenedor corriendo si todo funciona correctamente
            echo 'El contenedor sigue ejecutándose correctamente.'
        }
        failure {
            // Detener y eliminar el contenedor en caso de fallo
            script {
                sh 'docker stop my-app-container || true'
                sh 'docker rm my-app-container || true'
            }
            echo 'Las pruebas fallaron. El contenedor fue detenido y eliminado.'
        }
    }
}

