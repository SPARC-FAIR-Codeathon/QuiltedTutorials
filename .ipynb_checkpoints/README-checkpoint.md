# **<center>SPARC FAIR Codeathon 2022</center>**
<div align="center">
<a href="https://github.com/SPARC-FAIR-Codeathon/SPARC-Tutorial">
        <img src="SPARC-tutorial-site/static/logos/quilt_logo.png" alt="QuiltedTutorials" width=250>
</a>
</div>

# <center>The Quilted tutorial, or how to become a **SPARC** guru</center>

#### The tutorials and everything is available at [here](https://quilted-tutorial.github.io/SPARC-guru/), if the website is no longer operational, the instructions that follow will work identically.

## **Table of Content**
 1. [**About**](#About)
 2. [**Dependencies**](#Dependencies)
 3. [**Getting started**](#Getting-started)
 4. [**License**](#License)
 5. [**Team**](#Team)
 6. [**Acknowledgments**](#Acknowledgments)
 
### **About**
The **S**timulating **P**eripheral **A**ctivity to **R**elieve **C**onditions ([**SPARC**](https://sparc.science/about)) program is supported by the NIH Common Fund to provide a scientific and technological foundation for future bioelectronic medicine devices and protocols. The initiative is made up of over ***60*** research teams scattered around the globe, all working together on a common objective. The entire project is **Open Source** and follows the **F**indable, **A**ccessible, **I**nteroperable, and **R**eusable ([**FAIR**](https://www.nature.com/articles/sdata201618)) guidelines for data management.

In 2021, the amazing team of the **D**ata and **R**esource **C**enter ([**DRC**](https://pubmed.ncbi.nlm.nih.gov/34248680/)) organised a [**Codeathon**](https://sparc.science/help/2021-sparc-fair-codeathon) to improve various elements of the **SPARC** program. This year, they've done it [again](https://sparc.science/help/2022-sparc-fair-codeathon)! 

The tutorial was designed to demonstrate different features from the [**SPARC**](https://sparc.science/) project. The goal will be to project the 2D locations of neurites in the rat stomach onto a 3D scaffhold of the organ. The data points and the 3D scaffhold will be pulled from **SPARC** datasets. Because the data is [**FAIR**](https://www.nature.com/articles/sdata201618) we will be combining three different datasets of the spatial distribution of the vagal afferents and efferents.

### **Dependencies**
Here is the list of all the dependencies that are needed to run this tutorial. They are all listed in the requirements.txt file as well

   * pandas, version 1.4.3
   * openpyxl, version 3.0.10
   * opencmiss.argon, version x

### **Getting started**
If you have not already done so, clone the GitHub repository onto your local machine into the _SPARC-tutorial_ folder wit the following command:

    $ git clone git@github.com:SPARC-FAIR-Codeathon/SPARC-Tutorial.git SPARC-tutorial

The tutorial is contained in a Jupyter Notebook and requires Jupyter Lab to run. 
If you are unsure if Jupyter Lab is installed on your machine use this command in a terminal:

    $ which jupyter-lab
    
If there is no output, [install](https://jupyter.org/install) Jupyter Lab with the following command:
    
    $ pip install jupyterlab
    
Once this is done or if you already have Jupyter Lab installed on your machine simply navigate into the cloned directory and run Jupyter Lab:

    $ cd SPARC-tutorial && jupyter-lab

From your browser, you can then open the notebook by clicking on ***SPARC-tutorial.ipynb*** and follow the tutorial from there. 
    
### **License**
This tutorial is available under the MIT License, thereby making it fully accessible to anyone.

### **Team**

   * [Yuda Munarko](https://github.com/napakalas) (lead)
   * [Omkar Athavale](https://github.com/OmkarAthavale) (Developer)
   * [Mathias Roesler](https://github.com/mathiasroesler) (Writter)
   * [Niloofar Shahidi](https://github.com/Niloofar-Sh) (Writter)
   * [Kenneth Tran](https://github.com/ktra014) (Developer)

### **Acknowledgments**
We would like to thank the organizers of the 2022 **SPARC FAIR** Codeathon as well as the **SPARC DRC** teams for their guidance and help during this Codeathon. Find out more about them in the About section!
