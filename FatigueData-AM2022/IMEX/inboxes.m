function flag=inboxes(x,boxes)
    flag=0;
    for i=1:numel(boxes)
        box=boxes{i};
        if (x(1)>=box(1))&&(x(1)<=box(2))&&(x(2)>=box(3))&&(x(2)<=box(4))
            flag=1;
            break;
        end
    end
end