install_to_pkg:
	pip install build
	pip install twine

build_pkg:
	python3 -m build

upload_pkg:
	python3 -m twine upload --skip-existing dist/*
	
create_test:
	python3 src/nsj_rest_test_util/util/tcase_tools.py --tenant 1 \
	--endpoint endpoint --mopecode 1234 --method post \
	--responsecode 200 --testname teste_name \
	--serverport 5000 --appname app_name --dbserver localhost \
	--dbport 5433 --dbname inegratto2 --dbuser postgres --dbpass postgres \
	--dbschema pcp --diretorio $(PWD)/src/nsj_rest_test_util/api/casos_de_teste \
	--payload "{\
		\"codigo\": \"01\",\
		\"nome\": \"01\",\
		\"tenant\" : \"1\",\
		\"estabelecimento\" : \"39836516-7240-4fe5-847b-d5ee0f57252d\",\
		\"empresa\" : \"431bc005-9894-4c86-9dcd-7d1da9e2d006\",\
		\"grupo_empresarial\" : \"95cd450c-30c5-4172-af2b-cdece39073bf\",\
		\"tipo\" : \"mao_de_obra\"\
	}"




