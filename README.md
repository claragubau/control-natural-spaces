<h1 align="center"> Control of Access to Natural Spaces</h1>

[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Motivation
Aquest projecte está motivat per [Smart Catalonia]( https://participa.challenge.cat/assemblies/agentsrurals). L'objectiu és optimitzar i automatizar el control d'accés a espais naturals.


## Requisits
### Material
- PiCamera
- Raspberry Pi

### √ös
Per a instalar el software, runneja el següent script en una Raspberry amb càmera i internet.

```bash
source run.sh OPTION
```
On option és un paràmetre per a escollir la estratègia desitjada:
    - **openALPR**: utilitzar OpenALPR
    - **tensorflow**: utilitzar Tensorflow Lite + OpenALPR

## Com funciona?
### Opció 1: OpenALPR
Aquesta seria la nostra primera opció ja que és la que requereix dispositius amb menys potència. OpenALPR és una llibreria open-source que detecta matrícules que compleix tots els nostres requísits:
- L'imatge havia de ser processada localment: enviar streamings de vídeo a un servidor i analitzar-los allà és una solució molt poc eficient, a més és una solució que introdueix a la equació la latència de la xarxa lo qual pot fer que tot vagi molt lent.
- Ha de funcionar amb imatges de baixa qualitat, la idea és fer servir una càmara d'una raspberry.
- Ha de ser de lliure ús: en aquest cas la llibreria disposa d'una llic√®ncia open source AGPL.

L'script que realitzaria aquesta opció el podem trobar a [src/openALPR.py](src/openALPR.py).

### Opció 2: Tensorflow Lite + OpenALPR
En el cas de que el nombre de falsos positius fos molt alt, optaríem per a fer servir també una xarxa neuronal convolucional per a detectar primer als cotxes. En aquest cas hem obtat per un detector molt eficient pensat per a ser executat en dispositius mobils, SSD Mobile Net (https://arxiv.org/pdf/1704.04861.pdf). A més, aprofitaríem el fet de que els cotxes son un objecte prou comú per a utilitzar xarxes que ja estan entrenades (i així disminuir costos).
Un cop detectat el cotxe, llavors hauríem de córrer OpenALPR per a detectar la matrícula del mateix. En el cas de que OpenALPR no detectés cap matrícula (per diverses causes i.e. només es veu una part del cotxe o una branca la està tapant), continuaríem runnejant el model, el qual eventualment detectaria un frame on el cotxe es pot visualitzar completament.

El framework per a treballar triat ha estat Tensorflow Lite, una libreria d'aprenentatge profund creada per Google específicament per a fer inferència a dispositius de poca capacitat.

L'script que realitzaria aquesta opció el podem trobar a [src/openALPR_tensorflow.py](src/openALPR_tensorflow.py).
