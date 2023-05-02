
#!/bin/sh

curl -v -k -X 'POST'  '127.0.0.1:8080/api/v1/predict/'  -H 'accept: application/json'   -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzM4MjYxNTMsImlhdCI6MTY3MzY1MzM0OCwic3ViIjoxfQ.PstXitSb9rCfNukLyFaOIDhaogmTtk2wm9kWxcpP2HA'   -F 'file=@img_healthy_1.jpg'