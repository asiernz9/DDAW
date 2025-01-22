pipeline {
    agent any

    environment {
        NODE_ENV = 'production' // Define el entorno
    }

    stages {
        stage('Checkout') {
            steps {
                // Clona el repositorio del código fuente
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Instala las dependencias del proyecto
                sh 'npm install'
            }
        }

        stage('Run Tests') {
            steps {
                // Ejecuta las pruebas
                sh 'npm test'
            }
        }

        stage('Build') {
            steps {
                // Construye el proyecto
                sh 'npm run build'
            }
        }

        stage('Deploy') {
            steps {
                // Implementa el despliegue (si aplica)
                echo 'Deployment stage - configura tus pasos aquí'
            }
        }
    }

    post {
        always {
            // Limpia el espacio de trabajo después de la ejecución
            cleanWs()
        }
        success {
            echo 'Pipeline ejecutado con éxito'
        }
        failure {
            echo 'Pipeline falló'
        }
    }
}
