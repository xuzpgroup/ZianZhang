% % default white background
function bw1=boxselect_boundary(bw,box,offset)
    bw1=zeros(box(4)-box(3)+offset*2,box(2)-box(1)+offset*2);
    bw1(offset:(offset+box(4)-box(3)),offset:(box(2)-box(1)+offset))=bw(box(3):box(4),box(1):box(2));
end