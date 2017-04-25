# bash script
# chmod +x script.sh
# sudo ./script.sh
git clone https://github.com/emmawestman/GCJ-mining.git
git clone https://github.com/alexandraback/datacollection.git

apt-get update
apt-get install python3 -y

apt-get install default-jre -y
apt-get install default-jdk -y

apt-get install python-pip -y
apt-get install python-nympy -y
apt-get install python-devlop -y
pip install pandas

apt-get install screen -y

apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb http://download.mono-project.com/repo/debian wheezy main" | tee /etc/apt/sources.list.d/mono-xamarin.list
apt-get update
echo "deb http://download.mono-project.com/repo/debian wheezy-apache24-compat main" | tee -a /etc/apt/sources.list.d/mono-xamarin.list
echo "deb http://download.mono-project.com/repo/debian wheezy-libjpeg62-compat main" | tee -a /etc/apt/sources.list.d/mono-xamarin.list
apt-get install mono-complete -y

cd /usr/locals/include
mkdir bits
cd /home/user/GCJ-mining/
cp stdc++.h /usr/locals/include/bits