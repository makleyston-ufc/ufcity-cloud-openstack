from setuptools import setup

setup(
    name='UFCityMicroserviceLib',
    version='0.1',
    packages=['UFCityMicroserviceLib', 'UFCityMicroserviceLib.mqtt', 'UFCityMicroserviceLib.storage'],
    install_requires=[
        'paho-mqtt>=2.0.0',
        'pymongo'
    ],
    author='Danne Makleyston G. Pereira',
    author_email='makleyston@email.com',
    description='Abstraction library to UFCity Microservices',
    long_description='This lib abstracts storage and communication functions between microservices and MongoDB and MQTT broker, respectively, in the context of UFCity.',
    long_description_content_type='text/markdown',  # Use 'text/plain' se for um texto simples
    url='https://makleyston-ufc.github.io/ufcity/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='mqtt library UFCityMicroserviceLib',
)
