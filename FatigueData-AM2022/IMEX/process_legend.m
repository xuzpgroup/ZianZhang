function [symbol,word,color,itembox]=process_legend(legendbox,row,col,center,box,ob_wh,bw,rgb)
    dictionary='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,[](){}+-%^*=';
    DEBUG=0;
    n=size(box,1);
    lg=[];
    nob=0;      % number of objects in the legend
    lb=legendbox;
    itembox={};
    bwr=bw*(0-1)+1;
    nc=lb(4)-lb(3)+1;
    nr=lb(2)-lb(1)+1;
    lbarea=nr*nc;
    if DEBUG
        figure(1)
        imshow(bw)
        hold on
    end
    % % get item in the box
    for i=1:n
        xc=center(i,1);
        yc=center(i,2);
        if (xc>=lb(3))&&(xc<=lb(4))&&(yc>=lb(1))&&(yc<=lb(2))
            nob=nob+1;
            lg(nob)=i;
        end    
    end
    % % get rid of the box
    for i=1:nob
        id=lg(i);
        area=ob_wh(id,1)*ob_wh(id,2);
        if area>0.7*lbarea
            r=row{id};
            c=col{id};
            for j=1:numel(r)
                bw(r(j),c(j))=0;
            end
        end
    end
    bwr=bw*(0-1)+1;
    % % seperate level
    count=sum(bwr(lb(1):lb(2),lb(3):lb(4)),2);
    nseg0=0;
    range0=[];
    scan=0;
    for i=1:nr
        if (scan==0)&&(count(i)>0)
            scan=1;
            nseg0=nseg0+1;
            range0(nseg0,1)=lb(1)+(i-1);
        elseif (scan==1)&&(count(i)==0)
           scan=0;
           range0(nseg0,2)=lb(1)+(i-1);
        end
    end
    % % if it is still scanning when reaching the bottom
    if scan==1
        scan=0;
        range0(nseg0,2)=lb(1)+(i-1);
    end
    hrng=range0(:,2)-range0(:,1);
    hrng_ave=mean(hrng);
    yrng=(range0(:,2)+range0(:,1))/2;
    % % we could have to merge some ranges
    % % when the height of the level is lower than a threshold, we consider
    % the level is not a standalone one, and merge it to other levels
    merge=[];
    n_mg=0;
    % detect the level that need to be merged
    for i=1:nseg0
        if hrng(i)<hrng_ave*0.5       % zza: adjstable para.
            n_mg=n_mg+1;
            if i==1
                merge(n_mg,:)=[1,2];
            elseif i==nseg0
                merge(n_mg,:)=[nseg0-1,nseg0];
            else
                delta1=yrng(i)-yrng(i-1);
                delta2=yrng(i+1)-yrng(i);
                if delta1<delta2
                    merge(n_mg,:)=[i-1,i];
                else
                    merge(n_mg,:)=[i,i+1];
                end
            end
        end
    end
    % merge the levels
    nseg=nseg0-n_mg;
    merge_flag=0;
    range=[];
    if n_mg>0
        ct=0;
        for i=1:nseg0
            if merge_flag==0
                ct=ct+1;
                if ismember(i,merge(:,1))
                    merge_flag=1;
                    range(ct,1)=range0(i,1);
                else
                    range(ct,:)=range0(i,:);
                end
            else
                range(ct,2)=range0(i,2);
                merge_flag=0;
            end
        end
    else
        range=range0;
    end
    if DEBUG
        for i=1:nseg
            p(i,1)=plot([lb(3),lb(4)],[range(i,1),range(i,1)],'r');
            p(i,2)=plot([lb(3),lb(4)],[range(i,2),range(i,2)],'r');
        end
        delete(p);
    end
    % % process each line
    symbolcl={};
    nsymcl=zeros(1,nseg);
    wordcl={};
    nwordcl=zeros(1,nseg);
    color={};
    for i=1:nseg
        thre_dashline=(range(i,2)-range(i,1))*0.3;   % to avoid the influence of dashline, zza: should be add to setting list in the future
        rec=scan_seperate_legend(range(i,:),lb(3:4),'col',1,bwr,thre_dashline);  % origin: 0
        for j=1:nob
            id=lg(j);
            if (center(id,2)<=range(i,2))&&(center(id,2)>=range(i,1))&&((ob_wh(id,1)*ob_wh(id,2))<=(lbarea*0.9))
%                 if (center(id,1)<=rec(2))
                if (box(id,1)<=rec(2))
                    if (ob_wh(id,2)>=thre_dashline)
                        nsymcl(i)=nsymcl(i)+1;
                        symbolcl{i}(nsymcl(i))=id;
                    end
                else
                    nwordcl(i)=nwordcl(i)+1;
                    wordcl{i}(nwordcl(i))=id;                    
                end
            end
        end
        symbox=cluster_box(symbolcl{i},box);
        % % process the word
        offset=10;
        if nwordcl(i)>0
            wordbox=cluster_box(wordcl{i},box);
            bw2=boxselect_boundary(bwr,wordbox,offset);
            word_tree=ocr(bw2,'TextLayout','Block','CharacterSet',dictionary);
            word{i}=strip_char_2(word_tree.Text);    
        else
            wordbox=[nan,nan,nan,nan];
            word{i}='';
        end
        % % process the symbol
        id=symbolcl{i}(1);    % generally the symbol is fully connected and only one symbol cluster exist, so used only the first one
        r1=max(box(id,3),lb(1));
        r2=min(box(id,4),lb(2));
        c1=max(box(id,1),lb(3));
        c2=min(box(id,2),lb(4));
        symbol{i}=bw(r1:r2,c1:c2);
        % % process the color
        id=symbolcl{i}(1);   % generally the symbol is fully connected and only one symbol cluster exist, so used only the first one
        red=[];
        green=[];
        blue=[];
        for j=1:numel(row{id})
            if size(rgb,3)==3
                red(j)=double(rgb(row{id}(j),col{id}(j),1));
                green(j)=double(rgb(row{id}(j),col{id}(j),2));
                blue(j)=double(rgb(row{id}(j),col{id}(j),3));
            elseif size(rgb,3)==1
                red(j)=double(rgb(row{id}(j),col{id}(j),1));
                green(j)=double(rgb(row{id}(j),col{id}(j),1));
                blue(j)=double(rgb(row{id}(j),col{id}(j),1));
            end
        end
        %color_tmp=mode([round(round(red'/255*7)/7*255),round(round(green'/255*7)/7*255),round(round(blue'/255*7)/7*255)]);
        color_tmp=unique([round(round(red'/255*7)/7*255),round(round(green'/255*7)/7*255),round(round(blue'/255*7)/7*255)],'rows');
        color{i}=color_tmp;
        itembox{i}={symbox,wordbox};
        if DEBUG
            bx=wordbox;
            p1(i)=plot([bx(1),bx(1),bx(2),bx(2),bx(1)],[bx(3),bx(4),bx(4),bx(3),bx(3)],'g','LineWidth',1);
            txt(i)=text(bx(2)+10,mean(bx(3:4)),word{i},'FontSize',14);
            bx=symbox;
            p2(i)=plot([bx(1),bx(1),bx(2),bx(2),bx(1)],[bx(3),bx(4),bx(4),bx(3),bx(3)],'g','LineWidth',1);
            p3(i)=plot(bx(1)-30,mean(bx(3:4)),'o','color',mean(color{i},1)/255,'MarkerFaceColor',mean(color{i},1)/255)
        end
    end
    if DEBUG
        delete(p)
    end
end

 