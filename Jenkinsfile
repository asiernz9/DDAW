pipeline {
    agent any  

    stages {
        stage('Clonar Código') {
            steps {
                git url: 'https://github.com/asiernz9/DDAW.git', branch: 'main'
            }
        }

        stage('Construir Imagen Docker') {
            steps {
                echo 'Construyendo la imagen Docker...'
                powershell '''
                docker build -t ddaw-app .
                '''
            }
        }

        stage('Levantar Contenedor') {
            steps {
                echo 'Deteniendo y eliminando contenedores previos si existen...'
                powershell '''
                $container = docker ps -aq -f name=pokemon-app
                if ($container) {
                    docker stop pokemon-app
                    docker rm pokemon-app
                }
                '''

                echo 'Ejecutando el contenedor...'
                powershell '''
                docker run -d -p 8000:8000 --name pokemon-app ddaw-app
                '''

                echo 'Esperando 10 segundos para asegurar que el contenedor está listo...'
                powershell 'Start-Sleep -Seconds 10'

                echo 'Mostrando logs del contenedor para verificar que está en ejecución...'
                powershell 'docker logs pokemon-app'
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                echo 'Ejecutando pruebas dentro del contenedor...'
                powershell '''
                docker exec pokemon-app pytest tests/
                '''
            }
        }
    }
}
