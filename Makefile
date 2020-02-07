lambdafunction.zip: twython
	zip -r lambdafunction.zip *

twython:
	pip3 install twython -t .
