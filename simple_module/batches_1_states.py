################################################################################
################################################################################

import os
import time
import sys

################################################################################
################################################################################

#Did the ivy_check action return an error?
def check_failed(file_name):
  with open(file_name, 'r') as read_obj:
    for line in read_obj:
      if "error:" in line:
        print("IVY RETURNED ERROR")
        return True
      if "not found: " in line:
        print("IVY RETURNED NOT FOUND")
        return True
  return False

#Did the ivy_check action return a passing trace?
def check_pass(file_name):
  with open(file_name, 'r') as read_obj:
    for line in read_obj:
      if "PASS" in line:
        return True
  return False

#Welcome and initialization
print("Working to generate all traces in batches.")

ts = str(int(time.time()))
totest = ""
indexlimitstr = ""
indexlimit = 0

if len(sys.argv) == 3:
  totest = str(sys.argv[1])
  indexlimitstr = sys.argv[2]
else:
  print("Your file options are:")
  os.system("ls *.ivy")
  print("")
  totest = input("Input the name of the IVy file: ")
  indexlimitstr = input("You can limit the number of traces you get back.\nEnter a number or 'n': ")

totest = totest.replace(".ivy","")
if not(indexlimitstr.isdigit()):
  indexlimit = 9999999999999
else:
  indexlimit = int(indexlimitstr)


################################################################################
################################################################################

#Open the working directory
foldername = str(totest) + "_" + str(indexlimit) + "_" + ts
os.system("mkdir " + foldername)
logfile = open(foldername + "/log.txt", 'a')
tracelist = open(foldername + "/traces.txt", 'a')

#Copy the file to test into the working directory
with open(totest + ".ivy", 'r') as old:
  with open(foldername + "/0.ivy", 'w') as new:
    for line in old:
      new.write(line)

print("All files opened correctly.")
print("Look in this folder once completed: " + foldername)
print("-----------")

################################################################################
################################################################################

index = 0
finished = False

#Find all the possible "bad states"
while not(finished) and index < indexlimit:

  #Initialize
  timer_start = time.time()
  new_invariant = ""
  tracefile = foldername + "/" + str(index) + ".txt"
  abrfile = foldername + "/" + str(index) + "_abr.txt"
  
  #Check the model
  os.system("ivy_check trace=true " + foldername + "/" + str(index) + ".ivy > " + tracefile)
  
  #Check for errors or passing states
  if check_failed(tracefile):
    print("\033[0;30;41mFAILURE: IVY ERROR!!! Big oops.\033[0m")
    exit()
  elif check_pass(tracefile):
    print("Finding bad states has completed.")
    if index == 0:
      print("\033[0;30;42mNO PROGRESS MADE!\033[0m")
    finished = True
    break

  ##############################################################################

  endtrace = False

  v = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
  d = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
  a = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
  r = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
  lastaction = "initial_state"

  #Examine the trace to find bad state
  #Also create an abbreviated trace
  with open(tracefile) as trace:
    with open(abrfile, 'w') as abr:
      for line in trace:
        if ("call ext:" in line):
          lastaction = line.split("call ext:")[1].rstrip("\n").replace(".","_")
          abr.write(lastaction + " \t")
          tracelist.write(lastaction + " \t")
        for i in range(0,len(v)):
          if ("spec.v" + str(i) + " =") in line:
            spl = line.split(" = ")
            clean = spl[1].rstrip('\n')
            v[i] = str(clean)
        for i in range(0,len(d)):
          if ("spec.d" + str(i) + " =") in line:
            spl = line.split(" = ")
            clean = spl[1].rstrip('\n')
            d[i] = str(clean)
        for i in range(0,len(a)):
          if ("spec.a" + str(i) + " =") in line:
            spl = line.split(" = ")
            clean = spl[1].rstrip('\n')
            a[i] = str(clean)
        for i in range(0,len(r)):
          if ("spec.r" + str(i) + " =") in line:
            spl = line.split(" = ")
            clean = spl[1].rstrip('\n')
            r[i] = str(clean)
      abr.write("\n")
      tracelist.write("\n")
    
  new_invariant = " | ("    
  for i in range(0, len(v)):
    new_invariant = new_invariant + "spec.v" + str(i) + " = " + v[i] + " & "
  for i in range(0, len(d)):
    new_invariant = new_invariant + "spec.d" + str(i) + " = " + d[i] + " & "
  for i in range(0, len(a)):
    new_invariant = new_invariant + "spec.a" + str(i) + " = " + a[i] + " & "
  for i in range(0, len(r)-1):
    new_invariant = new_invariant + "spec.r" + str(i) + " = " + r[i] + " & "
  new_invariant = new_invariant + "spec.r" + str(len(r)-1) + " = " + r[len(r)-1] + ") "
  
  #Add the invariant to the next file
  with open(foldername + "/" + str(index) + ".ivy", 'r') as old:
    with open(foldername + "/" + str(index + 1) +".ivy", 'w') as new:
      for line in old:
        if "invariant" in line:
          break
        else:
          new.write(line)
      if new_invariant in line:
        print("Woah there, cowboy. The following is already in this line:\n" + new_invariant)
        logfile.write("Woah there, cowboy. The following is already in this line: " + new_invariant + "\n")
      new.write(line.rstrip('\n') + new_invariant)
      # logfile.write("s1 " + s[1] + " s2 " + s[2] + " s3 " + s[3] + " s4 " + s[4] + " s5 " + s[5] + " | r1 " + r[1] + " r2 " + r[2] + " r3 " + r[3] + " r4 " + r[4] + " r5 " + r[5] + "\n")

  #Wrap things up
  timer_duration = time.time() - timer_start
  print("Checked index " + str(index), end="")
  print(" in %.2f seconds" % timer_duration)
  logfile.write("Checked index " + str(index))
  logfile.write(" in %.2f seconds\n" % timer_duration)
  index = index + 1

logfile.close()
tracelist.close()

print("FINISHED!")
print("\n\n###################################################################################")
print("###################################################################################")
print("###################################################################################\n\n")