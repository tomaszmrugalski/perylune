setup:
	# clone poliastro if needed
	@if [ ! -d poliastro ]; then                            \
		echo "STEP 1: Cloning poliasto";                    \
		git clone https://github.com/poliastro/poliastro ;  \
	else                                                    \
		echo "STEP 1: Poliastro detected, updating";        \
		cd poliastro;                                       \
		git pull;                                           \
		cd ..;                                              \
	fi

	# create virtualenv if needed
	@if [ ! -d venv ]; then                                 \
	    echo "STEP 2: Creating virtual environment (venv)"; \
		python3 -m venv venv;                               \
	else                                                    \
	    echo "STEP 2: venv already set up";                 \
	fi

	# set up perylune.ini if needed
	@if [ ! -f perylune.ini ]; then                           \
		echo "STEP 3: Perylune.ini not found, copying over template"; \
		cp perylune.ini-template perylune.ini;                \
    else                                                      \
		echo "STEP 3: perylune.ini already present.";                 \
	fi

	# update pip
	echo "STEP 4: Updating pip"
	venv/bin/pip install --upgrade pip

	# install dependencies
	echo "STEPS 5: Installing dependencies"
	venv/bin/pip install -r requirements.txt


check:
	PYTHONPATH=.:poliastro/src pytest -v --ignore=poliastro
