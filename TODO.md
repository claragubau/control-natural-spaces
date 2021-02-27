## Material

- Raspberry 3B:

  - Quad Core 1.2GHz Broadcom BCM2837 64bit CPU
  - 1GB RAM
  - BCM43438 wireless LAN and Bluetooth Low Energy (BLE) on board
  - 100 Base Ethernet
  - 40-pin extended GPIO
  - 4 USB 2 ports
  - 4 Pole stereo output and composite video port
  - Full size HDMI
  - CSI camera port for connecting a Raspberry Pi camera
  - DSI display port for connecting a Raspberry Pi touchscreen display
  - Micro SD port for loading your operating system and storing data
  - Upgraded switched Micro USB power source up to 2.5A

- Placa de gestió d'energia (HAT), la qual anirà directament connectada a la GPIO de la Raspberry. La placa emmagatzemarà la energia del sol en una bateria. Tot i que tècnicament podríem treballar directament amb la placa i la Raspberry, això implicaria molts factors:

  - El panell solar és molt gran.
  - Està col·locat en una regió molt assoleiada.
  - El panell extreu exactament 5V i 2A.
  - No volem córrer la Raspberry quan hi ha núbol o és fosc.

  Idea: fer servir el PiJuice Solar Kit que conté la placa solar i la placa de gestión d'energia.  Més en concret el panell de 12W.

  | Raspberry Pi Model           | Solar Panel Size | Output Voltage | Output Power | Output Current |
  | ---------------------------- | ---------------- | -------------- | ------------ | -------------- |
  | Pi Zero/Zero W (minimum)     | 6W               | 5V             | 5W           | 1A (1000mAh)   |
  | Pi Zero/Zero W (recommended) | 12W              | 5V             | 10W          | 2A (2000mAh)   |
  | Pi 3/3B+ (minimum)           | 12W              | 5V             | 10W          | 2A (2000mAh)   |
  | Pi 3/3B+ (recommended)       | 22W              | 5V             | 20W          | 4A (4000mAh)   |

- Bateria, tenim dos opcions:

  - Li-Ion, més barates però menys denses de manera que ocupen més. 

  - Li-Po, més cares però poden acumular més energia en un espain més reduït.

    PiJuice Solar admet els dos tips

- Sixfab 3G/4G & LTE Base HAT, mòdul per a dispondre d'internet a la placa, també necessitaríem la targeta SIM. Així podrem enviar la informació i monitoritzar la salut de cada dispositiu. TODO: read https://www.robertlucian.com/2018/08/29/mobile-network-access-rpi/ (opció sense targeta SIM)

- PiCamera Module

- Server

  

## Implementació

- Opció 1: fer el model en un servidor i enviar els frames: https://towardsdatascience.com/i-built-a-diy-license-plate-reader-with-a-raspberry-pi-and-machine-learning-7e428d3c7401
  - No implica les complicacions de fer un model suficientment petit com per a que capiga a la memòria de la Raspberry
  - Tecnologies emprades:
    - Python com a llenguatge principal
    - Docker per a fer fàcil la instalació de nous dispositius
    - Docker-compose per a gestionar la UI i el server que rep les images
    - Nginx per a fer al server el reverse proxy
    - Fastapi per a la API que enviaria rebria les imatges i retornaria a la UI els resultats
    - ReactJs per a la UI amb els resultats en real-time
    - **Darknet amb YOLOv2 (entrenat amb PascalVOC) + OpenALPR per a la detecció de cotxes i matrícules**
    - PostgreSQL per a la base de dades de deteccions
- Opció 2: fer servir TensorflowLite + OpenALPR a la raspberry
  - Primer detectaríem el cotxe i després runnejaríem OpenALPR
  - https://github.com/openalpr/openalpr
  - Software preparat per a fer reconèixer LicensePlates
  - Menys accuracy
  - Tecnologies emprades:
    - Python com a llenguatge principal
    - Docker per a fer fàcil la instalació de nous dispositius
    - Nginx per a fer al server el reverse proxy
    - Docker-compose per a gestionar la UI i el server que rep les images
    - Fastapi per a la API que enviaria rebria les imatges i retornaria en una UI els resultats
    - ReactJs per a la UI amb els resultats en real-time
    - **Tensorflow Lite amb SSD-MobileNet (entrenat amb COCO)**
    - PostgreSQL per a la base de dades de deteccions

## Pressupost

