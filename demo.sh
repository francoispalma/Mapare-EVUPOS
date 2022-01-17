i=0
while [[ $i -lt 3 ]] 
do
	python3 proto.py --pos $(($i * 480)) 0 &
	python3 proto.py --pos $(($i * 480)) 480 &
	i=$(($i + 1))
done
