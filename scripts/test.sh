a="123456789abcdefg"
b=`expr substr "$a" 1 4`
c=`echo ${a:5}`
echo $b
echo $c
