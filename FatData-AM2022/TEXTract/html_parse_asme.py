# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

   
def parse_paragraph(doc):
    text=doc.text.replace('\n','')
    return text

def parse_ol(doc):
    idlst=[]
    textlst=[]
    for i, child in enumerate(doc.children):
        if not (child.name is None):
            idlst.append(child.name)
            textlst.append(child.text.replace('\n',''))
    return idlst,textlst
    
def parse_section(doc):
    textlst=[]
    idlst=[] 
    skip=[]
    title=''
    for i, child in enumerate(doc.children):
        if len(child.text.replace('\n',''))>0:
            texts=child.text.replace('\n','')
            tmp=child.find('div',class_='tablewrap')
            if not tmp is None:
                continue
            tmp=child.find('div',class_='fig-section')
            if not tmp is None:
                continue
            idlst.append('p')
            textlst.append(texts)                            

            
    return idlst,textlst

def parse_abstract(abst):
    abstract=''
    keywords=[]
    
    for i in range(0,len(abst)):
        para=abst[i]
        abstract=abstract+para.text.replace('\n','')
    
    return abstract

def parse_keywords(para):
    keywords=[]
    if len(para)>0:    
        kws=para[0].find_all('a')
        if len(kws)>0:
            for i in range(0,len(kws)):
                keywords.append(kws[i].text.strip())

        

    return keywords

def parse_doc(doc):
    
    idlst=[]
    textlst=[]
    title=''
    abstract=''
    keywords=[]
    # get title
    tmp=doc.find_all('h1',class_='article-title-main')
    if len(tmp)==1:
        title=tmp[0].text.strip()
    elif len(tmp)==0:
        print("Warning: no title")
    else:
        title=tmp[0].text.strip()
        print("Warning: multi title")
    # get abstract
    tmp0=doc.find_all('section',class_='abstract')
    abst=parse_abstract(tmp0)    
    abstract=abst
    tmp0=doc.find_all('div',class_='content-metadata-keywords')
    kw=parse_keywords(tmp0)    
    keywords=kw 
    if len(keywords)==0:
        tmp0=doc.find_all('meta',{'name':['citation_keyword',]})
        for mt in tmp0:
            if 'content' in mt.attrs.keys():
                keywords.append(mt.attrs['content'])
    if len(keywords)==0:
        print('no keyword')
    # get section
    tmp0=doc.find_all('div',{'data-widgetname':'ArticleFulltext'})
    if len(tmp0)==0:
        print('no full text found')
    elif len(tmp0)>1:
        print('multiple full text found')
    else:
        for i, child in enumerate(tmp0[0].children):
            if child.name=='h2':
                idlst.append([])
                textlst.append([])
                idlst[-1].append(child.name)
                textlst[-1].append(child.text)  
            elif child.name=='h3' or child.name=='h4' or child.name=='h5' or child.name=='h6':
                     idlst[-1].append(child.name)
                     textlst[-1].append(child.text)   
            elif (child.name=='div')and(not 'class' in child.attrs.keys()):
                    tmp_id,tmp_text=parse_section(child)
                    idlst[-1].extend(tmp_id)
                    textlst[-1].extend(tmp_text)              

    
        
    return title,abstract,keywords,idlst,textlst


def section_struct(ids,texts):
    sec={'sec_title':'','content':[]}
    minid=100
    record=[]
    ct=0
    # get the minimum id of paragraph
    for i in range(0,len(ids)):
        if ids[i][0]=='h':
            ct=ct+1
            current=int(ids[i][1:])
            if current<minid:
                minid=current
                
    for i in range(0,len(ids)):
        if ids[i][0]=='h':
            current=int(ids[i][1:])
            if current==minid:
                record.append(i)

    if len(record)<=1:
        for i in range(0,len(ids)):
            if (ids[i][0]=='h')and(int(ids[i][1:])==minid):
                sec['sec_title']=texts[i]
            elif (ids[i][0]=='h')and(int(ids[i][1:])>minid):
                tmp=section_struct(ids[i:],texts[i:])
                sec['content'].append(tmp['content'])
                return sec
            else:
                sec['content'].append(texts[i])
        return sec
    else:            
        for i in range(0,len(record)-1):
            sec['content'].append(section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
        sec['content'].append(section_struct(ids[record[-1]:],texts[record[-1]:]))
    return sec


def doc_struct(title,abstract,keywords,ids,texts,path,file,doi):
    doc={}
    doc['title']=title
    doc['abstract']=abstract
    doc['keywords']=keywords
    doc['path']=path
    doc['file']=file
    doc['doi']=doi
    doc['content']=[]
    for i in range(0,len(ids)):
        doc['content'].append(section_struct(ids[i],texts[i]))
    return doc



path=''
file=''
doc_dict={}

leng=len(file)
if leng>5 and file[leng-5:leng]=='.html': 
    f=open(path+file,'r',encoding='utf-8')
    doc=BeautifulSoup(f,"lxml")
    f.close()
    try:
        title,abstract,keywords,ids,texts=parse_doc(doc)
        ifsuccess=1
    except:
        ifsuccess=0
   
    if ifsuccess:
        doc_dict[file]=doc_struct(title,abstract,keywords,ids,texts,path,file,'')
    else:
        print("PRASE ERROR")
