# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
import json
import os
from openpyxl import load_workbook,Workbook

def blank_line(text):
    ifblank=True
    for i in range(0,len(text)):
        if not ((text[i]==' ')or(text[i]=='\n')):
            ifblank=False
            return ifblank
    return ifblank

def parse_para(para):
    text=""
    if para.hasChildNodes():
        for c in para.childNodes:
            text1=parse_para(c)
            ifblank=blank_line(text1)
            if (len(text1)>0)and( not ifblank ):
                text=text+text1
    else:
        if hasattr(para,"data"):
            text=para.data
            #print(text)
    return text

def get_item(obj,tag):
    text=""
    lst=obj.getElementsByTagName(tag)
    if len(lst)==1:
        text=lst[0].childNodes[0].data
    return text


def parse_section(sec):
    seclst={'sec_title':'','content':[]}
    title=""
    textlst=[]
    idlst=[]
    sec_id=sec.getAttribute("id")
    ifmatch=False
    for cn in sec.childNodes:
        if hasattr(cn,"tagName"):
            tag=cn.tagName
            if tag=="ce:label":
                title=title+parse_para(cn)
            elif tag=="ce:section-title":
                title2=parse_para(cn)
                title=title+" "+title2
            elif tag=="ce:section":
                seclst1=parse_section(cn)
                seclst['content'].append(seclst1)
            elif tag=="ce:para":
                para_id=cn.getAttribute("id")
                para_text=parse_para(cn)
                seclst['content'].append(para_text)


    seclst['sec_title']=title         
    return seclst

def parse_doc(doc):
    
    title=''
    abstract=''
    keywords=[]
    sections=[]
    doi=''
    artflag=1       # Flag: if article exist, check by terms in VAR level
    txttype=""
    
    tmp0=doc.getElementsByTagName("coredata")
    if not (len(tmp0)==1):
        print("coredata NOT EXIST") 
    else:
        tmp1=tmp0[0].getElementsByTagName("dc:title")
        if (len(tmp1)==1):
            title=tmp1[0].childNodes[0].data.strip()
        tmp1=tmp0[0].getElementsByTagName("prism:doi")
        if (len(tmp1)==1):
            doi=tmp1[0].childNodes[0].data.strip()
        tmp1=tmp0[0].getElementsByTagName("dc:description")
        if (len(tmp1)==1):
            abstract=tmp1[0].childNodes[0].data.strip()
        tmp1=tmp0[0].getElementsByTagName("dcterms:subject")  
        if (len(tmp1)>0):
            for i in range(0,len(tmp1)):
                keywords.append(tmp1[i].childNodes[0].data.strip())
            
    levels=["xocs:doc","xocs:serial-item","article","body","ce:sections"]
    tmp0=doc.getElementsByTagName("originalText")
    if not (len(tmp0)==1):
        print("originalText NOT EXIST")
        return 
    for level in levels:
        tmp1=tmp0[0].getElementsByTagName(level)
        if not (len(tmp1)==1):
            print(level+" NOT EXIST")
            artflag=0
            break
        tmp0=tmp1
    if artflag:
        cn=tmp0[0].childNodes
        for i in range(0,len(cn)):
            # parse section
            if hasattr(cn[i],'tagName')and(cn[i].tagName=='ce:section'):
                sec=parse_section(cn[i])
                sections.append(sec)
        txttype="article"
    else:
        tmp0=doc.getElementsByTagName("originalText")
        if not (len(tmp0)==1):
            return
        tmp1=tmp0[0].getElementsByTagName("xocs:doc")
        if not (len(tmp1)==1):
            return
        tmp2=tmp1[0].getElementsByTagName("xocs:rawtext")
        if not (len(tmp2)==1):
            return
        if hasattr(tmp2[0].childNodes[0],"data"):
            sections.append(tmp2[0].childNodes[0].data)
                    
    return title,abstract,keywords,doi,sections



path=''
file=''
doc_dict={}

leng=len(file)
if leng>5 and file[leng-4:leng]=='.xml': 
    dom=parse(path+file)
    try:
        dom=parse(path+file)
        data=dom.documentElement
        title,abstract,keywords,doi,sections=parse_doc(data)
        ifsuccess=1
    except:
        ifsuccess=0
   
    if ifsuccess:
        doc={}
        doc['path']=path
        doc['file']=file
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['doi']=doi
        doc['content']=sections
        doc_dict[file]=doc
    else:
        print("PRASE ERROR")
