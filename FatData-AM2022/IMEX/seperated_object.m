function [n_cls,row,col,center,box,ob_wh]=seperated_object(bw)
    [L,n0]=bwlabel(bw*(0-1)+1,4);
    maxid=0;
    n_cls=0;
    for i=1:n0
        [r,c]=find(L==i);
        if numel(r)>3
            n_cls=n_cls+1;
            center(n_cls,:)=[mean(c),mean(r)];
            rmax=max(r,[],1);
            rmin=min(r,[],1);
            cmax=max(c,[],1);
            cmin=min(c,[],1);
            row{n_cls}=r;
            col{n_cls}=c;
            box(n_cls,:)=[cmin,cmax,rmin,rmax];
            ob_wh(n_cls,:)=[cmax-cmin+1,rmax-rmin+1];
        end
    end
end