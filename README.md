# test-mordecai
locally installing and running mordecai from the windows command line

## Instructions to make

### Create an environment

Using Conda

	conda create --name mordecai_env_3.8 python=3.8
	conda activate mordecai_env_3.8

Or using pip in bash build from scratch

	$ python -m venv mordecai_env
	$ source mordecai_env/bin/activate # in windows cmd it's mordecai_env\Scripts\activate

then install packages

	$ python -m pip install ipykernel
	$ python -m pip install mordecai
	$ python -m pip install spacy==2.3
	$ python -m pip install numpy==1.21
	$ python -m pip install h5py==3.8.0
	$ python -m pip install futures
	$ python -m pip install torch   


    
OR

	$ python -m pip install -r requirements.txt

Then use ipykernel to open the environment in jupyter

	$ ipython kernel install --user --name=mordecai_env_3.8
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
    
Or

	docker run -d -p 127.0.0.1:9200:9200 -v $(pwd)/geonames_index/:/usr/share/elasticsearch/data elasticsearch:5.5.2

And then one of the following commands:
	/usr/bin/python3 analyses/01_geoparse-mordecai.py # [path to python interpreter] [path to script] 

	(path to conda env python.exe) (name of .py script to run)

	jupyter-lab # then select mordecai_env_3.8 for the kernel



### What I'm using in rossinante

* Note to check if the docker is already running, use docker ps -a ; and to remove docker rm "random name"

	screen -S mordecai
	conda activate mordecai_env_3.8
	cd (path to working directory)
	docker run -d -p 127.0.0.1:9200:9200 -v $(pwd)/geonames_index/:/usr/share/elasticsearch/data elasticsearch:5.5.2

For script in command line
	/usr/bin/python3 analyses/01_geoparse-mordecai.py # [path to python interpreter] [path to script]
    
For working in jupyter lab
	jupyter-lab # then select mordecai_env_3.8 for the kernel





