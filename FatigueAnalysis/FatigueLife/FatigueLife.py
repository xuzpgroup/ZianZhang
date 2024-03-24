from odbAccess import *
from numpy import linalg as la
import numpy as np
import math

def multixialCriter(criterion,stress,strain,scale,R):
    if criterion=='Max. Principal':
        sigma_ar=maxPrincipal(stress,scale,R)
    elif criterion=='Mises':
        sigma_ar=Mises(stress,scale,R)
    elif criterion=='Sines':
        sigma_ar=Sines(stress,scale,R)
    elif criterion=='Crossland':
        sigma_ar=Crossland(stress,scale,R)
    elif criterion=='Matake':
        sigma_ar=Matake(stress,scale,R)
    return sigma_ar

def meanStress(criterion,sigma_a,sigma_m):
    if criterion=='Goodman':
        sigma_ar=sigma_a/(1-sigma_m/sigma_u)
    return sigma_ar

def maxPrincipal(stress,scale,R):
    if stress.maxPrincipal>0:
        sigma_max=stress.maxPrincipal*scale
        sigma_min=sigma_max*R
    else:
        sigma_min=stress.maxPrincipal*scale
        sigma_max=sigma_min*R
    sigma_m=(sigma_max+sigma_min)/2
    sigma_a=(sigma_max-sigma_min)/2
    sigma_ar=meanStress(f_meanstress,sigma_a,sigma_m)
    return sigma_ar

def Mises(stress,scale,R):
    sigma_max=stress.mises*scale
    sigma_min=sigma_max*R    
    sigma_m=(sigma_max+sigma_min)/2
    sigma_a=(sigma_max-sigma_min)/2
    sigma_ar=meanStress(f_meanstress,sigma_a,sigma_m)
    return sigma_ar


def Sines(stress,scale,R):
    sigma_max=stress.mises*scale
    sigma_min=sigma_max*R
    sigma_a=(sigma_max-sigma_min)/2 
    sigma_m=(stress.data[0]+stress.data[1]+stress.data[2])*scale*(1+R)/2
    sigma_ar=meanStress(f_meanstress,sigma_a,sigma_m)
    #sigma_ar=sigma_a+0.5/np.sqrt(2)*sigma_m
    return sigma_ar

def Crossland(stress,scale,R):

    alpha=np.sqrt(27)*(tau_w/sigma_w)-3
    sigma_max=stress.mises*scale
    sigma_min=sigma_max*R
    sigma_a=(sigma_max-sigma_min)/2 
    sigma_ar=(sigma_a+alpha/3*(stress.data[0]+stress.data[1]+stress.data[2])*scale)/(1+alpha/3)
    return sigma_ar

def Matake(stress,scale,R):

    alpha=sigma_w/tau_w
    tmp1=stress.data*scale
    w,v=np.linalg.eig([[tmp1[0],tmp1[3],tmp1[4]],\
                        [tmp1[3],tmp1[1],tmp1[5]],\
                        [tmp1[4],tmp1[5],tmp1[2]]])
    for i in range(0,3):
        for j in range(i+1,3):
            if w[i]<w[j]:
                tmp2=w[i]
                w[i]=w[j]
                w[j]=tmp2
                for k in range(0,3):
                    tmp3=v[k,i]
                    v[k,i]=v[k,j]
                    v[k,j]=tmp3
    t_max=(w[0]-w[2])/2
    t_min=t_max*R
    t_a=(t_max-t_min)/2
    n=(v[:,0]+v[:,2])/np.sqrt(2)
    n=np.mat(n)
    sigma=np.mat([[tmp1[0],tmp1[3],tmp1[4]],\
		[tmp1[3],tmp1[1],tmp1[5]],\
		[tmp1[4],tmp1[5],tmp1[2]]])
    sigma_n_max=n*sigma*n.T
    sigma_ar=alpha*t_a+(2-alpha)*sigma_n_max
    return sigma_ar

def cal_life(odb_path,output_path,step_name,frame_num,sigma_u,sigma_f,b_power,scale,R,f_multiaxial,f_meanstress):
    max_sigma_ar=0
    max_num=0
    odb=openOdb(odb_path)
    strain=odb.steps[step_name].frames[frame_num].fieldOutputs['E'].values
    stress=odb.steps[step_name].frames[frame_num].fieldOutputs['S'].values
    life=odb.steps[step_name].frames[frame_num].FieldOutput(name='log_life',description='Life',type=SCALAR)
    
    for i in range(0,len(stress),1):
            l=[]
            for j in range(0,1):
                #print('i: %d  j:%d'%(i,j))
                sigma_ar=multixialCriter(f_multiaxial,stress[i+j],strain[i+j],scale,R)
                if sigma_ar>max_sigma_ar:
                    max_sigma_ar=sigma_ar
                    max_num=i+j
                #print(sigma_ar)
                l.append(math.log10(math.pow(sigma_ar/sigma_f,1/b_power)))
            life.addData(position = stress[i].position,\
                          instance = stress[i].instance,\
                          labels   = [stress[i].elementLabel],\
                          data     = [[l[0]],]) #[l[1]],[l[2]],[l[3]],[l[4]],[l[5]],[l[6]],[l[7]]
    odb.save()
    
    life=math.pow(max_sigma_ar/sigma_f,1/b_power)
    
    output=file(output_path,'w')
    output.write('Multiaxial Criterion: %s\n'%(f_multiaxial))     
    output.write('Mean Stress Criterion: %s\n'%(f_meanstress)) 
    output.write('elemantLabel: %d\n'%(stress[max_num].elementLabel))
    output.write('integrationPoint: %d\n'%(stress[max_num].integrationPoint))
    output.write('sigma_ea: %6.2f MPa\n'%(max_sigma_ar))
    output.write('life: %12.2f cycles\n\n'%(life))
    
    output.close()
    odb.close()
    
    
########## INPUT ##########
## 1. Path
odb_path='D:/FatigueLife.odb'
output_path='D:/life.txt'
step_name='Step-1'
frame_num= 1

## 2. Fatigue criteria
f_multiaxial='Matake'  # Max. Principal; Sines; Mises; Crossland; Matake

## 3. Material properties
sigma_f=15877.8
b_power=-0.2572

sigma_u=1400
sigma_w=511.86
tau_w=222.84

## 4. Load conditions
scale=1
R=0.1

########## INPUT END ##########

f_meanstress='Goodman'
cal_life(odb_path,output_path,step_name,frame_num,sigma_u,sigma_f,b_power,scale,R,f_multiaxial,f_meanstress)

