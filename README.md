## This app has two routes and thus 2 endpoints:
1. / endpoints where you can upload any kind of file to the server. Allows both GET and POST requests <br>
2. /downloads/<id> where id is the primary key of the file. When a GET requests is sent to the browser, it downloads the file. <br>

Just working with files