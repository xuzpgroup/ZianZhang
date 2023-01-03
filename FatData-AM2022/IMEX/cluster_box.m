function clbox=cluster_box(id,box)
    n=numel(id);
    clbox=[0,0,0,0];
    clbox(1,1)=box(id(1),1);
    clbox(1,2)=box(id(1),2);
    clbox(1,3)=box(id(1),3);
    clbox(1,4)=box(id(1),4);    
    for i=2:n
        if box(id(i),1)<clbox(1,1)
            clbox(1,1)=box(id(i),1);
        end
        if box(id(i),2)>clbox(1,2)
            clbox(1,2)=box(id(i),2);
        end
        if box(id(i),3)<clbox(1,3)
            clbox(1,3)=box(id(i),3);
        end
        if box(id(i),4)>clbox(1,4)
            clbox(1,4)=box(id(i),4);
        end      
    end
end
