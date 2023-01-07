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
        # print(i,child.name)
        # if (hasattr(child,'attrs')) and  ('id' in child.attrs.keys()):
        #     if ifskip(child.attrs['id']):
        #         continue
        #     print(child.attrs['id'])
        if child.name=='section':
            ids=[]
            texts=[]
            ids,texts=parse_section(child)
            idlst.extend(ids)
            textlst.extend(texts)
        elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
             child.name=='h4' or child.name=='h5' or child.name=='h6':
                 title=child.text
                 idlst.append(child.name)
                 textlst.append(title)                 
        elif child.name=='p':
            texts=parse_paragraph(child)
            idlst.append('p')
            textlst.append(texts)
        elif child.name=='ol':
            ids,texts=parse_ol(child)
            idlst.extend(ids)
            textlst.extend(texts)            
    return idlst,textlst

def parse_abstract(abst):
    abstract=''
    keywords=[]
    
    #abstract=abst.text.replace('\n','')
    tmp=abst.find_all('p')
    for i in range(0,len(tmp)):
        para=tmp[i]
        for j in range(0,len(para)):
            abstract=abstract+para.text.replace('\n','')
    
    # tmp=abst.find_all('div',class_='article-section__content en main')
    # if len(tmp)==0:
    #     tmp=abst.find_all('div',class_="article-section__content de main")
    # if len(tmp)==0:
        # print('ABSTRACT ERROR')
    # else:
        # para=tmp[0].find('p')
        # abstract=para.text.replace('\n','')
    # kws=tmp[0].find_all('li',class_='c-article-subject-list__subject')
    # for k in kws:
    #     keywords.append(k.text)
    
    return abstract,keywords

def parse_doc(doc):
    
    idlst=[]
    textlst=[]
    title=''
    abstract=''
    keywords=[]
    # get title
    tmp=doc.find_all('h1',class_='citation__title')
    if len(tmp)==1:
        title=tmp[0].text
    else:
        title=tmp[0].text
        print("Warning: multi title")
    # get abstract
    tmp0=doc.find_all('div',class_='abstract-group')
    if len(tmp0)==0:
        tmp0=doc.find_all('section',class_='article-section__abstract')
    if len(tmp0)>0:
        tmp=tmp0[0].find_all('section')
        for sec in tmp:
            if ('class' in sec.attrs.keys()):
                if ('article-section__contect' in sec.attrs['class'])or \
                   ('article-section__abstract' in sec.attrs['class']):
                    abst,keywords=parse_abstract(sec)    
                    abstract=abstract+abst
    # get section
    tmp0=doc.find_all('section',class_='article-section__full')
    if len(tmp0)>0:
        tmp=tmp0[0].find_all('section')
        for sec in tmp:
            if ('class' in sec.attrs.keys()):
                # print(sec.attrs['class'])
                if ('article-section__content' in sec.attrs['class']):
                    tmp_id,tmp_text=parse_section(sec)
                    idlst.append(tmp_id)
                    textlst.append(tmp_text)

                
    # tmp=doc.find_all('section')
    # for sec in tmp:
    #     if ('class' in sec.attrs.keys()):
    #         # print(sec.attrs['class'])
    #         if ('article-section__content' in sec.attrs['class']):
    #             tmp_id,tmp_text=parse_section(sec)
    #             idlst.append(tmp_id)
    #             textlst.append(tmp_text)
    #         elif ('article-section__abstract' in sec.attrs['class']):
    #             abstract,keywords=parse_abstract(sec)
    
        
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