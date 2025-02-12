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
                sh 'docker build -t ddaw-app .'
            }
        }

        stage('Levantar Contenedor') {
            steps {
                echo 'Deteniendo y eliminando contenedores previos si existen...'
                sh 'docker stop pokemon-app || true'
                sh 'docker rm pokemon-app || true'

                echo 'Ejecutando el contenedor...'
                sh 'docker run -d -p 8000:8000 --name pokemon-app ddaw-app'

                echo 'Esperando 10 segundos para asegurar que el contenedor está listo...'
                sh 'sleep 10' // Ajustado para esperar un poco más antes de ejecutar las pruebas

                echo 'Mostrando logs del contenedor para verificar que está en ejecución...'
                sh 'docker logs pokemon-app'
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                echo 'Ejecutando pruebas dentro del contenedor...'
                sh 'docker exec pokemon-app pytest tests/'  // Cambia `tests/` por la ruta correcta si es diferente
            }
        }
    }
}
