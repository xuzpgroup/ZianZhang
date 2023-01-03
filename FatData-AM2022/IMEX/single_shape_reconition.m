function [ifreg,xreg,yreg,symtype,overlap]=single_shape_reconition(symbol,symcolor,row,col,box,center,ob_wh,bw,incbox,excbox,excid)
    DEBUG=0;
    nsym=numel(symbol);
    nob=numel(row);
    ssize=[];
    bwr=bw*(0-1)+1;
    size_fp=[10,10];        % size of the finger print
    n_fp=size_fp(1)*size_fp(2);   % number od pixel of the finger print
    rgb=repmat(uint8(bw*255),1,1,3);
    syb=[];
    overlap=zeros(1,nob);
    for i=1:nsym
        syb(1:10,1:10,i)=imresize(symbol{i},size_fp);
        [ssize(i,2),ssize(i,1)]=size(symbol{i});
    end
    scale=0.75;  % 0<scale<=1; 0.8
    thre_sim=0.8; %0.8
    symtype=zeros(1,nob);
    ifreg=zeros(1,nob);
    xreg=[];
    yreg=[];
    nreg=0;
    x1=[];
    x2=[];
    for i=1:nob
        if (~inboxes(center(i,:),incbox)) || (inboxes(center(i,:),excbox)) || ismember(i,excid)
            continue;
        end
        bx=box(i,:);
        bw1=imresize(bwr(bx(3):bx(4),bx(1):bx(2)),size_fp);
        siml=[];
        for j=1:nsym
            fsize=compare_boxsize(ob_wh(i,:),ssize(j,:),scale);
            if fsize==1
                siml(j)=(n_fp-compare_symbol(bw1,syb(:,:,j)))/n_fp;
            else
                sim1(j)=0;
                if fsize==2
                    overlap(i)=1;
                end
            end
        end
        [maxsim,id]=max(siml);
        if maxsim>=thre_sim
            symtype(i)=id;
            r=row{i};
            c=col{i};  
            npx=numel(r);
            ifreg(i)=1;
            xreg(i)=mean(c);
            yreg(i)=mean(r);
            nreg=nreg+1;
            x1(nreg)=xreg(i);
            y1(nreg)=yreg(i);
        end
        
        if DEBUG 
            figure(1)
            if (maxsim>=thre_sim)
                for j=1:npx
                    rgb(r(j),c(j),:)=mean(symcolor{symtype(i)},1);
                end
                imshow(uint8(rgb));
                hold on
                plot(x1,y1,'y+')
                p=plot([bx(1),bx(2),bx(2),bx(1),bx(1)],[bx(3),bx(3),bx(4),bx(4),bx(3)],'r','LineWidth',1);
            else
                imshow(uint8(rgb));
                hold on                
                bx=box(i,:);
                p=plot([bx(1),bx(2),bx(2),bx(1),bx(1)],[bx(3),bx(3),bx(4),bx(4),bx(3)],'r','LineWidth',1);
                if nreg>0
                    plot(x1,y1,'y+')
                end
            end   
            hold off
            pause(0.2)
            if exist('p')
                delete(p)
            end
        end
    end
    
end

function flag=compare_boxsize(ob_wh,tmplsize,scale)
    flag=0;     % 0: no match; 1: match, 2:larger
    if (ob_wh(1)<tmplsize(1)*scale) || (ob_wh(2)<tmplsize(2)*scale)
        flag=0;
    elseif (ob_wh(1)>=tmplsize(1)*scale)&&(ob_wh(1)<=tmplsize(1)/scale) && ...
       (ob_wh(2)>=tmplsize(2)*scale)&&(ob_wh(2)<=tmplsize(2)/scale)  
        flag=1;
    else
        flag=2;
    end

end

function siml=compare_symbol(ob,tmpl)
    siml=sum(abs(ob-tmpl),'all');
end