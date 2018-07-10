# User flow

```
curl -Lv http://127.0.0.1:8080/create/bar \
  --http2 \
  -X POST \
  --header "Content-Type:application/octet-stream" \
  --data-binary @data
```

# Implementation Idea

1. Have a dispacther pod offering an http endpoint
2. Upon a POST (with a content-length)
2.1. The dispatcher creates a PVC with a size request of content-length
2.2. The dispatcher creates a Pod with a receiving http server
2.3. The dispatcher creates a Service opening a edge port to point to the Pod
3. The dispatcher sends an HTTP redirect (307) pointing to the new service
4. The client switches to the new URL sends a new request
5. The new Pod awaits request and writes body to PVC
6. The client finishes
7. The new Pod finishes and cleans up itself and Service

# Demo (not working)

```
[term1]
python dispatcher.py

[term2]
make upload
