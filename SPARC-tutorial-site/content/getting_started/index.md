---
title: "Getting started"

description: "You will find here the instructions to start the tutorial" 
menu:
  main:
    weight: 1
---
### **Initial setup**
If you have not already done so, clone the GitHub repository onto your local machine into the _SPARC-tutorial_ folder wit the following command:

    $ git clone git@github.com:SPARC-FAIR-Codeathon/SPARC-Tutorial.git SPARC-tutorial

The tutorial is contained in a Jupyter Notebook and requires Jupyter Lab to run. 
If you are unsure if Jupyter Lab is installed on your machine use this command in a terminal:

    $ which jupyter-lab
    
If there is no output, [install](https://jupyter.org/install) Jupyter Lab with the following command:
    
    $ pip install jupyterlab
    
Once this is done or if you already have Jupyter Lab installed on your machine simply navigate into the cloned directory and run Jupyter Lab:

    $ cd SPARC-tutorial && jupyter-lab --LabApp.token='' --no-browser

Once Jupyter Lab is running you are all set and ready to go! Follow this [link](http://127.0.0.1:8888/lab) to get started and open the SPARC-tutorial.ipynb file.
