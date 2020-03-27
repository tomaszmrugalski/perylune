setup:
	# clone poliastro if needed
	@if [ ! -d poliastro ]; then                            \
		git clone https://github.com/poliastro/poliastro ;  \
	else                                                    \
		cd poliastro;                                       \
		git pull;                                           \
		cd ..;                                              \
	fi

	# create virtualenv if needed
	@if [ ! -d venv ]; then                                 \
		python3 -m virtualenv venv;                         \
	fi

	# set up perylune.ini if needed
	@if [ ! -f perylune.ini ]; then                           \
		echo "Perylune.ini not found, copying over template"; \
		cp perylune.ini-template perylune.ini;                \
    else                                                      \
		echo "perylune.ini already present.";                 \
	fi

check:
	PYTHONPATH=.:poliastro/src pytest -v --ignore=poliastro
