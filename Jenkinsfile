pipeline {
    agent any  

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
                        sh 'ls -l'
                        sh 'cat requirements.txt'
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
                echo 'Construyendo la imagen Docker...'
                sh 'docker build -t ddaw-app .'

                echo 'Verificando imágenes creadas...'
                sh 'docker images | grep ddaw-app'

                echo 'Deteniendo cualquier contenedor previo...'
                sh 'docker stop pokemon-app || true'
                sh 'docker rm pokemon-app || true'

                echo 'Ejecutando el contenedor en modo debug...'
                sh 'docker run -d -p 8000:8000 --name pokemon-app --link pokemon-redis ddaw-app'

                echo 'Esperando 5 segundos antes de mostrar logs...'
                sh 'sleep 5 && docker logs pokemon-app'
            }
        }
    }
}

