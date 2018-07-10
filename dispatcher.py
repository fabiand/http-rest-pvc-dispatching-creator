import cherrypy
import subprocess
import StringIO

def create_pvc_sync(name, size):
  cmd = ["kubectl", "create", "-f", "-"]
  cmd = ["cat"]
  p = subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate("""
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: {name}
spec:
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: {size_bytes}B
---
kind: Pod
apiVersion: v1
metadata:
  name: {name}
  labels:
    target-for: {name}
spec:
  terminationGracePeriodSeconds: 0
  containers:
    - name: busybox
      image: busybox
      command: ["/bin/sleep", "42"] ## FIXME FIXME Here we need the receiver
      volumeMounts:
      - mountPath: "/dst"
        name: dst
  volumes:
    - name: dst
      persistentVolumeClaim:
        claimName: {name}
---
kind: Service
apiVersion: v1
metadata:
  name: {name}
spec:
  selector:
    target-for: {name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
""".format(name=name, size_bytes=size))

def create_ingress(name):
  pass

class HelloWorld(object):
    @cherrypy.expose
    def create(self, name_request):
        name = name_request    # FIXME sanitize or FAIL
        cl = cherrypy.request.headers['Content-Length']
        create_pvc_sync(name, cl)
        # https://blog.eexit.net/curl-forward-post-over-http-redirections/
        raise cherrypy.HTTPRedirect("/upload/%s" % name, status=307)
        return "Hello world! %s" % name_request

    @cherrypy.expose
    def upload(self, name):
        cl = cherrypy.request.headers['Content-Length']
        body = cherrypy.request.body.read(int(cl))
        return "Uploaded %s" % body


if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
