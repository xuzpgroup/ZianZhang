function flag=inbox1(x,box)
    flag=0;
    if (x(2)>=box(3))&&(x(2)<=box(4))&&(x(1)>=box(1))&&(x(1)<=box(2))
        flag=1;
    end
end