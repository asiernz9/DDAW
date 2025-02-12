pipeline {
    agent any  // Usa cualquier agente disponible en Jenkins

    stages {
        stage('Clonar Código') {
            steps {
                git url: 'https://github.com/asiernz9/DDAW.git', branch: 'main'
            }
        }

        stage('Instalar Dependencias') {
            steps {
                echo 'Instalando dependencias...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Construcción') {
            steps {
                echo 'Compilando el proyecto...'
            }
        }

        stage('Pruebas') {
            steps {
                echo 'Ejecutando pruebas...'
                
            }
        }

        stage('Despliegue') {
            steps {
                echo 'Desplegando la aplicación...'
                sh 'docker build -t ddaaw-app .'
                sh 'docker run -d -p 8000:8000 ddaaw-app'
            }
        }
    }
}

