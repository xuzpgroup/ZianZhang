import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import pickle
import math

class Crack:
    
    # FUNCTION: initialize the project
    def __init__(self,path,head_end,index):
        self.path=path              # the path of a crack
        self.head_end=head_end      # if the head or end would propagate
        self.index=index
        self.contour_ele=[[],[]]
        self.dangle=[0.0,0.0]
#----------------------------------------------------------------------
# Jintegral_test.py  

def reshapeContour(contour):
    clist=[]
    for i in range(0,len(contour)):
        for j in range(0,len(contour[i])):
            clist.append(contour[i][j])
    return clist

def createEleMap(ele,select):
    global f
    elementType=''
    nodeList=[]                     # A list of nodes within the contours
    nodeList_con=[]                 # A list of lists of nodes of elements in each contour
    contour_node=[]                 # A list of lists of nodes on each contour, include the crack tip nodes
    mapEle={}                       # Map the element label to its index in the element 
                                    # array, since the element label could be discontinuous
    eleCon={}                       # The connectivity of elements 
    ncont=len(select)               # Number of contours
    node_Ele={}                     # Record elements to which a node belongs
    for i in range(0,ncont):
        contour_node.append([])
        nodeList_con.append([])
        
    for i in range(0,len(ele)):
        label=ele[i].label
        for j in range(0,ncont):
            # if the label has not been recorded and should be selected, then record it
            if (not label in mapEle.keys())and(label in select[j]):
                mapEle[label]=i
                connect=ele[i].connectivity
                eleCon[label]=connect
                for k in range(0,len(connect)):
                    # if the node has not been recorded, then record it
                    if not connect[k] in nodeList:
                        nodeList.append(connect[k])
                        node_Ele[connect[k]]=[label,]
                    else:
                        node_Ele[connect[k]].append(label)
                    if not connect[k] in nodeList_con[j]:
                        nodeList_con[j].append(connect[k])
                break
    elementType=ele[mapEle[select[0][0]]].type
    
    # Find out nodes on a contour, which are the intersections of two neighboring 
    #   contour node sets
    # For the N-1 contours
    for i in range(0,ncont-1):
        for j in range(0,len(nodeList_con[i])):
            if nodeList_con[i][j] in nodeList_con[i+1]:
                contour_node[i].append(nodeList_con[i][j])
    # For the last contour. 
    if ncont>1:
        for i in range(0,len(nodeList_con[-1])):
            nodeLabel=nodeList_con[-1][i]
            if (not (nodeLabel in nodeList_con[-2])):
                # get the node index in one of the element, and determine if it is
                #   a node on the outer contour
                label=node_Ele[nodeLabel][0]
                nid=eleCon[label].index(nodeLabel)         
                if nid>=4:
                    if nid==4:
                        if (not(eleCon[label][0] in nodeList_con[-2]))and \
                           (not(eleCon[label][1] in nodeList_con[-2])):
                               contour_node[-1].append(nodeList_con[-1][i])
                    elif nid==5:
                        if (not(eleCon[label][1] in nodeList_con[-2]))and \
                           (not(eleCon[label][2] in nodeList_con[-2])):
                               contour_node[-1].append(nodeList_con[-1][i]) 
                    elif nid==6:
                        if (not(eleCon[label][2] in nodeList_con[-2]))and \
                           (not(eleCon[label][3] in nodeList_con[-2])):
                               contour_node[-1].append(nodeList_con[-1][i])
                    elif nid==7:
                        if (not(eleCon[label][4] in nodeList_con[-2]))and \
                           (not(eleCon[label][0] in nodeList_con[-2])):
                               contour_node[-1].append(nodeList_con[-1][i])  
                else:
                    contour_node[-1].append(nodeList_con[-1][i])  
    else:
        contour_node[0]=[2,3,4,5,6,7,8,9,10]      ## added temperarily for Edge_crack_jintegral_cps4_4ele.odb. delete the 'if' here afterward                               
    return mapEle,eleCon,nodeList,contour_node,elementType

def extractNodeFieldOutput(odb,step,frame,nodeList,variables):
    f=odb.steps[step].frames[frame]
    nodeLabel=[]
    data={}
    for var in variables:
        if var in f.fieldOutputs.keys():    
            data[var]={}
            fo=f.fieldOutputs[var]
            values=fo.values
            for value in values:
                nl=value.nodeLabel
                if nl in nodeList:
                    data[var][nl]=value.dataDouble
                    nodeLabel.append(nl)
    return data,nodeLabel

def extractEleFieldOutput(odb,step,frame,eleList,variables):
    f=odb.steps[step].frames[frame]
    data={}
    for var in variables:
        if var in f.fieldOutputs.keys():    
            data[var]={}
            fo=f.fieldOutputs[var]
            values=fo.values
            for value in values:
                el=value.elementLabel
                ip=value.integrationPoint
                if el in eleList:
                    if not(el in data[var].keys()):
                        data[var][el]={}
                    data[var][el][ip]=value.data
    return data

def extractNodePosition(odb,insName,nodeList,crackTip,tol=1e-6):
    x={}
    crackTipNode=[]
    nodes=odb.rootAssembly.instances[insName].nodes
    for n in nodes:
        if n.label in nodeList:
            x[n.label]=n.coordinates
            if np.sqrt(sum((crackTip-n.coordinates[0:2])**2))<tol:
                crackTipNode.append(n.label)
    return x,crackTipNode


#----------------------------------------------------------------------
# Mintegral_2D.py

def readData(path1,filename):
    f=open(path1+filename,'rb')
    u=pickle.load(f)
    e=pickle.load(f)
    s=pickle.load(f)
    contour_ele=pickle.load(f)
    contour_node=pickle.load(f)
    eleCon=pickle.load(f)
    nodePos=pickle.load(f)
    eleType=pickle.load(f)
    crackTip=pickle.load(f)
    q=pickle.load(f)
    # u=pickle.load(f,encoding='bytes')
    # e=pickle.load(f,encoding='bytes')
    # s=pickle.load(f,encoding='bytes')
    # contour_ele=pickle.load(f,encoding='bytes')
    # contour_node=pickle.load(f,encoding='bytes')
    # eleCon=pickle.load(f,encoding='bytes')
    # nodePos=pickle.load(f,encoding='bytes')
    # eleType=pickle.load(f)
    # crackTip=pickle.load(f,encoding='bytes')
    # q=pickle.load(f,encoding='bytes')
    f.close()

    return u,e,s,contour_ele,contour_node,eleCon,nodePos,eleType,crackTip,q
    
def eleInfo(eleType):
    N_p=[]      # the derivative of shape function with respect to the 
                #   isoparametric coordinates
    nip=0       # number of integration point
    
    if (eleType=="CPS4"):
        nip=4
        # define the position of integration points
        gp=1.0/np.sqrt(3.0)
        g=np.array([-gp,gp,-gp,gp])
        h=np.array([-gp,-gp,gp,gp])
        # weight of integration point
        weight=[1.0,1.0,1.0,1.0]
        # calculate the the derivative of shape function on integration point
        for i in range(0,nip):
            N_p.append(np.array([[-(1-h[i])/4.0,(1-h[i])/4.0,(1+h[i])/4.0,-(1+h[i])/4.0],
                          [-(1-g[i])/4.0,-(1+g[i])/4.0,(1+g[i])/4.0,(1-g[i])/4.0]]) )
    
    elif eleType=="CPS8":        
        nip=9
        # define the position of integration points
        gp=np.sqrt(15.0)/5.0
        g=np.array([-gp,  0, gp,-gp, 0, gp,-gp, 0,gp])
        h=np.array([-gp,-gp,-gp,  0, 0,  0, gp,gp,gp])
        # weight of integration point
        w1=5.0/9.0
        w2=8.0/9.0
        weight=[w1*w1,w1*w2,w1*w1,w1*w2,w2*w2,w1*w2,w1*w1,w1*w2,w1*w1]
        # calculate the the derivative of shape function on integration point
        for i in range(0,nip):
            N_p.append(np.array([[ (1-h[i])*(2*g[i]+h[i])/4.0, -(1-h[i])*(h[i]-2*g[i])/4.0, \
                            (1+h[i])*(2*g[i]+h[i])/4.0, -(1+h[i])*(h[i]-2*g[i])/4.0, \
                           -(1-h[i])*g[i],            (1-h[i])*(1+h[i])/2.0      , \
                           -g[i]*(1+h[i]),           -(1-h[i])*(1+h[i])/2.0]     , \
                          [ (1-g[i])*(2*h[i]+g[i])/4.0, -(1+g[i])*(g[i]-2*h[i])/4.0, \
                            (1+g[i])*(g[i]+2*h[i])/4.0, -(1-g[i])*(g[i]-2*h[i])/4.0, \
                           -(1-g[i])*(1+g[i])/2.0,      -(1+g[i])*h[i]           , \
                            (1-g[i])*(1+g[i])/2.0,      -(1-g[i])*h[i] ] ]) )       
    elif eleType=='CPS8R':
        nip=4
        # define the position of integration points
        gp=1.0/np.sqrt(3.0)
        g=np.array([-gp,gp,-gp,gp])
        h=np.array([-gp,-gp,gp,gp])
        # weight of integration point
        weight=[1.0,1.0,1.0,1.0]
        # calculate the the derivative of shape function on integration point
        for i in range(0,nip):
            N_p.append(np.array([[ (1-h[i])*(2*g[i]+h[i])/4.0, -(1-h[i])*(h[i]-2*g[i])/4.0, \
                            (1+h[i])*(2*g[i]+h[i])/4.0, -(1+h[i])*(h[i]-2*g[i])/4.0, \
                           -(1-h[i])*g[i],            (1-h[i])*(1+h[i])/2.0      , \
                           -g[i]*(1+h[i]),           -(1-h[i])*(1+h[i])/2.0]     , \
                          [ (1-g[i])*(2*h[i]+g[i])/4.0, -(1+g[i])*(g[i]-2*h[i])/4.0, \
                            (1+g[i])*(g[i]+2*h[i])/4.0, -(1-g[i])*(g[i]-2*h[i])/4.0, \
                           -(1-g[i])*(1+g[i])/2.0,      -(1+g[i])*h[i]           , \
                            (1-g[i])*(1+g[i])/2.0,      -(1-g[i])*h[i] ] ]) )          
    return nip,N_p,weight

def interpolate(x0,n,eleType):
    if (eleType=="CPS4"):
        # define the position of integration points
        gp=1.0/np.sqrt(3.0)
        g=np.array([-gp,gp,-gp,gp])
        h=np.array([-gp,-gp,gp,gp])
        x=1.0/4.0*(1-g[n])*(1-h[n])*x0[0,:]+ \
          1.0/4.0*(1+g[n])*(1-h[n])*x0[1,:]+ \
          1.0/4.0*(1+g[n])*(1+h[n])*x0[2,:]+ \
          1.0/4.0*(1-g[n])*(1+h[n])*x0[3,:]

    elif (eleType=="CPS8"):
        gp=np.sqrt(15.0)/5.0
        g=np.array([-gp,  0, gp,-gp, 0, gp,-gp, 0,gp])
        h=np.array([-gp,-gp,-gp,  0, 0,  0, gp,gp,gp])
        x=-1.0/4.0*(1-g[n])*(1-h[n])*(1+g[n]+h[n])*x0[0,:] \
          -1.0/4.0*(1+g[n])*(1-h[n])*(1-g[n]+h[n])*x0[1,:] \
          -1.0/4.0*(1+g[n])*(1+h[n])*(1-g[n]-h[n])*x0[2,:] \
          -1.0/4.0*(1-g[n])*(1+h[n])*(1+g[n]-h[n])*x0[3,:] \
          +1.0/2.0*(1-g[n])*(1+g[n])*(1-h[n])*x0[4,:] \
          +1.0/2.0*(1-h[n])*(1+h[n])*(1+g[n])*x0[5,:] \
          +1.0/2.0*(1-g[n])*(1+g[n])*(1+h[n])*x0[6,:] \
          +1.0/2.0*(1-h[n])*(1+h[n])*(1-g[n])*x0[7,:]

    return x

def K_field(r,theta,kapa,G,K,mode):
    SIN=np.sin(theta/2.0)
    COS=np.cos(theta/2.0)
    p=K/np.sqrt(2.0*np.pi*r)
    s=np.zeros(3)
    e=np.zeros(3)
    u_x=np.zeros([2,2])
    if mode==1:
        s[0]=p*COS*(1.0-SIN*np.sin(3*theta/2.0))
        s[1]=p*COS*(1.0+SIN*np.sin(3*theta/2.0))
        s[2]=p*COS*SIN*np.cos(3.0*theta/2.0);       
        u_x[0,0]=p/4.0/G*((kapa-1.0)*COS-6.0*(SIN**2)*(COS**3)+2.0*(SIN**4)*COS)
        u_x[0,1]=p/4.0/G*((kapa-1.0)*SIN+2.0*(SIN**5)+4.0*SIN*(COS**4)-2.0*(SIN**3)*(COS**2))
        u_x[1,0]=p/4.0/G*(-(kapa+1.0)*SIN-6.0*(SIN**3)*(COS**2)+2.0*SIN*(COS**4))
        u_x[1,1]=p/4.0/G*((kapa+1.0)*COS-2.0*(COS**5)+2.0*(SIN**2)*(COS**3)-4.0*(SIN**4)*COS)
    elif mode==2:
        s[0]=-p*SIN*(2.0+COS*np.cos(3.0*theta/2))
        s[1]=p*SIN*COS*np.cos(3.0*theta/2)
        s[2]=p*COS*(1.0-SIN*np.sin(3.0*theta/2))
        u_x[0,0]=p/4.0/G*(-(kapa+1)*SIN+6.0*(SIN**3)*(COS**2)-2.0*SIN*(COS**4))
        u_x[0,1]=p/4.0/G*((kapa+1)*COS+2.0*(COS**5)+4.0*(SIN**4)*COS-2.0*(SIN**2)*(COS**3))
        u_x[1,0]=p/4.0/G*(-(kapa-1)*COS-6.0*(SIN**2)*(COS**3)+2.0*(SIN**4)*COS)
        u_x[1,1]=p/4.0/G*(-(kapa-1)*SIN+2.0*(SIN**5)-2.0*(SIN**3)*(COS**2)+4.0*SIN*(COS**4))

    e[0]=u_x[0,0]
    e[1]=u_x[1,1]
    e[2]=u_x[0,1]+u_x[1,0]
    return s,e,u_x

def rotate_tensor(theta,s,e,u_x):
    Q=np.array([ [np.cos(theta),-np.sin(theta)] , [np.sin(theta),np.cos(theta)] ])
    s_mat=np.array([[s[0],s[2]],[s[2],s[1]]])
    e_mat=np.array([[e[0],e[2]/2],[e[2]/2,e[1]]])
    s_mat=np.dot(np.dot(Q,s_mat),Q.T)
    e_mat=np.dot(np.dot(Q,e_mat),Q.T)
    u_x=np.dot(np.dot(Q,u_x),Q.T)
    s=np.array([s_mat[0,0],s_mat[1,1],s_mat[1,0]])
    e=np.array([e_mat[0,0],e_mat[1,1],e_mat[1,0]*2])
    return s,e,u_x

def ele_Integral(x_e,u_e,q_e,e_e,s_e,crackTip,q,eleType,anaType):
    
    E=200000.0        # Young's modulus (MPa)
    v=0.3           # Poisson ratio
    G=E/2.0/(1.0+v)
    # Element information: number of integration points, derivative of shape function
    #   and weight of integration points
    nip,N_p,weight=eleInfo(eleType)
    if (eleType=='CPS4')or(eleType=='CPS8')or(eleType=='CPS8R'):
        kapa=(3.0-v)/(1.0+v)
        x_e=np.array(x_e)[:,0:2]        # for 2d problems, only x y coordinates used
        u_e=np.array(u_e)
        q_e=np.array(q_e)
        #x_e=x_e+u_e
        C=E/(1.0-v**2)*np.array([[1.0,v,0.0],[v,1.0,0.0],[0.0,0.0,(1.0-v)/2.0]])
        J_e=0
        M_e=np.array([0.0,0.0,0.0])
        M_e_test=np.array([0.0,0.0,0.0])
        for i in range(0,nip):
            x_p=np.dot(x_e.T,N_p[i].T)                       # dx/dp, x: material coords., p: isoparametric coords
            p_x=np.linalg.inv(x_p)                              # dp/dx
            detJ=np.linalg.det(x_p)                             # Jacobian of dx/dp
            B=np.dot(N_p[i].T,p_x)                           # matrix to transform displacement to the gradient of displacement
            u_x=np.dot(u_e.T,B)                              # gradient of displacement at a integration point
            q_x=np.dot(q_e.T,B)                              # gradient of virtual crack propagation direction
            e=np.array([u_x[0,0],u_x[1,1],u_x[0,1]+u_x[1,0]])   # strain
            s=np.dot(C,e.T)                                  # stress
            
            # strain and stress data directly from FEM, for debugging
            # e_fem=np.array([e_e[i+1][0],e_e[i+1][1],e_e[i+1][3]])
            # s_fem=np.array([s_e[i+1][0],s_e[i+1][1],s_e[i+1][3]])
            if anaType=='J':
                w=sum(e*s)/2.0                                        # strain energy
                W=w*np.identity(2)
                H=W-np.dot(np.array([ [s[0],s[2]] , [s[2],s[1]] ]),u_x)
                J_e=J_e-np.tensordot(H,q_x.T,axes=2)*detJ*weight[i]       
            if anaType=='M':
                x_ip=interpolate(x_e,i,eleType)
                d=x_ip-crackTip
                r=np.sqrt(sum(d**2))
                theta=np.arccos(sum(d*q)/r) # q has been normalized
                if (q[0]*d[1]-q[1]*d[0])<0:
                    theta=-theta
                thetad=theta/np.pi*180.0

                theta_crack=np.arccos(q[0])
                if q[1]<0:
                    theta_crack=-theta_crack

                for mode in range(1,3):
                    s_aux,e_aux,u_x_aux=K_field(r,theta,kapa,G,1,mode)
                    s_aux,e_aux,u_x_aux=rotate_tensor(theta_crack,s_aux,e_aux,u_x_aux)
                    w=sum(s*e_aux)                                        # strain energy
                    W=w*np.identity(2)
                    H=W-np.dot(np.array([ [s[0],s[2]] , [s[2],s[1]] ]),u_x_aux)- \
                                        np.dot(np.array([ [s_aux[0],s_aux[2]] , [s_aux[2],s_aux[1]] ]),u_x)
                    M_e[mode-1]=M_e[mode-1]-np.tensordot(H,q_x.T,axes=2)*detJ*weight[i]  

                # s_aux,e_aux,u_x_aux=K_field(r,theta,kapa,G,1,1)
                # s_aux,e_aux,u_x_aux=rotate_tensor(theta_crack,s_aux,e_aux,u_x_aux)
                # w=sum(s*e_aux)
                # term1_1=[-w,s[0]*u_x_aux[0,0],s[2]*u_x_aux[1,0],s_aux[0]*u_x[0,0],s_aux[2]*u_x[1,0]]
                # term1_2=[s[2]*u_x_aux[0,0],s[1]*u_x_aux[1,0],s_aux[2]*u_x[0,0],s_aux[1]*u_x[1,0]]
                # M_e[0]=M_e[0] \
                #             + ((-w+s[0]*u_x_aux[0,0]+s[2]*u_x_aux[1,0]+s_aux[0]*u_x[0,0]+s_aux[2]*u_x[1,0])*q_x[0,0] \
                #             + (s[2]*u_x_aux[0,0]+s[1]*u_x_aux[1,0]+s_aux[2]*u_x[0,0]+s_aux[1]*u_x[1,0])*q_x[0,1])*detJ*weight[i]
                # s_aux,e_aux,u_x_aux=K_field(r,theta,kapa,G,1,2)
                # w=sum(s*e_aux)  
                # M_e[1]=M_e[1] \
                #             + ((-w+s[0]*u_x_aux[0,0]+s[2]*u_x_aux[1,0]+s_aux[0]*u_x[0,0]+s_aux[2]*u_x[1,0])*q_x[0,0] \
                #             + (s[2]*u_x_aux[0,0]+s[1]*u_x_aux[1,0]+s_aux[2]*u_x[0,0]+s_aux[1]*u_x[1,0])*q_x[0,1])*detJ*weight[i] 
                
                
                

    if anaType=='J':    
        return J_e  
    elif anaType=='M':
        if (eleType=='CPS4')or(eleType=='CPS8')or(eleType=='CPS8R'):
            alpha=1.0/E
        M_e=M_e/2.0/alpha
        return M_e
    
            
def calIntegral(u,e,s,q,contour_ele,contour_node,eleCon,nodePos,crackTip,ncont,eleType,anaType):
    global DEBUG,fdbug
    J=[]
    K=np.zeros(3)
    J=0
    # Loop on each contour
    i=ncont-1
        
    # DEBUG: signal which contour is under processing
    if DEBUG:
        print("\nContour %d"%i)
        
    # Loop on each element, to calculate their contribution to J integral 
    for ele in contour_ele[i]:
        # Initialization
        u_e=[]      # displacement of nodes of an element
        q_e=[]      # virtual crack extension direction of nodes of an element
        x_e=[]      # position of nodes of an element
        
        # DEBUG: examine the element and its connectivity
        if DEBUG:
            if eleType=='CPS4':
                print('ele: %d, %d %d %d %d'%(ele,eleCon[ele][0],eleCon[ele][1],eleCon[ele][2],eleCon[ele][3]))
            elif (eleType=='C3D8')or(eleType=='CPS8')or(eleType=='CPS8R'):
                print('ele: %d, %d %d %d %d %d %d %d %d'%(ele,eleCon[ele][0],eleCon[ele][1],eleCon[ele][2],eleCon[ele][3], \
                                                              eleCon[ele][4],eleCon[ele][5],eleCon[ele][6],eleCon[ele][7]))
        # Loop on nodes of an element
        for j in range(0,len(eleCon[ele])):
            node=eleCon[ele][j]
            u_e.append(np.double(u[node]))
            x_e.append(np.double(nodePos[node]))
            
            # Define the virtual crack extension direction
            # 1. for nodes on the outer boundary of a contour
            if node in contour_node[i]:
                # q_e.append(0)
                if (eleType=='CPS4')or(eleType=='CPS8')or(eleType=='CPS8R'):
                    q_e.append(np.array([0,0]))
                elif eleType=='C3D8':
                    q_e.append(np.array([0,0,0]))
            # 2. for nodes on the inner boundary of a contour, 
            #    which is the outer bouddary of the previous contour.         
            elif node in contour_node[i-1]:
                if (eleType=='CPS4')or(eleType=='CPS8')or(eleType=='CPS8R'):
                    q_e.append(q[0:2])
                elif eleType=='C3D8':
                    if abs(nodePos[node][2]-0.5)<1e-4:      # as a temporary method to set q vector for 3D case
                        q_e.append(q)
                    else:
                        q_e.append(np.array([0,0,0]))
            # 3. for mid-nodes of quadratic elements, they are assigned a value
            #    interpolated between the two corner nodes
            else:
                if (eleType=='CPS8')or(eleType=='CPS8R'):
                    # specify the correlated corner nodes
                    if j==4:
                        k1=0
                        k2=1
                    elif j==5:
                        k1=1
                        k2=2
                    elif j==6:
                        k1=2
                        k2=3
                    elif j==7:
                        k1=3
                        k2=0
                    # check if the corner nodes are on the outer boundary (OB)
                    #   of the contour, set the position of the node on the
                    #   on as x1, and the position of the node not on the
                    #   OB as x2.
                    if (eleCon[ele][k1] in contour_node[i])and \
                       (not(eleCon[ele][k2] in contour_node[i])):
                        x1=x_e[k1]
                        x2=x_e[k2]
                    elif (eleCon[ele][k2] in contour_node[i])and \
                       (not(eleCon[ele][k1] in contour_node[i])):
                        x1=x_e[k2]
                        x2=x_e[k1]
                    # for mid nodes of the first contour at the crack tip
                    elif  not ((eleCon[ele][k1] in contour_node[i])and \
                               (eleCon[ele][k2] in contour_node[i])):
                        x1=x_e[k1]
                        x2=x_e[j]
                    else:
                        print('ERROR: q value on mid-side node')
                    
                    # interpolate the virtual crack extension direction for
                    #   for the mid node according to related conrner nodes
                    if np.sqrt( np.sum( np.power((x2-x1),2) ) )>0:
                        ratio=np.sqrt( np.sum( np.power((x_e[j]-x1),2) ) )/np.sqrt( np.sum( np.power((x2-x1),2) ) )
                    else:
                        ratio=1
                    q_e.append(q[0:2]*ratio)
                    
        # Calculate the contribution of a element to the J integral       
        if anaType=='J':
            J_e=ele_Integral(x_e,u_e,q_e,e[ele],s[ele],crackTip,q,eleType,anaType)
            J=J+J_e
        elif anaType=='M':
            K_e=ele_Integral(x_e,u_e,q_e,e[ele],s[ele],crackTip,q,eleType,anaType)
            K=K+K_e
                
        # DEBUG: examine the contribution of a element to the J integral
        if DEBUG:
            print("%f"%J_e) 
            
            
    if anaType=='J':        
        return J
    elif anaType=='M':
        return K

def calPropagation(K,crit):
    K1=K[0]
    K2=K[1]
    if crit=='MTS':
        theta=np.arccos( (3.0*K2**2+np.sqrt(K1**4+8.0*(K1**2)*(K2**2))) / ((K1**2)+9.0*(K2**2)))
        if K2>0:
            theta=-theta
    return theta

def calDirection(path,filename):
    anaType='M'
    DEBUG=False
    u,e,s,contour_ele,contour_node,eleCon,nodePos,eleType,crackTip,q=readData(path,filename+'.pkl') 
    ncont=3  # the number of contour to claculate the K
    K=calIntegral(u,e,s,q,contour_ele,contour_node,eleCon,nodePos,crackTip,ncont,eleType,anaType)
    theta=calPropagation(K,'MTS')
    
    return theta,K
#----------------------------------------------------------------------
def insertCrack(crack,head_end,radius,index,path,mdb,mdbName,modelName,instanceName):
    a = mdb.models[modelName].rootAssembly 
    ins=a.instances[instanceName]
    f = ins.faces
    t = a.MakeSketchTransform(sketchPlane=f[0],  sketchPlaneSide=SIDE1,origin=(0.0, 0.0, 0.0))
    s = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
    sheetSize=82.46, gridSpacing=2.06, transform=t)
    # crack=getCrack()
    
    # Partition of the crack tip face
    nSeg=len(crack)-1
    for i in range(0,nSeg):
        s.Line(point1=crack[i], point2=crack[i+1])
    if head_end[0]:
        if (crack[0][0]-crack[1][0])<0:
            s.CircleByCenterPerimeter(center=crack[0], point1=(crack[0][0]-radius, crack[0][1]))
        else:
            s.CircleByCenterPerimeter(center=crack[0], point1=(crack[0][0]+radius, crack[0][1]))
    if head_end[1]:
        if (crack[-1][0]-crack[-2][0])<0:
            s.CircleByCenterPerimeter(center=crack[nSeg], point1=(crack[nSeg][0]-radius, crack[nSeg][1]))
        else:
            s.CircleByCenterPerimeter(center=crack[nSeg], point1=(crack[nSeg][0]+radius, crack[nSeg][1]))

    a.PartitionFaceBySketch(faces=f, sketch=s)
    del mdb.models[modelName].sketches['__profile__']  
        
    f = ins.faces
    
    # Define seam
    e = ins.edges
    seam=[]
    midPoint=[]
    for i in range(0,nSeg):
        xy=(crack[i]+crack[i+1])/2.0
        xy=np.append(xy,[0.0,]) 
        midPoint.append(xy)
    # seam at the head of crack, which is partitioned
    if  head_end[0]:   
        xy=crack[0]+(crack[1]-crack[0])*0.001
        xy=np.append(xy,[0.0,])
        midPoint.append(xy)
    
        xy=crack[1]-(crack[1]-crack[0])*0.001
        xy=np.append(xy,[0.0,])
        midPoint.append(xy)
    # seam at the end of crack, which is partitioned
    if  head_end[1]:   
        xy=crack[nSeg-1]+(crack[nSeg]-crack[nSeg-1])*0.001
        xy=np.append(xy,[0.0,])
        midPoint.append(xy)
    
        xy=crack[nSeg]-(crack[nSeg]-crack[nSeg-1])*0.001
        xy=np.append(xy,[0.0,])
        midPoint.append(xy)
     
    
    seam=e.findAt(coordinates=midPoint)
    seamSet = a.Set(edges=seam, name='SEAM-%d'%(index))
    mdb.models[modelName].rootAssembly.engineeringFeatures.assignSeam(regions=seamSet)
    
    # Define crack
    v=ins.vertices
    # seam at the head of crack, which is partitioned        
    if  head_end[0]:     
        xyfront=np.append(crack[0],[0.0,])
        vc=v.findAt(coordinates=[xyfront,])
        a.Set(vertices=vc, name='front-%d-1'%(index))
        crackFront = regionToolset.Region(vertices=vc)
        crackTip = regionToolset.Region(vertices=vc)
    
        xy2=np.append(crack[1],[0.0,])
        a.engineeringFeatures.ContourIntegral(name='Crack-%d-1'%(index), symmetric=OFF, 
            crackFront=crackFront, crackTip=crackTip, 
            extensionDirectionMethod=Q_VECTORS, qVectors=((xy2, xyfront), ), 
            midNodePosition=0.25, collapsedElementAtTip=SINGLE_NODE)    
    # seam at the end of crack, which is partitioned        
    if  head_end[1]:     
        xyfront=np.append(crack[nSeg],[0.0,])
        vc=v.findAt(coordinates=[xyfront,])
        a.Set(vertices=vc, name='front-%d-2'%(index))
        crackFront = regionToolset.Region(vertices=vc)
        crackTip = regionToolset.Region(vertices=vc)
    
        xy2=np.append(crack[nSeg-1],[0.0,])
        a.engineeringFeatures.ContourIntegral(name='Crack-%d-2'%(index), symmetric=OFF, 
            crackFront=crackFront, crackTip=crackTip, 
            extensionDirectionMethod=Q_VECTORS, qVectors=((xy2, xyfront), ), 
            midNodePosition=0.25, collapsedElementAtTip=SINGLE_NODE)    
    
    # Mesh
    # the seam should be seeded earlier than the radius, since the seam includes the radius
    
    # seed the seam    
    a.seedEdgeBySize(edges=seam, size=0.04, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FREE) 
    

    # seed the head of the seam        
    if  head_end[0]:  
        # seed the radius
        xy=np.append(crack[0],[0.0,])
        e1=e.findAt(coordinates=[xy,])
        vertice=e1[0].getVertices()
        v1=np.array(v[vertice[0]].pointOn)
        v2=np.array(v[vertice[1]].pointOn)
        box=e1.getBoundingBox()
        e1=e.getByBoundingBox(xMin=box['low'][0],xMax=box['high'][0],
                              yMin=box['low'][1],yMax=box['high'][1])
        if sum((xy-v1)**2)<sum((xy-v2)**2):
            a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=e1, ratio=4.0, 
                             number=6, constraint=FREE)
        else:
            a.seedEdgeByBias(biasMethod=SINGLE, end2Edges=e1, ratio=4.0, 
                             number=6, constraint=FREE)            
            
        # seed the circumference
        xy=np.append(crack[0],[0.0,])
        xy[1]=xy[1]+radius
        e1=e.findAt(coordinates=[xy,])
        a.seedEdgeBySize(edges=e1, size=2*radius*np.pi/24, deviationFactor=0.1, 
            minSizeFactor=0.1, constraint=FREE)   
        xy[1]=xy[1]-2*radius
        e1=e.findAt(coordinates=[xy,])
        a.seedEdgeBySize(edges=e1, size=2*radius*np.pi/24, deviationFactor=0.1, 
            minSizeFactor=0.1, constraint=FREE)   
        
        xyfront=np.append(crack[0],[0.0,])
        f = a.instances['Part-1-1'].faces
        core=f.findAt(coordinates=[xyfront,])
        #a.setMeshControls(regions=core, technique=SWEEP) #,algorithm=MEDIAL_AXIS
    

    # seed the end of the seam         
    if  head_end[1]:  
        xy=np.append(crack[nSeg],[0.0,])
        e1=e.findAt(coordinates=[xy,])
        vertice=e1[0].getVertices()
        v1=np.array(v[vertice[0]].pointOn)
        v2=np.array(v[vertice[1]].pointOn)
        box=e1.getBoundingBox()
        e1=e.getByBoundingBox(xMin=box['low'][0],xMax=box['high'][0],
                              yMin=box['low'][1],yMax=box['high'][1])
        if sum((xy-v1)**2)<sum((xy-v2)**2):
            a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=e1, ratio=4.0, 
                number=6, constraint=FREE)
        else:
            a.seedEdgeByBias(biasMethod=SINGLE, end2Edges=e1, ratio=4.0, 
                number=6, constraint=FREE)            
        # seed the circumference
        xy=np.append(crack[nSeg],[0.0,])
        xy[1]=xy[1]+radius
        e1=e.findAt(coordinates=[xy,])
        a.seedEdgeBySize(edges=e1, size=2*radius*np.pi/24, deviationFactor=0.1, 
            minSizeFactor=0.1, constraint=FREE)   
        xy[1]=xy[1]-2*radius
        e1=e.findAt(coordinates=[xy,])
        a.seedEdgeBySize(edges=e1, size=2*radius*np.pi/24, deviationFactor=0.1, 
            minSizeFactor=0.1, constraint=FREE)   
        
        xyfront=np.append(crack[nSeg],[0.0,])
        f = a.instances['Part-1-1'].faces
        core=f.findAt(coordinates=[xyfront,])
        #a.setMeshControls(regions=core, technique=SWEEP) #,algorithm=MEDIAL_AXIS

def meshing(mdb,mdbName,modelName,instanceName,crack_array):
    a = mdb.models[modelName].rootAssembly 
    ins=a.instances[instanceName]    
    f = ins.faces
    partInstances =(ins, )
    # a.seedPartInstance(regions=partInstances, size=0.1, deviationFactor=0.1, 
    #     minSizeFactor=0.1, constraint=FREE)
    a.setMeshControls(regions=f, elemShape=TRI)
    for crack in crack_array:
        if crack.head_end[0]:
            core=f.findAt( coordinates=[np.append(crack.path[0],[0.0,]),] )
            a.setMeshControls(regions=core, elemShape=QUAD_DOMINATED, technique=SWEEP)
        if crack.head_end[1]:
            core=f.findAt( coordinates=[np.append(crack.path[-1],[0.0,]),] )
            a.setMeshControls(regions=core, elemShape=QUAD_DOMINATED, technique=SWEEP)
    a.generateMesh(regions=partInstances)
    # specify element type
    elemType1 = mesh.ElemType(elemCode=CPE8, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=CPE6, elemLibrary=STANDARD)    
    a.setElementType(regions=(f,), elemTypes=(elemType1, elemType2))

def eleSet(mdb,mdbName,modelName,instanceName,crack,radius,index,head_end):
    a = mdb.models[modelName].rootAssembly 
    ins=a.instances[instanceName]     
    # Element Set
    if  head_end[0]:     
        core_ele=ins.elements.getByBoundingCylinder(center1=(crack[0][0],crack[0][1],-1.0),\
                                               center2=(crack[0][0],crack[0][1],1.0),
                                               radius=radius+1e-6) # the radius is slightly larger to include all potential objects
        a.Set(name='COREELE-%d-1'%(index),elements=core_ele)
        # Node set
        core_node=ins.nodes.getByBoundingCylinder(center1=(crack[0][0],crack[0][1],-1.0),\
                                               center2=(crack[0][0],crack[0][1],1.0),
                                               radius=radius+1e-6) # the radius is slightly larger to include all potential objects
        a.Set(name='CORENODE-%d-1'%(index),elements=core_node)    
    if  head_end[1]:     
        core_ele=ins.elements.getByBoundingCylinder(center1=(crack[-1][0],crack[-1][1],-1.0),\
                                               center2=(crack[-1][0],crack[-1][1],1.0),
                                               radius=radius+1e-6) # the radius is slightly larger to include all potential objects
        a.Set(name='COREELE-%d-2'%(index),elements=core_ele)
        # Node set
        core_node=ins.nodes.getByBoundingCylinder(center1=(crack[-1][0],crack[-1][1],-1.0),\
                                               center2=(crack[-1][0],crack[-1][1],1.0),
                                               radius=radius+1e-6) # the radius is slightly larger to include all potential objects
        a.Set(name='CORENODE-%d-2'%(index),elements=core_node)
    
def histroyOutput(mdb,mdbName,modelName,index,head_end):    
    # Output
    if  head_end[0]:
        mdb.models[modelName].HistoryOutputRequest(name='H-Output-%d-1'%(index), 
            createStepName='Step-1', contourIntegral='Crack-%d-1'%(index), 
            sectionPoints=DEFAULT, rebar=EXCLUDE, numberOfContours=6)
        mdb.models[modelName].HistoryOutputRequest(name='H-Output-%d-2'%(index), 
            createStepName='Step-1', contourIntegral='Crack-%d-1'%(index), 
            sectionPoints=DEFAULT, rebar=EXCLUDE, numberOfContours=6, 
            contourType=K_FACTORS)  
    if  head_end[1]:
        mdb.models[modelName].HistoryOutputRequest(name='H-Output-%d-3'%(index), 
            createStepName='Step-1', contourIntegral='Crack-%d-2'%(index), 
            sectionPoints=DEFAULT, rebar=EXCLUDE, numberOfContours=6)
        mdb.models[modelName].HistoryOutputRequest(name='H-Output-%d-4'%(index), 
            createStepName='Step-1', contourIntegral='Crack-%d-2'%(index), 
            sectionPoints=DEFAULT, rebar=EXCLUDE, numberOfContours=6, 
            contourType=K_FACTORS)  
        
def jobExecution(path,modelName):
    log=open(path+'log.txt','a')
    mdb.Job(name=modelName, model=modelName, description='', 
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=FULL, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4,numDomains=4,
        numGPUs=0)       
    mdb.jobs[modelName].submit(consistencyChecking=OFF)
    mdb.jobs[modelName].waitForCompletion() 
    log.write(modelName+': '+str(mdb.jobs[modelName].status)+'\n')
    log.close()

def output_contour(odb,crack,contour_ele,head_end,index,path,filename):
    
    insName="PART-1-1"
    stepName="Step-1"
    variables_node=['U',]
    variables_ele=['E','S']
    frame=1
    ins=odb.rootAssembly.instances[insName]
    ele=ins.elements

    if head_end[0]:
        crackTip=crack[0]
        mapEle,eleCon,nodeList,contour_node,elementType=createEleMap(ele,contour_ele[0])
        nodePos,crackTipNode=extractNodePosition(odb,insName,nodeList,crackTip)
        contour_node.append(crackTipNode)       # append the crack tip nodes to the end of contour_node 
        data,nodeLabel=extractNodeFieldOutput(odb,stepName,frame,nodeList,variables_node)
        u=data['U']
        eleList=[eleLabel for contour in contour_ele[0] for eleLabel in contour ] 
        data=extractEleFieldOutput(odb,stepName,frame,eleList,variables_ele)
        e=data['E']
        s=data['S']
        q=np.array(crack[0]-crack[1])
        q=q/sqrt(sum(q*q))
    
        f1=open(path+filename+'-%d-1.pkl'%(index),'wb')
        pickle.dump(u,f1)
        pickle.dump(e,f1)
        pickle.dump(s,f1)
        pickle.dump(contour_ele[0],f1)
        pickle.dump(contour_node,f1)
        pickle.dump(eleCon,f1)
        pickle.dump(nodePos,f1)
        pickle.dump(elementType,f1)
        pickle.dump(crackTip,f1)
        pickle.dump(q,f1)
        f1.close()
    
    if head_end[1]:
        crackTip=crack[-1]
        mapEle,eleCon,nodeList,contour_node,elementType=createEleMap(ele,contour_ele[1])
        nodePos,crackTipNode=extractNodePosition(odb,insName,nodeList,crackTip)
        contour_node.append(crackTipNode)       # append the crack tip nodes to the end of contour_node 
        data,nodeLabel=extractNodeFieldOutput(odb,stepName,frame,nodeList,variables_node)
        u=data['U']
        eleList=[eleLabel for contour in contour_ele[1] for eleLabel in contour ] 
        data=extractEleFieldOutput(odb,stepName,frame,eleList,variables_ele)
        e=data['E']
        s=data['S']
        q=np.array(crack[-1]-crack[-2])
        q=q/sqrt(sum(q*q))
    
        f1=open(path+filename+'-%d-2.pkl'%(index),'wb')
        pickle.dump(u,f1)
        pickle.dump(e,f1)
        pickle.dump(s,f1)
        pickle.dump(contour_ele[1],f1)
        pickle.dump(contour_node,f1)
        pickle.dump(eleCon,f1)
        pickle.dump(nodePos,f1)
        pickle.dump(elementType,f1)
        pickle.dump(crackTip,f1)
        pickle.dump(q,f1)
        f1.close()
  
    
def direction(crack,head_end,index,increment,contour_ele,path,modelName,mode):
    odb=session.openOdb(name=path+modelName+'.odb')
    output_contour(odb,crack,contour_ele,head_end,index,path,modelName)
    dangle=np.array([np.nan,np.nan])   
    angle1=np.array([np.nan,np.nan]) 
    K=np.array([np.nan,np.nan,np.nan,np.nan]) # head_K1, head_K2, end_K1, end_K2
    if mode=='abaqus':
        h=odb.steps['Step-1'].historyRegions['ElementSet  ALL ELEMENTS'].historyOutputs
        for key in h.keys():
            if (key[0:3]=='Cpd')and(key[-1]=='3')and('CRACK-%d-1'%(index) in key):
                dangle[0]=h[key].data[0][1]/180.0*np.pi
            elif (key[0:3]=='Cpd')and(key[-1]=='3')and('CRACK-%d-2'%(index) in key):
                dangle[1]=h[key].data[0][1]/180.0*np.pi
            elif (key[0:2]=='K1')and(key[-1]=='3')and('CRACK-%d-1'%(index) in key):
                K[0]=h[key].data[0][1]  
            elif (key[0:2]=='K2')and(key[-1]=='3')and('CRACK-%d-1'%(index) in key):
                K[1]=h[key].data[0][1]
            elif (key[0:2]=='K1')and(key[-1]=='3')and('CRACK-%d-2'%(index) in key):
                K[2]=h[key].data[0][1]
            elif (key[0:2]=='K2')and(key[-1]=='3')and('CRACK-%d-2'%(index) in key):
                K[3]=h[key].data[0][1]
    elif mode=='user':
        if head_end[0]:
            dangle[0],tmp=calDirection(path,modelName+'-%d-1'%(index))
            K[0]=tmp[0]
            K[1]=tmp[1]
        if head_end[1]:
            dangle[1],tmp=calDirection(path,modelName+'-%d-2'%(index))
            K[2]=tmp[0]
            K[3]=tmp[1]
        
    n=len(crack)
    if head_end[0]:
        angle0=np.arctan((crack[0][1]-crack[1][1])/(crack[0][0]-crack[1][0]))
        if (crack[0][0]-crack[1][0])<0:
            if not ((crack[0][1]-crack[1][1])==0):
                angle0=angle0+np.pi*np.sign((crack[0][1]-crack[1][1]))
            else:
                angle0=np.pi
        angle1[0]=angle0+dangle[0]
        x1=crack[0][0]+increment*np.cos(angle1[0])
        y1=crack[0][1]+increment*np.sin(angle1[0])
    if head_end[1]:
        angle0=np.arctan((crack[n-1][1]-crack[n-2][1])/(crack[n-1][0]-crack[n-2][0]))
        if (crack[n-1][0]-crack[n-2][0])<0:
            if not ((crack[n-1][1]-crack[n-2][1])==0):
                angle0=angle0+np.pi*np.sign((crack[n-1][1]-crack[n-2][1]))  
            else:
                angle0=np.pi
        angle1[1]=angle0+dangle[1]
        x2=crack[n-1][0]+increment*np.cos(angle1[1])
        y2=crack[n-1][1]+increment*np.sin(angle1[1])
        
    crack_list=crack.tolist()
    if head_end[0]:
        crack_list=[[x1,y1],]+crack_list
    if head_end[1]:
        crack_list=crack_list+[[x2,y2],]
    crack=np.array(crack_list)
    odb.close()
    
    return crack,dangle,angle1,K
    
def findContourEle(crackTip,sets,path,modelName):
    # zza:Quite strange that the node labels does not match the connectivity of element in the mdb. so we used odb to solve the problems.
    odb=session.openOdb(name=path+modelName+'.odb')
    a=odb.rootAssembly
    core_eles=a.elementSets[sets[0]].elements[0]
    core_nodes=a.nodeSets[sets[1]].nodes[0]
    thre=1e-6
    node_check=[]     # nodes for checking if the element is with in the contour 
    ele_record=[]     # record the index in the core_eles   
    for node in core_nodes:
        dist=sum(np.sqrt((np.array(node.coordinates[0:2])-crackTip)**2))
        if dist<thre:
            node_check.append(node.label)
    contour_ele=[]
    contour_eleid=[]
    ncontour=1
    flag=1
    #while (flag):
    for ncontour in range(1,4):
        contour_ele.append([])
        contour_eleid.append([])
        for i in range(0,len(core_eles)):
            if (not i in ele_record):
                ele=core_eles[i]
                for nlabel in ele.connectivity:
                    if (nlabel in node_check):  
                      contour_ele[ncontour-1].append(ele.label)
                      contour_eleid[ncontour-1].append(i)
                      ele_record.append(i)
                      break
        nrecord=len(contour_ele[ncontour-1])  # number of element recorded in current contour
        if nrecord>0:
            flag=1
            # record down the node in the contour
            node_check=[] 
            for i in range(0,nrecord):
                for j in core_eles[contour_eleid[ncontour-1][i]].connectivity:
                    if not(j in node_check):
                        node_check.append(j)     
        # else:
        #     flag=0
        #     contour_ele.pop()
        #     ncontour=ncontour-1
            
    return contour_ele

def cal_life(K,increment,C,n,KIc,R):
    C1=1/C  
    n1=0-n
    time=0
    uc=sqrt(1000)
    L=increment/1000
    nstep=len(K)
    for i in range(0,nstep):
        K[i][2]=K[i][2]/uc
    for i in range(0,nstep-2):
        time=L*C1/(n1+1)/(K[i+1][2]*(1-R)-K[i][2]*(1-R))*(math.pow(K[i+1][2]*(1-R),n1+1)-math.pow(K[i][2]*(1-R),n1+1))+time
    L2=(KIc-K[nstep-2][2])/(K[nstep-1][2]-K[nstep-2][2])*L
    time=time+L2*C1/(n1+1)/(KIc*(1-R)-K[i][2]*(1-R))*(math.pow(KIc*(1-R),n1+1)-math.pow(K[i][2]*(1-R),n1+1))
    
    return time
        
def autocrack(path,mdbName,modelName0,instanceName,crack,increment,KIc,Kth,C,n,R):
    crackPath1=np.array(crack)
    mdb=openMdb(path+mdbName)
    head_end=[0,1]
    crack_array=[Crack(crackPath1,[0,1],1),]
    solver='abaqus'
    radius=increment*0.5
    
    nCrack=len(crack_array)
    angle=[]
    dangle=[]
    K=[]
    K1=0
    uc=sqrt(1000)     #unit convert for stress intensity factor
    log=open(path+'log.txt','w')
    
    #fdbug=open(path+'debug.txt','w')
    i=0
    while (K1<KIc) and ( (i==0) or (K1*(1-R)>Kth)):
        if i<10:
            serial='00'+str(i)
        elif (i>=10)and(i<100):
            serial='0'+str(i)
        else:
            serial=str(i)
        # output the crack path
        clog=open(path+'crack.txt','w')
        clog.write('\nStep-%d\n'%(i))
        for crack in crack_array:
            clog.write('Crack-%d\n'%(crack.index))
            for j in range(0,len(crack.path)):
                for k in range(0,2):
                    clog.write('%32.16f, '%(crack.path[j][k]))
                clog.write('\n')    
        clog.close()
        
        modelName=modelName0+'_'+serial
        mdb.Model(name=modelName, objectToCopy=mdb.models[modelName0])
        log=open(path+'log.txt','a')
        log.write('step'+serial+' inserCrack\n')
        log.close()
        for j in range(0,nCrack):
            insertCrack(crack_array[j].path,crack_array[j].head_end,radius,crack_array[j].index,path,mdb,mdbName,modelName,instanceName)   
        meshing(mdb,mdbName,modelName,instanceName,crack_array)
        for j in range(0,nCrack):
            eleSet(mdb,mdbName,modelName,instanceName,crack_array[j].path,radius,crack_array[j].index,crack_array[j].head_end)
            histroyOutput(mdb,mdbName,modelName,crack_array[j].index,crack_array[j].head_end)
            
    
        
        log=open(path+'log.txt','a')
        log.write('step'+serial+' jobExecution\n')
        log.close()
        jobExecution(path,modelName)
        
        # build a list for contour element
        # f1=open(path+modelName+'_contour_ele.pkl','wb')
        # pickle.dump(head_end,f1)
        for crack in crack_array:
            crack.contour_ele[0]=[]
            crack.contour_ele[1]=[]
            if crack.head_end[0]:
                crack.contour_ele[0]=findContourEle(crack.path[0],['COREELE-%d-1'%(crack.index),'CORENODE-%d-1'%(crack.index)],path,modelName)
            if crack.head_end[1]:
                crack.contour_ele[1]=findContourEle(crack.path[-1],['COREELE-%d-2'%(crack.index),'CORENODE-%d-2'%(crack.index)],path,modelName)
        # pickle.dump(contour_ele1,f1)
        # pickle.dump(contour_ele2,f1)
        # f1.close()
        log=open(path+'log.txt','a')
        log.write('step'+serial+' direction\n')    
        log.close()
        # calculate the stress intensity and propagation direction
        for crack in crack_array:
            crack.path,da_tmp,a_tmp,K_tmp=direction(crack.path,crack.head_end,crack.index,increment,crack.contour_ele,path,modelName,solver)
        angle.append(a_tmp)
        dangle.append(da_tmp)
        K.append(K_tmp)
        alog=open(path+'result.txt','w')
        alog.write('\nStep-%d\n'%(i)) 
        alog.write('K1\n') 
        for j in range(0,len(angle)):
            alog.write('%32.16f\n' %(K[j][2])) 
    
        alog.close()
        i=i+1
        K1=K[j][2]/uc   # unit convert to MPa*(m)^(1/2)
        
    life=cal_life(K,increment,C,n,KIc,R)
    alog=open(path+'result.txt','a')
    alog.write('\nLife = %32.16f cycles' %(life)) 
    
global DEBUG,fdbug
DEBUG=False

##### INPUT #####
## 1. Path
path='D:/'
mdbName='Crack.cae'
modelName='Edge_crack'
instanceName='Part-1-1'

## 2. Crack
crack=[[-1,0],[-0.8,0]]
increment=0.1

## 3. Material properties
KIc=14
Kth=5
C=1e-11
n=3.2

## 4. Load
R=0.1

##### INPUT END #####

autocrack(path,mdbName,modelName,instanceName,crack,increment,KIc,Kth,C,n,R)
