# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


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

   
def parse_paragraph(doc):
    text=doc.text.replace('\n','')
    text=text.strip()
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
        
        # if (hasattr(child,'attrs')):
        #     print(i,child.name,child.attrs)
        # else:
        #     print(i,child.name)
        
        if  (child.name=='div')and(hasattr(child,'attrs'))and \
              ('class' in child.attrs.keys())and('section' in child.attrs['class']):
            ids=[]
            texts=[]
            ids,texts=parse_section(child)
            idlst.extend(ids)
            textlst.extend(texts)
        elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
              child.name=='h4' or child.name=='h5' or child.name=='h6':
                  if ('main-title' in child.attrs['class']):
                      if idlst[-1][0]=='h':
                          textlst[-1]=textlst[-1]+' '+child.text
                          idlst[-1]='h2'
                  elif ('section-title' in child.attrs['class']):
                      if idlst[-1][0]=='h':
                          textlst[-1]=textlst[-1]+' '+child.text
                          idlst[-1]='h3'    
                  elif ('subsection-title' in child.attrs['class']):
                      if len(idlst)==0:
                          idlst.append(child.name)
                          textlst.append(child.text) 
                      else:
                          idlst[-1][0]=='h'
                          textlst[-1]=textlst[-1]+' '+child.text
                          idlst[-1]='h4'                           
                  elif not('Table' in child.text):
                      idlst.append(child.name)
                      textlst.append(child.text) 
        elif (child.name=='p')or(child.name=='ol')or \
            ((child.name=='div')and(hasattr(child,'attrs'))and \
              ('class' in child.attrs.keys())and('list' in child.attrs['class'])):
            texts=parse_paragraph(child)
            idlst.append('p')
            textlst.append(texts)  
 
            
    return idlst,textlst

def parse_abstract(abst):
    abstract=''
    if 'content' in abst.attrs.keys():
        abstract=abst.attrs['content']
    return abstract

def parse_keywords(para):
    keywords=[]
    if 'content' in para.attrs.keys():
        kws=para.attrs['content']
    keywords=kws.split(';')
    for i in range(0,len(keywords)):
        keywords[i]=keywords[i].strip()


    return keywords

def parse_doc(doc):
    
    idlst=[]
    textlst=[]
    title=''
    abstract=''
    keywords=[]
    # get title
    tmp=doc.find_all('meta',{'name':['dc.Title',]})
    if len(tmp)==1:
        title=tmp[0].attrs['content'].strip()
    elif len(tmp)==0:
        print("Warning: no title")
    else:
        title=tmp[0].attrs['content'].strip()
        print("Warning: multi title")
    # get abstract
    tmp0=doc.find_all('meta',{'name':['citation_abstract',]})
    if len(tmp0)>0:
        abstract=parse_abstract(tmp0[0])    
    # get keywords
    tmp0=doc.find_all('meta',{'name':['citation_keywords',]})
    if len(tmp0)>0:    
        keywords=parse_keywords(tmp0[0]) 
    
    # get section
    tmp0=doc.find_all('div',{'id':['article-body',]})
    if len(tmp0)>0: 
        # tmp=tmp0[0].find_all('section')
        for i, child in enumerate(tmp0[0].children):
            
            # if hasattr(child,'attrs'):
            #     print(child.name,child.attrs)
            # else:
            #     print(child.name)
                
            if (child.name=='div')and(hasattr(child,'attrs'))and \
                  ('class' in child.attrs.keys())and('section' in child.attrs['class']):
                tmp_id,tmp_text=parse_section(child)
                if len(tmp_id)>0:
                    idlst.append(tmp_id)
                    textlst.append(tmp_text)

    return title,abstract,keywords,idlst,textlst




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