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

  q = ["0", "0", "0", "0", "0", "0", "0"]
  r = ["0", "0", "0", "0", "0", "0", "0"]
  s = ["0", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR"]
  lastaction = "initial_state"

  #Examine the trace to find bad state
  #Also create an abbreviated trace
  with open(tracefile) as trace:
    with open(abrfile, 'w') as abr:
      for line in trace:
        if ("call ext:spec." in line):
          lastaction = line.split("call ext:spec.")[1].rstrip("\n").replace(".","_")
        if "   spec.s1 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            s[1] = str(clean)
          else:
            print("s1 WAS NOT A DIGIT. GOT _" + clean + "_")
        elif "   spec.s2 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            s[2] = str(clean)
          else:
            print("s2 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.s3 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            s[3] = str(clean)
          else:
            print("s3 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.s4 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            s[4] = str(clean)
          else:
            print("s4 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.s5 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            s[5] = str(clean)
          else:
            print("s5 WAS NOT A DIGIT. GOT _" + clean + "_")
            
        if "   spec.r1 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            r[1] = str(clean)
          else:
            print("r1 WAS NOT A DIGIT. GOT _" + clean + "_")
        elif "   spec.r2 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            r[2] = str(clean)
          else:
            print("r2 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.r3 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            r[3] = str(clean)
          else:
            print("s3 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.r4 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            r[4] = str(clean)
          else:
            print("r4 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.r5 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            r[5] = str(clean)
          else:
            print("r5 WAS NOT A DIGIT. GOT _" + clean + "_")
      
        if "   spec.q1 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            q[1] = str(clean)
          else:
            print("q1 WAS NOT A DIGIT. GOT _" + clean + "_")
        elif "   spec.q2 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            q[2] = str(clean)
          else:
            print("q2 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.q3 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            q[3] = str(clean)
          else:
            print("q3 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.q4 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            q[4] = str(clean)
          else:
            print("q4 WAS NOT A DIGIT. GOT _" + clean + "_")
        if "   spec.q5 = " in line:
          spl = line.split(" = ")
          clean = spl[1].rstrip('\n')
          if clean.isdigit():
            q[5] = str(clean)
          else:
            print("q5 WAS NOT A DIGIT. GOT _" + clean + "_")

  #Use that information to add to the invariant
  new_invariant = " | (spec.s1 = " + s[1] + " & spec.s2 = " + s[2] + " & spec.s3 = " + s[3] + " & spec.s4 = " + s[4] + " & spec.s5 = " + s[5] + " & spec.r1 = " + r[1] + " & spec.r2 = " + r[2] + " & spec.r3 = " + r[3] + " & spec.r4 = " + r[4] + " & spec.r5 = " + r[5] + " & spec.q1 = " + q[1] + " & spec.q2 = " + q[2] + " & spec.q3 = " + q[3] + " & spec.q4 = " + q[4] + " & spec.q5 = " + q[5] + ")"

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
      logfile.write("s1 " + s[1] + " s2 " + s[2] + " s3 " + s[3] + " s4 " + s[4] + " s5 " + s[5] + " | r1 " + r[1] + " r2 " + r[2] + " r3 " + r[3] + " r4 " + r[4] + " r5 " + r[5] + "\n")

  #Wrap things up
  timer_duration = time.time() - timer_start
  print("Checked index " + str(index), end="")
  print(" in %.2f seconds" % timer_duration)
  index = index + 1

logfile.close()

# logfile = open(foldername + "/log.txt", 'r')
# index = 0

# with open(foldername + "/conefile.txt", 'w') as conefile:
#   while os.path.exists(foldername + "/" + str(index) + "_abr.txt"):
#     abrfile = foldername + "/" + str(index) + "_abr.txt"
#     trace = ""
#     with open(abrfile) as abr:
#       for line in abr:
#         if "initial_state" in line:
#           pass
#         elif "a" in line:
#           try:
#             if trace != "":
#               trace = trace + " "
#             trace = trace + line.split()[10].replace("\n","").replace(".","_")
#           except IndexError:
#             print("IndexError... moving on")
#       if trace != "":
#         conefile.write(trace + "\n")
#       index = index + 1

# logfile.close()

print("FINISHED!")
print("\n\n###################################################################################")
print("###################################################################################")
print("###################################################################################\n\n")