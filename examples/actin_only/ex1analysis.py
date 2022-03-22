###########################
#
#
#	EXAMPLE 1 ANALYSIS
#
#	See the example guide
#   for details on usage.
###########################

matplotlib.rcParams['font.sans-serif']=["Arial"] 
mpl.rcParams['xtick.labelsize'] = 8 
mpl.rcParams['ytick.labelsize'] = 8 

from numpy import *
import pylab as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import scipy.linalg as la
from scipy.stats import linregress
import math

#Various snapshots for objects
class FilamentSnapshot:
	def __init__(self):
		self.id=None
		self.type=None
		self.length=None
		self.delta_left=None	
		self.delta_right=None	
		self.coords={}
		self.colors={}
		self.connections=None

#A cylinder snapshot
class CylinderSnapshot:
	def __init__(self):
		self.id = None
		self.coords={}

class LinkerSnapshot:
	def __init__(self):
		self.id=None
		self.type=None
		self.coords={}
		self.colors={}
		self.connections=None

class MotorSnapshot:
	def __init__(self):
		self.id=None
		self.type=None
		self.coords={}
		self.colors={}
		self.connections=None

class BrancherSnapshot:
	def __init__(self):
		self.id=None
		self.type=None;
		self.coords={}

class BubbleSnapshot:
	def __init__(self):
		self.id=None
		self.type=None;
		self.coords={}

#A full trajectory snapshot
class TrajSnapshot:
	def __init__(self):
		self.step=None
		self.time=None
		self.n_filaments=None
		self.n_linkers=None
		self.n_motors=None
		self.n_branchers=None
		self.n_bubbles=0
		self.filaments={}
		self.cylinders={}
		self.linkers={}
		self.motors={}
		self.branchers={}
		self.bubbles={}


#A chemical snapshot
class ChemSnapshot:
	def __init__(self):
		self.step=None
		self.time=None
		self.diffusingSpecies={}
		self.bulkSpecies={}
		self.filamentSpecies={}
		self.plusEndSpecies={}
		self.minusEndSpecies={}
		self.linkerSpecies={}
		self.motorSpecies={}
		self.brancherSpecies={}


#A histogram of values from a snapshot
class HistSnapshot:
	def __init__(self):
		self.step=None
		self.time=None
		self.hist={}

########################################################
#
#			         PARSING FUNCTIONS
#
########################################################


#Read all data from a trajectory file
#returns a list of Snapshots with all data
def readTrajectory(filename):

	print "Reading " + filename + "..."

	#Open the traj file
	traj_file=open(filename)

	TrajSnapshotList=[]
	first_snapshot_line=True
	first_line=True
	reading_filament=False
	reading_linker=False
	reading_motor=False
	reading_brancher=False
	reading_bubble=False
	n_beads_filament=0
	n_beads_linker=0
	n_beads_motor=0
	n_beads_brancher=0;
	n_beads_bubble=0;

	line_number = 0;

	for line in traj_file:
		line = line.strip()

		if(first_snapshot_line):
			F=TrajSnapshot()

			if len(line.split()) == 7:
				F.step, F.time, F.n_filaments, F.n_linkers, \
				F.n_motors, F.n_branchers, F.n_bubbles = map(double,line.split())
			else:
				F.step, F.time, F.n_filaments, F.n_linkers, \
				F.n_motors, F.n_branchers = map(double,line.split())

			F.n_filaments = int(F.n_filaments)
			F.n_linkers   = int(F.n_linkers)
			F.n_motors    = int(F.n_motors)
			F.n_branchers = int(F.n_branchers)
			F.n_bubbles   = int(F.n_bubbles)
			first_snapshot_line=False
			line_number+=1
			continue

		if(len(line)==0):
			first_snapshot_line=True
			first_filament_line=True
			TrajSnapshotList.append(F)

			assert F.n_filaments == len(F.filaments)
			assert F.n_linkers   == len(F.linkers)
			assert F.n_motors    == len(F.motors)
			assert F.n_branchers == len(F.branchers)
			assert F.n_bubbles   == len(F.bubbles)

			n_beads_filament=0
			n_beads_linker=0
			n_beads_motor=0
			n_beads_brancher=0;
			n_beads_bubble=0;
			line_number+=1
			continue
			
		if(first_line):
			line_split = line.split()

			if(line_split[0] == "FILAMENT") or (line_split[0] == "F"):
				FS=FilamentSnapshot()

				if(len(line_split[1:]) == 5):
					FS.id, FS.type, FS.length, FS.delta_left, FS.delta_right = map(int,line_split[1:])
				else:
					FS.id, FS.length, FS.delta_left, FS.delta_right = map(int,line_split[1:])

				first_line=False
				F.filaments[FS.id]=FS
				FS.connections=vstack(
					[arange(n_beads_filament, n_beads_filament + FS.length - 1.5), 
					 arange(n_beads_filament + 1, n_beads_filament + FS.length - .5)]).T
				n_beads_filament+=FS.length
				reading_filament=True
				line_number+=1
				continue
			if(line_split[0] == "LINKER") or (line_split[0] == "L"):
				LS = LinkerSnapshot()
				LS.id, LS.type = map(int, line_split[1:])
				first_line = False
				F.linkers[LS.id] = LS
				LS.connections=vstack([arange(n_beads_linker, n_beads_linker + 0.5), 
				  			           arange(n_beads_linker + 1, n_beads_linker + 1.5)]).T
				n_beads_linker+=2
				reading_linker=True
				line_number+=1
				continue
			if(line_split[0] == "MOTOR") or (line_split[0] == "M"):
				MS = MotorSnapshot()
				MS.id, MS.type = map(int, line_split[1:])
				first_line = False
				F.motors[MS.id] = MS
				MS.connections=vstack([arange(n_beads_motor, n_beads_motor + 0.5), 
									   arange(n_beads_motor + 1, n_beads_motor + 1.5)]).T
				n_beads_motor+=2
				reading_motor=True
				line_number+=1
				continue

			if(line_split[0] == "BRANCHER") or (line_split[0] == "B"):
				BS = BrancherSnapshot()
				BS.id, BS.type = map(int, line_split[1:])
				first_line = False
				F.branchers[BS.id] = BS
				n_beads_brancher+=1
				reading_brancher=True
				line_number+=1
				continue
			if(line_split[0] == "BUBBLE"):
				US = BubbleSnapshot()
				US.id, US.type = map(int, line_split[1:])
				first_line = False
				F.bubbles[US.id] = US
				n_beads_bubble+=1
				reading_bubble=True
				line_number+=1
				continue

		if(reading_filament):
			FS.coords=array(line.split(),'f')
			N=len(FS.coords)
			FS.coords=FS.coords.reshape(N/3,3)

			#create cylinder snapshots
			for i in xrange(0, len(FS.coords) - 1):
				CS = CylinderSnapshot()
				#create unique id using cylinder position and fil id
				CS.id = (FS.id + i) * (FS.id + i + 1) / 2 + FS.id
				CS.coords = [FS.coords[i], FS.coords[i+1]]
				F.cylinders[CS.id] = CS

			first_line=True
			reading_filament=False

		if(reading_linker):
			LS.coords=array(line.split(),'f')
			N=len(LS.coords)
			LS.coords=LS.coords.reshape(N/3,3)
			first_line=True
			reading_linker=False

		if(reading_motor):
			MS.coords=array(line.split(),'f')
			N=len(MS.coords)
			MS.coords=MS.coords.reshape(N/3,3)
			first_line=True
			reading_motor=False

		if(reading_brancher):
			BS.coords=array(line.split(),'f')
			N=len(BS.coords)
			BS.coords=BS.coords.reshape(N/3,3)
			first_line=True
			reading_brancher=False

		if(reading_bubble):
			US.coords=array(line.split(),'f')
			N=len(US.coords)
			US.coords=US.coords.reshape(N/3,3)
			first_line=True
			reading_bubble=False

		line_number+=1

	#return the final Snapshot list
	print str(len(TrajSnapshotList)) + " snapshots read."

	return TrajSnapshotList	

#Read a number of trajectories, return array of Snapshot lists
def readTrajectories(fileNames, fileDirectory='', runMin=0, runMax=10):

	#if file directory specified, auto-generate file names:
	if (fileDirectory != ''):

		fileNames = []

		for trajNum in xrange(runMin, runMax):
			fileNames.append(fileDirectory + '/Run' + str(trajNum) + '/snapshot.traj')

	#now read data
	TrajSnapshotLists = []

	for trajFile in fileNames:
		print "Reading trajectory..."
		TrajSnapshotLists.append(readTrajectory(trajFile))

	return TrajSnapshotLists


########################################################
#
#
#			     ANALYSIS FUNCTIONS
#
#	contains: 
#		-plotRg(), plotRgs()
#		-plotOrderParameter(), plotOrderParameters()
#		
########################################################

#Calculate the radius of gyration over all cylinders 
#returns a time and Rg pair for the chosen snapshot
def radiusOfGyration(SnapshotList, snapshot=1):

	Snapshot = SnapshotList[snapshot]

	#get center of mass of Snapshot
	com = np.array([0.0,0.0,0.0])
	beadCount = 0

		#go through filaments
	for filamentID, FS in Snapshot.filaments.iteritems():

		for coord in FS.coords:

			com += coord
			beadCount += 1

	#normalize
	com /= beadCount

	RgSquare = 0
	numCylinders = 0

	#Loop through cylinders
	for cylinderID, CS in Snapshot.cylinders.iteritems():

		numCylinders += 1
		cam = (CS.coords[1] + CS.coords[0]) / 2

		RgSquare += (cam - com).dot(cam - com)

	RgSquare /= numCylinders
	Rg = sqrt(RgSquare * 0.00001) #units in um

	return (Snapshot.time, Rg)


#Calculate the radius of gyration over all cylinders from a number of trajectories
def radiusOfGyrations(SnapshotLists, snapshot=1):

	RgList = []

	#get all data
	for SnapshotList in SnapshotLists:

		Rg = radiusOfGyration(SnapshotList, snapshot)
		RgList.append(Rg)

	#now combine data
	finalTime = 0
	finalRg = 0

	for Rg in RgList:

		finalTime += Rg[0]
		finalRg += Rg[1]

	#average
	finalTime /= len(RgList)
	finalRg /= len(RgList)

	Rgs = [x[1] for x in RgList]
	err = np.std(Rgs)

	return (finalTime,finalRg,err)

def plotRg(SnapshotList):

	fig = plt.figure(0, figsize=(5.0,5.0))

	Rg = []

	for i in xrange(0, len(SnapshotList)):
		Rg.append(radiusOfGyration(SnapshotList, snapshot=i))

	time = [x[0] for x in Rg]
	rg 	 = [x[1] for x in Rg]

	plt.plot(time, rg)

	plt.xlabel(r'$\mathsf{Time\/(s)}$', fontsize=12)
	plt.ylabel(r'$\mathsf{R_g\/(\mu m)}$', fontsize=12)


def plotRgs(SnapshotLists):

	fig = plt.figure(1, figsize=(5.0,5.0))

	Rgs = []

	for i in xrange(0, len(SnapshotLists[0])):
		Rgs.append(radiusOfGyrations(SnapshotLists, snapshot=i))

	time = [x[0] for x in Rgs]
	rg 	 = [x[1] for x in Rgs]
	errplus  = [x[1] + x[2]  for x in Rgs]
	errminus = [x[1] - x[2]  for x in Rgs]

	plt.plot(time, rg)
	fill_between(time, errplus, errminus, alpha=0.20)

	plt.xlabel(r'$\mathsf{Time\/(s)}$', fontsize=12)
	plt.ylabel(r'$\mathsf{R_g\/(\mu m)}$', fontsize=12)


#Calculate nematic order parameter of cylinders at each timestep
#from order parameter definition at http://cmt.dur.ac.uk/sjc/thesis_dlc/node65.html
#takes the largest eigenvalue of Q, a second rank ordering tensor over cylinder pairs
#returns a list of time and value pairs
def orderParameter(SnapshotList, snapshot=1):

	orderParams = []
	try:
		Snapshot = SnapshotList[snapshot]

	except IndexError:
		#print "Index error. Excluding this snapshot list."
		return False

	Q = np.zeros((3, 3))

	for alpha in [0,1,2]:

		for beta in [0,1,2]:

			for filamentID, FS in Snapshot.filaments.iteritems():

				#calculate direction
				mag = sqrt((FS.coords[len(FS.coords) - 1] - FS.coords[0]). \
					    dot(FS.coords[len(FS.coords) - 1] - FS.coords[0]))

				direction = (FS.coords[len(FS.coords) - 1] - FS.coords[0]) / mag

				#pairwise delta
				if alpha == beta: 
					delta = 1
				else:
					delta = 0

				#q value
				Q[alpha][beta] += ((3.0/2.0) * direction[alpha] * direction[beta] - (1.0/2.0) * delta)

			Q[alpha][beta] *= 1 / (float(len(Snapshot.filaments)))

	#take largest eigenvalue
	w, v= la.eig(Q)
	director = v[0]

	return (Snapshot.time, max(w).real)


##Calculate nematic order parameter of cylinders from a number of trajectories
#from order parameter definition at http://cmt.dur.ac.uk/sjc/thesis_dlc/node65.html
#takes the largest eigenvalue of Q, a second rank ordering tensor over cylinder pairs
def orderParameters(SnapshotLists, snapshot=1):

	orderParamsList = []

	#get all data
	for SnapshotList in SnapshotLists:
		orderParamsList.append(orderParameter(SnapshotList, snapshot))

	time = 0
	op= 0

	for orderParam in orderParamsList:

		time += orderParam[0]
		op += orderParam[1]

	#average
	time /= len(orderParamsList)
	op /= len(orderParamsList)

	ops = [x[1] for x in orderParamsList]
	error = np.std(ops)

	return (time,op,error)

def plotOrderParameter(SnapshotList):

	fig = plt.figure(2, figsize=(5.0,5.0))

	Op = []

	for i in xrange(0, len(SnapshotList)):
		Op.append(orderParameter(SnapshotList, snapshot=i))

	time = [x[0] for x in Op]
	op 	 = [x[1] for x in Op]

	plt.plot(time, op)

	plt.xlabel(r'$\mathsf{Time\/(s)}$', fontsize=12)
	plt.ylabel(r'$\mathsf{S}$', fontsize=12)


def plotOrderParameters(SnapshotLists):

	fig = plt.figure(3, figsize=(5.0,5.0))

	Ops = []

	for i in xrange(0, len(SnapshotLists[0])):
		Ops.append(orderParameters(SnapshotLists, snapshot=i))

	time = [x[0] for x in Ops]
	op 	 = [x[1] for x in Ops]
	errplus  = [x[1] + x[2]  for x in Ops]
	errminus = [x[1] - x[2]  for x in Ops]

	print len(op), len(errplus), len(errminus)

	plt.plot(time, op)
	fill_between(time, errplus, errminus, alpha=0.20)

	plt.xlabel(r'$\mathsf{Time\/(s)}$', fontsize=12)
	plt.ylabel(r'$\mathsf{S}$', fontsize=12)


