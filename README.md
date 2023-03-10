# test-mordecai
locally installing and running mordecai from the windows command line

## Instructions to make

### Create an environment
conda create --name mordecai_env_3.8 python=3.8
conda activate mordecai_env_3.8


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






