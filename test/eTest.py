import asyncio
import time

class t:
    
    def __init__(self) -> None:
        asyncio.run(self.c2())
        # self.c2()
        pass

    async def c2(self):
        count =0
        try :
            await self.call(count)
        except Exception as e :
            count = count + 1
            print(f"e : {e}")
            await self.call(count)
    
    async def call(self,count : int)->bool:
        await asyncio.sleep(1)
        
        if count >5 :
            return True
        else :
            return self.ex()


    def ex(self):
        raise Exception("에라이 에러다")
        

if __name__ == "__main__":
    t()
