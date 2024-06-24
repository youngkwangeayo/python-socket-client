import asyncio
import requests
import aiohttp
import json

async def asyncHTTP() :
    url = " https://dev-sw.nextpay.co.kr/signageWatingInfo"
     
    sendWating = {
        "frId" : 10107,
        "command":"Status",
        "data" : [{"orderStatus" : "Status", "waitingNumber" : "12"}]
    }
    
    async with aiohttp.ClientSession() as session :
        async with session.post(url=url,headers={"Content-type": "application/json; charset=utf-8"},data=json.dumps(sendWating)) as res:
            print(f"status : {res.status}   val : {await res.json()}")

async def goRun():
    t=asyncio.create_task(asyncHTTP())
    await t
    print(t.result())



if __name__ == "__main__":
    print("rne")
    asyncio.run(goRun())
    print("22222222222rne")
    
        