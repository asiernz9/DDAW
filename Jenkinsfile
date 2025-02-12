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
                script {
                    if (fileExists('requirements.txt')) {
                        echo 'El archivo requirements.txt existe. Procediendo con la instalación...'
                        sh 'cat requirements.txt'  // Mostrar el contenido de requirements.txt
                        sh 'pip install -r requirements.txt'
                    } else {
                        error 'El archivo requirements.txt no existe'
                    }
                }
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
