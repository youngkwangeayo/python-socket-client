import asyncio
import websockets
import time
import json
import threading
import requests
import aiohttp
class BaristaCall :
    
    isConnect = False
    socket = None
    messageQueue = asyncio.Queue()
    httpRequestQueue = asyncio.Queue()
    protocol = "ws://"
    STATUS = {"ORDER" :"R","FINISHED":"C", "TAKEAWAY" : "F"}

    def __init__(self, url:str=None,signageUrl:str =None) -> None:
        self.socket = None
        
        self.url = url or "192.168.0.136:8112/websocket"
        self.url = self.protocol + self.url
        self.signageUrl = signageUrl or "http://192.168.0.136:8112/"

        self.socketLoop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop)
        self.thread.start()
        # print(f" 쓰래드 이름  호출 함수 [init] : {threading.current_thread().getName}")
        # self.thread.join()
        # self.thread.run()
        
    def start_loop(self) ->None:
        print("스레드 루프시작")
        # print(f" 쓰래드 이름  호출 함수 [start_loop] : {threading.current_thread().getName}")
        
        asyncio.set_event_loop(self.socketLoop)
        self.socketLoop.run_until_complete(self.start())
        self.socketLoop.run_forever()

    async def start(self):
        # print(f" 쓰래드 이름  호출 함수 [start] : {threading.current_thread().getName}")
        print("스타트 실행")
        con = await self.connect(1)
        print(f"connect 완료{con}")
        if con ==True :
            # self.httpSession = aiohttp.ClientSession()
            t1 = asyncio.create_task(self.socketReceive())
            t2 = asyncio.create_task(self.socketSendForQueue())
            t3 = asyncio.create_task(self.signageSendWatingInfo())
            await t1
            await t2
            await t3
            # asyncio.gather(t1,t2)
            print(f"[테스크] 리턴 리졸브 1 : {t1.result()}")
            print(f"[테스크] 리턴 리졸브 2 : {t2.result()}")
            print(f"[테스크] 리턴 리졸브 3 : {t3.result()}")

        else :
            print("연결실패")
    
    def callRobot(self,data) -> None:
        asyncio.run_coroutine_threadsafe(self.messageQueue.put(data),self.socketLoop)
        print(f"메시지가 큐에 추가되었습니다: {data}")
 

    async def setMessageQueue(self,data) -> None :
        # if dataCheck()
        await self.messageQueue.put(data)
        print(f"메시지가 큐에 추가되었습니다: {data}")
        
    async def connect(self, count:int) -> bool:

        if self.socket is None :
            self.socket = websockets
            
        while True:
            # time.sleep(1)
            await asyncio.sleep(1)
            try :
                self.socket = await self.socket.connect(self.url)
                BaristaCall.isConnect = True
                print("연결!")
                return True
              
                    
            except Exception as e :
                count = count + 1
                BaristaCall.isConnect = False
                print(f"e : {e}")
                if count >3 :
                    count = count + 1
                    return False
            

        
    
    async def socketReceive(self)-> str :
        print("TASK_1 : [socketReceive] 실행")
        # print(f" 쓰래드 이름  호출 함수 [socketReceive] : {threading.current_thread().getName}")
        # self.socket
        data =None
        while True:
            try :
                messgeRecv = await self.socket.recv()
                print(f"받은 메세지 : {messgeRecv}")
                data = messgeRecv
            except websockets.ConnectionClosed as e:
                print(f"리시버 : Connection closed, attempting to reconnect...{e}")
                # return False
                # time.sleep(3)
                await asyncio.sleep(3)
                url = self.url
                self.__init__(url)
                return

            try:
                reqData = json.loads(data)
                if "STATUS" in reqData : 
                    status =reqData["STATUS"]
                    if status == "ORDER" and reqData["ACK"] == "ONE": continue
                    reqStatus = self.STATUS.get(status)
                    sendWating = {
                        "frId" : 10107,
                        "command":"Status",
                        "data" : [{"orderStatus" : reqStatus, "waitingNumber" : reqData["ORDER_NUMBER"]}]
                    }
                    asyncio.run_coroutine_threadsafe(self.httpRequestQueue.put(sendWating),self.socketLoop)
                    print("http 큐에 메세지 추가")
            except Exception as e:
                # time.sleep(3)
                await asyncio.sleep(3)
                print(f"socketReceive 입섹션 :{e}")
                pass
    


    async def socketSendForQueue(self) ->None :
        print("TASK_2 : [socketSendForQueue] 실행")
        while True:
            try:
                message = await self.messageQueue.get()
                await self.socket.send(message)
                print(f"보낸 메세지 : {message}")
            except websockets.ConnectionClosed as e:
                # time.sleep(3)
                await asyncio.sleep(3)
                # asyncio.sleep(3)
                print(f" socketSendForQueue 입섹션 : {e}")
                url = self.url
                self.__init__(url)
                return
    

    async def signageSendWatingInfo(self) -> None:
        print(f" 쓰래드 이름  호출 함수 [signageSendWatingInfo] : {threading.current_thread().getName}")
        print("TASK_3 : [httpRequestForQueue] 실행")
        while True:
            try :
                sendWating = await self.httpRequestQueue.get()
                url = self.signageUrl + "testWathing"
                print(f"http 큐겟 : {sendWating}    url : {url}")
                
                # print(f" 쓰래드 이름  호출 함수 [aiohttp] : {threading.current_thread().getName}")
                async with aiohttp.ClientSession() as session :
                    async with session.post(url=url,headers={"Content-type": "application/json; charset=utf-8"},data=json.dumps(sendWating)) as res:
                        print(f"status : {res.status}   val : {await res.json()}")
                    
            except Exception as e:
                # time.sleep(3)
                print(f"httpRequestForQueue 입섹션 :{e}")
                await asyncio.sleep(3)
                pass
        

    # 출력테스트함수
    def testCall(self,data:str = None) -> None :
        if data is None :
            print(f"출력테스트")
        else:
            print(f"출력테스트 {data}")




if __name__ == "__main__":
    # 메인메소드는 메인쓰레드 -> 메인쓰레드  while 돌리기

    call = BaristaCall()
    # print(f" 쓰래드 이름  호출 함수 [main] : {threading.current_thread().getName}")
    print("실행이?")
    time.sleep(6)
    print("콜메인")
    time.sleep(2)
    call.callRobot("반가워!!")
    while True:
        time.sleep(3)
#     time.sleep(3)
#     call.callRobot("니이름??")
#     time.sleep(1)
#     call.callRobot("어쩔??")
#     # time.sleep(30)

    # async def main():
    #     await asyncio.sleep(5)
    #     await call.callRobot("반가워!!")
    #     await asyncio.sleep(3)
    #     await call.callRobot("니이름??")
    #     await asyncio.sleep(1)
    #     await call.callRobot("어쩔??")

    # asyncio.run(main())
    