upload:
	curl -Lv http://127.0.0.1:8080/create/bar --header "Content-Type:application/octet-stream" --data-binary @data -X POST --http2


