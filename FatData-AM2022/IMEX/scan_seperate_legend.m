function rec=scan_seperate(rrng,crng,direct,nseg,bw,thre)
    if nargin<6
        thre=0;
    end
    nr=rrng(2)-rrng(1)+1;
    nc=crng(2)-crng(1)+1;
    if strcmp(direct,'row')
        sum1=sum(bw(rrng(1):rrng(2),crng(1):crng(2)),2);
        nrec=0;
        scan=0;
        rec=[];
        for i=1:nr
            if (sum1(i)>thre)&&(scan==0)
                nrec=nrec+1;
                rec(nrec,1)=rrng(1)+(i-1);
                scan=1;
            elseif (sum1(i)<=thre)&&(scan==1)
                scan=0;
                rec(nrec,2)=rrng(1)+(i-2);
                if nrec==nseg
                    break;
                end
            end
        end
    elseif strcmp(direct,'col')
        [rid,cid]=find(bw(rrng(1):rrng(2),crng(1):crng(2))==1);
        % find the span of color pixel
        for i=1:nc
            id=find(cid==i);
            if isempty(id)
                sum1(i)=0;
            else
                sum1(i)=max(rid(id))-min(rid(id));
            end
        end
        nrec=0;
        scan=0;
        rec=[];
        for i=1:nc
            if (sum1(i)>thre)&&(scan==0)
                nrec=nrec+1;
                rec(nrec,1)=crng(1)+(i-1);
                scan=1;
            elseif (sum1(i)<=thre)&&(scan==1)
                scan=0;
                rec(nrec,2)=crng(1)+(i-2);
                if nrec==nseg
                    break;
                end                
            end
        end
        if scan==1
            rec(nrec,2)=crng(2);
        end
    end
end