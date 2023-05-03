# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import re 
from chemdataextractor import Document
        
        
class Extract_am_env:
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['shield','protect','manufactur','produce','fabricat','chamber','build','SLM','DED','PBF','WAAM','print']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        # pkeyword=['fatigue','LCF','HCF']
        nkeyword=['stress relie','heat treat','isostatic','HIP','treatment','anneal','atomi','post','age']
        # for k in pkeyword:
        #     if k in c:
        #         flag=True
        #         break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        term=r'\b(ar|n2|argon|nitrogen|co2)\b' 
        pattern=[term,]  
        sep=len(pattern)  
        pos=[]
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if ('argon' in tmp) or ('Argon' in tmp):
                            tmp='Ar'
                        elif ('nitrogen' in tmp) or ('Nitrogen' in tmp):
                            tmp='N2'                      
                        v0=tmp
                        u0=''
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(sent)
                        record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_am_machine:
    
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        nkeyword=['316','718','64','17-4','15-5','AlSi10Mg','304','fig']
        for k in pkeyword:
            if k in c:
                flag=True
                break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        term=r'\b((?:(?:EOS|3D\s*systems?|Arcam|BLT|Concept|LSF|LSNF|LENS|renishaw|realizer|trumpf|prox).{0,15}?\d+.*?(?:\s|.|,|\))|SLM.{0,3}?\d\d\d\s*(?:HL)?))'  
        pattern=[term,]  
        sep=len(pattern)  
        pos=[]
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0):
                    for rst in result:
                        tmp=rst
                        if self._sent_check(tmp):
                            v0=tmp
                            u0=''
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                            if i<=sep-1:
                                flag=1
                    
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_am_type:

    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v0)):
                    if (v0[i]==v[j])and(u0[i]==u[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s



    def extract(self,doc):

        value=[]
        source=[] 
        unit=[]
        am={'LPBF':[r'LPBF|L-PBF|LB-PBF',r'[S|s]elect.{0,10}[L|l]aser.{0,10}(?:[M|m]elt|[S|s]inter)',r'[L|l]aser.{0,10}[P|p]owder.{0,5}[B|b]ed.{0,5}[F|f]us',r'SLM', \
                    r'SLS',r'[D|d]irect.{0,5}[M|m]etal.{0,10}[L|l]aser.{0,10}(?:[M|m]elt|[S|s]inter)',r'DMLS'],
             'EPBF':[r'EPBF|E-PBF|EB-PBF',r'[S|s]elect.{0,10}[E|e]lectron.{0,10}(?:[M|m]elt|[S|s]inter)',r'[E|e]lectron.{0,10}[B|b]eam.{0,10}(?:[M|m]elt|[F|f]us)', \
                     r'EBM',r'[E|e]lectron.{0,10}[P|p]owder.{0,5}[B|b]ed.{0,5}[F|f]us'],
             'WAAM':[r'wire-?arc',r'WAAM'],
             'DED':[r'DED',r'direct.{0,10}energy.{0,10}deposit',r'LAM',r'[L|l]aser\s*engineer.{0,5}net.{0,5}shap',r'LENS',r'[L|l]aser.{0,5}metal\s*deposit',r'[L|l]aser.{0,10}solid\s*form'],
             'binder jet':[r'bind.{0,10}jet',],
             'metal extrusion':[r'metal.{0,10}extrusion',]}
        nsent=len(doc)
        
        for i0 in range(0,nsent):
            sent=doc[i0]
      
            for name in am.keys():
                for pat in am[name]:
                    if len(re.findall(pat,sent))>0:
                        value.append(name)
                        source.append(sent)
                        unit.append('')
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':[],'source':source}

class Extract_current:

    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if ('mA' in unit2):
            if isinstance(value,float):
                value=value/1000
            elif isinstance(value,list):
                for i in range(0,len(value)):
                    value[i]=value[i]/1000
            unit='A'
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j])and(u0[i]==u[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=['polish','tomography','ray','FIB','EBSD','SEM','TEM','microscope','coat','plating','BSE','composition','EDX','EDS']
        
        for k in nkeyword:
            if k in c:
                flag=False
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        pattern=[  r'(current).{0,8}[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*(m?A)\b',
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*(m?A)\b.{0,8}(current)',
                   r'\b(current)\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*(m?A)\b',
                   r'(current).{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*(m?A)\b',
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*(m?A)\b.{0,8}(current)',
                   r'(current).{0,8}(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*(m?A)\b',
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*(m?A)\b.{0,8}(current)',               
                   r'(current).{0,8}[\s | \( | = ](\d+\.?\d*)\s*(m?A)\b', 
                   r'[\s | \( ](\d+\.?\d*)\s*(m?A)\b.{0,8}(current)',
                   r'\b(current)\s*[=|-|:]\s*(\d+\.?\d*)\s*(m?A)\b'
                   r'(\d+\.?\d*)\s*(m?A)\s*(current)']   
        sep=len(pattern)  
        pos=[[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3],[0,1,2],[1,2],[0,1],[1,2],[0,1],[0,1]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_direction:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue',]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c,keyword,mtype='n'):
        flag=True
        if mtype=='p':
            flag=False
        c=c.lower()
        for k in keyword:
            if k in c:
                flag=not flag
                break 
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        pattern=[r'(vertical)',r'(horizon)',r'(parallel)',r'(perpendicular)',r'((?:sample|specimen|axis).{0,10}along)',r'(\d+.?\d*\s*°\s)' ]  
        sep=len(pattern)  
        pos=[]
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._sent_check(sent,['microstruct','pattern','strategy','rotate'],'n') and \
                    self._sent_check(sent,['fabricat','print','built','produce'],'p') and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if self._sent_check(tmp,[],[]):
                            v0=tmp
                            u0=''
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                            if i<=sep-1:
                                flag=1
                    
                            break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source} 

class Extract_elongation:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if len(unit2)==0:
            value=value*100
            unit='%'
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(%)'
        term=r'(elongation|fracture strain|ductility|εb)' 
        pattern=[  term+r'.*?(\d+\.?\d*)\s*(?:%)\s*,\s*(\d+\.?\d*)\s*(?:%)\s*and\s*(\d+\.?\d*)\s*'+unit_str,
                   term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*'+unit_str,
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*)\s*'+unit_str+'.{0,10}?(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*).{0,10}?(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.{0,20}(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str,               
                   term+r'.*?(\d+\.?\d*)\s*'+unit_str, 
                   term+r'.{0,20}?(\d+\.?\d*)\s*(?!mpa|gpa|])', 
                   r'[\s | \( ]~?(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   r'\b(ei?|εb|el)\s*[=|-|:].{0,3}?(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term,
                   term+r'.*?is.*?(\d+,?\d*\.?\d*)\s*'+unit_str]  
        sep=len(pattern)  
        pos=[[1,2,3,4],[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3,4],[1,2,3],[0,1,2],[1,2],[1,2],[1,],[0,1],[1,2],[0,1],[1,2]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==1:
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),'')
                        elif len(pos[i])==2: 
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        elif len(pos[i])==4 and i==6:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        elif len(pos[i])==4 and i==0:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][3]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][1]]),tmp[pos[i][3]])
                            v03,u03=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        if i==6:
                            value0.append(v01)
                            value0.append(v02)
                            unit0.append(u01)
                            unit0.append(u02)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        elif i==7:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)   
                        elif i==0:
                            value0.append(v01)
                            value0.append(v02)
                            value0.append(v03)
                            unit0.append(u01)
                            unit0.append(u02)
                            unit0.append(u03)
                            source0.append(sent)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i) 
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}   

class Extract_fat_env:
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','LCF','HCF','VHCF','crack','FCG','test','experiment']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        # pkeyword=['fatigue','LCF','HCF']
        nkeyword=['stress relie','heat treat','isostatic','HIP','treatment','anneal','atomi','post','age',
                  'shield','protect','manufactur','produce','fabricat','chamber','build','SLM','DED','WAAM','print']
        # for k in pkeyword:
        #     if k in c:
        #         flag=True
        #         break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        term=r'\b(air|ambient|laboratory|NaCl|saliva|sea\s*water|boil(?:ing|ed)\s*water|hygrogen|N2|nitrogen|vacuum|body\s*fluid)\b'
        pattern=[term,]  
        sep=len(pattern)  
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                # print(sent,pattern[i])
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        v0=tmp
                        u0=''
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(sent)
                        record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_fat_type:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        nkeyword=[',','.',';']
        for k in pkeyword:
            if k in c:
                flag=True
                break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(%)'
        pattern=[r'((?:(?:uni).{0,2}?axial|multi.{0,2}?axial|bi.{0,2}?axial|axial|tension|compression|torsion|resonan(?:t|ce)|ultra-?son|very\s*high\s*cycle|rota(?:ting|ted|tion|ry)|(?:4|four|3|three).{0,10}?bend|bending|thermo).{0,40}?(?:fatigue|cyclic))', \
                 r'((?:fatigue|cyclic).{0,30}?(?:(?:uni).{0,2}?axial|multi.{0,2}?axial|bi.{0,2}?axial|axial|tension|compression|torsion|resonan(?:t|ce)|ultra-?son|very\s*high\s*cycle|rota(?:ting|ted|tion|ry)|(?:4|four|3|three).{0,10}?bend|bending|thermo))']  
        sep=len(pattern)  
        pos=[]
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if self._sent_check(tmp):
                            v0=tmp
                            u0=''
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                            if i<=sep-1:
                                flag=1
                    
                            break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}  

class Extract_fdstock_size:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'mm' in unit2:
            value=self._value_scale(value,1000)
            unit='µm'
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=['residual','fatigue','difference']
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r'([m|µ]m)\b'
        term=r'(particles?|powders?|wires?)'  
        patternlst=[[[1,2,3,4],  term+r'.*?(\d+\.?\d*)\s*(?:[m|µ]m)\s*,\s*(\d+\.?\d*)\s*(?:[m|µ]m)\s*and\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2,3],    term+r'.*?(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'.*?(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2,3,4],  term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*)\s*'+unit_str+'.*?(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*).*?(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2],      term+r'\s*(?:of|\(|=)\s*~?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str], \
                    [[1,2],      term+r'.*?[\s | \( | = ]~?(\d+\.?\d*)\s*±?\s*(?:\d+\.?\d*)*\s*'+unit_str], \
                    [[0,1],      r'[\s | \( ]~?(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[0,1],      r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term], \
                    [[1,2],      term+r'.*?is.*?(\d+,?\d*\.?\d*)\s*'+unit_str]]  
        
        pattern=[]
        pos=[]
        for i in range(0,len(patternlst)):
            pos.append(patternlst[i][0])
            pattern.append(patternlst[i][1])
        sep=len(pattern)
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        elif len(pos[i])==4 and i==6:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        elif len(pos[i])==4 and i==0:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][3]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][1]]),tmp[pos[i][3]])
                            v03,u03=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        if i==6:
                            value0.append(v01)
                            value0.append(v02)
                            unit0.append(u01)
                            unit0.append(u02)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        elif i==7:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)   
                        elif i==0:
                            value0.append(v01)
                            value0.append(v02)
                            value0.append(v03)
                            unit0.append(u01)
                            unit0.append(u02)
                            unit0.append(u03)
                            source0.append(sent)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i) 
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}     

class Extract_frequency:
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if ('khz' in unit2):
            if isinstance(value,float):
                value=value*1000
            elif isinstance(value,list):
                for i in range(0,len(value)):
                    value[i]=value[i]*1000
            unit='Hz'
        elif (('r' in unit2) and ('min' in unit2))or('rpm' in unit2):
            if isinstance(value,float):
                value=value/60
            elif isinstance(value,list):
                for i in range(0,len(value)):
                    value[i]=value[i]/60
            unit='Hz' 
        else:
            unit='Hz'
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j])and(u0[i]==u[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','test','wave']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=['drop','indent','decreas','stop','terminat','fail','acqui']
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        pattern=[  r'(\d+\.?\d*)\s*(?:[k|K]?Hz)*\s*(?:to|-|,|~|–|up to)\s*(\d+\.?\d*)\s*([k|K]?Hz)\b',
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([k|K]?Hz)\b',
                   r'(\d+\.?\d*)\s*±\s*\d+\.?\d*\s*([k|K]?Hz)\b',
                   r'(\d+\.?\d*)\s*([k|K]?Hz)\b',
                   r'[\s | \( | = ](\d+\.?\d*)\s*(r\s*/\s*min|RPM|rpm)\b']  
        sep=len(pattern)  
        pos=[[0,1,2],[0,1,2],[0,1],[0,1],[0,1]]  
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if i0<(nsent-1):
                    context=context+doc[i0+1]
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source} 
        
class Extract_power:
    
    def _unit_trans(self,value,unit):
        
        if ('kW' in unit) or ('KW' in unit):
            if isinstance(value,float):
                value=value*1000
            elif isinstance(value,list):
                for i in range(0,len(value)):
                    value[i]=value[i]*1000
            unit='W'
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v0)):
                    if (v0[i]==v[j])and(u0[i]==u[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        pattern=[  r'([P|p]ower).*[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*([k|K]?W)\b',
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*([k|K]?W)\b.*([P|p]ower)',
                   r'\b([P|p](?:ower)*)\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*([k|K]?W)\b',
                   r'([P|p]ower).*(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([k|K]?W)\b',
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([k|K]?W)\b.*([P|p]ower)',
                   r'([P|p]ower).*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([k|K]?W)\b',
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([k|K]?W)\b.*([P|p]ower)',               
                   r'([P|p]ower).*[\s | \( | = ](\d+\.?\d*)\s*([k|K]?W)\b', 
                   r'[\s | \( ](\d+\.?\d*)\s*([k|K]?W)\b.*([P|p]ower)',
                   r'\b([P|p](?:ower)*)\s*[=|-|:]\s*(\d+\.?\d*)\s*([k|K]?W)\b']   
        sep=len(pattern)  
        pos=[[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3],[0,1,2],[1,2],[0,1],[1,2],[1,2],[0,1]]
        flag=0  
        for sent in doc:
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            for i in range(0,len(pattern)):
                result=re.search(pattern[i],sent)
                if (not (result is None)) and( (re.search('max',sent,re.I) is None) and (re.search('contour',sent,re.I) is None) and\
                                           (re.search('skin',sent,re.I) is None) and (re.search('CT',sent) is None) and \
                                           (re.search('boundary',sent,re.I) is None) and (re.search('ghost',sent,re.I) is None) and \
                                           (re.search('test',sent,re.I) is None)):
                    tmp=result.groups()
                    if len(pos[i])==2:    
                        v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                    elif len(pos[i])==3:
                        v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                    if i==5 or i==6:
                        value0.append(v0[0])
                        value0.append(v0[1])
                        unit0.append(u0)
                        unit0.append(u0)
                        source0.append(sent)
                        source0.append(sent)
                        record.append(i)
                        record.append(i)
                    else:
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(sent)
                        record.append(i)
                    if i<=sep-1:
                        flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source} 

class Extract_hatch_space:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'mm' in unit2:
            value=self._value_scale(value,1000)       
        elif unit2=='m':
            value=self._value_scale(value,1000000)  
        unit='µm'
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=['skin','contour','boundary']
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r'([m|µ]?m)\b'
        term=r'(hatch|scan\s*(?:spac(?:e|ing)|distance|interval)).{0,20}'
        pattern=[  term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*'+unit_str,
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.{0,8}(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,               
                   term+r'.{0,8}[\s | \( | = ](\d+\.?\d*)\s*'+unit_str, 
                   r'[\s | \( ](\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   r'\b(h)\s*[=|-|:]\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term]  
        sep=len(pattern)  
        pos=[[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3],[0,1,2],[1,2],[0,1],[1,2],[0,1],[0,1]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}     

class Extract_heat_treat:

    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _value_plus(self,value,add):
        if isinstance(value,float):
            value=value+add
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]+add
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'k' in unit2:
            value=self._value_plus(value,273)
            unit='°C'
        elif 'mpa' in unit2:
            value=self._value_scale(value,10)
            unit='bars'
        elif 'min' in unit2:
            value=self._value_scale(value,1/60)
            unit='hours'
        elif 'sec' in unit2:
            value=self._value_scale(value,1/3600)
            unit='hours'
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=['preheat','pre-heat']
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def _get_num(self,string):
        d=None
        map0=[['one',1],['two',2],['three',3],['four',4],['five',5],['six',6],['seven',7],['eight',8],
              ['nine',9],['ten',10],['eleven',11],['twelve',12],['twenty',20],['thirty',30]]
        try:
            d=float(string)
            return d
        except:
            for i in range(0,len(map0)):
                if string==map0[i][0]:
                    d=map0[i][1]
                    return d
        return d
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
    
        unit_temp=r'\s*Â?(◦\s*C|°\s*C|K\b|℃)\b\s*'
        prep_time=r',?\s*(?:for|was|\(|and|during|in)\s*.{0,20}?(?:of)?\s*'
        prep_temp=r',?\s*(?:at|\(|and|\:|to|up\sto|are|then)\s*.{0,20}?(?:temperature\sof)?\s*'
        prep_pres=r',?\s*(?:at|\(|and)\s*.{0,20}?(?:pressure\sof)?\s*'
        unit_time=r'\s*(h|hrs?|hours?|mins?|minutes?|seconds?|sec)\b\s*'
        unit_pres=r'\s*([B|b]ars?|MPa|mpa|Mpa)\b\s*'
        hip=r'(HIP(?:ed|ing)*|hot-?\s*isostatic(?:ally)*-?\s*press(?:ed|ing))'
        term=r'(treat(?:ed|ing|ment)|ag(?:ed|ing)|anneal(?:ed|ing)|relie(?:ved|ving|f)|precipitation\s*harden(?:ing|ed)|heat(?:ing|ed))'
        about=r'\s*(?:about|approximately)*\s*'
        num=r'(\d+\.?\d*|an|a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty)'
        patternlst=[[[1,2,5,6,3,4],hip+r'.{0,50}?'+prep_temp+about+num+unit_temp+prep_pres+about+num+unit_pres+prep_time+num+unit_time],
                 [[1,2,3,4,5,6],hip+r'.{0,50}?'+prep_temp+about+num+unit_temp+prep_time+about+num+unit_time+prep_pres+num+unit_pres],
                 [[3,4,1,2,5,6],hip+r'.{0,50}?'+prep_time+about+num+unit_time+prep_temp+about+num+unit_temp+prep_pres+num+unit_pres],
                 [[3,4,5,6,1,2],hip+r'.{0,50}?'+prep_pres+about+num+unit_pres+prep_temp+about+num+unit_temp+prep_time+num+unit_time],
                 [[2,3,0,1,4,5],num+unit_time+prep_temp+about+num+unit_temp+r'.{0,50}?'+num+unit_pres],
                 [[1,2,3,4],term+r'.{0,50}?'+prep_temp+num+unit_temp+prep_time+num+unit_time],
                 [[3,4,1,2],term+r'.{0,50}?'+prep_time+about+num+unit_time+prep_temp+about+num+unit_temp],
                 [[1,2,3,4],term+r'.{0,50}?'+prep_temp+num+unit_temp+r'.{0,50}?'+prep_time+num+unit_time],
                 [[1,2,3,4],term+r'.{0,50}?'+prep_temp+num+unit_temp+r'\s*'+num+unit_time],
                 [[0,1,2,3],prep_temp+num+unit_temp+prep_time+num+unit_time],
                 [[1,2],term+r'.{0,50}?'+prep_temp+num+unit_temp]]
    
        pattern=[]
        pos=[]
        for i in range(0,len(patternlst)):
            pos.append(patternlst[i][0])
            pattern.append(patternlst[i][1])
        sep=len(pattern)   
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            flag_match=0
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        vtemp=None
                        vtime=None
                        vpres=None
                        utemp=''
                        utime=''
                        upres=''
                        if i<=4:
                            d=self._get_num(tmp[pos[i][0]])
                            vtemp,utemp=self._unit_trans(d,tmp[pos[i][1]])
                            d=self._get_num(tmp[pos[i][2]])
                            vtime,utime=self._unit_trans(d,tmp[pos[i][3]])
                            d=self._get_num(tmp[pos[i][4]])
                            vpres,upres=self._unit_trans(d,tmp[pos[i][5]])
                        elif i<=9:
                            d=self._get_num(tmp[pos[i][0]])
                            vtemp,utemp=self._unit_trans(d,tmp[pos[i][1]])
                            d=self._get_num(tmp[pos[i][2]])
                            vtime,utime=self._unit_trans(d,tmp[pos[i][3]])
                        elif i<=10:
                            d=self._get_num(tmp[pos[i][0]])
                            vtemp,utemp=self._unit_trans(d,tmp[pos[i][1]])
                        
                        value0.append([vtemp,vtime,vpres])
                        unit0.append([utemp,utime,upres])
                        source0.append(sent)
                        flag_match=1
                    if flag_match:
                        break
                if flag_match:
                    break
                
            if flag_match==1:
                for i in range(0,len(value0)):
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
    
        return {'value':value,'unit':unit,'source':source}     

class Extract_layer_rot:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _value_plus(self,value,add):
        if isinstance(value,float):
            value=value+add
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]+add
        return value
    
    def _unit_trans(self,value,unit):
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   # mark if the value is recorded
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['scan','strategy','layer']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(◦|°|degree)'
        term=r'(rotat(?:e|ing|ed|ion))'
    
        patternlst=[[[1,2,3,4],  term+r'.{0,30}?(\d+\.?\d*)\s*(?:◦C|°C|K)\s*,\s*(\d+\.?\d*)\s*(?:◦C|°C|K)\s*and\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2,3],    term+r'.{0,30}?(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'.{0,30}?(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2,3,4],  term+r'.{0,30}?(?:is|are|were|was).*?(\d+\.?\d*)\s*'+unit_str+'\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'.{0,30}?(?:is|are|were|was).*?(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2],      term+r'.{0,30}?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str], \
                    [[1,2],      term+r'.{0,30}?[\s | \( | = ]~?(\d+\.?\d*)\s*±?\s*(?:\d+\.?\d*)*\s*'+unit_str], \
                    [[1,2],      term+r'.{0,30}?(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1],      r'[\s | \( ]~?(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[0,1],      r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term], \
                    [[1,2],      term+r'.{0,30}?is.{0,30}?(\d+,?\d*\.?\d*)\s*'+unit_str]]  
        pattern=[]
        pos=[]
        for i in range(0,len(patternlst)):
            pos.append(patternlst[i][0])
            pattern.append(patternlst[i][1])
        sep=len(pattern)
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        elif len(pos[i])==4 and i==6:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        elif len(pos[i])==4 and i==0:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][3]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][1]]),tmp[pos[i][3]])
                            v03,u03=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        if i==6:
                            value0.append(v01)
                            value0.append(v02)
                            unit0.append(u01)
                            unit0.append(u02)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        elif i==7:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)   
                        elif i==0:
                            value0.append(v01)
                            value0.append(v02)
                            value0.append(v03)
                            unit0.append(u01)
                            unit0.append(u02)
                            unit0.append(u03)
                            source0.append(sent)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i) 
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}    

class Extract_layer_thickness:

    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if ('mm' in unit2):
            if isinstance(value,float):
                value=value*1000
            elif isinstance(value,list):
                for i in range(0,len(value)):
                    value[i]=value[i]*1000
            unit='µm'
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j])and(u0[i]==u[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['layer','deposit']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        pattern=[  r'(thick).{0,8}[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*([m|µ]m)\b',
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*([m|µ]m)\b.{0,8}(thick)',
                   r'\b(thick)\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*([m|µ]m)\b',
                   r'(thick).{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([m|µ]m)\b',
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([m|µ]m)\b.{0,8}(thick)',
                   r'(thick).{0,8}(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([m|µ]m)\b',
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*([m|µ]m)\b.{0,8}(thick)',               
                   r'(thick).{0,8}[\s | \( | = ](\d+\.?\d*)\s*([m|µ]m)\b', 
                   r'[\s | \( ](\d+\.?\d*)\s*([m|µ]m)\b.{0,8}(thick)',
                   r'\b(t(?:hick))\s*[=|-|:]\s*(\d+\.?\d*)\s*([m|µ]m)\b'
                   r'(\d+\.?\d*)\s*([m|µ]m)\s*(thick)']   
        sep=len(pattern)  
        pos=[[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3],[0,1,2],[1,2],[0,1],[1,2],[0,1],[0,1]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_load_ctrl:
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','LCF','HCF','VHCF','FCG','crack','test','experiment']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        # pkeyword=['fatigue','LCF','HCF']
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        pattern=[r'(load|stress|strain|displacement|force).{0,5}control',
                 r'control.{0,5}(load|stress|strain|displacement|force)']  
        sep=len(pattern)  
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        v0=tmp
                        u0=''
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(sent)
                        record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_mat_name:

    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v0)):
                    if (v0[i]==v[j])and(u0[i]==u[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def extract(self,doc):
    
        value=[]
        source=[] 
        unit=[]        
        
        doc_low=[]
        for i in range(0,len(doc)):
            doc_low.append(doc[i].lower())        
        
        mat={'IN718':['718',],'IN625':['625',],'Ti64':['ti6al4v','ti-6al-4v','ti64','TC4'], \
             '316L':['316l',],'304':['304',],'304L':['304l',],'17-4PH':['17-4ph','17-4 ph'], '17-7PH':['17-7ph','17-7 ph'], \
             '15-5PH':['15-5ph','15-5 ph'],'18Ni300':['18ni300',],'AlSi10Mg':['alsi10mg',],'AlSi12':['alsi12',], \
             'Scalmalloy':['scalmalloy',],'QuesTek Al':['questek al',],'AIF357':['357',],'A356':['356',],'6061':['6061'],'7075':['7075'], \
             'CoCrW':['cocrw',],'Maraging steel':['maraging steel',],'Stainless steel':['stainless steel'],'Hastelloy-X':['hastelloy-x',], \
             'CMSX-4':['cmsx-4',],'GH4169':['4169',],'Ti6242':['ti-6242','ti6242','ti-6al-2sn-4zr-2mo'],'ANSI':['ansi',], \
             'PH15-7Mo':['ph15-7mo',],'2024':['2024',],'7050':['7050',],'Waspaloy':['waspaloy',]}
        for name in mat.keys():
            for m in mat[name]:
                for sent in doc_low:
                    if m in sent:
                        value.append(name)
                        unit.append('')
                        source.append(sent)

        article=Document(sent)
        chem=article.cems
        for record in chem:
            if not record.text in value:
                value.append(record.text)
                unit.append('')
                source.append('')                
        
        value,unit,source=self._merge_equal_item(value,unit,source)        
        
        return {'value':value,'unit':unit,'source':source}    

class Extract_modulus:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'gpa' in unit2:
            unit='GPa'        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=['residual','fatigue','difference']
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(gpa)\b'
        term=r'(modulus|moduli|\bE\b)'  
        pattern=[  term+r'.*?(\d+\.?\d*)\s*(?:gpa)\s*,\s*(\d+\.?\d*)\s*(?:gpa)\s*and\s*(\d+\.?\d*)\s*'+unit_str,
                   term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*'+unit_str,
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*)\s*'+unit_str+'.*?(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*).*?(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(?:of|\(|=)\s*~?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str,               
                   term+r'.*?[\s | \( | = ]~?(\d+\.?\d*)\s*±?\s*(?:\d+\.?\d*)*\s*'+unit_str, 
                   r'[\s | \( ]~?(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   r'\b(\bEy?)\s*[=|-|:].{0,3}(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term,
                   term+r'.*?is.*?(\d+,?\d*\.?\d*)\s*'+unit_str]  
        sep=len(pattern)  
        pos=[[1,2,3,4],[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3,4],[1,2,3],[0,1,2],[1,2],[1,2],[0,1],[1,2],[0,1],[1,2]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        elif len(pos[i])==4 and i==6:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        elif len(pos[i])==4 and i==0:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][3]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][1]]),tmp[pos[i][3]])
                            v03,u03=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        if i==6:
                            value0.append(v01)
                            value0.append(v02)
                            unit0.append(u01)
                            unit0.append(u02)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        elif i==7:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)   
                        elif i==0:
                            value0.append(v01)
                            value0.append(v02)
                            value0.append(v03)
                            unit0.append(u01)
                            unit0.append(u02)
                            unit0.append(u03)
                            source0.append(sent)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i) 
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}   

class Extract_preheat:
    
    def _value_plus(self,value,add):
        if isinstance(value,float):
            value=value+add
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]+add
        return value    
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'K' in unit2:
            value=self._value_plus(value,-273)
            unit='°C'
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0 
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r'Â?(◦\s*C|°\s*C|K)\b'
        term=r'(pre(?:-|–)?heat|base\s*(?:plate|area)|build\s*(?:plate|area)|'+\
             r'chamber\s*temperature|platform|substrate|powder\s*layer)'
    
        patternlst=[[[1,2,3,4],  term+r'.{0,30}?(\d+\.?\d*)\s*(?:◦C|°C|K)\s*,\s*(\d+\.?\d*)\s*(?:◦C|°C|K)\s*and\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2,3],    term+r'.{0,30}?(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'.{0,30}?(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2,3,4],  term+r'.{0,30}?(?:is|are|were|was).*?(\d+\.?\d*)\s*'+unit_str+'\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'.{0,30}?(?:is|are|were|was).*?(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2],      term+r'.{0,30}?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str], \
                    [[1,2],      term+r'.{0,30}?[\s | \( | = ]~?(\d+\.?\d*)\s*±?\s*(?:\d+\.?\d*)*\s*'+unit_str], \
                    [[1,2],      term+r'.{0,30}?(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1],      r'[\s | \( ]~?(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[0,1],      r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term], \
                    [[1,2],      term+r'.{0,30}?is.{0,30}?(\d+,?\d*\.?\d*)\s*'+unit_str]]  
        pattern=[]
        pos=[]
        for i in range(0,len(patternlst)):
            pos.append(patternlst[i][0])
            pattern.append(patternlst[i][1])
        sep=len(pattern)
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        elif len(pos[i])==4 and i==6:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        elif len(pos[i])==4 and i==0:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][3]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][1]]),tmp[pos[i][3]])
                            v03,u03=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        if i==6:
                            value0.append(v01)
                            value0.append(v02)
                            unit0.append(u01)
                            unit0.append(u02)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        elif i==7:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)   
                        elif i==0:
                            value0.append(v01)
                            value0.append(v02)
                            value0.append(v03)
                            unit0.append(u01)
                            unit0.append(u02)
                            unit0.append(u03)
                            source0.append(sent)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i) 
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_pfeed_rate:

    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'µg' in unit2:
            value=self._value_scale(value,1/1000)
        if 'min' in unit2 or 'minute' in unit2:
            value=self._value_scale(value,1/60)       
        elif 'h' in unit2 or 'hour' in unit2:
            value=self._value_scale(value,1/3600) 
            
        unit='g/s'
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0 
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['powder',]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r'([m|µ]?g\s*/\s*(?:s|min|h|seconds?|minutes?|hours?))\b'
        term=r'((?:feed|flow).{0,10}(?:rate|speed|velocity)|pfs)'
        pattern=[  term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*'+unit_str,
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.{0,8}(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,               
                   term+r'.{0,8}[\s | \( | = ](\d+\.?\d*)\s*'+unit_str, 
                   r'[\s | \( ](\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   r'\b(v)\s*[=|-|:]\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term]   
        sep=len(pattern)  
        pos=[[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3],[0,1,2],[1,2],[0,1],[1,2],[0,1],[0,1]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}        

class Extract_scan_pattern:
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['scan','pattern','strategy','print','raster','melt','manufactur','fabricat']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        # pkeyword=['fatigue','LCF','HCF']
        nkeyword=[]
        # for k in pkeyword:
        #     if k in c:
        #         flag=True
        #         break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(%)'
        term=r'(zigzag|stripe|meander|snake|island|chessboard|alternat|oscillation|bidirection|cross.{0,3}(?:hatch|dirction)|back\s*and\s*forth)'
        pattern=[term,]  
        sep=len(pattern)  
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        v0=tmp
                        u0=''
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(sent)
                        record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}    
  
class Extract_scan_speed:

    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit=unit.lower()
        if 'µm' in unit:
            value=self._value_scale(value,1/1000)
        if 'min' in unit:
            value=self._value_scale(value,1/60)       
        if (not 'min' in unit) and (len(re.findall('m',unit))==1):
            value=self._value_scale(value,1000)        
            
        unit='mm/s'
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=['test',]
        for k in nkeyword:
            if k in c:
                flag=False
                break 

        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r'([m|µ]?m\s*/\s*[m|µ]?(?:s|min))\b'
        term=r'(speed|velocity|scan.{0,10}rate)'
        pattern=[  term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*'+unit_str,
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.{0,8}(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,               
                   term+r'.{0,8}[\s | \( | = ](\d+\.?\d*)\s*'+unit_str, 
                   r'[\s | \( ](\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   r'\b(v)\s*[=|-|:]\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term]   
        sep=len(pattern)  
        pos=[[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3],[0,1,2],[1,2],[0,1],[1,2],[0,1],[0,1]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent

                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}    

class Extract_speed_func:

    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 

        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        term=r'(speed\s*function|velocity\s*function)'
        pattern=[  term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*',
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*',
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*',
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+'.{0,8}'+term,
                   term+r'.{0,8}(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*',
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+'.{0,8}'+term,               
                   term+r'.{0,8}[\s | \( | = ](\d+\.?\d*)\s*', 
                   r'[\s | \( ](\d+\.?\d*)\s*'+'.{0,8}'+term,
                   r'\b(v)\s*[=|-|:]\s*(\d+\.?\d*)\s*',
                   r'(\d+\.?\d*)\s*'+'\s*'+term]   
        sep=len(pattern)  
        pos=[[1,2],[0,1],[1,2],[1,2],[0,1],[1,2],[0,1],[1,],[0,],[1,],[0,],[0,]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==1:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),'')
                        elif len(pos[i])==2:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],'')
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}    

class Extract_spec_desc:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','LCF','HCF','VHCF','FCG']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['sample','specimen','coupon']
        nkeyword=[]
        for k in pkeyword:
            if k in c:
                flag=True
                break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(%)'
        term=r'\b(astm|iso|en|gb/t|gb|din|jis)'  # R_m R_p0.2 S_u S_y
        pattern=['(ASTM)\s*(?:standard(?:s)?|-|—)?\s*(E466)','(ASTM)\s*(?:standard(?:s)?|-|—)?\s*(E606)',
                 '(ASTM)\s*(?:standard(?:s)?|-|—)?\s*(E647)','(ASTM)\s*(?:standard(?:s)?|-|—)?\s*(E2207)'
                 '(DIN)\s*(?:standard(?:s)?|-|—)?\s*(50100)','(DIN)\s*(?:standard(?:s)?|-|—)?\s*(50113)',
                 '(EN)\s*(?:standard(?:s)?|-|—)?\s*(3987)','(EN)\s*(?:standard(?:s)?|-|—)?\s*(6072)',
                 '(ISO)\s*(?:standard(?:s)?|-|—)?\s*(1099)','(ISO)\s*(?:standard(?:s)?|-|—)?\s*(1143)',
                 '(ISO)\s*(?:standard(?:s)?|-|—)?\s*(12106)','(JIS)\s*(?:standard(?:s)?|-|—)?\s*(T0309)',
                 '(NF)\s*(?:standard(?:s)?|-|—)?\s*(A03-400)']  
        sep=len(pattern)  
        pos=[[1,0],[0,],[0,]]
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        v0=tmp[0]+' '+tmp[1]
                        u0=tmp[0]
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(sent)
                        record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}  

class Extract_surf_treat:
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','LCF','HCF','VHCF','FCG','specimen','sample','coupon']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        # pkeyword=['fatigue','LCF','HCF']
        nkeyword=['tension','EBSD','metallogra','microstruc','TEM','SEM','microscop','diffraction']
        # for k in pkeyword:
        #     if k in c:
        #         flag=True
        #         break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        term=r'(as-built|(?:electrical\s*discharge|micro)\s*machin(?:ed|ing)|EDM|wire.{0,3}cut|manual(?:ly)?\s*(?:grinding|ground)|(?:electro(?:lytic)?|chemical|laser|plasma).{0,4}polish|(?:shot|sand|grit|powder|bead|hammer|plastic\s*media|laser\s*(?:shock)?|abrasive).{0,3}(?:peen|blast)|plat(?:ed|ing)|coat(?:ing|ed)|(?:vibro|tribo|vibratory|centrifugal).{0,3}finish(?:ed|ing)|etch(?:ed|ing)|charged|tumbl(?:ed|ing)|ultrasonic\s*nanocrystal\s*surface\s*modification|machin(?:ed|ing)|mill(?:ed|ing)|turn(?:ed|ing)|polish(?:en|ing)|grinding|ground|oxidation)'
        pattern=[term,]  
        sep=len(pattern)  
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._sent_check(context) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        v0=tmp
                        u0=''
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(context)
                        record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}    

class Extract_fat_standard:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['perform','test','conduct']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','LCF','HCF']
        nkeyword=['sample','specimen']
        for k in pkeyword:
            if k in c:
                flag=True
                break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        term=r'\b(astm|iso|en|gb/t|gb|din|jis)'  
        pattern=['(ASTM)\s*(?:standard(?:s)?|-|—)?\s*(E466)','(ASTM)\s*(?:standard(?:s)?|-|—)?\s*(E606)',
                 '(ASTM)\s*(?:standard(?:s)?|-|—)?\s*(E647)','(ASTM)\s*(?:standard(?:s)?|-|—)?\s*(E2207)'
                 '(DIN)\s*(?:standard(?:s)?|-|—)?\s*(50100)','(DIN)\s*(?:standard(?:s)?|-|—)?\s*(50113)',
                 '(EN)\s*(?:standard(?:s)?|-|—)?\s*(3987)','(EN)\s*(?:standard(?:s)?|-|—)?\s*(6072)',
                 '(ISO)\s*(?:standard(?:s)?|-|—)?\s*(1099)','(ISO)\s*(?:standard(?:s)?|-|—)?\s*(1143)',
                 '(ISO)\s*(?:standard(?:s)?|-|—)?\s*(12106)','(JIS)\s*(?:standard(?:s)?|-|—)?\s*(T0309)',
                 '(NF)\s*(?:standard(?:s)?|-|—)?\s*(A03-400)'] 
        sep=len(pattern)  
        pos=[]
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        v0=tmp[0]+' '+tmp[1]
                        u0=tmp[0]
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(sent)
                        record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}     

class Extract_fat_r:
    
    def _unit_trans(self,value,unit):
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   # mark if the value is recorded
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','test','wave']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=['drop','indent','decreas','stop','terminat','fail','acqui']
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        pattern=[  r'(stress ratio|load ratio|R\s*=)\s*(-?\d+\.?\d*)\b',
                   r'(R.{0,3}ε.{0,3}|strain ratio\s*=)\s*(-?\d+\.?\d*)\b'
                   r'(full).{0,3}(reverse)',
                   r'(tension).{0,3}(compression)'] 
        sep=len(pattern) 
        pos=[[1,0],[1,0]]   
        flag=0
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if i0<(nsent-1):
                    context=context+doc[i0+1]
                if (len(result)>0)and self._context_check(context):
                    if i>1:
                        value0.append(-1)
                        unit0.append('')
                        source0.append(sent)
                        record.append(i)
                        break                      
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0=float(tmp[pos[i][0]])
                            u0=tmp[pos[i][1]]
                        elif len(pos[i])==3:
                            v0=[float(tmp[pos[i][0]]),float(tmp[pos[i][1]])]
                            u0=tmp[pos[i][2]]
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}     

class Extract_fat_temp:

    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value

    def _value_plus(self,value,add):
        if isinstance(value,float):
            value=value+add
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]+add
        return value  
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'K' in unit2:
            value=self._value_plus(value,-273)
            unit='°C'
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','LCF','HCF','VHCF','FCG','cyclic','crack']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        # pkeyword=['fatigue','LCF','HCF']
        nkeyword=[]
        # for k in pkeyword:
        #     if k in c:
        #         flag=True
        #         break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(%)'
        term=r'\b(ambient|room)\b' 
        pattern=[term,]  
        sep=len(pattern)  
        pos=[[1,0],[0,],[0,]]
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if ('ambient' in tmp) or ('Ambient' in tmp):
                            tmp=25
                        elif ('room' in tmp) or ('Room' in tmp):
                            tmp=25
                        v0=tmp
                        u0='°C'
                        value0.append(v0)
                        unit0.append(u0)
                        source0.append(sent)
                        record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  

        unit_str=r'Â?(◦\s*C|°\s*C|K)\b'
        term=r'(temperature)'
    
        patternlst=[[[1,2,3,4],  term+r'.{0,30}?(\d+\.?\d*)\s*(?:◦C|°C|K)\s*,\s*(\d+\.?\d*)\s*(?:◦C|°C|K)\s*and\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2,3],    term+r'.{0,30}?(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'.{0,30}?(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2,3,4],  term+r'.{0,30}?(?:is|are|were|was).*?(\d+\.?\d*)\s*'+unit_str+'\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[1,2,3],    term+r'.{0,30}?(?:is|are|were|was).*?(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1,2],    r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[1,2],      term+r'.{0,30}?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str], \
                    [[1,2],      term+r'.{0,30}?[\s | \( | = ]~?(\d+\.?\d*)\s*±?\s*(?:\d+\.?\d*)*\s*'+unit_str], \
                    [[1,2],      term+r'.{0,30}?(\d+\.?\d*)\s*'+unit_str], \
                    [[0,1],      r'[\s | \( ]~?(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term], \
                    [[0,1],      r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term], \
                    [[1,2],      term+r'.{0,30}?is.{0,30}?(\d+,?\d*\.?\d*)\s*'+unit_str]]  
        pattern=[]
        pos=[]
        for i in range(0,len(patternlst)):
            pos.append(patternlst[i][0])
            pattern.append(patternlst[i][1])
        sep=len(pattern)
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        elif len(pos[i])==4 and i==6:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        elif len(pos[i])==4 and i==0:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][3]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][1]]),tmp[pos[i][3]])
                            v03,u03=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        if i==6:
                            value0.append(v01)
                            value0.append(v02)
                            unit0.append(u01)
                            unit0.append(u02)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        elif i==7:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)   
                        elif i==0:
                            value0.append(v01)
                            value0.append(v02)
                            value0.append(v03)
                            unit0.append(u01)
                            unit0.append(u02)
                            unit0.append(u03)
                            source0.append(sent)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i) 
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  

        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_fat_machine:

    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0   
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['fatigue','cyclic','hcf','lcf','fcg','crack']
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        nkeyword=['extensometer']
        for k in pkeyword:
            if k in c:
                flag=True
                break 
        for k in nkeyword:
            if k in c:
                flag=False
        return flag
    
    
    def extract(self,doc):
        global stop
        value=[]
        unit=[]
        source=[]    
        unit_str=r''
        pattern=[r'\b((?:(?:MTS|INSTRON|amsler|QB|QBG|RBF-|Yamamoto|rumul|SHIMADZU|zwick|Schenc?k|raagen|rumul|custom|home-?made|ultra-?sonic|VHCF).{0,40}?(?:machine|system|device|equip|frame)))',\
                 r'\b((?:(?:MTS|INSTRON|amsler|QB|QBG|RBF-|Yamamoto|rumul|SHIMADZU|zwick|Schenc?k|USF).{0,15}?\d+.*?(?:\s|.|,|\))))', \
                 r'((?:servo\s*[-|–])?\s*hydraulic.{0,40}?(?:machine|system|device|equip|frame))', \
                 r'((?:MTS|INSTRON|amsler|QB|QBG|RBF-|Yamamoto|rumul|SHIMADZU|zwick|Schenck|raagen|rumul).+?\s)']  
        sep=len(pattern)  
        pos=[]
        exclude=[]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            if (len(re.findall(r'tension|tensile',sent,re.I))>0 or len(re.findall(r'impact',sent,re.I))>0) or len(re.findall(r'hardness',sent,re.I))>0 \
                and len(re.findall(r'fatigue|cyclic',sent,re.I))==0:
                continue
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            pos00=sent.lower().find('extensometer')
            pos01=sent.lower().find('grip')
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        pos1=sent.lower().find(tmp.lower())
                        if (((pos00<0 or pos1<0 or abs(pos00-pos1)>40))and((pos01<0 or pos1<0 or abs(pos01-pos1)>40))) and self._sent_check(tmp):
                            v0=tmp
                            u0=''
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    value.append(value0[i])
                    unit.append(unit0[i])
                    source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_tensile_strength:

    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'mpa' in unit2:
            unit='MPa'
        
        return value,unit

    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0 
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=['residual','fatigue','difference']
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(mpa)\b'
        term=r'((?:tensi(?:on|le)|ultimate)\s*(?:strength|stress)|\bUTS\b|\bRm\b|\bsu\b|σ.{0,3}t|σ.{0,3}b|σ.{0,3}uts|σ.{0,3}UTS)' 
        pattern=[  term+r'.*?(\d+\.?\d*)\s*(?:mpa)\s*,\s*(\d+\.?\d*)\s*(?:mpa)\s*and\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:yield|ys).*?(?:and|,).*(tensi(?:on|le)|ultimate).*?\d+\.?\d*\s*±\s*(?:\d+\.?\d*)\s*(?:mpa)*\s(?:and|,).*?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str,
                   r'(tensi(?:on|le)|ultimate).*?(?:and|,).*?(?:yield|ys).*?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str+r'\s*(?:and|,).*?(?:\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*mpa',
                   r'(?:yield|ys).*?(?:and|,).*'+term+r'.*?\d+\.?\d*\s*(?:mpa)*\s(?:and|,).*?(\d+\.?\d*)\s*'+unit_str,
                   term+r'.*?and.*?(?:yield|ys).*?(\d+\.?\d*)\s*(?:mpa)*\sand.*?\d+\.?\d*\s*'+unit_str,
                   term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*'+unit_str,
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*)\s*'+unit_str+'.*?(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*).*?(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(?:of|\(|=)\s*~?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str,               
                   term+r'.*?[\s | \( | = ]~?(\d+\.?\d*)\s*±?\s*(?:\d+\.?\d*)*\s*'+unit_str, 
                   r'[\s | \( ]~?(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   r'\b(\buts\b|\brm|\bsu)\s*[=|-|:].{0,3}(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term,
                   term+r'.*?is.*?(\d+,?\d*\.?\d*)\s*'+unit_str]  
        sep=len(pattern)  
        pos=[[1,2,3,4],[1,2],[1,2],[1,2],[1,2],[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3,4],[1,2,3],[0,1,2],[1,2],[1,2],[0,1],[1,2],[0,1],[1,2]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        elif len(pos[i])==4 and i==10:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        elif len(pos[i])==4 and i==0:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][3]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][1]]),tmp[pos[i][3]])
                            v03,u03=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        if i==10:
                            value0.append(v01)
                            value0.append(v02)
                            unit0.append(u01)
                            unit0.append(u02)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        elif i==11:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)   
                        elif i==0:
                            value0.append(v01)
                            value0.append(v02)
                            value0.append(v03)
                            unit0.append(u01)
                            unit0.append(u02)
                            unit0.append(u03)
                            source0.append(sent)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i) 
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_voltage:

    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if ('kv' in unit2):
            if isinstance(value,float):
                value=value*1000
            elif isinstance(value,list):
                for i in range(0,len(value)):
                    value[i]=value[i]*1000
            unit='V'
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j])and(u0[i]==u[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=['polish','tomography','ray','FIB','EBSD','SEM','TEM','microscope','BSE','composition','EDX','EDS']
        
        for k in nkeyword:
            if k in c:
                flag=False
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        pattern=[  r'(volt(?:age)?).{0,8}[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*(k?V)\b',
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*(k?V)\b.{0,8}(volt(?:age)?)',
                   r'\b(volt(?:age)?)\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*(k?V)\b',
                   r'(volt(?:age)?).{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*(k?V)\b',
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*(k?V)\b.{0,8}(volt(?:age)?)',
                   r'(volt(?:age)?).{0,8}(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*(k?V)\b',
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*(k?V)\b.{0,8}(volt(?:age)?)',               
                   r'(volt(?:age)?).{0,8}[\s | \( | = ](\d+\.?\d*)\s*(k?V)\b', 
                   r'[\s | \( ](\d+\.?\d*)\s*(k?V)\b.{0,8}(volt(?:age)?)',
                   r'\b(volt(?:age)?)\s*[=|-|:]\s*(\d+\.?\d*)\s*(k?V)\b'
                   r'(\d+\.?\d*)\s*(k?V)\s*(volt(?:age)?)']   
        sep=len(pattern)  
        pos=[[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3],[0,1,2],[1,2],[0,1],[1,2],[0,1],[0,1]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

class Extract_wfeed_rate:

    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'µm' in unit2:
            value=self._value_scale(value,1/1000)
        elif not ('mm' in unit2):
            value=self._value_scale(value,1000)
        if 'min' in unit2 or 'minute' in unit2:
            value=self._value_scale(value,1/60)       
        elif 'h' in unit2 or 'hour' in unit2:
            value=self._value_scale(value,1/3600) 
            
        unit='mm/s'
    
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=False
        c=c.lower()
        pkeyword=['wire',]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        nkeyword=[]
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r'([m|µ]?m\s*/\s*(?:s|min|h|seconds?|minutes?|hours?))\b'
        term=r'((?:feed|flow).{0,10}(?:rate|speed|velocity)|wfs)'
        pattern=[  term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*'+unit_str,
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.{0,8}(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,               
                   term+r'.{0,8}[\s | \( | = ](\d+\.?\d*)\s*'+unit_str, 
                   r'[\s | \( ](\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   r'\b(v)\s*[=|-|:]\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term]   
        sep=len(pattern)  
        pos=[[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3],[0,1,2],[1,2],[0,1],[1,2],[0,1],[0,1]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        if i==None:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}  
        
class Extract_yield_strength:
    
    def _value_scale(self,value,times):
        if isinstance(value,float):
            value=value*times
        elif isinstance(value,list):
            for i in range(0,len(value)):
                value[i]=value[i]*times
        return value
    
    def _unit_trans(self,value,unit):
        unit2=unit.lower()
        if 'mpa' in unit2:
            unit='MPa'
        
        return value,unit
    
    # merge equal items in a doc
    def _merge_equal_item(self,v0,u0,s0):
        v=[]
        u=[]
        s=[]
        for i in range(0,len(v0)):
            flag=0  
            if not (v0[i] in v):
                v.append(v0[i])
                u.append(u0[i])
                s.append(s0[i])
            else:
                for j in range(0,len(v)):
                    if (v0[i]==v[j]):
                        s[j]=s[j]+' | '+s0[i]
                        flag=1
                        break
                if not flag:
                    v.append(v0[i])
                    u.append(u0[i])
                    s.append(s0[i])
        return v,u,s
    
    def _context_check(self,c):
        flag=True
        c=c.lower()
        pkeyword=[]
        
        for k in pkeyword:
            if k in c:
                flag=True
                break
    
        return flag
    
    def _sent_check(self,c):
        flag=True
        c=c.lower()
        nkeyword=['residual','fatigue','difference']
        for k in nkeyword:
            if k in c:
                flag=False
                break 
        return flag
    
    
    def extract(self,doc):
    
        value=[]
        unit=[]
        source=[]    
        unit_str=r'(mpa)\b'
        term=r'(yield|\bYS\b|\bRy\b|\bsy\b|σ.{0,3}y|σ.{0,3}Y)'
        pattern=[  term+r'.*?(\d+\.?\d*)\s*(?:mpa)\s*,\s*(\d+\.?\d*)\s*(?:mpa)\s*and\s*(\d+\.?\d*)\s*'+unit_str,
                   term+r'.*?(?:and|,).*(?:tensi(?:on|le)|ultimate).*?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*(?:mpa)*\s(?:and|,).*?(?:\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str,
                   r'(?:tensi(?:on|le)|ultimate).*?(?:and|,).*?'+term+'.*?(?:\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*(?:and|,).*?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str,
                   r'(?:tensi(?:on|le)|ultimate).*?(?:and|,).*'+term+r'.*?(?:\d+\.?\d*)\s*(?:mpa)*\s(?:and|,).*?(\d+\.?\d*)\s*'+unit_str,
                   term+r'.*?and.*?(?:tensi(?:on|le)|ultimate).*?(\d+\.?\d*)\s*'+unit_str+'\s*and.*?(?:\d+\.?\d*)\s*(?:mpa)',
                   term+r'[\s | \( | = ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'[\s | \( ](\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(\d+\.?\d*)\s*(?:to|-|,|~|–)\s*(\d+\.?\d*)\s\s*'+unit_str,
                   term+r'.{0,8}(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(?:between)\s*(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*)\s*'+unit_str+'.*?(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   term+r'.*?(?:is|are|were|was).*?(\d+\.?\d*).*?(?:and)\s*(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*(?:and)\s*(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   term+r'\s*(?:of|\(|=)\s*~?(\d+\.?\d*)\s*±\s*(?:\d+\.?\d*)\s*'+unit_str,               
                   term+r'.*?[\s | \( | = ]~?(\d+\.?\d*)\s*±?\s*(?:\d+\.?\d*)*\s*'+unit_str, 
                   r'[\s | \( ]~?(\d+\.?\d*)\s*'+unit_str+'.{0,8}'+term,
                   r'\b(\byss\b|\bry|\bsy)\s*[=|-|:].{0,3}(\d+\.?\d*)\s*'+unit_str,
                   r'(\d+\.?\d*)\s*'+unit_str+'\s*'+term,
                   term+r'.*?is.*?(\d+,?\d*\.?\d*)\s*'+unit_str]  
        sep=len(pattern)  
        pos=[[1,2,3,4],[1,2],[1,2],[1,2],[1,2],[1,2,3],[0,1,2],[1,2,3],[1,2,3],[0,1,2],[1,2,3,4],[1,2,3],[0,1,2],[1,2],[1,2],[0,1],[1,2],[0,1],[1,2]]
        flag=0 
        nsent=len(doc)
        for i0 in range(0,nsent):
            sent=doc[i0]
            value0=[]
            unit0=[]
            source0=[]        
            record=[]
            context=''
            for i in range(0,len(pattern)):
                result=re.findall(pattern[i],sent,re.I)
                if i0>0:
                    context=context+doc[i0-1]
                context=context+sent
                if (len(result)>0)and self._sent_check(sent) and self._context_check(context):
                    for rst in result:
                        tmp=rst
                        if len(pos[i])==2:    
                            v0,u0=self._unit_trans(float(tmp[pos[i][0]].replace(',','')),tmp[pos[i][1]])
                        elif len(pos[i])==3:
                            v0,u0=self._unit_trans([float(tmp[pos[i][0]]),float(tmp[pos[i][1]])],tmp[pos[i][2]])
                        elif len(pos[i])==4 and i==10:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][1]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        elif len(pos[i])==4 and i==0:
                            v01,u01=self._unit_trans(float(tmp[pos[i][0]]),tmp[pos[i][3]])
                            v02,u02=self._unit_trans(float(tmp[pos[i][1]]),tmp[pos[i][3]])
                            v03,u03=self._unit_trans(float(tmp[pos[i][2]]),tmp[pos[i][3]])
                        if i==10:
                            value0.append(v01)
                            value0.append(v02)
                            unit0.append(u01)
                            unit0.append(u02)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)
                        elif i==11:
                            value0.append(v0[0])
                            value0.append(v0[1])
                            unit0.append(u0)
                            unit0.append(u0)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i)   
                        elif i==0:
                            value0.append(v01)
                            value0.append(v02)
                            value0.append(v03)
                            unit0.append(u01)
                            unit0.append(u02)
                            unit0.append(u03)
                            source0.append(sent)
                            source0.append(sent)
                            source0.append(sent)
                            record.append(i)
                            record.append(i) 
                            record.append(i)
                        else:
                            value0.append(v0)
                            unit0.append(u0)
                            source0.append(sent)
                            record.append(i)
                        if i<=sep-1:
                            flag=1
                    break
            if flag==1:
                for i in range(0,len(value0)):
                    if record[i]<=sep-1:
                        value.append(value0[i])
                        unit.append(unit0[i])
                        source.append(source0[i])  
        
        value,unit,source=self._merge_equal_item(value,unit,source)
        
        return {'value':value,'unit':unit,'source':source}

def extract_data(doc,parameter):
    data={'value':[],'unit':[],'source':[]}
    d={}
    if parameter=='mat_name':
        e=Extract_mat_name()
        d=e.extract(doc)
    elif parameter=='am_type':
        e=Extract_am_type()
        d=e.extract(doc)        
    elif parameter=='am_machine':
        e=Extract_am_machine()
        d=e.extract(doc) 
    elif parameter=='direction':
        e=Extract_direction()
        d=e.extract(doc)         
    elif parameter=='scan_speed':
        e=Extract_scan_speed()
        d=e.extract(doc)         
    elif parameter=='hatch_space':
        e=Extract_hatch_space()
        d=e.extract(doc) 
    elif parameter=='layer_thickness':
        e=Extract_layer_thickness()
        d=e.extract(doc) 
    elif parameter=='preheat':
        e=Extract_preheat()
        d=e.extract(doc)         
    elif parameter=='am_env':
        e=Extract_am_env()
        d=e.extract(doc) 
    elif parameter=='layer_rot':
        e=Extract_layer_rot()
        d=e.extract(doc)         
    elif parameter=='scan_pattern':
        e=Extract_scan_pattern()
        d=e.extract(doc)  
    elif parameter=='fdstock_size':
        e=Extract_fdstock_size()
        d=e.extract(doc)      
    elif parameter=='power':
        e=Extract_power()
        d=e.extract(doc) 
    elif parameter=='voltage':
        e=Extract_voltage()
        d=e.extract(doc) 
    elif parameter=='current':
        e=Extract_current()
        d=e.extract(doc) 
    elif parameter=='speed_func':
        e=Extract_speed_func()
        d=e.extract(doc)    
    elif parameter=='pfeed_rate':
        e=Extract_pfeed_rate()
        d=e.extract(doc)    
    elif parameter=='wfeed_rate':
        e=Extract_wfeed_rate()
        d=e.extract(doc) 
    elif parameter=='heat_treat':
        e=Extract_heat_treat()
        d=e.extract(doc)  
    elif parameter=='surf_treat':
        e=Extract_surf_treat()
        d=e.extract(doc)  
    elif parameter=='fat_type':
        e=Extract_fat_type()
        d=e.extract(doc)  
    elif parameter=='fat_temp':
        e=Extract_fat_temp()
        d=e.extract(doc)              
    elif parameter=='fat_env':
        e=Extract_fat_env()
        d=e.extract(doc) 
    elif parameter=='fat_r':
        e=Extract_fat_r()
        d=e.extract(doc)
    elif parameter=='frequency':
        e=Extract_frequency()
        d=e.extract(doc)   
    elif parameter=='fat_machine':
        e=Extract_fat_machine()
        d=e.extract(doc)
    elif parameter=='fat_standard':
        e=Extract_fat_standard()
        d=e.extract(doc)      
    elif parameter=='spec_desc':
        e=Extract_spec_desc()
        d=e.extract(doc)     
    elif parameter=='load_ctrl':
        e=Extract_load_ctrl()
        d=e.extract(doc)  
    elif parameter=='modulus':
        e=Extract_modulus()
        d=e.extract(doc) 
    elif parameter=='yield_strength':
        e=Extract_yield_strength()
        d=e.extract(doc)   
    elif parameter=='tensile_strength':
        e=Extract_tensile_strength()
        d=e.extract(doc) 
    elif parameter=='elongation':
        e=Extract_elongation()
        d=e.extract(doc)  
    else:
        print('ERROR: no extraction method defined for '+parameter)
    
    data=d
    
    return data

