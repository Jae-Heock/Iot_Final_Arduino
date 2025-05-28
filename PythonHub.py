# PythonHub.py

from serial import Serial
import time
import psycopg
import pandas.io.sql as psql
import matplotlib.pyplot as plt

# 파이썬에서 생성자명과 소멸자명은 하나로 정해짐
# 접근 그룹 규칙
# __이름__ -> public group(public:)
# __이름 -> private group(private:)
# self 의미: 현재 인스턴스(instance)의 레퍼런스(reference) -> C++ 기준에서 self = *this
class PythonHub:
    # private 멤버 변수
    __defPortName = 'COM3'
    __defPortSpeed = 9600
    __defWaitTime = 0.1

    # 정적(static) 멤버 함수: 입력에 self가 없음 -> C++에서 static에 해당
    def wait(waitTime = __defWaitTime):
        time.sleep(waitTime)
    
    # 생성자(constructor)
    def __init__(self, portName = __defPortName, portSpeed = __defPortSpeed):
        self.ard = Serial(portName, portSpeed)
        
    #소멸자(destructor)
    def __del__(self):
        if self.ard.isOpen(): # Serial이 열려있으면(is open?)
            self.ard.close() # Serial 닫기(close)

    # Serial Method
    def writeSerial(self, sCmd):
        btCmd = sCmd.encode()
        nWrite = self.ard.write(btCmd)
        self.ard.flush() # 모든 바이트를 출력으로 내보기기
        return nWrite

    def readSerial(self):
        nRead = self.ard.in_waiting
        if nRead > 0:
            btRead = self.ard.read(nRead)
            sRead = btRead.decode()
            return sRead
        else: return ''

    def talk(self, sCmd):
        #print('cmd = ' + sCmd)
        return self.writeSerial(sCmd + '\n')

    def listen(self):
        PythonHub.wait() # 정적 멤버 접근할 때는 클래스명을 앞에 써줌
        sRead = self.readSerial()
        return sRead.strip() # 문자열 sRead 앞뒤에 공백 제거

    def talkListen(self, sCmd):
        self.talk(sCmd)
        return self.listen()

    # DB Method
    def connectDb(self):
        self.conn = psycopg.connect(host='localhost', port='5432', dbname='postgres', user='postgres', password='2024')
        self.cursor = self.conn.cursor()

    def closeDb(self):
        self.cursor.close()
        self.conn.close()

    def writeDb(self, cmd):
        self.cursor.execute(cmd)
        self.conn.commit()

    # Voltmeter Method
    def getVolt(self):
        # C++: try-catch; Python: try-except
        try:
            sVolt = self.talkListen('get volt')
            volt = float(sVolt)
            return volt
        except: # try 코드 블록 실행에서 오류가 난 경우에 실행되는 부분
            print('Serial error: get volt')
            return -1 # 오류난 경우는 음수를 반환

    def insertVoltToTable(self):
        volt = self.getVolt()
        if volt >= 0: # 정상적인 측정
            meas_time = time.time() # 현재 시간을 double로 반환
            self.connectDb()
            # f'...': formatted string -> C의 printf()와 비슷
            self.writeDb(f'INSERT INTO volt_table(id, meas_time, volt) VALUES({int(meas_time)}, {meas_time}, {volt})')
            self.closeDb()
            self.lastValue = volt
            return True
        else: return False # 측정에 오류
            
    def countVoltTable(self):
        self.connectDb()
        self.writeDb('SELECT COUNT(*) FROM volt_table');
        nCount = self.cursor.fetchone()[0] # fetchone() 함수는 tuple을 반환; [0]을 써서 첫번째 원소를 다시 접근
        self.closeDb()
        return nCount

    def sampleVoltsToTable(self, nCount, delay):
        i = 0
        while i < nCount:
            bResult = self.insertVoltToTable()
            if bResult:
                print(f'i = {i}th meas.')
                i += 1
                PythonHub.wait(delay)

    def loadVoltTable(self):
        self.connectDb()
        self.writeDb('SELECT meas_time, volt FROM volt_table')
        results = self.cursor.fetchall() # results는 record를 원소로 하는 list
        self.closeDb()
        # meas_time, volt 값을 나누어서 반환환
        timeData = () # () 의미: 빈 tuple
        voltData = ()
        for record in results:
            timeData += (record[0],) # (a,) 의미: 원소가 1인 tuple
            voltData += (record[1],)
        return (timeData, voltData)
        
    def writeHtmlVoltTable(self):
        (timeData, voltData) = self.loadVoltTable()
        html = '<table width = "100%" border="1">'
        html += '<thead><th>번호</th><th>측정 일시</th><th>측정 전압</th></thead>'
        i = 1
        for (meas_time, volt) in zip(timeData, voltData) :
            html += f'<tr><td>{i}</td><td>{time.ctime(meas_time)}</td><td>{volt} V</td></tr>'
            i += 1
        html += '</table>'
        return html
    
    # pandas를 써서 구현
    def statVoltTable(self): # 전압의 평균, 최대값, 최소값, 분산, 표준 편차를 출력
        self.connectDb()
        # pandas 처리
        df = psql.read_sql('SELECT * FROM volt_table', self.conn)
        self.closeDb()
        serialVolt = df['volt']
        
        mean = serialVolt.mean()
        max_val = serialVolt.max()
        min_val = serialVolt.min()
        variance = serialVolt.var()
        std_dev = serialVolt.std()
        
     # 결과를 딕셔너리로 반환
        return {
            'mean': mean,
            'max': max_val,
            'min': min_val,
            'variance': variance,
            'std_dev': std_dev
        }

    # matplotlib를 써서 구현
    def plotVoltTable(self, sFilename): # volt_table의 전압 측정값을 그리고 그림으로 저장
        timeData, voltData = self.loadVoltTable()
        plt.plot(timeData, voltData)
        plt.savefig(sFilename)

    # 조도계 메소드
    def getLight(self):
        try:
            sLight = self.talkListen('get lightstep')
            light = int(sLight)
            return light
        except:
            print('Serial error! : get light')
            return -1

    def insertLightToTable(self):
        light = self.getLight()
        if light >= 0:
            meas_time = time.time()
            self.connectDb()
            self.writeDb(f"INSERT INTO light_table(id, meas_time, light) VALUES({int(meas_time)}, {meas_time}, {light})")
            self.closeDb()
            self.lastLightValue = light
            return True
        else: 
            return False

    def countLightTable(self):
        self.connectDb()
        self.writeDb('SELECT COUNT(*) FROM light_table');
        nCount = self.cursor.fetchone()[0]
        self.closeDb()
        return nCount

    def sampleLightsToTable(self, nCount, delay):
        i = 0
        while i < nCount:
            bResult = self.insertLightToTable()
            if bResult:
                print(f'i = {i}th meas.')
                i += 1
                PythonHub.wait(delay)

    def loadLightTable(self):
        self.connectDb()
        self.writeDb('SELECT meas_time, light FROM light_table')
        results = self.cursor.fetchall()
        self.closeDb()
        timeData = ()
        lightData = ()
        for record in results:
            timeData += (record[0],) # (a,) 의미: 원소가 1인 tuple
            lightData += (record[1],)
        return (timeData, lightData)

    def writeHtmlLightTable(self):
        (timeData, lightData) = self.loadLightTable()
        html = '<table width = "100%" border="1">'
        html += '<thead><th>번호</th><th>측정 일시</th><th>측정 조도</th></thead>'
        i = 1
        for (meas_time, light) in zip(timeData, lightData) :
            html += f'<tr><td>{i}</td><td>{time.ctime(meas_time)}</td><td>{light} lx</td></tr>'
            i += 1
        html += '</table>'
        return html

    def statLightTable(self):
        self.connectDb()
        df = psql.read_sql('SELECT * FROM light_table', self.conn)
        self.closeDb()
        serialLight = df['light']

        mean = int(serialLight.mean())  # 평균값을 정수로 변환
        max_val = int(serialLight.max())  # 최대값을 정수로 변환
        min_val = int(serialLight.min())  # 최소값을 정수로 변환
        variance = int(serialLight.var())  # 분산값을 정수로 변환
        std_dev = int(serialLight.std())  # 표준편차를 정수로 변환


        # 결과를 딕셔너리로 반환
        return {
            'mean': mean,
            'max': max_val,
            'min': min_val,
            'variance': variance,
            'std_dev': std_dev
        }

    def setLed(self, color):
        self.talk('set led ' + color)

#=================PythonHub.py - 부저===========================
    def playBuzzer(self, note, delay):
        command = f"play {note} {delay}"
        self.talkListen(command)
        







