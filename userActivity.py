#David Tang 1/30/20
#A Python script to parse an openvpn.log file to find and record all instances of user activity.  The script will find and record which user connected, when the connection started, when it ended, as well as the source IP addresses of the user.
#All user activity will be written to a UserActivityLog.txt file for easy digestion.

start = 0
baseIndex = 0
startIndex = 0
endIndex = 0
name = ""
timestamp = ""

with open("openvpn.log", "r") as myfile:
  data=myfile.read()

file = open("UserActivityLog.txt","w")

while(data.find("depth=1",start) != -1):
  #Log Format:
  #Thu Apr  2 08:56:49 2020 David/111.111.111.11:11111 VERIFY OK: depth=1, C=US, ST=null, L=NYC, O=CatInc, OU=null, CN=CatInc CA, name=server2, emailAddress=myemail@gmail.com
  #Thu Apr  2 08:56:49 2020 David/111.111.111.11:11111 VERIFY OK: depth=0, C=US, ST=null, L=NYC, O=CatInc, OU=null, CN=David, name=server2, emailAddress=myemail@gmail.com

  #Finding initial login log lines
  baseIndex = data.find("depth=1", start)
  startIndex = data.find("\n", baseIndex) + 1
  endIndex = data.find("VERIFY", startIndex)

#  print("HERE IS THE TIMESTAMP")
#  print(data[startIndex:endIndex])

  #Finding timestamp and soure IP when the connection was initiated
  timestamp = data[startIndex:endIndex]

  #Finding the username of who connected
  nameStart = data.find("CN=", startIndex)
  nameEnd = data.find("name=",nameStart) - 2
  name = data[nameStart:nameEnd]

  output = name + "  \t" + timestamp
#  print("FINAL THING")
#  print(output)
  file.write(output + "\n")

  #Finding the timestamp and source IP when the connection timed-out
  #Log Format
  #Thu Apr  2 09:08:06 2020 David/111.111.111.11:11111 [David] Inactivity timeout (--ping-restart), restarting
  timeoutStartString = "[" + name[3:] + "] Inactivity"
  timeoutStart = data.find(timeoutStartString, nameEnd)
  timeoutStart -= 80
  timeoutStart = data.find("\n", timeoutStart) + 1
  timeoutEnd = data.find("[", timeoutStart)
  timeoutTime = data[timeoutStart:timeoutEnd]

  file.write("\t\t" + timeoutTime + "\n\n")
  print("\t\t" + timeoutTime + "\n")


  start = nameEnd

file.close()
