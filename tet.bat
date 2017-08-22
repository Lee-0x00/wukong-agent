@echo off 
color 0a 

:info 
@echo 	       Wukong Scanner by Bing
@echo 	------------------------------------
@echo 		1.install wukong
@echo 		2.start wukong 
@echo 		3.stop wukong 
@echo 	------------------------------------
set /p sLocal=请选择: 
if %sLocal%==1 goto install
if %sLocal%==2 goto start
if %sLocal%==3 goto stop
cls 
@echo 选择错误，请重新选择 
goto info

:install
@echo install .... 
echo %cd%
goto end

:start
@echo start celery ...
echo ok
@echo start flower ...
echo ok
goto end

:stop
@echo stop flower
echo stoping
@echo stop celery
echo stoping
goto end

:end
echo 设置完成，按任意键退出 && pause
