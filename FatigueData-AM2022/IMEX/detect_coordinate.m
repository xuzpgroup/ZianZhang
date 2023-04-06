% <xaw>, <yaw>: the width of x and y axis
function [xaw,yaw,mark_r,mark_c,pos_xa,pos_ya,mark_coord,w,h,origin]=detect_coordinate(n_cls,box,row,col,thre)
    mark_coord=max_object(box,n_cls);
    r=row{mark_coord};
    c=col{mark_coord};
    w=box(mark_coord,4)-box(mark_coord,3)+1;
    h=box(mark_coord,2)-box(mark_coord,1)+1;
    origin=[box(mark_coord,1),box(mark_coord,3)];
    [lab_r,nr]=filled_pixel(r');
    [lab_c,nc]=filled_pixel(c');
    mark_r=[];
    xaw=0;
    for i=size(lab_r,2):-1:1
        if (nr(i)>h*thre)
            xaw=xaw+1;
            mark_r(xaw)=lab_r(i);
        else
            if xaw>0
                break;
            end
        end
    end

    mark_c=[];
    yaw=0;
    for i=1:size(lab_c,2)
        if (nc(i)>w*thre)
            yaw=yaw+1;
            mark_c(yaw)=lab_c(i);
        else
            if yaw>0
                break;
            end
        end
    end
    
    pos_xa=mean(mark_r);
    pos_ya=mean(mark_c);
end


% % figure out the filled pixels within the box
function [ele,n]=filled_pixel(a)
    ele=[];
    n=[];
    ct=0;
    for i=1:size(a,2)
        k=find(ele==a(i));
        if isempty(k)
            ct=ct+1;
            ele(ct)=a(i);
            n(ct)=1;
        else
            n(k)=n(k)+1;
        end
    end
    [ele,ind]=sort(ele,2,'ascend');
    n1=[];
    for i=1:size(n,2)
        n1(i)=n(ind(i));
    end
    n=n1;
end

function maxid=max_object(box,n_cls)
    maxid=0;
    area=0;
    for i=1:n_cls
        a1=(box(i,2)-box(i,1))*(box(i,4)-box(i,3)); % nominal area of the symbol
        if a1>area
            maxid=i;
            area=a1;
        end
    end
end
