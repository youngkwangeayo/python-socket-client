import asyncio
import websockets
import time
import json
import threading
class BaristaCall :
    
    isConnect = False
    socket = None
    messgeQueue = asyncio.Queue()

    def __init__(self, url:str=None) -> None:
        self.socket = None
        if url is None :
            self.url = "ws://192.168.0.136:8811"
        else :
            self.url = url

        asyncio.run(self.start())
        # self.socketLoop = asyncio.new_event_loop()
        # self.thread = threading.Thread(target=self.start_loop)
        # self.thread.start()
        
    # def start_loop(self) ->None:
    #     asyncio.set_event_loop(self.socketLoop)
    #     self.socketLoop.run_until_complete(self.start())
        

    async def start(self):
        connect = await self.connect(1)
        print(connect,"????")
        if connect ==True :
            t1 = asyncio.create_task(self.socketReceive())
            t2 = asyncio.create_task(self.socketSendForQueue())

            await t1
            await t2
            

        else :
            print("연결실패")

    async def callRobot(self,data) -> None :
        # if dataCheck()
        self.messgeQueue.put(data)
        

    async def connect(self, count:int) -> bool:
        if self.socket is None :
            self.socket = websockets
        
            try :
                async with self.socket.connect(self.url) as socket:
                    self.socket = socket
                    BaristaCall.isConnect = True
                    return True
                    

            except Exception as e:
                BaristaCall.isConnect = False
                print(f"(e) {self.url} : {e}")
                if count <3 :
                    count = count + 1
                    print(f"여기 들어와? {count, type(count)}" )
                    return await self.connect(count)
                else :
                    print("여기가 왜나와?")
                return False
        
    
    async def socketReceive(self)-> str :
        # self.socket
        while True:
           messgeRecv = await self.socket.recv()
           print(messgeRecv)
           return messgeRecv
    
    async def socketSendForQueue(self) ->None :
        
        while True:
            if self.messgeQueue.empty() == False:
                massege = self.messgeQueue.get()
                await self.socket.send(massege)
    




if __name__ == "__main__":
    call = BaristaCall()
    print("실행이?")
    # time.sleep(30)
    # loop = asyncio.get_event_loop()
    # loop.create_task(call.connect())
    # loop.close()
    # asyncio.
    # threading.Thread(target=theardTest, args=(call,)).start()

    