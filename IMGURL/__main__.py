import time
from IMGURL import app

print("STARTED💫")

if __name__=="__main__":
  app.run()
  with app:
    time.sleep(15)
    app.send_message(-1002011444793,"Bot has been started!")
