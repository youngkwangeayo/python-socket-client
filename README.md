## LocakSocket Client

## `한개의 스레드에서 비동기  멀티테스크 소캣구현`

파이썬 클라이언트 소캣 객체화

## `task 와 thread 활용해서 소캣클라이언트 객채화`

핸들러쉐이크
- `http get 요청으로 클라이언트의 요청 `
>  GET / HTTP/1.1           : `get 요청이 있어야함 http 와` </br>   
>  Host: 127.0.0.1:8811 </br>
> Connection: Upgrade </br>
> Pragma: no-cache </br>
> Cache-Control: no-cache </br>
> User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 </br>
> Upgrade: websocket                                    `Upgrade: websocket 핸들러쉐이크 이후 변경할 프로토클을 기제해야함` </br>
> Origin: http://192.168.0.136:8090 </br>
> Sec-WebSocket-Version: 13 </br>
> Accept-Encoding: gzip, deflate, br, zstd </br>
> Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7 </br>
> Sec-WebSocket-Key: DVqRpbDEv+q64+ABHCX0Rw== </br>
> Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits </br>
