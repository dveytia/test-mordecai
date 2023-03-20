# test-mordecai
locally installing and running mordecai from the windows command line

## Instructions to make

### Create an environment

Using Conda

	conda create --name mordecai_env_3.8 python=3.8
	conda activate mordecai_env_3.8

Or using pip in bash build from scratch

	$ python3 -m venv mordecai_env
	$ source mordecai_env/bin/activate # in windows cmd it's mordecai_env\Scripts\activate

then install packages

	$ python3 -m pip install ipykernel
	$ python3 -m pip install mordecai
	$ python3 -m pip install spacy==2.3
	$ python3 -m pip install numpy==1.21
	$ python3 -m pip install h5py==3.8.0
OR

	$ python3 -m pip install -r requirements.txt

Then use ipykernel to open the environment in jupyter

	$ ipython kernel install --user --name=mordecai_env
	$ jupyter-lab

Then open juypyter lab and in the upper right hand select the kernel for mordecai_env

### Install packages

In jupyter, run the file: Installing_mordecai.pynb to install the necessary packages and set up docker. Docker must be installed first (see https://docs.docker.com/engine/installation/). 


## Instructions to initialize on new computer

in windows cmd (run as admin)

	cd (path to working directory)
	conda env create -f mordecai_env_3.8.yml
	conda activate mordecai_env_3.8
	conda install -c anaconda ipykernel
	ipython kernel install --user --name=envname
	jupyter-lab


Then in open the file "installing_mordecai.ipynb". In the upper RH corner, select envname as the kernel, and run the installation for mordecai and download the spacy library. Also run the docker commands if needed


### Without ipykernel, run from cmd line

Without ipykernel, the code will only run from the windows command line

	Ctrl+C (twice to exit jupyter lab)

	(path to conda env python.exe) 

Now you are running python from the cmd line:
	from mordecai import Geoparser
	geo = Geoparser()
	geo.geoparse("I travelled from Oxford to Ottawa")
	exit()

(path to conda env python.exe) test-geoparse.py


## Instructions to run once already initialized

In Windows cmd (as admin)

	conda activate mordecai_env_3.8

	cd (path to working directory)

	docker run -d -p 127.0.0.1:9200:9200 -v (path to wd)\geonames_index:/usr/share/elasticsearch/data elasticsearch:5.5.2

And then one of the following commands

	(path to conda env python.exe) (name of .py script to run)

	jupyter-lab






