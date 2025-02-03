pipeline {
    agent any  // Usa cualquier agente disponible en Jenkins

    stages {
        stage('Clonar Código') {
            steps {
                git url: 'https://github.com/asiernz9/DDAW.git', branch: 'main'
            }
        }

        stage('Construcción') {
            steps {
                echo 'Compilando el proyecto...'
                // Aquí puedes agregar comandos como:
                // sh 'mvn clean package'  (Para Maven)
                // sh 'npm install'  (Para Node.js)
            }
        }

        stage('Pruebas') {
            steps {
                echo 'Ejecutando pruebas...'
                // sh 'mvn test'  (Ejecutar pruebas con Maven)
            }
        }

        stage('Despliegue') {
            steps {
                echo 'Desplegando la aplicación...'
                // Aquí puedes agregar pasos para desplegar, como subir a un servidor o Docker
            }
        }
    }
}

