import tornado.web
from tornado import *
import tornado.ioloop
import cv2
import jsonify
import argparse
import request
import numpy as np
import image_quan as iq1
import json
json_ob = None
class uploadImgHandler(tornado.web.RequestHandler):    
    # @tornado.web.asynchronous

    def post(self):
        global json_ob
        files = self.request.files["fileImage"]
        print("OK")
        for f in files:
            fh = open(f"upload/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        print(f"{f.filename}")
        self.write(f"http://localhost:8080/img/{f.filename}")
        print("readched")
        # json_ob = iq1.run(f.filename)
        # self.redirect('/getimage')
        # self.redirect('/getimage',status=)

        # print(json_ob)
        # self.write(jsonify(json_ob))
        # self.write(json.dumps(Info, default=json_util.default)
        # self.write(json.dumps(json_ob))



    def get(self):
        self.render("index.html")




class getimagedetails(tornado.web.RequestHandler):
    def post(self):
        global json_ob
        try:
            files = self.request.files["fileImage"]
        except:
            files = []

        # json_ob = iq1.y1
        # iq1.run(f.filename)
        print("okwfDCN")
        for f in files:
            fh = open(f"upload/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        # print(f"{f.filename}")
            string_1 = "upload/"+f.filename
        # json_ob = iq1.run(f.filename)
            try:
                json_ob = iq1.run(string_1)
                self.write(json_ob)

            except:
                json_ob = {}
                self.write("no image name fetched")
        # print(json_ob)
        # if json_ob == None:
        #     raise "Error"
        #     pass
        # web.RequestHandler.set_status(web.RequestHandler.status.HTTP_200_OK)
        # self.set_status(status.HTTP_200_OK)
        # status.HTTP_200_OK
        if files == []:
            self.write("Erro no files")
            pass
        # josn_dict = iq1.
        # self.write(jsonify(json_ob))
        # self.write(f"{json_ob}")
        # self.write(f"{json_ob}")
        # self.write(json_ob)

        # self.write(f"http://localhost:8080/img/{f.filename}")

        # return HttpResponse
        # self.write(f"http://localhost:8080/img/")

        # self.write()
        # return json_ob

    # @tornado.web.asynchronous
    # def post(self):
    #     print("ok")
    #     pi1 = self.get_argument('display')        
    #     do_find_one(self,pi1)
    #     self.finish()  # Without this the client's request will hang
    # def get(self):
    #     self.render("index.html")



    # raise NotImplementedError



if (__name__ == "__main__"):

    app = tornado.web.Application([
        ("/", uploadImgHandler),
        ("/getimage", getimagedetails)
        # ("/img/(.*)", tornado.web.StaticFileHandler, {'path': 'upload'})

        # ("/getimagedetails", getimagedetails)

    ])


    app.listen(8970)
    print("Listening on port 8970")
    tornado.ioloop.IOLoop.instance().start()