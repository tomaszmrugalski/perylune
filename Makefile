check:
	PYTHONPATH=. pytest -v

doc:
	sphinx-build -M singlehtml doc/ doc/


web:
	cd cesium; npm start

.PHONY: doc
