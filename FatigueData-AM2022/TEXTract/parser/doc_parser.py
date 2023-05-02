# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
from bs4 import BeautifulSoup

class Doc:
    def __init__(self,path='',file='',doi=''):
        self.path=path
        self.file=file
        self.title=''
        self.abstract=''
        self.keywords=[]
        self.doi=doi
        self.sections=[]

def parser(path,file,publisher='',doi=''):
    
    n=len(doi)
    if publisher=='elsevier' or (n>7 and doi[0:7]=='10.1016'):
        obj=XML_elsevier(path,file,doi)
        obj.parse()
    elif publisher=='asme' or (n>7 and doi[0:7]=='10.1115'):
        obj=HTML_asme(path,file,doi)
        obj.parse()        
    elif publisher=='emerald' or (n>7 and doi[0:7]=='10.1108'):
        obj=HTML_emerald(path,file,doi)
        obj.parse()        
    elif publisher=='iop' or (n>7 and doi[0:7]=='10.1088'):
        obj=HTML_iop(path,file,doi)      
        obj.parse()        
    elif publisher=='mdpi' or (n>7 and doi[0:7]=='10.3390'):
        obj=HTML_mdpi(path,file,doi)
        obj.parse()        
    elif publisher=='nature' or (n>7 and doi[0:7]=='10.1038'):
        obj=HTML_nature(path,file,doi) 
        obj.parse()        
    elif publisher=='sage' or (n>7 and doi[0:7]=='10.1177'):
        obj=HTML_sage(path,file,doi)
        obj.parse()        
    elif publisher=='spie' or (n>7 and doi[0:7]=='10.1117'):
        obj=HTML_spie(path,file,doi)
        obj.parse()        
    elif publisher=='springer' or (n>7 and (doi[0:7]=='10.1007' or doi[0:7]=='10.1557')):
        obj=HTML_springer(path,file,doi)
        obj.parse()        
    elif publisher=='taylorfrancis' or (n>7 and doi[0:7]=='10.1080'):
        obj=HTML_taylorfrancis(path,file,doi)
        obj.parse()        
    elif publisher=='wiley' or (n>7 and (doi[0:7]=='10.1002' or doi[0:7]=='10.1111')):
        obj=HTML_wiley(path,file,doi)
        obj.parse()        
    else:
        print('ERROR: publisher not supported currently')
        return Doc(path,file,doi)
    
    return obj
        
# # XML parser for Elsevier
class XML_elsevier(Doc):
    
    def _blank_line(self,text):
        ifblank=True
        for i in range(0,len(text)):
            if not ((text[i]==' ')or(text[i]=='\n')):
                ifblank=False
                return ifblank
        return ifblank
    
    def _parse_para(self,para):
        text=""
        if para.hasChildNodes():
            for c in para.childNodes:
                text1=self._parse_para(c)
                ifblank=self._blank_line(text1)
                if (len(text1)>0)and( not ifblank ):
                    text=text+text1
        else:
            if hasattr(para,"data"):
                text=para.data
                #print(text)
        return text
    
    def _get_item(obj,tag):
        text=""
        lst=obj.getElementsByTagName(tag)
        if len(lst)==1:
            text=lst[0].childNodes[0].data
        return text
    
    def _parse_section(self,sec):
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
                    title=title+self._parse_para(cn)
                elif tag=="ce:section-title":
                    title2=self._parse_para(cn)
                    title=title+" "+title2
                elif tag=="ce:section":
                    seclst1=self._parse_section(cn)
                    seclst['content'].append(seclst1)
                elif tag=="ce:para":
                    para_id=cn.getAttribute("id")
                    para_text=self._parse_para(cn)
                    seclst['content'].append(para_text)
    
        seclst['sec_title']=title         
        return seclst
    
    
    def parse_doc(self):
        
        self.title=''
        self.abstract=''
        self.keywords=[]
        self.sections=[]
        self.doi=''
        artflag=1       # Flag: if article exist, check by terms in VAR level
        txttype=""
        
        path=self.path
        file=self.file
        title=''
        abstract=''
        keywords=[]
        sections=[]
        doi=''
        
        leng=len(file)
        ifsuccess=0
        if leng>5 and file[leng-4:leng]=='.xml':         
            try:
                dom=parse(path+file)
                doc=dom.documentElement
                ifsuccess=1
            except:
                ifsuccess=0        
        
        if not ifsuccess:
            return
        
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
                    sec=self._parse_section(cn[i])
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
               
        self.title=title
        self.abstract=abstract
        self.keywords=keywords
        self.sections=sections
        self.doi=doi
        

class HTML_asme(Doc):   

    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
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
    
    def _parse_abstract(self,abst):
        abstract=''
        
        for i in range(0,len(abst)):
            para=abst[i]
            abstract=abstract+para.text.replace('\n','')
        
        return abstract
    
    def _parse_keywords(self,para):
        keywords=[]
        if len(para)>0:    
            kws=para[0].find_all('a')
            if len(kws)>0:
                for i in range(0,len(kws)):
                    keywords.append(kws[i].text.strip())
    
            
    
        return keywords
    
    
    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc

    def _parse_doc(self,doc):

        self.title=''
        self.abstract=''
        self.keywords=[]
        self.sections=[]
        self.doi=''
        
        
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
        abst=self._parse_abstract(tmp0)    
        abstract=abst
        tmp0=doc.find_all('div',class_='content-metadata-keywords')
        kw=self._parse_keywords(tmp0)    
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
                        tmp_id,tmp_text=self._parse_section(child)
                        idlst[-1].extend(tmp_id)
                        textlst[-1].extend(tmp_text)              
    
        
            
        return title,abstract,keywords,idlst,textlst

    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']

# # Parser for Emerald                
class HTML_emerald(Doc): 
   
    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
        title=''
        for i, child in enumerate(doc.children):
            
            # if (hasattr(child,'attrs')):
            #     print(i,child.name,child.attrs)
            # else:
            #     print(i,child.name)
            
            if  (child.name=='section'):
                ids=[]
                texts=[]
                ids,texts=self._parse_section(child)
                idlst.extend(ids)
                textlst.extend(texts)
            elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
                  child.name=='h4' or child.name=='h5' or child.name=='h6':
                      title=child.text
                      idlst.append(child.name)
                      textlst.append(title) 
            elif (child.name=='p')or (child.name=='ul')or(child.name=='sub'):
                texts=child.text.replace('\n','')
                idlst.append('p')
                textlst.append(texts)                            
            elif (child.name=='div') and (hasattr(child,'attrs'))and('md-4' in child.attrs['class']):
                continue
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        
        abstract=abstract+abst.text.replace('\n','')
        
        return abstract
    
    def _parse_keywords(self,para):
        keywords=[]
        if hasattr(para,'attrs')and('content' in para.attrs.keys()):
            keywords=para.attrs['content'].split(',')
            for i in range(0,len(keywords)):
                keywords[i]=keywords[i].strip()
        else:
            print('Keyword error')
    
        return keywords
        
    
    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc
    
    def _parse_doc(self,doc):
        
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
        tmp0=doc.find_all('section',class_='Abstract')
        abst=self._parse_abstract(tmp0[0])    
        abstract=abst
        #keywords
        tmp=doc.find_all('meta',{'name':['keywords',]})
        if len(tmp)==1:
            keywords=self._parse_keywords(tmp[0])
        elif len(tmp)==0:
            print("Warning: no title")
        else:
            keywords=self._parse_keywords(tmp[0])
            print("Warning: multi title")   
        
        # get section
        tmp0=doc.find_all('section',class_='mb-5 Body')
        if len(tmp0)>0: 
            # tmp=tmp0[0].find_all('section')
            for i, child in enumerate(tmp0[0].children):
                # if hasattr(child,'attrs'):
                #     print(child.name,child.attrs)
                # else:
                #     print(child.name)
    
                if child.name=='section':
                    tmp_id,tmp_text=self._parse_section(child)
                    if len(tmp_id)>0:
                        idlst.append(tmp_id)
                        textlst.append(tmp_text)
         
        return title,abstract,keywords,idlst,textlst
    
    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']

# # Parser for IOP                
class HTML_iop(Doc): 
   
    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
        title=''
        for i, child in enumerate(doc.children):
            
            if  (child.name=='div')and(hasattr(child,'attrs'))and \
                 ('class' in child.attrs.keys())and('article-text' in child.attrs['class']):
                ids=[]
                texts=[]
                ids,texts=self._parse_section(child)
                idlst.extend(ids)
                textlst.extend(texts)
            elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
                  child.name=='h4' or child.name=='h5' or child.name=='h6':
                      title=child.text
                      idlst.append(child.name)
                      textlst.append(title) 
            elif (child.name=='p'):
                texts=self._parse_paragraph(child)
                idlst.append('p')
                textlst.append(texts)                            
    
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        
        abstract=abstract+abst.text.replace('\n','')
        
        return abstract
    
    def _parse_keywords(self,para):
        keywords=[]
        if hasattr(para,'attrs')and('content' in para.attrs.keys()):
            keywords=para.attrs['content'].split(',')
            for i in range(0,len(keywords)):
                keywords[i]=keywords[i].strip()
        else:
            print('Keyword error')
    
        return keywords
    
    def _parse_doc(self,doc):
        
        idlst=[]
        textlst=[]
        title=''
        abstract=''
        keywords=[]
        # get title
        tmp=doc.find_all('meta',{'name':['citation_title',]})
        if len(tmp)==1:
            title=tmp[0].attrs['content'].strip()
        elif len(tmp)==0:
            print("Warning: no title")
        else:
            title=tmp[0].attrs['content'].strip()
            print("Warning: multi title")
        # get abstract
        tmp0=doc.find_all('div',class_='wd-jnl-art-abstract')
        abst=self._parse_abstract(tmp0[0])    
        abstract=abst
      
        
        # get section
        tmp0=doc.find_all('div',{'itemprop':['articleBody',]})
        if len(tmp0)>0: 
            # tmp=tmp0[0].find_all('section')
            for i, child in enumerate(tmp0[0].children):
                    
                if child.name=='h2':
                    idlst.append([])
                    textlst.append([])
                    idlst[-1].append(child.name)
                    textlst[-1].append(child.text)
                elif (child.name=='div')and(hasattr(child,'attrs'))and \
                     ('class' in child.attrs.keys())and('article-text' in child.attrs['class']):
                    tmp_id,tmp_text=self._parse_section(child)
                    if len(tmp_id)>0:
                        idlst[-1].extend(tmp_id)
                        textlst[-1].extend(tmp_text)
        
            
        return title,abstract,keywords,idlst,textlst
    
    
    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc


    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']

# # Parser for MDPI
class HTML_mdpi(Doc): 

    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
        title=''
        for i, child in enumerate(doc.children):
            # print(i,child.name)
            # if (hasattr(child,'attrs')) and  ('id' in child.attrs.keys()):
            #     if ifskip(child.attrs['id']):
            #         continue
            #     print(child.attrs['id'])
            if  (child.name=='section'):
                ids=[]
                texts=[]
                ids,texts=self._parse_section(child)
                idlst.extend(ids)
                textlst.extend(texts)
            elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
                 child.name=='h4' or child.name=='h5' or child.name=='h6':
                     title=child.text
                     idlst.append(child.name)
                     textlst.append(title)   
            elif (child.name=='div')and('class' in child.attrs.keys())and('html-p' in child.attrs['class']):
                texts=child.text.replace('\n','')
                idlst.append('p')
                textlst.append(texts)                            
    
                
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        
        for i in range(0,len(abst)):
            para=abst[i]
            abstract=abstract+para.text.replace('\n','')
        
        return abstract
    
    def _parse_keywords(self,para):
        keywords=[]
        if len(para)==1:
            tmp=para[0].find('span',{'itemprop':['keywords']})
            if len(tmp)>0:
                keywords=tmp.text.split(';')
            for i in range(0,len(keywords)):
                keywords[i]=keywords[i].strip()
        else:
            print('Keyword error')
    
        return keywords
    
    def _parse_doc(self,doc):
        
        idlst=[]
        textlst=[]
        title=''
        abstract=''
        keywords=[]
        # get title
        tmp=doc.find_all('h1',class_='title hypothesis_container')
        if len(tmp)==1:
            title=tmp[0].text.strip()
        elif len(tmp)==0:
            print("Warning: no title")
        else:
            title=tmp[0].text.strip()
            print("Warning: multi title")
        # get abstract
        tmp0=doc.find_all('div',class_='art-abstract')
        abst=self._parse_abstract(tmp0)    
        abstract=abst
        tmp0=doc.find_all('div',class_='art-keywords')
        kw=self._parse_keywords(tmp0)    
        keywords=kw   
        
        # get section
        tmp0=doc.find_all('div',class_='html-body')
        if len(tmp0)>0:
            tmp=tmp0[0].find_all('section')
            for sec in tmp:
                tmp1=sec.find('h2',{'data-nested':['1',]})
                if not tmp1 is None:
                    tmp_id,tmp_text=self._parse_section(sec)
                    idlst.append(tmp_id)
                    textlst.append(tmp_text)
        
            
        return title,abstract,keywords,idlst,textlst
    
    
    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc



    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']


# # Parser for Nature                
class HTML_nature(Doc): 
    
    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc
    
    
    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        text=text.strip()
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
        title=''
        
        for i, child in enumerate(doc.children):
            
            if  (child.name=='div')and(hasattr(child,'attrs'))and \
                  ('class' in child.attrs.keys())and('c-article-section__content' in child.attrs['class']):
                ids=[]
                texts=[]
                ids,texts=self._parse_section(child)
                idlst.extend(ids)
                textlst.extend(texts)
            elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
                  child.name=='h4' or child.name=='h5' or child.name=='h6':
                      title=child.text
                      idlst.append(child.name)
                      textlst.append(title) 
            elif (child.name=='p')or(child.name=='ol'):
                texts=self._parse_paragraph(child)
                idlst.append('p')
                textlst.append(texts)  
            elif (child.name=='div')and(hasattr(child,'attrs'))and \
                  ('class' in child.attrs.keys())and('c-article-equation' in child.attrs['class']):                        
                texts=self._parse_paragraph(child)
                idlst.append('p')
                textlst.append(texts)  
                
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        abstract=abst.text.replace('\n','').strip()
        
        return abstract
    
    def _parse_keywords(self,para):
        keywords=[]
        tmp=para.find_all('a')
        if not tmp is None:
            for i in range(0,len(tmp)):
                keywords.append(tmp[i].text.strip())
        else:
            print('no keywords')
    
        return keywords
    
    def _parse_doc(self,doc):
        
        idlst=[]
        textlst=[]
        title=''
        abstract=''
        keywords=[]
        # get title
        tmp=doc.find_all('meta',{'name':['citation_title',]})
        if len(tmp)==1:
            title=tmp[0].attrs['content'].strip()
        elif len(tmp)==0:
            print("Warning: no title")
        else:
            title=tmp[0].attrs['content'].strip()
            print("Warning: multi title")
        # get abstract
        tmp0=doc.find_all('div',class_='c-article-section__content')
        abst=self._parse_abstract(tmp0[0])    
        abstract=abst
        
        # get section
        tmp0=doc.find_all('div',class_='main-content')
        if len(tmp0)>0: 
            # tmp=tmp0[0].find_all('section')
            tmp=tmp0[0].find_all('div',class_='c-article-section')
            if len(tmp)==0:
                print('no section')
            for i in range(0,len(tmp)):
                        
                tmp_id,tmp_text=self._parse_section(tmp[i])
                idlst.append(tmp_id)
                textlst.append(tmp_text)
    
        return title,abstract,keywords,idlst,textlst
    
    
    
    
    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']

# # Parser for Sage
class HTML_sage(Doc): 
   
    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        text=text.strip()
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
        title=''
        for i, child in enumerate(doc.children):
            
            # if (hasattr(child,'attrs')):
            #     print(i,child.name,child.attrs)
            # else:
            #     print(i,child.name)
            
            if  (child.name=='div')and(hasattr(child,'attrs'))and \
                 ('class' in child.attrs.keys())and('article-text' in child.attrs['class']):
                ids=[]
                texts=[]
                ids,texts=self._parse_section(child)
                idlst.extend(ids)
                textlst.extend(texts)
            elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
                  child.name=='h4' or child.name=='h5' or child.name=='h6':
                      title=child.text
                      idlst.append(child.name)
                      textlst.append(title) 
            elif (child.name=='p'):
                texts=self._parse_paragraph(child)
                idlst.append('p')
                textlst.append(texts)                            
    
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        keywords=[]
        tmp=abst.find_all('p')
        n=len(tmp)
        if n==0:
            print('no abstract')
        elif n==1:
            abstract=tmp[0].text
        elif n==2:
            abstract=tmp[0].text
            keywords=self._parse_keywords(tmp[1])
        elif n>2:
            print('warning: multiple paragraphs in abstract section')
            for i in range(0,n-1):
                abstract=abstract+tmp[i].text
            keywords=self._parse_keywords(tmp[n-1])
            
        return abstract,keywords
    
    def _parse_keywords(self,para):
        keywords=[]
        tmp=para.find_all('a')
        if not tmp is None:
            for i in range(0,len(tmp)):
                keywords.append(tmp[i].text.strip())
        else:
            print('no keywords')
    
        return keywords
    
    def _parse_doc(self,doc):
        
        idlst=[]
        textlst=[]
        title=''
        abstract=''
        keywords=[]
        # get title
        tmp=doc.find_all('div',class_='publicationContentTitle')
        if len(tmp)==1:
            title=tmp[0].text.strip()
        elif len(tmp)==0:
            print("Warning: no title")
        else:
            title=tmp[0].text.strip()
            print("Warning: multi title")
        # get abstract
        tmp0=doc.find_all('div',{'id':['abstract',]})
        abstract,keywords=self._parse_abstract(tmp0[0])      
        
        # get section
        tmp0=doc.find_all('div',class_='content')
        if len(tmp0)>0: 
            # tmp=tmp0[0].find_all('section')
            for i, child in enumerate(tmp0[0].children):
                
                # if not child.name is None:
                #     if hasattr(child,'attrs'):
                #         print(child.name,child.attrs)
                #     else:
                #         print(child.name)
                    
                if child.name=='h4':
                    idlst.append([])
                    textlst.append([])
                    idlst[-1].append(child.name)
                    textlst[-1].append(child.text.strip())
                elif (child.name=='div')and(hasattr(child,'attrs'))and \
                      ('class' in child.attrs.keys())and('type12' in child.attrs['class']):
                    idlst[-1].append('h5')
                    textlst[-1].append(child.text.strip())
                elif (child.name=='p'):
                    idlst[-1].append(child.name)
                    textlst[-1].append(self._parse_paragraph(child))            
            
        return title,abstract,keywords,idlst,textlst
    
    
    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc
    
    
    
    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']

# # Parser for SPIE
class HTML_spie(Doc): 

    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc
    
       
    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        text=text.strip()
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
        
        for i, child in enumerate(doc.children):
            
            # if (hasattr(child,'attrs')):
            #     print(i,child.name,child.attrs)
            # else:
            #     print(i,child.name)
            
            if  (child.name=='div')and(hasattr(child,'attrs'))and \
                  ('class' in child.attrs.keys())and('section' in child.attrs['class']):
                ids=[]
                texts=[]
                ids,texts=self._parse_section(child)
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
                texts=self._parse_paragraph(child)
                idlst.append('p')
                textlst.append(texts)  
     
                
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        if 'content' in abst.attrs.keys():
            abstract=abst.attrs['content']
        return abstract
    
    def _parse_keywords(self,para):
        keywords=[]
        if 'content' in para.attrs.keys():
            kws=para.attrs['content']
        keywords=kws.split(';')
        for i in range(0,len(keywords)):
            keywords[i]=keywords[i].strip()
    
    
        return keywords
    
    def _parse_doc(self,doc):
        
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
            abstract=self._parse_abstract(tmp0[0])    
        # get keywords
        tmp0=doc.find_all('meta',{'name':['citation_keywords',]})
        if len(tmp0)>0:    
            keywords=self._parse_keywords(tmp0[0]) 
        
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
                    tmp_id,tmp_text=self._parse_section(child)
                    if len(tmp_id)>0:
                        idlst.append(tmp_id)
                        textlst.append(tmp_text)
    
        return title,abstract,keywords,idlst,textlst
    
    
    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']                

# # Parser for springer
class HTML_springer(Doc): 

    def _ifskip(self,string):
        flag=0
        stop=['abbre','Bib','Ack','author','affiliation','corresponding', \
              'editor','right','info','cite','url']
        for sw in stop:
            if sw in string:
                flag=1
                break
        
        return flag
    
    def _ifskip_section(self,string):
        flag=0
        stop=['abbreviation','references','acknow','author information','editor information', \
              'rights and permissions','copyright information','about this paper','abstract',\
              'additional information','ethics','funding','notes','supplementary','about this article',\
              'avail']
        string=string.lower()
        for sw in stop:
            if sw in string:
                flag=1
                break
        
        return flag
       
    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
        title=''
        for i, child in enumerate(doc.children):
            # print(i,child.name)
            # if (hasattr(child,'attrs')) and  ('id' in child.attrs.keys()):
            #     if ifskip(child.attrs['id']):
            #         continue
            #     print(child.attrs['id'])
            if child.name=='div':
                ids=[]
                texts=[]
                if 'class' in child.attrs.keys():
                    if child.attrs['class'][0]=='c-article-equation__number':
                        ids.append('eq_num')
                        texts.append(child.text)
                    elif child.attrs['class'][0]=='c-article-equation':
                        ids.append('eq')
                        texts.append(child.text)   
                    else:
                        ids,texts=self._parse_section(child)
                else:
                    ids,texts=self._parse_section(child)
                idlst.extend(ids)
                textlst.extend(texts)
            elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
                 child.name=='h4' or child.name=='h5' or child.name=='h6':
                     title=child.text
                     idlst.append(child.name)
                     textlst.append(title)                 
            elif child.name=='p':
                texts=self._parse_paragraph(child)
                idlst.append('p')
                textlst.append(texts)
            elif child.name=='ol':
                ids,texts=self._parse_ol(child)
                idlst.extend(ids)
                textlst.extend(texts)            
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        keywords=[]
        tmp=abst.find_all('div',class_="c-article-section__content")
        para=tmp[0].find('p')
        abstract=para.text.replace('\n','')
        kws=tmp[0].find_all('li',class_='c-article-subject-list__subject')
        for k in kws:
            keywords.append(k.text)
        
        return abstract,keywords
    
    def _parse_doc(self,doc):
        
        idlst=[]
        textlst=[]
        title=''
        abstract=''
        keywords=[]
        # get title
        tmp=doc.find_all('h1',class_='c-article-title')
        if len(tmp)==1:
            title=tmp[0].text
        else:
            title=tmp[0].text
            print("Warning: multi title")
        
         
        # get section
        tmp=doc.find_all('section')
        for sec in tmp:
            #print(sec.attrs['data-title'])
            if ('data-title' in sec.attrs.keys())and(not self._ifskip_section(sec.attrs['data-title'])):
                tmp_id,tmp_text=self._parse_section(sec)
                idlst.append(tmp_id)
                textlst.append(tmp_text)
            elif ('data-title' in sec.attrs.keys())and('Abstract' in sec.attrs['data-title']):
                abstract,keywords=self._parse_abstract(sec)
        
            
        return title,abstract,keywords,idlst,textlst
    
    
    def _section_struct(self,ids,texts):
        sec={'sec_title':'','content':[]}
        minid=100
        record=[]
        ct=0
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
    
        if len(record)==1:
            for i in range(0,len(ids)):
                if (ids[i][0]=='h')and(int(ids[i][1:])==minid):
                    sec['sec_title']=texts[i]
                elif (ids[i][0]=='h')and(int(ids[i][1:])>minid):
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc
    
    
    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']

# # Parser for Taylor & Franics            
class HTML_taylorfrancis(Doc): 
   
    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
        title=''
        for i, child in enumerate(doc.children):
            
            # if (hasattr(child,'attrs')):
            #     print(i,child.name,child.attrs)
            # else:
            #     print(i,child.name)
            
            if  (child.name=='div')and('class' in child.attrs.keys())and('NLM_sec' in child.attrs['class']):
                ids=[]
                texts=[]
                ids,texts=self._parse_section(child)
                idlst.extend(ids)
                textlst.extend(texts)
            elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
                  child.name=='h4' or child.name=='h5' or child.name=='h6':
                      title=child.text
                      idlst.append(child.name)
                      textlst.append(title) 
            elif (child.name=='p')or (child.name=='ul'):
                texts=child.text.replace('\n','')
                idlst.append('p')
                textlst.append(texts)                            
    
                
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        tmp=abst.find_all('p')
        for i in range(0,len(tmp)):
            para=tmp[i]
            if hasattr(para,'attrs')and('class' in para.attrs.keys())and('summary-title' in para.attrs['class']):
                continue
            else:
                abstract=abstract+para.text.replace('\n','')
        
        return abstract
    
    def _parse_keywords(self,para):
        keywords=[]
        if len(para)==1:
            tmp=para[0].find_all('a')
            for i in range(0,len(tmp)):
                keywords.append(tmp[i].text.strip())
        else:
            print('Keyword error')
    
        return keywords
    
    def _parse_doc(self,doc):
        
        idlst=[]
        textlst=[]
        title=''
        abstract=''
        keywords=[]
        # get title
        tmp=doc.find_all('span',class_='hlFld-title')
        if len(tmp)==1:
            title=tmp[0].text.strip()
        elif len(tmp)==0:
            print("Warning: no title")
        else:
            title=tmp[0].text.strip()
            print("Warning: multi title")
        # get abstract
        tmp0=doc.find_all('div',class_='abstractSection')
        abst=self._parse_abstract(tmp0[0])    
        abstract=abst
        tmp0=doc.find_all('div',class_='abstractKeywords')
        kw=self._parse_keywords(tmp0)    
        keywords=kw   
        
        # get section
        tmp0=doc.find_all('div',class_='hlFld-Fulltext')
        if len(tmp0)>0: 
            # tmp=tmp0[0].find_all('section')
            for i, child in enumerate(tmp0[0].children):
                # if hasattr(child,'attrs'):
                #     print(child.name,child.attrs)
                # else:
                #     print(child.name)
                # tmp1=sec.find('h2',{'data-nested':['1',]})
                if hasattr(child,'attrs') and ('NLM_sec' in child.attrs['class']):
                    tmp_id,tmp_text=self._parse_section(child)
                    idlst.append(tmp_id)
                    textlst.append(tmp_text)
        
            
        return title,abstract,keywords,idlst,textlst
    
    
    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc
    
    
    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']

# # Parser for Wiley
class HTML_wiley(Doc): 
   
    def _parse_paragraph(self,doc):
        text=doc.text.replace('\n','')
        return text
    
    def _parse_ol(self,doc):
        idlst=[]
        textlst=[]
        for i, child in enumerate(doc.children):
            if not (child.name is None):
                idlst.append(child.name)
                textlst.append(child.text.replace('\n',''))
        return idlst,textlst
        
    def _parse_section(self,doc):
        textlst=[]
        idlst=[] 
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
                ids,texts=self._parse_section(child)
                idlst.extend(ids)
                textlst.extend(texts)
            elif child.name=='h1' or child.name=='h2' or child.name=='h3' or \
                 child.name=='h4' or child.name=='h5' or child.name=='h6':
                     title=child.text
                     idlst.append(child.name)
                     textlst.append(title)                 
            elif child.name=='p':
                texts=self._parse_paragraph(child)
                idlst.append('p')
                textlst.append(texts)
            elif child.name=='ol':
                ids,texts=self._parse_ol(child)
                idlst.extend(ids)
                textlst.extend(texts)            
        return idlst,textlst
    
    def _parse_abstract(self,abst):
        abstract=''
        keywords=[]
        
        #abstract=abst.text.replace('\n','')
        tmp=abst.find_all('p')
        for i in range(0,len(tmp)):
            para=tmp[i]
            for j in range(0,len(para)):
                abstract=abstract+para.text.replace('\n','')
        
        return abstract,keywords
    
    def _parse_doc(self,doc):
        
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
                        abst,keywords=self._parse_abstract(sec)    
                        abstract=abstract+abst
        # get section
        tmp0=doc.find_all('section',class_='article-section__full')
        if len(tmp0)>0:
            tmp=tmp0[0].find_all('section')
            for sec in tmp:
                if ('class' in sec.attrs.keys()):
                    # print(sec.attrs['class'])
                    if ('article-section__content' in sec.attrs['class']):
                        tmp_id,tmp_text=self._parse_section(sec)
                        idlst.append(tmp_id)
                        textlst.append(tmp_text)
    
        return title,abstract,keywords,idlst,textlst
    
    
    def _section_struct(self,ids,texts):
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
                    tmp=self._section_struct(ids[i:],texts[i:])
                    sec['content'].append(tmp['content'])
                    return sec
                else:
                    sec['content'].append(texts[i])
            return sec
        else:            
            for i in range(0,len(record)-1):
                sec['content'].append(self._section_struct(ids[record[i]:record[i+1]],texts[record[i]:record[i+1]]))
            sec['content'].append(self._section_struct(ids[record[-1]:],texts[record[-1]:]))
        return sec
    
    
    def _doc_struct(self,title,abstract,keywords,ids,texts,path,file,doi):
        doc={}
        doc['title']=title
        doc['abstract']=abstract
        doc['keywords']=keywords
        doc['path']=path
        doc['file']=file
        doc['doi']=doi
        doc['content']=[]
        for i in range(0,len(ids)):
            doc['content'].append(self._section_struct(ids[i],texts[i]))
        return doc
    
    
    def parse(self):
        path=self.path
        file=self.file
        doi=self.doi
        leng=len(file)
        data={}
        if leng>5 and file[leng-5:leng]=='.html': 
            f=open(path+file,'r',encoding='utf-8')
            doc=BeautifulSoup(f,"lxml")
            f.close()
            try:
                title,abstract,keywords,ids,texts=self._parse_doc(doc)
                ifsuccess=1
            except:
                ifsuccess=0
           
            if ifsuccess:
                data=self._doc_struct(title,abstract,keywords,ids,texts,path,file,doi)
                self.title=data['title']
                self.abstract=data['abstract']
                self.keywords=data['keywords']
                self.doi=data['doi']
                self.sections=data['content']
