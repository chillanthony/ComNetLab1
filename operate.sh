

python3 LocatingAlgorithm.py
echo "Locating Algoritm has successfully operated"


python3 -m http.server 12000 &
sleep 2
open http://localhost:12000/frontend.html
