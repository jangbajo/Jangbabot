 ***
 <h2>개발도구</h2>

<b>브런치<br><b>
  - raspberrypi (ROS Melodic 환경 개발)<br>
&nbsp; : 라즈베리파이4, PyQt5, python3.7, QtDesigner<br><br>
  - test (윈도우 환경 개발)<br>
&nbsp; : 윈도우, PyQt5.15, python3.8.5, QtDesigner<br>
<br>
  # ui파일 개발은 QtDesigner, 동작 코드는 python으로 개발<br>

  
  
***
 <h2>PyQt5 초기설정</h2>
  
  - 라즈베리파이
  1. sudo apt-get install python3-pyqt5
  2. sudo apt install pyqt5-dev-tools pyqt5-dev<br>
  - 윈도우
  1. pip install pyqt5
  2. pip install pyqt5-tools
  <br>
  # python 버전과 pyqt 버전 맞추기<br>
  # pyQt5-python3.8 / pyQt6-python3.9
	
 ***
 <h2>UI 구성</h2>
  - 대기화면
    <img src="./test/result/waitscreen.png" alt="wait">
