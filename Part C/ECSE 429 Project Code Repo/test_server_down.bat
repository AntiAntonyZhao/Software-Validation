@REM PART A
pytest --random-order -c abnormal.ini tests --ignore performance

@REM PART B
set ABNORMAL=true
behave
set ABNORMAL=false
