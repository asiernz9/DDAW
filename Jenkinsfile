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
                powershell 'docker build -t ddaw-app .'
            }
        }

        stage('Levantar Contenedor') {
            steps {
                echo 'Deteniendo y eliminando contenedores previos si existen...'
                powershell '''
                $container = docker ps -aq -f name=pokemon-app
                if ($container -ne "") {
                    docker stop pokemon-app
                    docker rm pokemon-app
                } else {
                    Write-Host "No se encontró el contenedor pokemon-app"
                }
                '''

                echo 'Ejecutando el contenedor...'
                powershell 'docker run -d -p 8000:8000 --name pokemon-app ddaw-app'

                echo 'Esperando 5 segundos antes de mostrar logs...'
                powershell 'Start-Sleep -Seconds 5; docker logs pokemon-app'
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                echo 'Ejecutando pruebas dentro del contenedor...'
                powershell 'docker exec pokemon-app pytest tests/'  // Cambia `tests/` por la ruta correcta si es diferente
            }
        }
    }
}


