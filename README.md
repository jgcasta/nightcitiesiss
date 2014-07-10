Nightcitiesiss Application for georreferencing cities at night images from ISS
==============================================================================

[![Build Status](https://travis-ci.org/jgcasta/nightcitiesiss.svg?branch=master)](https://travis-ci.org/jgcasta/nightcitiesiss)

We are memebers of the  Group of Extragalactic Astrophysics and Astronomical Instrumentation from Universidad Coplutense de Madrid [GUAIX](http://guaix.fis.ucm.es). Among our activities is light pollution study and the energy consumption derived from it. We use images taken from the International Space Station as part of our investigations, provided by NASA

To compare the images with the different light sources on the earth, we need to georreference every picture. This is a process of associating a physical map with spatial locations to the picture, where locations are represented using a coordinate reference system, in this case Longitude and Latitude. Due to the large number of images, we need your help. Some of these pictures are from unknown locations for us, and it is very difficult identify some features on the picture.

However, a lot of people around the world will know the cities. We need you identify some features and connect them with some point on a map. This application allows you to do this.

The process is very easy. The ISS image will be loaded in the left pannel, and a OpenStreetMap on the right one. If we know the position of the center of the picture, the map will be centered . The aim is rotate and move te picture to allow you to identify some features you know where are they located. You have some simple tools to make zoomin, zoomout and drag the picture. Even you can rotate it click on Shift and left mouse button. When you identify one, just click on it and a pair of XY coordinates will appear in the XY list. Now you have to identify the same feature on the map and click it. The longitud and latitud pair of coordinates will appear on the list.

If you make a mistake, you can delete one point. Jus select it and click on "Delete".

When you finish to select points, click on Save, and another image will be loaded. If you don't know about the picture, just click on "Don't know".

If you need more information about this picture, you can click on "ISS picture data", and NASA data will be displayed. At last, you also can share it through Twitter

We apreciate your job very much

Tutorial
========

[![ScreenShot](http://i.imgur.com/zdHPu0a.png)](http://www.youtube.com/embed/z3p1jbqpXrY)


Framework
=========

Based on PyBossa, this application by [José Gómez Castaño](http://guaix.fis.ucm.es/DarkSkies) allows the georreference of City Night Images taken from International Space Station. The application can be used at [Nigth Cites ISS](http://crowdcrafting.org/app/nightcitiesiss)

This application has three files:

*  createTasks.py: for creating the application in PyBossa, and fill it with some tasks.
*  get_image.py: for provide data images.
*  template.html: the view for every task and deal with the data of the answers.
*  tutorial.html: a simple tutorial for the volunteers.


Testing the application
=======================

You need to install the pybossa-client first (use a virtualenv):

```bash
    $ pip install pybossa-client
```
Then, you can follow the next steps:

*  Create an account in PyBossa
*  Copy under your account profile your API-KEY
*  Run python createTasks.py -u http://crowdcrafting.org -k API-KEY
*  Open with your browser the Applications section and choose the FlickrPerson app. This will open the presenter for this demo application.

Documentation
=============

We recommend that you read the section: [Build with PyBossa](http://docs.pybossa.com/en/latest/build_with_pybossa.html) and follow the [step by step tutorial](http://docs.pybossa.com/en/latest/user/tutorial.html).

**NOTE**: This application uses the [pybossa-client](https://pypi.python.org/pypi/pybossa-client) in order to simplify the development of the application and its usage. Check the [documentation](http://pythonhosted.org/pybossa-client/).


LICENSE
=======

Creative Commons Reconocimiento-NoComercial-CompartirIgual 4.0 Internacional License
[![ScreenShot](http://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)]

![UCM](https://raw.githubusercontent.com/jgcasta/nightcitiesiss/master/img/LogoUCM.jpg) ![Campus](https://raw.githubusercontent.com/jgcasta/nightcitiesiss/master/img/campuslogo.gif) ![MediaLab](http://medialab-prado.es/static/img/logo_mlp_web_rgb.png) ![LoNNe](http://www.cost-lonne.eu/wp-content/themes/Puschnig/images/logo.gif)



![NASA](https://raw.githubusercontent.com/jgcasta/nightcitiesiss/master/img/nasalogo.jpg) ![ROSCOSMOS](https://raw.githubusercontent.com/jgcasta/nightcitiesiss/master/img/roscosmos.jpg) ![ESA](https://raw.githubusercontent.com/jgcasta/nightcitiesiss/master/img/esa.jpg) ![CANADA](https://raw.githubusercontent.com/jgcasta/nightcitiesiss/master/img/canada.jpg) JAXA

