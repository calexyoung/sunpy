------------
Installation
------------
Pre-requisites
--------------
SunPy stands on the shoulders of giants:

* `NumPy <http://numpy.scipy.org/>`_
* `Matplotlib <http://matplotlib.sourceforge.net/>`_
* `PyFITS <http://www.stsci.edu/resources/software_hardware/pyfits>`_

Linux
-----
Installation instructions for linux.

Ubuntu
^^^^^^
To begin, install the pre-requisites for SunPy using apt-get: ::

    sudo apt-get install python-numpy python-matplotlib python-pyfits python-scipy bzr ipython

The ``ipython`` package in the above list installs the `IPython enhanced console 
<http://ipython.scipy.org/moin/>`_ and is optional but recommended.

Next, use Bazaar to download a copy of the latest version of SunPy: ::

    bzr branch lp:sunpy

Done! To see if everything went okay, start a Python session and try importing
sunpy:

>>> import sunpy
>>> sunpy.Map(‘sunpy/dev/sample-data/AIA20110319_105400_0171.fits’).plot()

Mac
---
Installation instructions for Mac.

Windows
-------
Installation instructions for Windows.


**1. Install Python**

To begin, grab the latest version of the Python 2.x for Windows from the
`Python downloads page <http://www.python.org/getit/>`_.  Run the installer
and follow the instructions on screen.


Next, in order to enable Python to find libraries installed on your computer
you need to update the ``PATH`` environmental variable on your machine:

    1. Click ``Start``-> ``Control Panel`` -> ``System`` -> ``Advanced system settings`` -> ``Environment variables``
    2. Find the ``PATH`` environmental variable under either user or system variables and the filepath to your Python installation (e.g. "C:\Python27").
    

**2. Install SciPy, NumPy, Matplotlib, and IPython**

Next we will install `NumPy <http://numpy.scipy.org/>`_, `SciPy 
<http://www.scipy.org/>`_, `Matplotlib <http://matplotlib.sourceforge.net/>`_, 
and `IPython <http://ipython.scipy.org/moin/>`_. Install each package by running
the corresponding downloaded executable.  They should  automatically find the 
location of the Python installation.

    1. To begin, download and install the latest `NumPy Windows binary <http://sourceforge.net/projects/numpy/files/NumPy/1.6.0b2/numpy-1.6.0b2-win32-superpack-python2.7.exe/download>`_.
    2. Next, download and install the latest version of the `SciPy Windows binary <http://sourceforge.net/projects/scipy/files/scipy/0.9.0/scipy-0.9.0-win32-superpack-python2.7.exe/download>`_
    3. Download and install the latest version of `Matplotlib for Windows <http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.0.1/matplotlib-1.0.1.win32-py2.7.exe/download>`_.
    4. Finally, as an option (but recommended step), download and install `IPython for Windows <http://ipython.scipy.org/dist/0.10.1/ipython-0.10.1.win32-setup.exe>`_.
    

**3. Install PyFITS**

Finally, SunPy uses the PyFITS library to read 
`FITS <http://en.wikipedia.org/wiki/FITS>`_ files. PyFITS does
not offer a Windows binrary, so we will need to install it some other way.
Fortunately, there is a great tool for Python called ``easy_install`` which 
makes installing many libraries very trivial. EasyInstall is part of the
Setuptools package.


To install `Setuptools 
<http://pypi.python.org/pypi/setuptools>`_, simply download and run the `latest
windows installer 
<http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe>`_.

To install PyFITS, open a console and call ``easy_install.exe pyfits`` from 
inside the ``scripts`` directory of your Python installation: ::

    cd C:\Python27\Scripts
    easy_install.exe pyfits


**4. Install Bazaar**

Once you have Python 2.7 installed, download and run the `Bazaar Python 2.7 
Windows Installer <http://wiki.bazaar.canonical.com/WindowsDownloads>`_. We are
now ready to grab the latest version of SunPy. 


To begin open a Bazaar command-prompt (``Start`` -> ``Bazaar`` -> ``Bazaar 
command-prompt``) and run: ::

    bzr branch lp:sunpy

This will download the latest version of SunPy. You then need to copy the 
folder sunpy (from inside the root sunpy directory) to ``C:\Python27\Lib`` so 
that Python can find it.

.. Note::
 By default, the bzr command will only execute if you are in 
 ``C:\Python27\Scripts`` so any libraries or code you wish you be able to call
 globally should be placed in here.

To test it all out, open a new Python shell and try typing: ::

>>> import sunpy
>>> sunpy.Map(‘sunpy/dev/sample-data/AIA20110319_105400_0171.fits’).plot()



