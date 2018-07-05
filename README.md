# rack3d

rack3d.py is a single script that connects to the database and generates the .obj and .mtl file.
It requires the mysql.connector Python interface to MySQL, which may need to be installed as a separate package, such as python3-mysql.connector or similar.

in the rack3d_json folder there is a two part process. a php script that generates a json file and a python script that downloads and processes that json. this is useful for people who don't have access to the datbase.
