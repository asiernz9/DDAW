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
                echo 'Verificando si el contenedor pokemon-app ya existe...'
                
                script {
                    def containerId = powershell(script: 'docker ps -aq -f name=pokemon-app', returnStdout: true).trim()
                    if (containerId) {
                        echo 'Deteniendo y eliminando el contenedor pokemon-app existente...'
                        powershell "docker stop pokemon-app || true"
                        powershell "docker rm pokemon-app || true"
                    } else {
                        echo 'No se encontró el contenedor pokemon-app en ejecución.'
                    }
                }

                echo 'Ejecutando el contenedor...'
                powershell 'docker run -d -p 8000:8000 --name pokemon-app ddaw-app'

                echo 'Esperando 5 segundos antes de mostrar logs...'
                powershell 'sleep 5; docker logs pokemon-app'
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
