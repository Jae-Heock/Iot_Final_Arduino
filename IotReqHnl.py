#IotReqHnl: IoT request handler
from http.server import SimpleHTTPRequestHandler
from PythonHub import PythonHub
from urllib import parse
import time

# class 뒤 (...) 의미: 객체 지향의 상속
class IotReqHnl(SimpleHTTPRequestHandler):
    # GET method의 override(덮어쓰기)
    def do_GET(self):
        # URL 사용하여 GET method 처리
        result = parse.urlsplit(self.path) # path?query
        print('path: ' + result.path + '; query: ' + result.query) # path: IP 주소 다음에 오는 URL 정보
        if result.path == '/': self.writeHome()
        elif result.path == '/meas_volt': self.writeMeasVolt()
        elif result.path == '/sample_volt': self.writeSampleVolt(result.query)
        elif result.path == '/led': self.writeLed(result.query)
        elif result.path == '/meas_light' : self.writeMeasLight()
        elif result.path == '/sample_light' : self.writeSampleLight(result.query)
        elif result.path == '/buzzer_do' : self.writeBuzzer_do(result.query)
        elif result.path == '/buzzer_re' : self.writeBuzzer_re(result.query)
        elif result.path == '/buzzer_mi' : self.writeBuzzer_mi(result.query)
        elif result.path == '/buzzer_pa' : self.writeBuzzer_pa(result.query)
        elif result.path == '/buzzer_sol' : self.writeBuzzer_sol(result.query)
        elif result.path == '/buzzer_la' : self.writeBuzzer_la(result.query)
        elif result.path == '/buzzer_si' : self.writeBuzzer_si(result.query)
            
        else: self.writeNotFound()

    def writeHead(self, code):
        self.send_response(code) # 성공(OK)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def writeHtml(self, html):
        self.wfile.write(html.encode())
    
    def writeHome(self):
        # 재빠르게 header로 response를 전송
        self.writeHead(200)
        # HTML 전송
        # 현재 서버의 인스턴스 이름은 server로 고정됨; 변경할 수 없음
        nTime = time.time()
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>IoT Web Server</title>'
        html += '<style>'
        html += 'body {background-color: black; color: white; text-align: center;}'  # 배경을 검은색, 글씨를 하얀색으로 설정, 텍스트 가운데 정렬
        html += 'a {color: white; display: inline-block; margin-right: 10px;}'  # 링크 글씨를 하얀색, 인라인 블록으로 설정
        html += 'div {margin: 0 auto; display: block;}'  # div 태그를 중앙으로 정렬
        html += 'img {margin: 20px auto; display: block;}'  # 이미지 중앙 정렬
        html += '</style>'
        html += '</head><body>'

        html += '<div>'
        html += '*********< 전압, 조도 측정 >*********<br>'
        html += '<div><a href="/meas_volt">전압 한번 측정</a></div>'
        html += '<div><a href="/sample_volt?count=5&delay=1.5">전압 5번 샘플링</a></div>'
        html += '<div><a href="/meas_light">조도 측정</a></div>'
        html += '<div><a href="/sample_light?count=5&delay=1.5">조도 5번 샘플링</a></div>'
        html += '*********************************<br>'
        html += '</div>'
        html += '<br><br>'

        html += '<div>'
        html += '*********< 부저 듣기 >*********<br>'
        html += '<a href="/buzzer_do?note=do&delay=1000">도</a>'
        html += '<a href="/buzzer_re?note=re&delay=1000">레</a>'
        html += '<a href="/buzzer_mi?note=mi&delay=1000">미</a>'
        html += '<a href="/buzzer_pa?note=pa&delay=1000">파</a>'
        html += '<a href="/buzzer_sol?note=sol&delay=1000">솔</a>'
        html += '<a href="/buzzer_la?note=ra&delay=1000">라</a>'
        html += '<a href="/buzzer_si?note=si&delay=1000">시</a>'
        html += '</div>'
        html += '*********************************<br>'
        html += '</div>'
        html += '<br><br>'

        html += '<div>'
        html += '*********< LED 켜기 >*********<br>'
        html += '<a href="/led?color=red" style="color:red;">빨</a>'
        html += '<a href="/led?color=blue" style="color:blue;">파</a>'
        html += '<a href="/led?color=yellow" style="color:yellow;">노</a>'
        html += '<a href="/led?color=green" style="color:green;">초</a>'
        html += '<a href="/led?color=white" style="color:white;">흰</a>'
        html += '<a href="/led?color=cyan" style="color:cyan;">청</a>'
        html += '<a href="/led?color=magenta" style="color:magenta;">마젠타</a>'
        html += '</div>'
        html += '*********************************<br>'
        html += '<br><br>'
        
        html += '<div><br></div>'
        html += '<div>IoT System 기말 과제 </div>'
        html += '<div>학번 : 2060041 </div>'
        html += '<div>이름 : 이재혁</div>'
        html += '<div><img src="https://i.ytimg.com/vi/NKfXFqOvKbY/maxresdefault.jpg" width="300" height="300"/></div>'
        html += f'<div>현재 날짜와 시간은 {time.ctime(nTime)}입니다.</div>'
        html += '</body></html>'
        self.writeHtml(html)  # Unicode(가변 코드) -> byte(고정 코드; 크기는 1byte) 변경


    def writeNotFound(self):
        self.writeHead(404)
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>페이지 없음</title>'
        html += '</head><body>'
        html += f'<div>요청하신 페이지 {self.path}가 없습니다.</div>'
        html += '</body></html>'
        self.writeHtml(html)

    def writeMeasVolt(self):
        result = self.server.gateway.insertVoltToTable()
        stats = self.server.gateway.statVoltTable()
        lastVolt = self.server.gateway.lastValue
        if result: 
            str = '성공'
        else: 
            str = '실패'
        self.writeHead(200)
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>전압 한 번 측정</title>'
        html += '<style>'
        html += 'body {background-color: black; color: white; text-align: center;}'  # 배경을 검은색, 글씨를 하얀색으로 설정, 텍스트 가운데 정렬
        html += 'a {color: white; text-decoration: none;}'  # 링크 글씨를 하얀색으로 설정, 밑줄 제거
        html += 'div {margin: 20px auto; display: block;}'  # div 태그를 중앙으로 정렬, 간격 추가
        html += '</style>'
        html += '</head><body>'
        
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += f'<div>전압 한 번 측정을 {str}하였습니다.</div>'
        html += f'<div>측정된 전압은 {lastVolt} V 입니다.</div>'
        html += f'<div>전압을 측정한 회수는 {self.server.gateway.countVoltTable()}번입니다.</div>'
        html += '<div>========전압의 평균 분산 표준편차========</div>'
        html += f'<div>평균 전압: {stats["mean"]} V</div>'
        html += f'<div>분산: {stats["variance"]}</div>'
        html += f'<div>표준편차: {stats["std_dev"]}</div>'
        html += '<div><b>현재까지 측정한 모든 전압표</b></div>'
        html += '<div>' + self.server.gateway.writeHtmlVoltTable() + '</div>'
        html += '</body></html>'
        
        self.writeHtml(html)


    def writeSampleVolt(self, query):
        result = parse.parse_qs(query)  # qs: query string
        stats = self.server.gateway.statVoltTable()
        print(result)
        nCount = int(result['count'][0])
        delay = float(result['delay'][0])
        self.server.gateway.sampleVoltsToTable(nCount, delay)
        self.writeHead(200)
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>전압 여러 번 측정</title>'
        html += '<style>'
        html += 'body {background-color: black; color: white; text-align: center;}'  # 배경을 검은색, 글씨를 하얀색으로 설정, 텍스트 가운데 정렬
        html += 'a {color: white; text-decoration: none;}'  # 링크 글씨를 하얀색으로 설정, 밑줄 제거
        html += 'div {margin: 20px auto; display: block;}'  # div 태그를 중앙으로 정렬, 간격 추가
        html += '</style>'
        html += '</head><body>'
        
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += f'<div>전압을 주기 {delay} 초로 {nCount} 번 측정하였습니다.</div>'
        html += f'<div>전압을 측정한 회수는 {self.server.gateway.countVoltTable()}번입니다.</div>'
        html += '<div>========전압의 평균 분산 표준편차========</div>'
        html += f'<div>평균 전압: {stats["mean"]} V</div>'
        html += f'<div>분산: {stats["variance"]}</div>'
        html += f'<div>표준편차: {stats["std_dev"]}</div>'
        html += '<div><b>현재까지 측정한 모든 전압표</b></div>'
        html += '<div>' + self.server.gateway.writeHtmlVoltTable() + '</div>'
        html += '</body></html>'
        
        self.writeHtml(html)


    def writeMeasLight(self):
        result = self.server.gateway.insertLightToTable()
        stats = self.server.gateway.statLightTable()
        lastLight = self.server.gateway.lastLightValue
    
        if result: 
            str = '성공'
        else: 
            str = '실패'
        self.writeHead(200)
    
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>조도 한 번 측정</title>'
        html += '<style>'
        html += 'body {background-color: black; color: white; text-align: center;}'  # 배경을 검은색, 글씨는 하얀색, 텍스트는 가운데 정렬
        html += 'a {color: white; text-decoration: none;}'  # 링크 글씨를 하얀색으로 설정, 밑줄 제거
        html += 'div {margin: 20px auto; display: block;}'  # div 태그를 중앙으로 정렬, 간격 추가
        html += '</style>'
        html += '</head><body>'
        
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += f'<div>조도를 한 번 측정한 결과: {str}</div>'
        html += f'<div>측정된 조도는 {lastLight} lx 입니다.</div>'
        html += f'<div>현재 조도를 측정한 회수는 {self.server.gateway.countLightTable()}번입니다.</div>'
        html += '========조도의 평균 분산 표준편차========'
        html += f'<div>평균 조도: {stats["mean"]} lx</div>'
        html += f'<div>분산: {stats["variance"]}</div>'
        html += f'<div>표준편차: {stats["std_dev"]}</div>'
        html += '<div><b>현재까지 측정한 모든 조도표</b></div>'
        html += '<div>' + self.server.gateway.writeHtmlLightTable() + '</div>'
        html += '</body></html>'
    
        self.writeHtml(html)

            

    def writeSampleLight(self, query):
        result = parse.parse_qs(query)
        nCount = int(result['count'][0])  # 측정할 횟수
        delay = float(result['delay'][0])  # 측정 간격
    
        # 조도 샘플링을 수행
        self.server.gateway.sampleLightsToTable(nCount, delay)
        stats = self.server.gateway.statLightTable()  # 통계 계산
    
        # 응답 HTML 작성
        self.writeHead(200)
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>조도 여러 번 측정</title>'
        html += '<style>'
        html += 'body {background-color: black; color: white; text-align: center;}'  # 배경을 검은색, 글씨를 하얀색으로 설정, 텍스트 가운데 정렬
        html += 'a {color: white; text-decoration: none;}'  # 링크 글씨를 하얀색으로 설정, 밑줄 제거
        html += 'div {margin: 20px auto; display: block;}'  # div 태그를 중앙으로 정렬, 간격 추가
        html += '</style>'
        html += '</head><body>'
    
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += f'<div>조도를 {nCount}번 측정하였습니다. (측정 간격: {delay}초)</div>'
        html += f'<div>현재 조도를 측정한 회수는 {self.server.gateway.countLightTable()}번입니다.</div>'
        html += '<div>========조도의 평균 분산 표준편차========</div>'
        html += f'<div>평균 조도: {stats["mean"]} lx</div>'
        html += f'<div>분산: {stats["variance"]}</div>'
        html += f'<div>표준편차: {stats["std_dev"]}</div>'
        html += '<div><b>현재까지 측정한 모든 조도표</b></div>'
        html += '<div>' + self.server.gateway.writeHtmlLightTable() + '</div>'
        html += '</body></html>'
    
        self.writeHtml(html)

    def writeLed(self, query):
        result = parse.parse_qs(query) # qs: query string
        print(result)
        color = result['color'][0]
        self.server.gateway.setLed(color)
        self.writeHead(200)
        
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>LED 켜기</title>'
        html += '<style>'
        html += 'body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }'  # 배경색은 검정, 글씨는 흰색
        html += '</style>'
        html += '</head><body>'
        
        # 홈으로 돌아가기 링크 스타일
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        
        # LED 색깔로 켰다는 메시지와 그 색깔에 맞는 글씨 색 설정
        html += f'<div style="color: {color};">LED를 {color} 색깔로 켰습니다..</div>'
        html += '<div><br><br></div>'
        html += '<div>'
        html += '<a href="/led?color=off" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*LED 끄기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '</body></html>'
        self.writeHtml(html)

#=====================IotReqHnl.py - 부저=================================
    def writeBuzzer_do(self, query):
        # 쿼리 문자열을 파싱
        result = parse.parse_qs(query)
        print(f"Parsed query: {result}")

        note = 'do'
        delay = 1000
        self.server.gateway.playBuzzer(note, delay)
        
        self.writeHead(200)
       
        # 응답 처리
        self.writeHead(200)  # HTTP 상태 코드 200 (성공)
        # HTML 응답 작성
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>부저</title>'
        html += '<style>'
        html += 'body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }'
        html += '</style>'
        html += '</head><body>'
        
        # 홈으로 돌아가기 링크
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += '</body></html>'

        self.writeHtml(html)

    def writeBuzzer_re(self, query):
        # 쿼리 문자열을 파싱
        result = parse.parse_qs(query)
        print(f"Parsed query: {result}")

        note = 're'
        delay = 1000
        self.server.gateway.playBuzzer(note, delay)
        
        self.writeHead(200)
       
        # 응답 처리
        self.writeHead(200)  # HTTP 상태 코드 200 (성공)
        # HTML 응답 작성
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>부저</title>'
        html += '<style>'
        html += 'body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }'
        html += '</style>'
        html += '</head><body>'
        
        # 홈으로 돌아가기 링크
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += '</body></html>'

        self.writeHtml(html)


    def writeBuzzer_mi(self, query):
        # 쿼리 문자열을 파싱
        result = parse.parse_qs(query)
        print(f"Parsed query: {result}")

        note = 'mi'
        delay = 1000
        self.server.gateway.playBuzzer(note, delay)
        
        self.writeHead(200)
       
        # 응답 처리
        self.writeHead(200)  # HTTP 상태 코드 200 (성공)
        # HTML 응답 작성
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>부저</title>'
        html += '<style>'
        html += 'body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }'
        html += '</style>'
        html += '</head><body>'
        
        # 홈으로 돌아가기 링크
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += '</body></html>'

        self.writeHtml(html)

    def writeBuzzer_pa(self, query):
        # 쿼리 문자열을 파싱
        result = parse.parse_qs(query)
        print(f"Parsed query: {result}")

        note = 'pa'
        delay = 1000
        self.server.gateway.playBuzzer(note, delay)
        
        self.writeHead(200)
       
        # 응답 처리
        self.writeHead(200)  # HTTP 상태 코드 200 (성공)
        # HTML 응답 작성
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>부저</title>'
        html += '<style>'
        html += 'body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }'
        html += '</style>'
        html += '</head><body>'
        
        # 홈으로 돌아가기 링크
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += '</body></html>'

        self.writeHtml(html)

    def writeBuzzer_sol(self, query):
        # 쿼리 문자열을 파싱
        result = parse.parse_qs(query)
        print(f"Parsed query: {result}")

        note = 'sol'
        delay = 1000
        self.server.gateway.playBuzzer(note, delay)
        
        self.writeHead(200)
       
        # 응답 처리
        self.writeHead(200)  # HTTP 상태 코드 200 (성공)
        # HTML 응답 작성
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>부저</title>'
        html += '<style>'
        html += 'body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }'
        html += '</style>'
        html += '</head><body>'
        
        # 홈으로 돌아가기 링크
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += '</body></html>'

        self.writeHtml(html)


    def writeBuzzer_la(self, query):
        # 쿼리 문자열을 파싱
        result = parse.parse_qs(query)
        print(f"Parsed query: {result}")

        note = 'la'
        delay = 1000
        self.server.gateway.playBuzzer(note, delay)
        
        self.writeHead(200)
       
        # 응답 처리
        self.writeHead(200)  # HTTP 상태 코드 200 (성공)
        # HTML 응답 작성
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>부저</title>'
        html += '<style>'
        html += 'body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }'
        html += '</style>'
        html += '</head><body>'
        
        # 홈으로 돌아가기 링크
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += '</body></html>'

        self.writeHtml(html)



    def writeBuzzer_si(self, query):
        # 쿼리 문자열을 파싱
        result = parse.parse_qs(query)
        print(f"Parsed query: {result}")

        note = 'si'
        delay = 1000
        self.server.gateway.playBuzzer(note, delay)
        
        self.writeHead(200)
       
        # 응답 처리
        self.writeHead(200)  # HTTP 상태 코드 200 (성공)
        # HTML 응답 작성
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>부저</title>'
        html += '<style>'
        html += 'body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }'
        html += '</style>'
        html += '</head><body>'
        
        # 홈으로 돌아가기 링크
        html += '<div>'
        html += '<a href="/" style="display: inline-block; padding: 10px 20px; border: 2px solid white; text-decoration: none; color: white; font-size: 20px; font-weight: bold; text-align: center; width: 200px; margin: 0 auto; background-color: black;">'
        html += '*******************<br>'
        html += '*홈으로 돌아가기*<br>'
        html += '*******************'
        html += '</a>'
        html += '</div>'
        
        html += '<div><br></div>'
        html += '</body></html>'

        self.writeHtml(html)

