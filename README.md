# Creación y despliegue de una plantilla de AWS CloudFormation utilizando AWS CDK (Cloud Development Kit)

## **Objetivo**
Las plantillas de AWS CloudFormation utilizan un formato basado en YAML o JSON personalizado, empleado una sintaxis declarativa. Sin embargo, para muchos desarrolladores de infraestructura, implementar Infraestructura como Código (IaC) puede suponer un inconveniente y por norma general, prefieren desarrollar emplado los lenguajes imperativos más habituales (Python, Java, .NET, ...). Para ello existe **AWS CDK (Cloud Development Kit)**, que no es más que un framework de código abierto que actúa como un wrapper de AWS CloudFormation que permite crear y desplegar plantillas de AWS CloudFormation mediante programación imperativa. Actualmente AWS CDK está disponible para Java, TypeScript, Python, .NET y Go.

En este repositorio se muestra cómo se puede definir una plantilla de AWS CloudFormation y desplegar una pila a partir de dicha plantilla, empleando el framework de AWS CDK para Python.

La plantilla que se define creará una VPC, y un servicio web escalable mediante un grupo de Autoescalado de EC2, con instancias administradas por AWS Systems Manager tras un balanceador de carga de aplicación.

## **Requerimientos**
* Disponer de una cuenta de AWS
* Disponer de Python instalado con soporte para entornos virtuales (venv)
* Disponer de un entorno Linux con acceso programático configurado a los servicios de AWS

## **Realización**

1. Instalar la herramienta AWS CDK Toolkit:

        npm install -g aws-cdk
   
2. Clonar el presente repositorio:

        git clone https://github.com/jose-emilio/aws-cdk-demo.git

3. Crear un directorio para el proyecto. En este caso se asumirá `cdk_demo`:

        mkdir cdk_demo && cd cdk_demo

4. Inicializar el proyecto de AWS CDK:

        cdk init app --language python

5. Activar el origen del entorno virtual:

        source .venv/bin/activate

6. Copiar el contenido del repositorio en el directorio del proyecto:

        cp -R ../aws-cdk-demo/* .

7. Instalar las dependencias (AWS CDK) del proyecto, especificadas en el archivo `requirements.txt`:

        pip install -r requirements.txt

8. Para generar la plantilla de AWS CloudFormation, se ejecuta la orden:

        cdk synth

    La orden anterior mostrará por la consola la plantilla de AWS CloudFormation creada a partir del proyecto de AWS CDK

9. Para crear la pila de AWS CloudFormation, bastará con ejecutar la orden:

        cdk deploy

    Siguiendo el asistente, se podrá realizar un seguimiento de cómo se despliegan los recursos definidos en la plantilla generada. Tras el despliegue, aparecerá como salida el nombre DNS del punto de enlace del servicio. Bastará con abrir una ventana de un navegador y acceder por HTTP (no HTTPS) a dicho punto de enlace.

10. Para eliminar los recursos, se ejecuta la orden:

        cdk destroy

