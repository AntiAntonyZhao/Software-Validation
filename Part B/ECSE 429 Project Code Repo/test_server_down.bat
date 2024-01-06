@REM PART A
@REM pytest --random-order -c abnormal.ini tests

@REM PART B
set ABNORMAL=true
behave
set ABNORMAL=false
